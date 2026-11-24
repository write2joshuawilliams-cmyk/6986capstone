# IRIS — Lightweight On-Premises AI-Assisted IT Work Triage

INAI 6986 capstone | Joshua Williams | Mid-sized state agency case study

IRIS recommends routine generalist handling or escalation for IT work items. It is advisory only and cannot authorize production changes. A deterministic priority guide and local SOP, policy and strategy evidence retrieval are planned separate components.

## Evidence to date
- Synthetic dataset: 200 scenarios, four domains, 120 train / 40 validation / 40 protected test.
- Selected model: TF-IDF + Multinomial Naive Bayes. Validation recall 90%; held-out recall 85%, precision 94.4%, accuracy 90%. Recall target 90% not met; precision safeguard 80% met. No post-test tuning reported. Prototype only.
- Local Python API and n8n core routing demonstrated on Windows. Routine, escalation, duplicate, bad input and service failure paths exercised. Actual reviewer interaction and persistent workflow audit trail remain to be verified.

## Repository map
- `data/`: development and frozen evaluation inputs. Do not use test data for selection or tuning.
- `modeling/assignment3/`: executed development notebook.
- `modeling/assignment4/`: executed evaluation notebook and result files.
- `model_api/`: Windows API source and setup; original frozen model must be supplied separately.
- `n8n/`: initial importable workflow definition; replace/add the actual tested export when available.

## Reproduction
Use Python 3.13 and scikit-learn 1.6.1 for the local API. Copy the original `assignment3_selected_model_naive_bayes.joblib` into `model_api/`; expected SHA-256 `e7e440cacfc5926e4eab482bc9baad188eebedf2dbab22b21b3d49fcffac4239`. Run `install_api.bat`, then `start_api_venv.bat`. Check `http://localhost:8000/health`. Run n8n locally (observed version 2.49.5) and import the workflow. Keep both services local. Use synthetic demo requests only.

For notebook reproduction, place the corresponding dataset in the notebook working directory. The evaluation notebook also requires the original frozen model; its schema adapter uses the frozen CSV's final label. Reproduction is not a new tuning round.

## Privacy
No private agency documents, credentials, local databases or live work items belong here. The original project is preserved in the archive/original-project-scope branch. This main branch is being migrated; missing artifacts are not yet published.