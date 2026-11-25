# IT Work Triage — Priority Assessment v1.0

Independent deterministic advisory service, Assignment 5. No new trained model. Proposed synthetic business rules, not an adopted agency SLA or authorization. The reviewer supplies impact, urgency and incident/recovery indicators. Missing inputs default to unknown, never silently to no. Alignment status comes from the alignment service when integrated. Unknown information makes any assigned priority provisional and requires review. A critical outage or active security incident overrides the matrix to P1; critical recovery failure and potential policy conflict impose a P2 minimum (priority of review, not execution). High/high also maps to P1. Review is required for P1/P2, unknowns, or any alignment status other than Aligned. All results are advisory only.

| Impact / urgency | High | Medium | Low |
|---|---|---|---|
| High | P1 | P2 | P2 |
| Medium | P2 | P3 | P3 |
| Low | P2 | P3 | P4 |

Unknown matrix input returns Undetermined unless a safety override supplies a provisional priority. Human review may override the recommendation; actual review workflow is not implemented here.

Windows: run install_priority.bat, then start_priority.bat. Visit http://localhost:8002/health or /docs. Run run_priority_tests.bat while the service runs; it writes priority_regression_results.txt. Keep services bound to loopback. Test only synthetic data. Development results use the available local FastAPI/Pydantic versions, not the pinned Windows environment; repeat tests after installation. Do not upload .venv or __pycache__.
