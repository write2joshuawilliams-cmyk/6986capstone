# Dataset iteration history

Retrospective record — November 25, 2026. Counts and batch purposes are drawn from the original workbooks, not reconstructed experiment outcomes.

| Stage | Added | Total | Purpose documented at the time |
|---|---:|---:|---|
| Pilot | 40 | 40 | Establish balanced four-domain binary decision dataset and labeling rules. |
| Batch 2 | 40 | 80 | Fill weak coverage areas identified in the coverage matrix rather than paraphrase pilot cases. |
| Batch 3 | 40 | 120 | Broaden lifecycle, resilience, audit/logging, retention, security requirements, contract scope and support coverage. |
| Final 80 | 80 | 200 | Harden decision boundaries with borderline and mixed-signal scenarios; use technical terms across both labels. |

## Verified workbook counts

- `Williams_INAI6986_40_Scenario_Pilot_Dataset(1).xlsx` / `Pilot_Classifier`: 40 rows; Backup/DR: 5 routine, 5 escalation; Infrastructure: 5 routine, 5 escalation; Procurement/Vendor/RFP: 5 routine, 5 escalation; Security/Policy: 5 routine, 5 escalation.
- `Williams_INAI6986_Batch2_40_Scenarios(1).xlsx` / `Batch2_Classifier`: 40 rows; Backup/DR: 5 routine, 5 escalation; Infrastructure: 5 routine, 5 escalation; Procurement/Vendor/RFP: 5 routine, 5 escalation; Security/Policy: 5 routine, 5 escalation.
- `Williams_INAI6986_Batch3_40_Scenarios(1).xlsx` / `Batch3_Classifier`: 40 rows; Backup/DR: 5 routine, 5 escalation; Infrastructure: 5 routine, 5 escalation; Procurement/Vendor/RFP: 5 routine, 5 escalation; Security/Policy: 5 routine, 5 escalation.
- `Williams_INAI6986_Final80_Hardening_Scenarios(1).xlsx` / `Final80_Classifier`: 80 rows; Backup/DR: 10 routine, 10 escalation; Infrastructure: 10 routine, 10 escalation; Procurement/Vendor/RFP: 10 routine, 10 escalation; Security/Policy: 10 routine, 10 escalation.

The final hardening workbook contains 51 Borderline and 29 Moderate cases; its signal_type field records 62 Mixed, 16 Routine cues, 1 Escalation cues and 1 Conflicting. These are author-assigned metadata, not independently validated difficulty ratings. They were excluded from model features.

## Consolidation and evaluation
The final 200 cases contain 50 per domain and 100 per label; the split is 120 training, 40 validation and 40 test. Only the 40 test labels received independent review (38/40 initial agreement). The author adjudicated the two disputed backup cases. A blank review log or draft batch is not evidence that a planned review gate was completed. No batch-level model evaluation or measured incremental benefit from each batch is established.

| Evaluation | Result / lesson |
|---|---|
| Original keyword baseline | Validation recall 10%; original test recall 55%; test-informed rule exposure limits comparison. |
| Logistic Regression / Linear SVM | Both 85% validation recall. |
| Naive Bayes | 90% validation recall, 100% precision; selected. Small sample limits comparisons. |
| Frozen NB-v1 original test | 85% recall (17/20), below 90% target. |
| Independent 20-case set | 55.56% recall (5/9); generalization concern. |
| Stopword-only diagnostic | 80% validation, 85% original test, 44.44% independent recall. |
| Reviewer-label sensitivity | Original test recall 88.89% (16/18) under reviewer labels; target still missed. |
| Training-derived rule comparator | 50% validation, 70% original test, 11.11% independent recall; retrospective comparator. |
| Integrated safety evaluation | Seven known false negatives routed to review in both conditions (14/14 runs); not an estimate of overall system recall or review workload. |

The frozen NB-v1 model was not retrained or tuned in the supplemental experiments. These results support a supervised research pilot only, not production readiness.

## Historical scope transition
The project author confirmed a Week 9 pivot due to data authorization/availability, concerns about academic originality as reliance on another team's work increased, practical generalist-team value and avoidance of external inference dependencies. The original RAG branch preserves document preparation and pilot artifacts: https://github.com/write2joshuawilliams-cmyk/6986capstone/tree/archive/original-project-scope . The planned reviewer became unavailable; Johnathan Smythe subsequently reviewed the revised project test set. Exact batch dates are not established here.
