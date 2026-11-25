"""Post-test diagnostic; never changes the original frozen model or datasets."""
from pathlib import Path
import hashlib, json, math, datetime, sys
import pandas as pd
import sklearn, joblib
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix

EXPECTED = {
 'development': 'd2eb9a0f4af18ae06d798addd05c93082655a3ea59b01ee8553cbbb1a0dccd3e',
 'original_test': '495ec57c87f8bdc2fa77571621e90c882be485379088249f162601eac71fda2e',
 'independent': 'c069343457ed8adae4af9da3dfc6840c201cc53025af044181c36abfb179ce50',
 'model': 'e7e440cacfc5926e4eab482bc9baad188eebedf2dbab22b21b3d49fcffac4239',
}
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
# Use the original word tokenizer and contiguous unigram/bigram analyzer.
# Retain only features whose every token is in the fixed English stopword list.
# Do not join words across removed technical tokens.
BASE_ANALYZER = TfidfVectorizer(lowercase=True, ngram_range=(1,2)).build_analyzer()
def style_analyzer(text):
    return [term for term in BASE_ANALYZER(text) if all(w in ENGLISH_STOP_WORDS for w in term.split())]
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

def run(root=None):
    if sklearn.__version__!='1.6.1': raise RuntimeError('Use scikit-learn 1.6.1; found '+sklearn.__version__)
    folder=Path(__file__).resolve().parent
    root=Path(root).resolve() if root else folder.parent.parent
    paths={'development':root/'Data/Williams_INAI6986_Development_Train_Validation_v1_0.xlsx', 'original_test':root/'Data/Williams_INAI6986_Frozen_Test_Set_v1_0.csv', 'independent':root/'Supplemental Evaluation/Independent_Robustness_Set/Independent_Robustness_Set_v1_0.csv', 'model':root/'Assignment 3 - Data and Model/assignment3_selected_model_naive_bayes.joblib'}
    hashes={k:sha(v) for k,v in paths.items()}
    if hashes!=EXPECTED: raise RuntimeError('Input hash mismatch; stop and investigate. '+json.dumps(hashes))
    out=folder/'results'
    if out.exists(): raise RuntimeError('Results directory already exists; preserve existing evidence.')
    dev=pd.read_excel(paths['development'],sheet_name='Development_Data').rename(columns={'escalation_label':'label'})
    if len(dev)!=160 or set(dev.split)!={'Train','Validation'}: raise ValueError('Unexpected development split')
    train=validate(dev[dev.split=='Train'].copy(),120,60)
    val=validate(dev[dev.split=='Validation'].copy(),40,20)
    # Diagnostic fit occurs before reading either evaluation test file.
    diagnostic=Pipeline([('tfidf',TfidfVectorizer(analyzer=style_analyzer)),('model',MultinomialNB())])
    diagnostic.fit(train.scenario_text,train.label)
    features=diagnostic.named_steps['tfidf'].get_feature_names_out()
    assert all(all(w in ENGLISH_STOP_WORDS for w in term.split()) for term in features)
    original=validate(pd.read_csv(paths['original_test']).rename(columns={'final_label':'label'}),40,20)
    independent=validate(pd.read_csv(paths['independent']).rename(columns={'reference_label':'label'}),20,9)
    sets={'validation':val,'original_test':original,'independent':independent}
    ids=[set(d.scenario_id) for d in [train,*sets.values()]]
    if any(ids[i]&ids[j] for i in range(len(ids)) for j in range(i)): raise ValueError('Overlapping scenario IDs')
    frozen=joblib.load(paths['model'])
    report={}; records=[]
    for name,d in sets.items():
        report[name]={}
        for model_name,model in [('frozen_NB_v1',frozen),('style_only_NB',diagnostic)]:
            pred=model.predict(d.scenario_text)
            report[name][model_name]=metrics(d.label,pred)
            for (_,r),p in zip(d.iterrows(),pred):
                records.append(dict(dataset=name,model=model_name,scenario_id=r.scenario_id,domain=r.domain,reference_label=int(r.label),prediction=int(p),error_type='correct' if p==r.label else ('FN' if r.label else 'FP')))
    # Verify original model reproduces the previously recorded counts before saving.
    for name,counts in {'validation':(20,0,2,18),'original_test':(19,1,3,17),'independent':(7,4,4,5)}.items():
        m=report[name]['frozen_NB_v1']
        if tuple(m[k] for k in ['TN','FP','FN','TP'])!=counts: raise RuntimeError('Frozen model comparison did not reproduce: '+name)
    if {k:sha(v) for k,v in paths.items()}!=hashes: raise RuntimeError('Input changed during run')
    record=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),sklearn_version=sklearn.__version__,input_hashes=hashes,protocol='Post-test diagnostic; fixed stopword-only contiguous unigram/bigram analyzer; train only; no tuning',n_features=len(features),metrics=report,frozen_model_unchanged=True)
    out.mkdir()
    pd.DataFrame(records).to_csv(out/'predictions.csv',index=False)
    pd.DataFrame([dict(dataset=d,model=m,**{k:v for k,v in x.items() if not isinstance(v,list)}) for d,ms in report.items() for m,x in ms.items()]).to_csv(out/'comparison.csv',index=False)
    pd.DataFrame({'feature':features}).to_csv(out/'style_vocabulary.csv',index=False)
    (out/'run.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(record,indent=2))
    return record
if __name__=='__main__': run(sys.argv[1] if len(sys.argv)>1 else None)
