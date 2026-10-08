# RAG-Based Decision Support System for Policy and Architecture Alignment

**Author:** Joshua Williams  
**Organization:** Alabama Medicaid Agency  
**Course:** INAI 6986 - AI Capstone  
**Model family:** Deep Learning (LLM + RAG)  
**Execution environment:** Agency-controlled on-premises AI infrastructure  
**Workflow automation:** n8n

## Project overview

This capstone develops a Retrieval-Augmented Generation (RAG) decision-support system for reviewing technology proposals, RFPs, major change requests, architecture proposals, and priority work items against an approved corpus of Alabama Medicaid Agency technology governance, security, data-protection, and architecture sources.

The system is designed to retrieve relevant governing passages, identify potential policy conflicts or missing requirements, and produce structured findings with citations for human review. It is **not** an autonomous compliance or approval system.

## Data boundary

The capstone's model-development and retrieval experiments are designed to run on **agency-controlled on-premises AI systems**. Corpus text, cleaned extracts, embeddings, vector indexes, retrieved passages, prompts, and model outputs are intended to remain within that environment.

The public GitHub repository contains **code, configuration, schemas, and de-identified/public-use evaluation artifacts only**. Raw source documents are intentionally excluded.

## Current corpus profile

The current source corpus contains:

- **8 documents**
- **276 source pages**
- approximately **66,994 cleaned words**
- 3 OCR-processed ITPG governance PDFs
- 5 sources that were machine-readable at intake

Candidate chunking configurations:

| Configuration | Target tokens | Overlap | Chunks |
|---|---:|---:|---:|
| Config A | 500 | 75 | 221 |
| Config B | 750 | 100 | 158 |
| Config C | 1000 | 150 | 107 |

The first controlled vector-retrieval experiment uses **750 tokens / 100 overlap / top-k 5 / no reranker / no metadata filter**.

## Evaluation design

The evaluation separates retrieval quality from finding quality.

### Retrieval comparison

Both retrieval methods are evaluated on the same frozen scenarios:

- keyword/full-text baseline -> Retrieval Hit@5
- vector retrieval -> Retrieval Hit@5
- average rank of the first expected governing source

### Finding comparison

For finding-level comparison, each retriever's top-five passages are passed to the **same fixed local LLM and the same prompt/output schema**. This allows comparison of:

- Policy Conflict recall
- Missing Requirement recall
- precision
- citation accuracy
- unsupported-claim rate

Fixed prototype thresholds:

- **>= 85% recall** for Potential Policy Conflict
- **>= 85% recall** for Missing Requirement
- **>= 90% citation accuracy**

Thresholds are fixed before final tuning. Confidence intervals will be reported.

## Gold set

The final target is 100 scenarios:

- 40 Potential Policy Conflict
- 40 Missing Requirement
- 10 Aligned
- 10 Needs Human Review

A 25-scenario pilot set is included for pipeline testing. The pilot set is **not represented as fully frozen or independently validated until the reviewer process is complete**. Additional scenarios will use realistic vendor/project-team language to reduce lexical leakage from policy clauses.

Independent reviewer: **Brad Bird / Office of the CISO**.

## Repository structure

```text
6986capstone/
├── .gitignore
├── README.md
├── requirements.txt
├── configs/
│   ├── chunking_500_75.json
│   ├── chunking_750_100.json
│   ├── chunking_1000_150.json
│   └── vector_config_1.json
├── scripts/
│   ├── parse_documents.py
│   ├── chunk_documents.py
│   ├── run_baseline.py
│   └── run_vector_onprem.py
├── evaluation/
│   ├── gold_set_schema.json
│   ├── gold_set_pilot_25.csv
│   └── freeze_log.csv
├── artifacts/
│   ├── corpus_profile.json
│   └── chunk_manifest.csv
├── data/
│   ├── raw/          # local only; ignored by git
│   └── processed/    # local only; ignored by git
└── n8n/
    └── README.md
```

## Reproducibility workflow

1. Place approved source files locally under `data/raw/`.
2. Run `scripts/parse_documents.py` to create cleaned local text and a corpus profile.
3. Run `scripts/chunk_documents.py --config configs/chunking_750_100.json`.
4. Run `scripts/run_baseline.py` against the pilot/frozen evaluation set.
5. Select and pin an approved local embedding model.
6. Run `scripts/run_vector_onprem.py`.
7. Record exact local model name/path, version/hash, runtime version, device/hardware, and run date before reporting results.
8. After retrieval evaluation, run the matched finding-level comparison using the same local LLM/prompt for both retrieval paths.

## Security / repository rules

Do **not** commit:

- raw policy/source documents
- OCR output containing restricted material
- model weights
- embeddings/vector stores
- API keys or credentials
- `.env` files
- local runtime configuration containing secrets
- PII/PHI, credentials, vendor pricing, or restricted operational data

This repository is intended to demonstrate the reproducible project workflow without publishing the operational corpus or model assets.

## AI use

OpenAI ChatGPT was used as an academic drafting/coding assistant to help organize project documentation and create portions of the reproducible data-preparation/evaluation workflow. The documents supplied for that academic work were identified by the project author as public-use policy/strategy documents. The capstone RAG/model experiment itself is intended to execute on agency-controlled on-premises AI infrastructure.
