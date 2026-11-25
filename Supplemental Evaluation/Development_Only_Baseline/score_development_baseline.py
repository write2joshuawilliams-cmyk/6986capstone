"""Retrospective training-only lexical rule comparator; not a new blinded test."""
from pathlib import Path
import hashlib, json, math, datetime, sys
from collections import Counter
import pandas as pd
import sklearn, joblib
from sklearn.feature_extraction.text import CountVectorizer, ENGLISH_STOP_WORDS
from sklearn.metrics import confusion_matrix

EXPECTED = {
 'development': 'd2eb9a0f4af18ae06d798addd05c93082655a3ea59b01ee8553cbbb1a0dccd3e',
 'original_test': '495ec57c87f8bdc2fa77571621e90c882be485379088249f162601eac71fda2e',
 'independent': 'c069343457ed8adae4af9da3dfc6840c201cc53025af044181c36abfb179ce50',
 'model': 'e7e440cacfc5926e4eab482bc9baad188eebedf2dbab22b21b3d49fcffac4239',
}
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def wilson(k,n):
    if not n: return [None,None]
    z=1.95996398454; p=k/n; d=1+z*z/n
    c=(p+z*z/(2*n))/d; h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return [max(0,c-h),min(1,c+h)]
def metrics(y,p):
    tn,fp,fn,tp=map(int,confusion_matrix(y,p,labels=[0,1]).ravel())
    def ratio(a,b): return a/b if b else None
    return dict(n=len(y),TN=tn,FP=fp,FN=fn,TP=tp,recall=ratio(tp,tp+fn),recall_Wilson95=wilson(tp,tp+fn),precision=ratio(tp,tp+fp),precision_Wilson95=wilson(tp,tp+fp),accuracy=ratio(tp+tn,len(y)),accuracy_Wilson95=wilson(tp+tn,len(y)),f1=ratio(2*tp,2*tp+fp+fn),false_positive_rate=ratio(fp,fp+tn))
def validate(df,n,pos):
    if len(df)!=n or df.scenario_id.nunique()!=n or df.scenario_text.isna().any() or not set(df.label).issubset({0,1}) or df.label.sum()!=pos:
        raise ValueError('Unexpected dataset size, labels or missing text')
    return df


# Fixed protocol: binary unigram presence, excluding standard English stopwords.
# Candidate terms must occur in >=3 training documents and have >=80% training precision.
# Greedily add up to 10 OR rules, maximizing additional detected training escalations
# subject to aggregate training precision >=80%; tie-break on fewer new false positives,
# then lexical order. Stop if no eligible rule adds a true positive.
# No validation or test observations participate in rule selection.
ANALYZER = CountVectorizer(lowercase=True, stop_words='english').build_analyzer()
def tokens(text): return set(ANALYZER(text))
def fit_rules(train):
    docs=[tokens(t) for t in train.scenario_text]
    y=[int(v) for v in train.label]
    pos=Counter(); total=Counter()
    for d,l in zip(docs,y):
        total.update(d)
        if l: pos.update(d)
    candidates=sorted(t for t,n in total.items() if n>=3 and 5*pos[t]>=4*n)
    masks={t:{i for i,d in enumerate(docs) if t in d} for t in candidates}
    chosen=[]; covered=set(); steps=[]
    for step in range(10):
        eligible=[]
        for t in candidates:
            if t in chosen: continue
            new=masks[t]-covered; union=covered|masks[t]
            tp=sum(y[i] for i in union); add_tp=sum(y[i] for i in new)
            if add_tp and 5*tp>=4*len(union):
                eligible.append((-add_tp,len(new)-add_tp,t,union))
        if not eligible: break
        _,_,t,covered=min(eligible,key=lambda a:a[:3]);chosen.append(t)
        steps.append(dict(step=step+1,term=t,training_term_support=total[t],training_term_positive=pos[t],**{k:v for k,v in metrics(y,[int(i in covered) for i in range(len(y))]).items() if not isinstance(v,list)}))
    return chosen,steps,candidates

def predict(texts,rules):
    r=set(rules)
    return [int(bool(tokens(t)&r)) for t in texts]

