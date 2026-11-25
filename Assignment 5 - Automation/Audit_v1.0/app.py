from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Literal
from pathlib import Path
import sqlite3, json, hashlib, secrets
from datetime import datetime, timezone
from contextlib import contextmanager

DB = Path(__file__).with_name('audit.sqlite3')
app = FastAPI(title='IT Work Triage — Audit and Review', version='1.0.0')
def now(): return datetime.now(timezone.utc).isoformat()
def canonical(x): return json.dumps(x, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False)
@contextmanager
def transaction():
    with sqlite3.connect(DB, timeout=10) as c:
        c.row_factory=sqlite3.Row
        c.execute('BEGIN IMMEDIATE')
        yield c

def init():
    with transaction() as c:
        c.execute('CREATE TABLE IF NOT EXISTS items (id TEXT PRIMARY KEY, payload TEXT NOT NULL, digest TEXT NOT NULL, state TEXT NOT NULL, attempt INTEGER NOT NULL, token TEXT NOT NULL, result TEXT, decision TEXT, updated TEXT NOT NULL)')
        c.execute('CREATE TABLE IF NOT EXISTS events (seq INTEGER PRIMARY KEY AUTOINCREMENT, id TEXT NOT NULL, event TEXT NOT NULL, at TEXT NOT NULL, details TEXT NOT NULL)')
@app.on_event('startup')
def startup(): init()
def event(c,id,kind,details): c.execute('INSERT INTO events(id,event,at,details) VALUES(?,?,?,?)',(id,kind,now(),canonical(details)))
def row(c,id):
    r=c.execute('SELECT * FROM items WHERE id=?',(id,)).fetchone()
    if not r: raise HTTPException(404,'Unknown work item')
    return r

def view(r):
    return dict(request_id=r['id'],state=r['state'],attempt=r['attempt'],work_item=json.loads(r['payload']),assessment=json.loads(r['result']) if r['result'] else None,review_decision=json.loads(r['decision']) if r['decision'] else None,updated_at=r['updated'],production_authorized=False)
class Intake(BaseModel):
    request_id: str=Field(min_length=1,max_length=100)
    scenario_text: str=Field(min_length=5,max_length=10000)
    domain: str|None=Field(default=None,max_length=100)
    impact: Literal['low','medium','high','unknown']='unknown'
    urgency: Literal['low','medium','high','unknown']='unknown'
    critical_outage: Literal['yes','no','unknown']='unknown'
    active_security_incident: Literal['yes','no','unknown']='unknown'
    critical_recovery_failure: Literal['yes','no','unknown']='unknown'
class Begin(BaseModel):
    work_item: Intake
    retry: bool=False
class Finish(BaseModel):
    request_id: str
    attempt_token: str
    assessment: dict
class Review(BaseModel):
    reviewer: str=Field(min_length=1,max_length=100)
    decision: Literal['accept_recommendation','reject_recommendation','override_recommendation']
    justification: str=Field(min_length=5,max_length=2000)
    override_recommendation: Literal['generalist_handling','escalation']|None=None
@app.get('/health')
def health():
    with transaction() as c: c.execute('SELECT count(*) FROM items').fetchone()
    return {'status':'ok','version':'1.0.0','storage':'SQLite','production_authorized':False}
@app.post('/begin')
def begin(b:Begin):
    p=b.work_item.model_dump(); p['request_id']=p['request_id'].strip(); p['scenario_text']=p['scenario_text'].strip(); id=p['request_id']
    if not id or len(p['scenario_text'])<5: raise HTTPException(400,'Blank ID or scenario')
    payload=canonical(p); digest=hashlib.sha256(payload.encode()).hexdigest()
    with transaction() as c:
        r=c.execute('SELECT * FROM items WHERE id=?',(id,)).fetchone()
        if r:
            if r['digest']!=digest: raise HTTPException(409,'Request ID already used with different inputs')
            if not (b.retry and r['state']=='failed'):
                event(c,id,'duplicate_suppressed',{'state':r['state']}); return {**view(r),'start_assessment':False}
            attempt=r['attempt']+1; token=secrets.token_hex(24)
            c.execute('UPDATE items SET state=?,attempt=?,token=?,result=NULL,updated=? WHERE id=?',('processing',attempt,token,now(),id)); event(c,id,'retry_started',{'attempt':attempt})
        else:
            attempt=1; token=secrets.token_hex(24)
            c.execute('INSERT INTO items VALUES(?,?,?,?,?,?,?,?,?)',(id,payload,digest,'processing',attempt,token,None,None,now())); event(c,id,'assessment_started',{'attempt':attempt})
        return {**view(row(c,id)),'start_assessment':True,'attempt_token':token}
@app.post('/finish')
def finish(b:Finish):
    with transaction() as c:
        r=row(c,b.request_id); a=b.assessment
        if r['state']!='processing' or not secrets.compare_digest(r['token'],b.attempt_token): raise HTTPException(409,'Attempt is not active')
        if a.get('request_id')!=b.request_id or a.get('production_authorized') is not False: raise HTTPException(422,'Unsafe or mismatched assessment')
        if a.get('status')=='assessed' and isinstance(a.get('review_required'),bool) and all(isinstance(a.get(k),dict) for k in ('classification','alignment','priority')):
            # Never trust a routine flag alone.
            cl,al,pr=(a[k] for k in ('classification','alignment','priority'))
            safe=cl.get('prediction_code')==0 and al.get('alignment_status')=='Aligned' and al.get('review_required') is False and pr.get('priority') in ('P3','P4') and pr.get('review_required') is False and pr.get('provisional') is False
            state='routine_advisory' if safe and a['review_required'] is False else 'pending_review'
        else: state='failed'
        c.execute('UPDATE items SET state=?,result=?,updated=? WHERE id=?',(state,canonical(a),now(),b.request_id)); event(c,b.request_id,'assessment_recorded',{'attempt':r['attempt'],'state':state,'assessment':a}); return view(row(c,b.request_id))
@app.get('/items')
def items():
    with transaction() as c: return [view(r) for r in c.execute('SELECT * FROM items ORDER BY updated DESC')]
@app.get('/items/{id}')
def item(id:str):
    with transaction() as c: return view(row(c,id))
@app.get('/items/{id}/events')
def events(id:str):
    with transaction() as c:
        row(c,id); return [dict(sequence=r['seq'],event=r['event'],at=r['at'],details=json.loads(r['details'])) for r in c.execute('SELECT * FROM events WHERE id=? ORDER BY seq',(id,))]
@app.post('/items/{id}/review')
def review(id:str,b:Review):
    if len(b.justification.strip())<5 or not b.reviewer.strip(): raise HTTPException(422,'Reviewer and justification required')
    if (b.decision=='override_recommendation') != (b.override_recommendation is not None): raise HTTPException(422,'Override recommendation required only for override')
    with transaction() as c:
        r=row(c,id)
        if r['state']!='pending_review': raise HTTPException(409,'No completed assessment awaiting review')
        d={**b.model_dump(),'reviewed_at':now(),'production_authorized':False}
        c.execute('UPDATE items SET state=?,decision=?,updated=? WHERE id=?',('reviewed',canonical(d),now(),id)); event(c,id,'review_recorded',d); return view(row(c,id))
