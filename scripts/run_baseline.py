#!/usr/bin/env python3
"""
Simple BM25-style keyword baseline.
Input:
  evaluation/gold_set_pilot_25.csv
  artifacts/chunks_750_100.csv (or another chunk file)
Output:
  artifacts/baseline_results.csv
"""
from pathlib import Path
from collections import Counter
import csv, math, re, argparse

ROOT=Path(__file__).resolve().parents[1]

def tok(s):
    return re.findall(r"[a-z0-9]+(?:[-'][a-z0-9]+)?",(s or "").lower())

def load(path):
    with open(path,encoding="utf-8-sig",newline="") as f:
        return list(csv.DictReader(f))

ap=argparse.ArgumentParser()
ap.add_argument("--chunks",default=str(ROOT/"artifacts"/"chunks_750_100.csv"))
ap.add_argument("--gold",default=str(ROOT/"evaluation"/"gold_set_pilot_25.csv"))
args=ap.parse_args()

chunks=load(args.chunks)
gold=load(args.gold)
docs=[tok(c["text"]) for c in chunks]
N=len(docs)
avgdl=sum(map(len,docs))/max(N,1)
df=Counter()
for d in docs:
    for t in set(d): df[t]+=1

def score(q,d):
    tf=Counter(d); dl=len(d); k1=1.5; b=.75; s=0
    for term in q:
        n=df.get(term,0)
        if not n or not tf.get(term): continue
        idf=math.log(1+(N-n+.5)/(n+.5))
        fq=tf[term]
        s += idf*(fq*(k1+1))/(fq+k1*(1-b+b*dl/avgdl))
    return s

results=[]
for g in gold:
    query=tok(g.get("baseline_keywords") or g["scenario_text"])
    ranked=sorted(((score(query,d),i) for i,d in enumerate(docs)), reverse=True)[:5]
    expected={x for x in g["expected_document_ids"].split(";") if x}
    hit_rank=""
    top=[]
    for rank,(s,i) in enumerate(ranked,1):
        c=chunks[i]
        top.append(f"{rank}. {c['document_id']} | {c['chunk_id']} | {s:.4f}")
        if not hit_rank and c["document_id"] in expected: hit_rank=rank
    results.append({
        "scenario_id":g["scenario_id"],
        "retrieval_hit_at_5":"Hit" if hit_rank else "Miss",
        "hit_rank":hit_rank,
        "top_5":"\n".join(top)
    })

out=ROOT/"artifacts"/"baseline_results.csv"
with out.open("w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(results[0].keys()))
    w.writeheader(); w.writerows(results)
print(out)
