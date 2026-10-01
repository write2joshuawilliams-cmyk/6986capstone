# 6986capstone
AUM 6986 capstone
# RAG-Based Decision Support System for Policy and Architecture Alignment

**Author:** Joshua Williams  
**Organization:** Alabama Medicaid Agency  
**Course:** INAI 6986 - Capstone Project  
**Model Family:** Deep Learning (LLM + RAG) | GPT-4.1 via Azure OpenAI  
**Workflow Automation:** n8n  

---

## 📌 Project Overview
This project develops a Retrieval-Augmented Generation (RAG) decision-support system to evaluate technology review documents—such as RFPs, major change requests, project proposals, and priority work lists—against an approved corpus of Alabama Medicaid Agency technology governance, security, and architecture standards. 

The system retrieves relevant governing passages, identifies potential policy conflicts or missing requirements, and generates structured, cited findings for human review while preserving a strict human-in-the-loop decision boundary.

---

## 📁 Repository Structure
```text
6986capstone/
├── .gitignore               # Exclusion rules for sensitive data and secrets
├── README.md                # Project documentation and setup guide
├── requirements.txt         # Python dependencies
├── configs/                 # RAG pipeline, embedding, and chunking configurations
├── scripts/                 # Ingestion, parsing, chunking, and baseline execution scripts
│   ├── parse_documents.py   # Document text extraction and normalization
│   ├── chunk_and_index.py   # Text chunking and vector index creation
│   └── run_baseline.py      # Keyword/full-text search baseline evaluation
├── evaluation/              # Synthetic evaluation scenarios and benchmarking
│   └── gold_set_schema.json # Schema for locked gold-set evaluation scenarios
└── n8n/                     # n8n workflow definitions and routing logic
