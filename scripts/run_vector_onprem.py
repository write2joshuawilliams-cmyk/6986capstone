#!/usr/bin/env python3
"""
INAI 6986 - On-Premises Vector Retrieval Experiment
Configuration 1: 750-token chunks / 100-token overlap / top-k=5 / no reranker / no metadata filter.

No external model API is used.
The embedding model must already be available on the on-premises AI system or at a local filesystem path.
"""

import os
import csv
import json
from pathlib import Path
import numpy as np
from sentence_transformers import SentenceTransformer

HERE = Path(__file__).resolve().parent
CHUNKS_CSV = HERE / "chunks_750_100.csv"
GOLD_CSV = HERE / "gold_set_vector_input.csv"
OUTPUT_CSV = HERE / "vector_results.csv"
CACHE = HERE / "embedding_cache_local.npz"
TOP_K = 5

MODEL_PATH = os.environ.get("LOCAL_EMBEDDING_MODEL_PATH")
DEVICE = os.environ.get("LOCAL_DEVICE", "cuda")

if not MODEL_PATH:
    raise SystemExit(
        "Set LOCAL_EMBEDDING_MODEL_PATH to an approved on-premises embedding model name or local filesystem path."
    )

# Optional: force offline behavior when models are pre-staged locally.
os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

model = SentenceTransformer(MODEL_PATH, device=DEVICE)

def load_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

chunks = load_csv(CHUNKS_CSV)
gold = load_csv(GOLD_CSV)

if CACHE.exists():
    cache = np.load(CACHE)
    corpus_vectors = cache["vectors"]
    if corpus_vectors.shape[0] != len(chunks):
        raise RuntimeError("Embedding cache does not match the current chunk file. Delete the cache and rerun.")
    print(f"Loaded {len(chunks)} cached local corpus embeddings.")
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
    print("Saved local embedding cache:", CACHE)

# Prevent answer leakage: query = scenario text only.
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
    expected_ids = {x.strip() for x in g["expected_document_ids"].split(";") if x.strip()}

    hit_rank = None
    hit_chunk_id = ""
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

    results.append({
        **g,
        "retrieval_hit_at_5": "Hit" if hit_rank is not None else "Miss",
        "hit_rank": hit_rank or "",
        "matched_chunk_id": hit_chunk_id,
        "top_5_json": json.dumps(top5, ensure_ascii=False),
        "embedding_model_path": MODEL_PATH,
        "device": DEVICE,
    })

with OUTPUT_CSV.open("w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=list(results[0].keys()))
    writer.writeheader()
    writer.writerows(results)

hits = [r for r in results if r["retrieval_hit_at_5"] == "Hit"]
ranks = [int(r["hit_rank"]) for r in hits]
print()
print("ON-PREMISES VECTOR RETRIEVAL SUMMARY")
print(f"Embedding model/path: {MODEL_PATH}")
print(f"Device: {DEVICE}")
print(f"Scenarios: {len(results)}")
print(f"Hit@5: {len(hits)}/{len(results)} = {len(hits)/len(results):.1%}")
print(f"Average hit rank: {sum(ranks)/len(ranks):.2f}" if ranks else "Average hit rank: N/A")
print("Results:", OUTPUT_CSV)
