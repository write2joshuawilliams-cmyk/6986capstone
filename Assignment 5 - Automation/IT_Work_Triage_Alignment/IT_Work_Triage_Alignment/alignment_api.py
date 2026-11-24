"""Local deterministic evidence retrieval and advisory alignment, independent of classifier."""
from pathlib import Path
import json, re
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

ROOT = Path(__file__).resolve().parent / 'knowledge_base'
EVIDENCE = []
for path in sorted(ROOT.glob('*.json')):
    doc = json.loads(path.read_text(encoding='utf-8'))
    for section in doc['sections']:
        EVIDENCE.append({**{k:v for k,v in doc.items() if k!='sections'}, **section})
if not EVIDENCE:
    raise RuntimeError('No knowledge base documents found.')
VECTOR = TfidfVectorizer(stop_words='english', ngram_range=(1,2))
MATRIX = VECTOR.fit_transform([f"{s['title']} {s['heading']} {s['passage']}" for s in EVIDENCE])
app = FastAPI(title='IT Work Triage — Local Document Alignment',version='1.0.0')
class AlignmentRequest(BaseModel):
    request_id: str = Field(min_length=1,max_length=100)
    scenario_text: str = Field(min_length=5,max_length=10000)
    domain: Optional[str] = Field(default=None,max_length=100)

def hit(pattern,text):
    return bool(pattern and re.search(pattern,text,re.I|re.S))

def assess(text):
    scores=cosine_similarity(VECTOR.transform([text]),MATRIX)[0]
    matches=[]
    for i,s in enumerate(EVIDENCE):
        conflict=hit(s['conflict_pattern'],text)
        relevant=hit(s['relevance_pattern'],text)
        # Require explicit domain-specific cue; TF-IDF ranks candidates, not compliance.
        if not relevant:
            continue
        if conflict:
            status='Potential Conflict'
            explanation='A predefined risk cue matched the work item. Confirm the actual facts and applicable exception process with the document owner.'
        elif hit(s['alignment_pattern'],text):
            status='Aligned'
            explanation='The work item explicitly mentions the expected indicators for this section. This is a preliminary textual match, not authorization or verified compliance.'
        else:
            status='Requires Review'
            explanation='Relevant guidance was retrieved, but the text does not establish all required conditions; verify with the document owner.'
        matches.append(dict(document_id=s['document_id'],document_title=s['title'],document_type=s['type'],document_domain=s['domain'],version=s['version'],section=s['section_id'],heading=s['heading'],citation=f"{s['document_id']} v{s['version']} §{s['section_id']}",retrieved_passage=s['passage'],retrieval_score=round(float(scores[i]),4),alignment_status=status,explanation=explanation,provenance=s['provenance']))
    matches.sort(key=lambda x:(x['alignment_status']=='Potential Conflict',x['retrieval_score']),reverse=True)
    statuses={x['alignment_status'] for x in matches}
    overall='Potential Conflict' if 'Potential Conflict' in statuses else 'Requires Review' if 'Requires Review' in statuses else 'Aligned' if statuses else 'Unmapped'
    return overall,matches

@app.get('/health')
def health():
    return {'status':'ok','documents_loaded':len({s['document_id'] for s in EVIDENCE}),'sections_loaded':len(EVIDENCE),'retrieval':'TF-IDF ranking with deterministic relevance and alignment rules','synthetic_corpus':True}

@app.post('/align')
def align(req:AlignmentRequest):
    if not req.request_id.strip() or len(req.scenario_text.strip())<5:
        raise HTTPException(400,'Nonblank request ID and scenario text of at least five characters required.')
    status,matches=assess(req.scenario_text.strip())
    return {'request_id':req.request_id.strip(),'domain':req.domain,'alignment_status':status,'policy':[x for x in matches if x['document_type']=='Policy'],'sop':[x for x in matches if x['document_type']=='SOP'],'strategy':[x for x in matches if x['document_type']=='Strategy'],'evidence_count':len(matches),'review_required':status!='Aligned','advisory_only':True,'production_authorized':False,'limitations':'Synthetic documents; rule-based textual matching may miss relevant guidance or misread negation. Unmapped is not approval. Human verification and existing controls always apply.'}
