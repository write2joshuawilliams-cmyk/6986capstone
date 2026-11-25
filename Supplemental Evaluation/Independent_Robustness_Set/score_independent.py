from pathlib import Path
import csv, json, hashlib, math, sys, datetime
import sklearn, joblib
from sklearn.metrics import confusion_matrix

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def wilson(k,n):
    if not n: return [None,None]
    z=1.95996398454; p=k/n; den=1+z*z/n
    center=(p+z*z/(2*n))/den; half=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
    return [max(0,center-half),min(1,center+half)]
def metrics(rows):
    tn,fp,fn,tp=map(int,confusion_matrix([int(r['reference_label']) for r in rows],[r['prediction'] for r in rows],labels=[0,1]).ravel())
    ratio=lambda a,b:a/b if b else None
    return dict(n=len(rows),TN=tn,FP=fp,FN=fn,TP=tp,recall=ratio(tp,tp+fn),recall_Wilson95=wilson(tp,tp+fn),precision=ratio(tp,tp+fp),precision_Wilson95=wilson(tp,tp+fp),accuracy=ratio(tp+tn,len(rows)),accuracy_Wilson95=wilson(tp+tn,len(rows)),f1=ratio(2*tp,2*tp+fp+fn),false_positive_rate=ratio(fp,fp+tn))
def run(folder, model_path):
    folder=Path(folder); model_path=Path(model_path)
    if sklearn.__version__!='1.6.1': raise RuntimeError('Use scikit-learn 1.6.1; found '+sklearn.__version__)
    manifest=json.loads((folder/'manifest.json').read_text())
    data=folder/'Independent_Robustness_Set_v1_0.csv'
    if sha(data)!=manifest['dataset_sha256'] or sha(folder/'reviewer_original.txt')!=manifest['source_sha256']: raise RuntimeError('Dataset/source hash mismatch')
    if sha(model_path)!=manifest['model_sha256']: raise RuntimeError('Frozen model hash mismatch')
    with data.open(encoding='utf-8',newline='') as f: rows=list(csv.DictReader(f))
    assert len(rows)==20 and len({r['scenario_id'] for r in rows})==20 and sum(int(r['reference_label']) for r in rows)==9
    out=folder/'results'; out.mkdir(exist_ok=True)
    if (out/'run.json').exists(): raise RuntimeError('Result already recorded; preserve it. Do not rerun for tuning.')
    model=joblib.load(model_path)
    predictions=model.predict([r['scenario_text'] for r in rows])
    for r,p in zip(rows,predictions):
        r['prediction']=int(p); r['error_type']='correct' if int(r['reference_label'])==int(p) else ('FN' if int(r['reference_label']) else 'FP')
    overall=metrics(rows); domains={d:metrics([r for r in rows if r['domain']==d]) for d in dict.fromkeys(r['domain'] for r in rows)}
    record=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),model_sha256=sha(model_path),dataset_sha256=sha(data),sklearn_version=sklearn.__version__,overall=overall,domains=domains,recall_target_met=overall['recall']>=.90,precision_reference_met=overall['precision'] is not None and overall['precision']>=.80,recall_delta_vs_original=overall['recall']-.85,no_training_or_tuning=True)
    with (out/'predictions.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    (out/'run.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps(record,indent=2)); print('Errors:',[(r['scenario_id'],r['error_type']) for r in rows if r['error_type']!='correct'])
    return record
if __name__=='__main__':
    folder=Path(__file__).resolve().parent
    model=Path(sys.argv[1]) if len(sys.argv)>1 else folder.parent.parent/'Assignment 3 - Data and Model'/'assignment3_selected_model_naive_bayes.joblib'
    run(folder,model)
