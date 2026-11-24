"""Regression fixtures from v1.0 desktop demos; not independent evaluation."""
import json, sys, urllib.request, urllib.error
CASES=[
('ALIGN-001','Security/Policy','A vendor requests permanent privileged administrator access to production servers without multifactor authentication.','Potential Conflict','POL-001','SOP-002','2'),
('ALIGN-002','Infrastructure','Apply approved operating system patches during the documented maintenance window using an approved change ticket, verified backup, rollback plan, and post-change validation.','Requires Review','POL-002','SOP-001','1'),
('ALIGN-003','Infrastructure','Apply approved operating system patches using documented authorization, an approved change ticket, completed impact assessment, approved maintenance window, verified backup, documented rollback plan, and post-change validation.','Aligned','POL-002','SOP-001','1'),
('ALIGN-004','Backup/DR','Reduce production backup retention from 90 days to 14 days without data owner approval or security review to reclaim storage capacity.','Potential Conflict','POL-003','SOP-003','1'),
('ALIGN-005','Procurement/Vendor/RFP','Purchase a new enterprise storage array without competitive procurement review, security assessment, or documented business justification.','Potential Conflict','POL-004','SOP-004','3'),
('ALIGN-006','Other','Organize a retirement luncheon and purchase decorations for the employee break room.','Unmapped',None,None,None),
('ALIGN-007','Infrastructure','Apply approved operating system patches using documented authorization, an approved change ticket, not completed impact assessment, approved maintenance window, verified backup, documented rollback plan, and post-change validation.','Requires Review','POL-002','SOP-001','1'),
('ALIGN-008','Backup/DR','Request to reduce backup retention from 90 days to 14 days to reclaim storage capacity.','Requires Review','POL-003','SOP-003','1'),
]
def run(get,post):
 h=get('/health');assert h['engine_version']=='1.1.0' and h['documents_loaded']==9
 failures=0
 for i,d,t,w,p,s,st in CASES:
  code,x=post('/align',dict(request_id=i,domain=d,scenario_text=t))
  ev=[e for k in ('policy','sop','strategy') for e in x.get(k,[])]
  ok=code==200 and x.get('alignment_status')==w and x.get('production_authorized') is False and x.get('advisory_only') is True and all(e['retrieval_score']>0 for e in ev)
  if p: ok=ok and any(e['document_id']==p for e in x['policy']) and any(e['document_id']==s for e in x['sop']) and any(e['document_id']=='STR-001' and e['section']==st for e in x['strategy'])
  else: ok=ok and not ev
  if i=='ALIGN-003':ok=ok and not any(e['document_id']=='POL-003' for e in ev)
  failures+=not ok
  print(f'{i}: {"PASS" if ok else "FAIL"} | expected={w} actual={x.get("alignment_status")} | citations={", ".join(e["citation"] for e in ev)}')
 code,_=post('/align',dict(request_id='ALIGN-INVALID',scenario_text='')); ok=code==422;failures+=not ok;print(f'Invalid input: {"PASS" if ok else "FAIL"} | HTTP {code}')
 print(f'{len(CASES)+1-failures}/{len(CASES)+1} regression cases passed.');return failures
if __name__=='__main__':
 if '--in-process' in sys.argv:
  from fastapi.testclient import TestClient
  from alignment_api import app
  c=TestClient(app)
  def post(p,d):
   r=c.post(p,json=d);return r.status_code,r.json()
  sys.exit(bool(run(lambda p:c.get(p).json(),post)))
 def call(p,d=None):
  req=urllib.request.Request('http://127.0.0.1:8001'+p,data=None if d is None else json.dumps(d).encode(),headers={'Content-Type':'application/json'})
  try:
   with urllib.request.urlopen(req,timeout=10) as r:return r.status,json.load(r)
  except urllib.error.HTTPError as e:return e.code,json.load(e)
 sys.exit(bool(run(lambda p:call(p)[1],call)))
