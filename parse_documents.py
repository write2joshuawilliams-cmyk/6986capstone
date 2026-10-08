#!/usr/bin/env python3
"""
Parse and clean local PDF/DOCX sources into Markdown-like text.

Raw documents remain under data/raw/ and are excluded from Git.
This script is intentionally conservative: it removes formatting noise
but does not rewrite source meaning.
"""
from pathlib import Path
from collections import Counter
import re, json, hashlib
import fitz
from docx import Document

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "processed"
ART = ROOT / "artifacts"
OUT.mkdir(parents=True, exist_ok=True)
ART.mkdir(parents=True, exist_ok=True)

def sha256(path):
    h = hashlib.sha256()
    with open(path,"rb") as f:
        for block in iter(lambda:f.read(1024*1024), b""):
            h.update(block)
    return h.hexdigest()

def normalize(s):
    repl = {"\u00a0":" ","\u2013":"-","\u2014":"-","\u2018":"'","\u2019":"'","\u201c":'"',"\u201d":'"',"\u00ad":""}
    for a,b in repl.items():
        s=s.replace(a,b)
    s=re.sub(r"[ \t]+"," ",s)
    return s.strip()

def clean_pdf(path):
    doc=fitz.open(path)
    pages=[]
    boundary=[]
    for i,p in enumerate(doc,1):
        lines=[normalize(x) for x in (p.get_text("text") or "").splitlines()]
        lines=[x for x in lines if x]
        pages.append(lines)
        boundary += lines[:3] + lines[-3:]
    counts=Counter(x for x in boundary if len(x)<=160)
    repeated={x for x,c in counts.items() if c>=max(3, round(len(pages)*0.2))}
    out=[]
    for i,lines in enumerate(pages,1):
        out.append(f"<!-- PAGE {i} -->")
        for j,line in enumerate(lines):
            edge=j<3 or j>=len(lines)-3
            if edge and line in repeated: continue
            if edge and re.fullmatch(r"(page\s*)?\d+(\s*/\s*\d+)?",line,re.I): continue
            out.append(line)
        out.append("")
    return "\n".join(out), len(doc)

def clean_docx(path):
    d=Document(path)
    out=[]
    for p in d.paragraphs:
        txt=normalize(p.text)
        if not txt: continue
        style=(p.style.name or "").lower() if p.style else ""
        if "heading" in style:
            m=re.search(r"(\d+)",style)
            level=max(1,min(6,int(m.group(1)) if m else 2))
            out.append("#"*level+" "+txt)
        else:
            out.append(txt)
        out.append("")
    return "\n".join(out), None

profile=[]
for path in sorted(RAW.iterdir()):
    if path.suffix.lower() not in {".pdf",".docx"}:
        continue
    if path.suffix.lower()==".pdf":
        text,pages=clean_pdf(path)
    else:
        text,pages=clean_docx(path)
    target=OUT/(path.stem+".md")
    target.write_text(text,encoding="utf-8")
    words=len(re.findall(r"\b[\w'-]+\b",text))
    profile.append({
        "source_file":path.name,
        "cleaned_file":target.name,
        "pages":pages,
        "cleaned_words":words,
        "sha256":sha256(path)
    })

(ART/"corpus_profile.json").write_text(json.dumps(profile,indent=2),encoding="utf-8")
print(f"Processed {len(profile)} documents")
print(f"Total cleaned words: {sum(x['cleaned_words'] for x in profile):,}")
