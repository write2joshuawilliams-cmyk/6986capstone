# Lightweight On-Premises AI-Assisted IT Work Triage for Generalist State Agency IT Teams

INAI 6986 capstone | Joshua Williams | Mid-sized state agency case study

The prototype recommends routine generalist handling or escalation for IT work items. It is advisory only and cannot authorize production changes. Deterministic priority assessment and local SOP, policy and strategy evidence retrieval are planned separate components.

## Repository map

- [Assignment 1 — Proposal](Assignment%201%20-%20Proposal/)
- [Assignment 2 — Plan and Progress](Assignment%202%20-%20Plan%20and%20Progress/)
- [Progress Log 2](Assignment%202B%20-%20Logs/)
- [Assignment 3 — Data and Model](Assignment%203%20-%20Data%20and%20Model/): notebooks, validation results and frozen model.
- [Assignment 4 — Model Testing](Assignment%204%20-%20Model%20Testing/): notebooks, held-out evaluation and robustness evidence.
- [Assignment 5 — Automation](Assignment%205%20-%20Automation/): local API, workflow definitions and demonstration screenshots.
- [Data](Data/): synthetic development and frozen evaluation inputs and review evidence.

## Results

200 synthetic scenarios in four domains: 120 training, 40 validation and 40 protected test. TF-IDF + Multinomial Naive Bayes achieved validation recall 90% and held-out recall 85%, precision 94.4%, accuracy 90%. The 90% recall target was missed; the 80% precision safeguard was met. No post-test tuning reported. Prototype only.

## Local reproduction

Open [the API folder](Assignment%205%20-%20Automation/API/). Use Python 3.13 and scikit-learn 1.6.1. The original frozen model is included. Expected SHA-256:

`e7e440cacfc5926e4eab482bc9baad188eebedf2dbab22b21b3d49fcffac4239`

Run `install_api.bat`, then `start_api_venv.bat`. Check `http://localhost:8000/health`. Start local n8n (tested version 2.49.5), import `IT_Work_Triage_v1_TESTED.json`, and use synthetic requests at `http://localhost:5678/webhook-test/it-work-triage`. The workflow display name and webhook path were changed after the original demonstrations; re-test the renamed endpoint. No classification logic changed.

Routine, escalation, duplicate, invalid input and service failure paths were exercised in the original workflow. Actual reviewer interaction and persistent workflow audit logging remain outstanding.

For notebook reproduction, copy the corresponding dataset from Data into the notebook working directory. The evaluation notebook also requires the original frozen model. Do not use the frozen test set for tuning.

## Privacy and history

Do not publish private agency documents, credentials, personal information, local databases or live work items. Historical submission documents and screenshots remain as evidence; the original project scope is preserved in the archive/original-project-scope branch.
