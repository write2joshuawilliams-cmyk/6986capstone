# Lightweight On-Premises AI-Assisted IT Work Triage for Generalist State Agency IT Teams

INAI 6986 capstone | Joshua Williams | Mid-sized state agency case study

A local, advisory-only academic prototype for generalist IT teams. It combines a frozen text classifier, deterministic priority assessment, local policy/SOP/strategy evidence retrieval, n8n orchestration, persistent audit records, human review and a browser-based prioritized work-item list. No assessment or reviewer decision authorizes production work.

## Repository map

- [Assignment 1 — Proposal](Assignment%201%20-%20Proposal/)
- [Assignment 2 — Plan and Progress](Assignment%202%20-%20Plan%20and%20Progress/)
- [Progress Log 2](Assignment%202B%20-%20Logs/)
- [Assignment 3 — Data and Model](Assignment%203%20-%20Data%20and%20Model/)
- [Assignment 4 — Model Testing](Assignment%204%20-%20Model%20Testing/)
- [Assignment 5 — Automation: setup and evidence](Assignment%205%20-%20Automation/README.md)
- [Data — synthetic datasets and review evidence](Data/)

## Model and results

200 synthetic scenarios in four domains: 120 training, 40 validation and 40 protected test. TF-IDF + Multinomial Naive Bayes (NB-v1) achieved validation recall 90%; held-out recall 85%, precision 94.4%, F1 89.5% and accuracy 90%. The 90% recall target was missed; the 80% precision safeguard was met. No post-test tuning. Model confidence is uncalibrated. Priority and alignment are deterministic components, not additional trained models.

Frozen model SHA-256: `e7e440cacfc5926e4eab482bc9baad188eebedf2dbab22b21b3d49fcffac4239`.

## Final prototype (November 25, 2026)

See [Assignment 5 setup instructions](Assignment%205%20-%20Automation/README.md) for installation and startup. The tested configuration is NB-v1, alignment 1.1.0, priority 1.0.0, audit 1.0.0, n8n 2.49.5 with workflow v3.1, dashboard 1.2.0 and startup launcher 1.2. The dashboard is served locally at `http://127.0.0.1:8004/`.

Demonstrations include routine and escalation paths, human acceptance/rejection/override, duplicate suppression, service failure, controlled retry, version mismatch blocking and a ranked work-item list. Dashboard v1.0 passed 14 planned checks; the priority-list extension passed 11 planned checks in the recorded demonstrations. These are functional checks, not estimates of real-world accuracy or production readiness.

## Reproduction and limitations

For notebook reproduction, copy the corresponding dataset from Data into the notebook working directory; the evaluation notebook also requires the frozen model. Do not tune on the frozen test set. For the integrated prototype, follow the Assignment 5 instructions and use synthetic data only.

Reviewer identities are self-reported, documents are synthetic, and auditing is not tamper-resistant. Alignment may miss evidence or misread negation. Unmapped is not approval. Recovery from abruptly interrupted processing is limited. Keep all services on loopback; no production use, credentials, personal information, private agency documents or runtime databases. Historical versions and evidence are retained for academic traceability. Written milestone and final governance deliverables are separate from the software freeze.
