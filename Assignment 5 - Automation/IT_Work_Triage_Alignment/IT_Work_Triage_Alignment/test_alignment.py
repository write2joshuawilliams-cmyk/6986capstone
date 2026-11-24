from fastapi.testclient import TestClient
from alignment_api import app
c=TestClient(app)
assert c.get('/health').json()['documents_loaded']==9
cases=[('DEMO-ALIGN-001','A vendor requests permanent privileged administrator access to production servers without multifactor authentication.','Potential Conflict'),('DEMO-ALIGN-002','Apply approved operating system patches during the documented maintenance window using the existing change procedure.','Requires Review'),('DEMO-ALIGN-003','Request to reduce backup retention from 90 days to 14 days to reclaim storage capacity.','Requires Review'),('DEMO-ALIGN-004','A purchase request for a new storage platform requires lifecycle cost analysis.','Requires Review'),('DEMO-ALIGN-005','Reserve a conference room for a staff birthday party.','Unmapped'),('DEMO-ALIGN-006','Approved operating system patching during the scheduled maintenance window using the existing change procedure; impact assessment completed, rollback confirmed, work recorded, service health validated.','Aligned')]
for i,t,want in cases:
    r=c.post('/align',json={'request_id':i,'scenario_text':t}); assert r.status_code==200; x=r.json();assert x['alignment_status']==want,(i,x['alignment_status']);assert x['production_authorized'] is False
    print(i,x['alignment_status'],x['evidence_count'],[(p['citation'],p['alignment_status']) for k in ('policy','sop','strategy') for p in x[k]])
assert c.post('/align',json={'request_id':'x','scenario_text':''}).status_code==422
print('7 interface tests passed (including invalid input).')