def run(root=None):
    if sklearn.__version__!='1.6.1': raise RuntimeError('Use scikit-learn 1.6.1; found '+sklearn.__version__)
    folder=Path(__file__).resolve().parent
    root=Path(root).resolve() if root else folder.parent.parent
    paths={'development':root/'Data/Williams_INAI6986_Development_Train_Validation_v1_0.xlsx','original_test':root/'Data/Williams_INAI6986_Frozen_Test_Set_v1_0.csv','independent':root/'Supplemental Evaluation/Independent_Robustness_Set/Independent_Robustness_Set_v1_0.csv','model':root/'Assignment 3 - Data and Model/assignment3_selected_model_naive_bayes.joblib'}
    hashes={k:sha(v) for k,v in paths.items()}
    if hashes!=EXPECTED: raise RuntimeError('Input hash mismatch: '+json.dumps(hashes))
    out=folder/'results'
    if out.exists(): raise RuntimeError('Results already exist; preserve original evidence.')
    dev=pd.read_excel(paths['development'],sheet_name='Development_Data').rename(columns={'escalation_label':'label'})
    if len(dev)!=160 or set(dev.split)!={'Train','Validation'}: raise ValueError('Unexpected development split')
    train=validate(dev[dev.split=='Train'].copy(),120,60)
    rules,steps,candidates=fit_rules(train)
    # The comparator is fixed before loading either test dataset.
    val=validate(dev[dev.split=='Validation'].copy(),40,20)
    original=validate(pd.read_csv(paths['original_test']).rename(columns={'final_label':'label'}),40,20)
    independent=validate(pd.read_csv(paths['independent']).rename(columns={'reference_label':'label'}),20,9)
    sets={'train':train,'validation':val,'original_test':original,'independent':independent}
    ids=[set(d.scenario_id) for d in sets.values()]
    if any(ids[i]&ids[j] for i in range(len(ids)) for j in range(i)): raise ValueError('Overlapping scenario IDs')
    frozen=joblib.load(paths['model']); report={}; records=[]
    for name,d in sets.items():
        report[name]={}
        for model_name,pred in [('training_only_OR_rules',predict(d.scenario_text,rules)),('frozen_NB_v1',frozen.predict(d.scenario_text))]:
            report[name][model_name]=metrics(d.label,pred)
            for (_,r),p in zip(d.iterrows(),pred):
                records.append(dict(dataset=name,model=model_name,scenario_id=r.scenario_id,domain=r.domain,reference_label=int(r.label),prediction=int(p),error_type='correct' if p==r.label else ('FN' if r.label else 'FP'),matched_rules='; '.join(sorted(tokens(r.scenario_text)&set(rules))) if model_name=='training_only_OR_rules' else ''))
    for name,counts in {'validation':(20,0,2,18),'original_test':(19,1,3,17),'independent':(7,4,4,5)}.items():
        m=report[name]['frozen_NB_v1']
        if tuple(m[k] for k in ['TN','FP','FN','TP'])!=counts: raise RuntimeError('Frozen model results differ: '+name)
    if {k:sha(v) for k,v in paths.items()}!=hashes: raise RuntimeError('Input changed during run')
    record=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),sklearn_version=sklearn.__version__,pandas_version=pd.__version__,input_hashes=hashes,protocol='Retrospective training-only binary unigram OR comparator; min support 3; min training precision 80%; maximum 10 rules; greedy gain; no validation/test selection',candidate_count=len(candidates),rules=rules,metrics=report,frozen_model_unchanged=True,original_keyword_baseline_reported_recall={'train':0.10,'validation':0.10,'original_test':0.55},original_keyword_baseline_test_contaminated=True)
    out.mkdir()
    pd.DataFrame(records).to_csv(out/'predictions.csv',index=False)
    pd.DataFrame(steps,columns=['step','term','training_term_support','training_term_positive','n','TN','FP','FN','TP','recall','precision','accuracy','f1','false_positive_rate']).to_csv(out/'rule_selection.csv',index=False)
    pd.DataFrame([dict(dataset=d,model=m,**{k:v for k,v in x.items() if not isinstance(v,list)}) for d,ms in report.items() for m,x in ms.items()]).to_csv(out/'comparison.csv',index=False)
    (out/'run.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(record,indent=2));return record
if __name__=='__main__': run(sys.argv[1] if len(sys.argv)>1 else None)
