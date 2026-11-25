# Assignment 5 — Version-guarded workflow v3.1 testing evidence

Date: November 25, 2026

| Test | Evidence | Observed result |
|---|---|---|
| VERSION-001 | Valid component versions workflow and audit record | Routine advisory; attempt 1; alignment engine 1.1.0; Aligned; P3; production_authorized false. |
| VERSION-002 | Incorrect component version workflow and audit record | Failed; attempt 1; alignment unavailable or version mismatch (expected 1.1.0); recorded HTTP 503; review required; production_authorized false. |
| VERSION-002 retry | Corrected version retry workflow and audit record | Routine advisory; attempt 2; alignment engine 1.1.0; Aligned; P3; production_authorized false. |

All three planned scenarios passed. The mismatch test specifically exercised the outdated alignment service; other component mismatches were not independently tested. The retry event history is not included in these screenshots. Health-based version checks are not cryptographic verification of all services.

The n8n startup certificate-trust error was observed after reboot but is not a version-guard test. Its screenshot was removed from the current public tree because it displayed a local account path; retain private troubleshooting evidence locally. Earlier Git history may still contain the image.
