#!/usr/bin/env python3
from pathlib import Path
import argparse, csv, json, re

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
ARTIFACTS = ROOT / "artifacts"
ARTIFACTS.mkdir(parents=True, exist_ok=True)

PAGE_RE = re.compile(r"<!--\s*PAGE\s+(\d+)\s*-->", re.I)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")

def normalize_id(name):
    return re.sub(r"[^A-Za-z0-9]+", "_", name).strip("_").upper()

def infer_domain(stem):
    s = stem.lower()
    if "security" in s: return "Security"
    if "itpg" in s or "governance" in s: return "Governance"
    if "data protection" in s: return "Data Protection"
    if "infrastructure principles" in s or "storage strategy" in s or "guide" in s: return "Architecture"
    if "strategic" in s: return "Strategy"
    return "Other"

def tokens(text):
    return re.findall(r"\S+", text)

def parse_units(text):
    page = None
    section = ""
    units = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        pm = PAGE_RE.fullmatch(line)
        if pm:
            page = int(pm.group(1))
            continue
        hm = HEADING_RE.match(line)
        if hm:
            section = hm.group(2).strip()
            continue
        units.append({"text": line, "page": page, "section": section})
    return units

def build_chunks(units, target, overlap):
    flat = []
    for u in units:
        for tok in tokens(u["text"]):
            flat.append({"token": tok, "page": u["page"], "section": u["section"]})
    step = max(1, target - overlap)
    result = []
    for start in range(0, len(flat), step):
        part = flat[start:start+target]
        if not part:
            break
        pages = [x["page"] for x in part if x["page"] is not None]
        sections = [x["section"] for x in part if x["section"]]
        result.append({
            "text": " ".join(x["token"] for x in part),
            "token_count": len(part),
            "page_start": min(pages) if pages else "",
            "page_end": max(pages) if pages else "",
            "section": sections[-1] if sections else ""
        })
        if start + target >= len(flat):
            break
    return result

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    args = ap.parse_args()
    cfg = json.loads(Path(args.config).read_text(encoding="utf-8"))
    target = int(cfg["target_tokens"])
    overlap = int(cfg["overlap_tokens"])
    strategy = f"{target}_{overlap}"

    rows = []
    for path in sorted(PROCESSED.glob("*.md")):
        doc_id = normalize_id(path.stem)
        title = path.stem.replace("_", " ")
        domain = infer_domain(path.stem)
        units = parse_units(path.read_text(encoding="utf-8"))
        for idx, c in enumerate(build_chunks(units, target, overlap), start=1):
            rows.append({
                "chunk_id": f"{doc_id}__{strategy}__{idx:04d}",
                "document_id": doc_id,
                "title": title,
                "domain": domain,
                "strategy": strategy,
                "chunk_index": idx,
                "token_count": c["token_count"],
                "page_start": c["page_start"],
                "page_end": c["page_end"],
                "section": c["section"],
                "text": c["text"],
            })

    if not rows:
        raise SystemExit(f"No cleaned Markdown files found in {PROCESSED}. Run parse_documents.py first.")

    out = ARTIFACTS / f"chunks_{strategy}.csv"
    fields = ["chunk_id","document_id","title","domain","strategy","chunk_index","token_count","page_start","page_end","section","text"]
    with out.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    print(f"Wrote {len(rows)} chunks to {out}")

if __name__ == "__main__":
    main()
