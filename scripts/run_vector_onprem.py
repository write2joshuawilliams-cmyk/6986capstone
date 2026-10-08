#!/usr/bin/env python3
import os, csv, json
from pathlib import Path
import numpy as np
from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).resolve().parents[1]
CHUNKS_CSV = ROOT / "artifacts" / "chunks_750_100.csv"
GOLD_CSV = ROOT / "evaluation" / "gold_set_pilot_25.csv"
OUTPUT_CSV = ROOT / "artifacts" / "vector_results.csv"
CACHE = ROOT / "artifacts" / "embedding_cache_local.npz"
TOP_K = 5

MODEL_PATH = os.environ.get("LOCAL_EMBEDDING_MODEL_PATH")
DEVICE = os.environ.get("LOCAL_DEVICE", "cuda")

if not MODEL_PATH:
    raise SystemExit("Set LOCAL_EMBEDDING_MODEL_PATH before running.")

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

def load_csv(path):
    if not path.exists():
        raise FileNotFoundError(f"Required file not found: {path}")
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def require_columns(rows, required, name):
    if not rows:
        raise RuntimeError(f"{name} is empty.")
    missing = [c for c in required if c not in rows[0]]
    if missing:
        raise RuntimeError(f"{name} missing columns: {missing}")

chunks = load_csv(CHUNKS_CSV)
gold = load_csv(GOLD_CSV)

require_columns(chunks, ["chunk_id","document_id","title","domain","page_start","page_end","section","text"], "chunk file")
require_columns(gold, ["scenario_id","scenario_text","expected_document_ids","expected_class"], "gold-set file")

model = SentenceTransformer(MODEL_PATH, device=DEVICE)

if CACHE.exists():
    corpus_vectors = np.load(CACHE)["vectors"]
    if corpus_vectors.shape[0] != len(chunks):
        raise RuntimeError("Embedding cache does not match current chunks. Delete the cache and rerun.")
else:
    corpus_inputs = [
        f"Document: {c['title']}\nDomain: {c['domain']}\nSection: {c['section']}\n\n{c['text']}"
        for c in chunks
    ]
    corpus_vectors = model.encode(
        corpus_inputs,
        batch_size=32,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=True,
    ).astype(np.float32)
    np.savez_compressed(CACHE, vectors=corpus_vectors)

query_vectors = model.encode(
    [g["scenario_text"] for g in gold],
    batch_size=32,
    convert_to_numpy=True,
    normalize_embeddings=True,
    show_progress_bar=True,
).astype(np.float32)

results = []
for g, qv in zip(gold, query_vectors):
    scores = corpus_vectors @ qv
    top_idx = np.argsort(-scores)[:TOP_K]
    expected_ids = {x.strip() for x in (g.get("expected_document_ids") or "").split(";") if x.strip()}
    hit_rank = None
    hit_chunk_id = ""
    matched_source = ""
    top5 = []

    for rank, idx in enumerate(top_idx, start=1):
        c = chunks[int(idx)]
        top5.append({
            "rank": rank,
            "score": float(scores[idx]),
            "chunk_id": c["chunk_id"],
            "document_id": c["document_id"],
            "title": c["title"],
            "page_start": c["page_start"],
            "page_end": c["page_end"],
            "section": c["section"],
        })
        if hit_rank is None and c["document_id"] in expected_ids:
            hit_rank = rank
            hit_chunk_id = c["chunk_id"]
            matched_source = c["title"]

    results.append({
        "scenario_id": g["scenario_id"],
        "scenario_type": g.get("scenario_type", ""),
        "domain": g.get("domain", ""),
        "scenario_text": g["scenario_text"],
        "expected_class": g["expected_class"],
        "expected_document_ids": g.get("expected_document_ids", ""),
        "retrieval_hit_at_5": "Hit" if hit_rank is not None else "Miss",
        "hit_rank": hit_rank or "",
        "matched_chunk_id": hit_chunk_id,
        "matched_source": matched_source,
        "top_5_json": json.dumps(top5, ensure_ascii=False),
        "embedding_model_path": MODEL_PATH,
        "device": DEVICE,
    })

with OUTPUT_CSV.open("w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(results[0].keys()))
    w.writeheader()
    w.writerows(results)

hits = [r for r in results if r["retrieval_hit_at_5"] == "Hit"]
ranks = [int(r["hit_rank"]) for r in hits]

print("ON-PREMISES VECTOR RETRIEVAL SUMMARY")
print(f"Scenarios: {len(results)}")
print(f"Hit@5: {len(hits)}/{len(results)} = {len(hits)/len(results):.1%}")
print(f"Average hit rank: {sum(ranks)/len(ranks):.2f}" if ranks else "Average hit rank: N/A")
print(f"Results: {OUTPUT_CSV}")
