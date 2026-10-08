#!/usr/bin/env python3
"""
Chunk cleaned Markdown documents using an approximate tokenizer.
For the formal experiment, keep the same tokenizer/settings across configurations.
"""
from pathlib import Path
import argparse, json, csv, re

ROOT=Path(__file__).resolve().parents[1]
PROCESSED=ROOT/"data"/"processed"
ART=ROOT/"artifacts"

def tokens(text):
    return re.findall(r"\S+", text)

def chunk_words(words, target, overlap):
    step=max(1,target-overlap)
    for i in range(0,len(words),step):
        piece=words[i:i+target]
        if piece:
            yield i//step+1, " ".join(piece)
        if i+target>=len(words):
            break

ap=argparse.ArgumentParser()
ap.add_argument("--config",required=True)
args=ap.parse_args()
cfg=json.loads(Path(args.config).read_text())
target=int(cfg["target_tokens"])
overlap=int(cfg["overlap_tokens"])

rows=[]
for path in sorted(PROCESSED.glob("*.md")):
    text=path.read_text(encoding="utf-8")
    words=tokens(text)
    doc_id=re.sub(r"[^A-Za-z0-9]+","_",path.stem).strip("_").upper()
    for idx,piece in chunk_words(words,target,overlap):
        rows.append({
            "chunk_id":f"{doc_id}__{target}_{overlap}__{idx:04d}",
            "document_id":doc_id,
            "source_file":path.name,
            "strategy":f"{target}_{overlap}",
            "chunk_index":idx,
            "token_count_approx":len(tokens(piece)),
            "text":piece
        })

out=ART/f"chunks_{target}_{overlap}.csv"
with out.open("w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)
print(f"Wrote {len(rows)} chunks to {out}")
