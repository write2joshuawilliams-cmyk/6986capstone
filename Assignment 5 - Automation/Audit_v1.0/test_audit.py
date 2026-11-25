import json, urllib.request, urllib.error, uuid
BASE='http://127.0.0.1:8003'
def call(path,data=None,expected=200):
    req=urllib.request.Request(BASE+path,data=None if data is None else json.dumps(data).encode(),headers={'Content-Type':'application/json'})
    try:
        with urllib.request.urlopen(req,timeout=15) as r: code=r.status; body=json.load(r)
    except urllib.error.HTTPError as e: code=e.code; body=json.load(e)
    assert code==expected,(path,code,body)
    return body
prefix='AUD-'+uuid.uuid4().hex[:10]
def intake(s): return {'request_id':prefix+s,'scenario_text':'Synthetic approved operating system maintenance request.','domain':'Infrastructure','impact':'medium','urgency':'medium','critical_outage':'no','active_security_incident':'no','critical_recovery_failure':'no'}
def begin(p,retry=False): return call('/begin',{'work_item':p,'retry':retry})
def finish(p,b,risk=False,fail=False):
    a={'request_id':p['request_id'],'production_authorized':False,'status':'manual_review' if fail else 'assessed','review_required':risk or fail,'classification':{'prediction_code':int(risk)},'alignment':{'alignment_status':'Potential Conflict' if risk else 'Aligned','review_required':risk},'priority':{'priority':'P2' if risk else 'P3','review_required':risk,'provisional':False}}
    return call('/finish',{'request_id':p['request_id'],'attempt_token':b['attempt_token'],'assessment':a})
def run():
    assert call('/health')['status']=='ok';print('PASS health')
    p=intake('-routine');b=begin(p);assert b['start_assessment'];assert finish(p,b)['state']=='routine_advisory';print('PASS routine audit record')
    assert not begin(p)['start_assessment'];print('PASS duplicate suppression')
    call('/begin',{'work_item':{**p,'scenario_text':'Different synthetic request'}},409);print('PASS changed payload rejected')
    for i,decision in enumerate(['accept_recommendation','reject_recommendation','override_recommendation']):
        p=intake('-review'+str(i));b=begin(p);assert finish(p,b,True)['state']=='pending_review';path='/items/'+p['request_id'];assert call(path)['state']=='pending_review';d={'reviewer':'Demo reviewer','decision':decision,'justification':'Synthetic review demonstration.'}
        if i==2:
            call(path+'/review',d,422);d['override_recommendation']='generalist_handling'
        result=call(path+'/review',d);assert result['state']=='reviewed' and result['production_authorized'] is False;call(path+'/review',d,409);assert any(e['event']=='review_recorded' for e in call(path+'/events'));print('PASS '+decision+' and repeat review blocked')
    p=intake('-retry');b=begin(p);assert finish(p,b,fail=True)['state']=='failed';assert not begin(p)['start_assessment'];b2=begin(p,True);assert b2['attempt']==2 and b2['start_assessment'];call('/finish',{'request_id':p['request_id'],'attempt_token':b['attempt_token'],'assessment':{}},409);assert finish(p,b2)['state']=='routine_advisory';print('PASS explicit retry and stale token blocked')
    p=intake('-hold');b=begin(p);assert finish(p,b,True)['state']=='pending_review';assert not begin(p)['start_assessment'];print('PASS no-response hold')
    print('9/9 regression groups passed.')
if __name__=='__main__':run()
