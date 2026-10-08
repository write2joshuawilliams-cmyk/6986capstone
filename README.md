# RAG-Based Decision Support System for Policy and Architecture Alignment

**Author:** Joshua Williams  
**Organization:** Alabama Medicaid Agency  
**Course:** INAI 6986 - AI Capstone  
**Model family:** Deep Learning (LLM + RAG)  
**Execution environment:** Agency-controlled on-premises AI infrastructure  
**Workflow automation:** n8n

## Project overview

This capstone develops a Retrieval-Augmented Generation (RAG) decision-support system for reviewing technology proposals, RFPs, major change requests, architecture proposals, and priority work items against an approved corpus of Alabama Medicaid Agency technology governance, security, data-protection, and architecture sources.

The system retrieves relevant governing passages, identifies potential policy conflicts or missing requirements, and produces structured findings with citations for human review. It is **not** an autonomous compliance or approval system.

## Data boundary

The capstone's retrieval and model experiments are designed to run on **agency-controlled on-premises AI infrastructure**. Corpus text, cleaned extracts, embeddings, vector indexes, retrieved passages, prompts, and model outputs are intended to remain within that environment.

This public GitHub repository contains **code, configuration, schemas, and public-use/de-identified evaluation artifacts only**. Raw source documents are intentionally excluded.

## Current corpus profile

- **8 source documents**
- **276 source pages**
- approximately **66,994 cleaned words**
- **3 OCR-processed** ITPG governance PDFs
- **5 machine-readable** sources at intake

| Configuration | Target tokens | Overlap | Chunks |
|---|---:|---:|---:|
| Config A | 500 | 75 | 221 |
| Config B | 750 | 100 | 158 |
| Config C | 1000 | 150 | 107 |

The first controlled vector-retrieval experiment uses **750-token chunks / 100-token overlap / top-k 5 / no reranker / no metadata filter**.

## Evaluation design

### Retrieval comparison
- BM25/full-text baseline -> Retrieval Hit@5
- vector retrieval -> Retrieval Hit@5
- average rank of the first expected governing source

### Finding comparison
Each retriever's top-five passages will be passed to the **same fixed local LLM and same prompt/output schema**.

Metrics:
- Potential Policy Conflict recall
- Missing Requirement recall
- precision
- citation accuracy
- unsupported-claim rate

Fixed thresholds:
- **>= 85% recall** for Potential Policy Conflict
- **>= 85% recall** for Missing Requirement
- **>= 90% citation accuracy**

Confidence intervals will be reported with final results.

## Gold set

Final target:
- 40 Potential Policy Conflict
- 40 Missing Requirement
- 10 Aligned
- 10 Needs Human Review

A 25-scenario pilot set is included for pipeline testing. Pilot cases remain **Draft** until blind independent review/adjudication is completed.

Independent reviewer: **Brad Bird / Office of the CISO**.

## Repository structure

```text
6986capstone/
├── .gitignore
├── README.md
├── requirements.txt
├── configs/
├── scripts/
├── evaluation/
├── artifacts/
├── data/
└── n8n/
```

## Reproducibility workflow

1. Place approved source files locally under `data/raw/`.
2. Run `scripts/parse_documents.py`.
3. Run:
   `python scripts/chunk_documents.py --config configs/chunking_750_100.json`
4. Run the keyword baseline:
   `python scripts/run_baseline.py`
5. Select and pin an approved local embedding model.
6. Set:
   `LOCAL_EMBEDDING_MODEL_PATH=<approved local model path or identifier>`
   `LOCAL_DEVICE=cuda`
7. Run:
   `python scripts/run_vector_onprem.py`
8. Record exact local model, version/hash, runtime, hardware/device, and run date before reporting results.

## Security / repository rules

Do **not** commit raw source documents, restricted OCR output, model weights, embeddings/vector stores, secrets, credentials, `.env` files, PII/PHI, confidential vendor pricing, or restricted operational data.

## AI use disclosure

OpenAI ChatGPT was used as an academic drafting/coding assistant to help organize project documentation and create portions of the reproducible data-preparation and evaluation workflow. The documents supplied for that academic work were identified by the project author as public-use policy/strategy documents. The capstone RAG/model experiment itself is intended to execute on agency-controlled on-premises AI infrastructure.
