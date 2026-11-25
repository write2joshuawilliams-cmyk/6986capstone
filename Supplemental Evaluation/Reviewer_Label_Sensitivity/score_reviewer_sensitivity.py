import csv,json,hashlib,math,sys
from pathlib import Path
from openpyxl import load_workbook

def hashfile(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def metrics(rows,label):
    tn,fp,fn,tp=[sum(int(r[label])==a and int(r['model_prediction'])==b for r in rows) for a,b in [(0,0),(0,1),(1,0),(1,1)]]
    def rate(k,n):
        if not n:return None,None
        p=k/n;z=1.959963984540054;d=1+z*z/n;c=(p+z*z/(2*n))/d;h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
        return p,[max(0,c-h),min(1,c+h)]
    r,ri=rate(tp,tp+fn);p,pi=rate(tp,tp+fp);a,ai=rate(tp+tn,len(rows))
    return dict(n=len(rows),TN=tn,FP=fp,FN=fn,TP=tp,recall=r,recall_Wilson95=ri,precision=p,precision_Wilson95=pi,accuracy=a,accuracy_Wilson95=ai,f1=2*tp/(2*tp+fp+fn),recall_target_met=r>=.9)
def main():
    root=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parents[2]
    pred=root/'Assignment 4 - Model Testing'/'assignment4_test_predictions.csv';review=root/'Data'/'Williams_INAI6986_Independent_Review_Evidence_FINAL.xlsx';test=root/'Data'/'Williams_INAI6986_Frozen_Test_Set_v1_0.csv'
    inputs={'predictions':pred,'review':review,'frozen_test':test};hashes={k:hashfile(v) for k,v in inputs.items()}
    expected={'predictions':'14728e8d9c0b9be20051b34cb186765a906dab1c9df21b1d40418f8015cac104','review':'f51da20a6aded513667a846880e203354e619891ca8fb8d0372d950015ae9d75','frozen_test':'495ec57c87f8bdc2fa77571621e90c882be485379088249f162601eac71fda2e'}
    if hashes!=expected: raise ValueError(f'Input hashes differ: {hashes}')
    def readcsv(p):return list(csv.DictReader(p.open(encoding='utf-8-sig',newline='')))
    ps=readcsv(pred);ts=readcsv(test);w=load_workbook(review,read_only=True,data_only=True);it=iter(w['Review_Evidence'].values);headers=next(it);rs=[dict(zip(headers,r)) for r in it if r[0] is not None]
    def index(rows):
        out={r['scenario_id']:r for r in rows};assert len(rows)==len(out)==40;return out
    p,t,r=map(index,(ps,ts,rs));assert p.keys()==t.keys()==r.keys()
    rows=[]
    for id,x in p.items():
        y=r[id];z=t[id];assert x['scenario_text']==y['scenario_text']==z['scenario_text'];assert x['domain']==y['domain']==z['domain'];assert int(x['escalation_label'])==int(y['final_adjudicated_label'])==int(z['final_label']);assert all(int(v) in (0,1) for v in [x['model_prediction'],y['reviewer_label'],y['project_label'],y['final_adjudicated_label']])
        rows.append(dict(scenario_id=id,domain=x['domain'],model_prediction=int(x['model_prediction']),project_label=int(y['project_label']),final_label=int(y['final_adjudicated_label']),reviewer_label=int(y['reviewer_label']),review_date_as_recorded=y['review_date']))
    result=dict(protocol='Post-test sensitivity analysis of saved predictions; no inference or training',input_hashes=hashes,final_labels=metrics(rows,'final_label'),reviewer_labels=metrics(rows,'reviewer_label'),disagreements=[x for x in rows if x['final_label']!=x['reviewer_label']],review_date_as_recorded=sorted(set(str(x['review_date_as_recorded']) for x in rows)))
    out=Path(__file__).resolve().parent/'results';out.mkdir(exist_ok=True)
    for name in ['run.json','comparison.csv','label_comparison.csv']:
        if (out/name).exists():raise FileExistsError(out/name)
    (out/'run.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    for name,data in [('comparison.csv',[dict(reference=k,**result[k]) for k in ['final_labels','reviewer_labels']]),('label_comparison.csv',rows)]:
        with (out/name).open('w',newline='',encoding='utf-8') as f:wr=csv.DictWriter(f,fieldnames=list(data[0]));wr.writeheader();wr.writerows(data)
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
