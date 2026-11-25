from typing import Literal
from fastapi import FastAPI
from pydantic import BaseModel, Field, ConfigDict, field_validator

app = FastAPI(title='IT Work Triage — Priority Assessment', version='1.0.0')
Level = Literal['low','medium','high','unknown']
Signal = Literal['yes','no','unknown']
class PriorityRequest(BaseModel):
    model_config = ConfigDict(extra='forbid')
    request_id: str = Field(min_length=1,max_length=100)
    impact: Level = 'unknown'
    urgency: Level = 'unknown'
    critical_outage: Signal = 'unknown'
    active_security_incident: Signal = 'unknown'
    critical_recovery_failure: Signal = 'unknown'
    alignment_status: Literal['Aligned','Requires Review','Potential Conflict','Unmapped','Unavailable','Not Assessed'] = 'Not Assessed'
    @field_validator('request_id')
    @classmethod
    def nonblank(cls,v):
        if not v.strip(): raise ValueError('request_id must not be blank')
        return v.strip()

MATRIX = {'high':{'high':1,'medium':2,'low':2}, 'medium':{'high':2,'medium':3,'low':3}, 'low':{'high':2,'medium':3,'low':4}}
LABELS = {1:'Critical',2:'High',3:'Medium',4:'Low'}
@app.get('/health')
def health():
    return {'status':'ok','engine_version':'1.0.0','method':'deterministic impact/urgency matrix and safety overrides'}

@app.post('/priority')
def priority(r: PriorityRequest):
    unknown = [k for k in ('impact','urgency','critical_outage','active_security_incident','critical_recovery_failure') if getattr(r,k)=='unknown']
    reasons=[]
    rank=MATRIX.get(r.impact,{}).get(r.urgency)
    if rank is not None: reasons.append(f'Impact {r.impact} and urgency {r.urgency} map to P{rank}.')
    if r.critical_outage=='yes' or r.active_security_incident=='yes':
        rank=1; reasons.append('Critical outage or active security incident: immediate escalation.')
    elif r.critical_recovery_failure=='yes':
        rank=min(rank or 2,2); reasons.append('Critical recovery failure: at least P2.')
    if r.alignment_status=='Potential Conflict':
        rank=min(rank or 2,2); reasons.append('Potential policy conflict: at least P2 for review, not approval to execute.')
    if unknown: reasons.append('Missing or unknown inputs require human assessment: '+', '.join(unknown)+'.')
    if rank is None: reasons.append('Insufficient information to assign a priority.')
    review=bool(unknown or rank in (None,1,2) or r.alignment_status!='Aligned')
    return {'request_id':r.request_id,'priority':f'P{rank}' if rank else 'Undetermined','priority_label':LABELS.get(rank,'Needs assessment'),'provisional':bool(unknown or r.alignment_status in ('Not Assessed','Unavailable','Unmapped')),'review_required':review,'missing_inputs':unknown,'reasons':reasons,'engine_version':'1.0.0','advisory_only':True,'production_authorized':False}
