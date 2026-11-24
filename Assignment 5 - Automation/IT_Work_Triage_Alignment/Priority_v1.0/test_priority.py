import json, urllib.request, urllib.error, sys
base=dict(impact='low',urgency='low',critical_outage='no',active_security_incident='no',critical_recovery_failure='no',alignment_status='Aligned')
cases=[('critical outage',{'critical_outage':'yes'},'P1',True),('security incident',{'active_security_incident':'yes'},'P1',True),('recovery failure',{'critical_recovery_failure':'yes'},'P2',True),('planned maintenance',{'impact':'medium','urgency':'medium'},'P3',False),('low impact',{},'P4',False),('policy conflict',{'alignment_status':'Potential Conflict'},'P2',True),('unknown impact',{'impact':'unknown'},'Undetermined',True),('unmapped',{'alignment_status':'Unmapped'},'P4',True),('high impact and urgency',{'impact':'high','urgency':'high'},'P1',True),('unknown incident',{'active_security_incident':'unknown'},'P4',True)]
def run(post):
    passed=0
    for i,(name,changes,expected,review) in enumerate(cases,1):
        status,result=post(dict(base,**changes,request_id=f'PRI-{i:03}'))
        ok=status==200 and result.get('priority')==expected and result.get('review_required')==review and result.get('production_authorized') is False
        passed+=ok; print(f'PRI-{i:03} {name}: {"PASS" if ok else "FAIL"} | expected={expected} actual={result.get("priority")} | review={result.get("review_required")}')
    status,_=post({'request_id':'','impact':'invalid'})
    ok=status==422; passed+=ok; print(f'Invalid input: {"PASS" if ok else "FAIL"} | HTTP {status}')
    print(f'{passed}/{len(cases)+1} regression cases passed.')
    return 0 if passed==len(cases)+1 else 1

def http_post(data):
    req=urllib.request.Request('http://127.0.0.1:8002/priority',data=json.dumps(data).encode(),headers={'Content-Type':'application/json'},method='POST')
    try:
        with urllib.request.urlopen(req,timeout=10) as response: return response.status,json.load(response)
    except urllib.error.HTTPError as e: return e.code,{}
if __name__=='__main__': sys.exit(run(http_post))
