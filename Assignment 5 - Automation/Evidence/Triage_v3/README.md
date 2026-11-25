# Assignment 5 — Audited Workflow v3 Testing Evidence

Contains 28 original screenshots from the standalone audit regression test through the integrated reviewer override. The screenshots were renamed and WebP images converted to PNG without resizing or editing. Earlier alignment, priority and v2 workflow evidence is not duplicated.

All work items and reviewer roles shown are synthetic demonstration examples. Screenshots establish the visible behavior, not independent security certification. Reviewer identity is not authenticated; automatic component version enforcement and final system regression testing remain outstanding. Review screenshots before public release. No runtime database is included.

## Evidence index

| File | Evidence |
|---|---|
| Audit_v1.0_Regression_Test_Results.png | Standalone audit and review: 9/9 regression groups passed. |
| FINAL-001_Routine_Audited_Assessment.png | Routine routing and audit commit verification nodes executed. |
| FINAL-001_Persistent_Audit_Record.png | Stored routine assessment: aligned, P3, no production authorization. |
| FINAL-002_Human_Review_Audited_Assessment.png | Human review branch executed. |
| FINAL-002_Pending_Human_Review_Record.png | Stored pending review: escalation, potential conflict, P2. |
| FINAL-002_Reviewer_API_Input_Schema.png | Reviewer endpoint input schema; setup evidence. |
| FINAL-002_Reviewer_Acceptance.png | Acceptance submission returned HTTP 200. |
| FINAL-002_Human_Review_Audit_Trail.png | Acceptance event, justification and timestamp recorded. |
| FINAL-002_Duplicate_After_Human_Review.png | Existing audit record branch bypassed assessment engines. |
| FINAL-001_Post_Restart_Routine_Record.png | Routine record retrieved after reported audit service restart. |
| FINAL-002_Post_Restart_Reviewed_Record.png | Reviewed record preserved after reported restart. |
| FINAL-002_Post_Restart_Audit_History.png | Review and duplicate suppression events preserved. |
| FINAL-003_Alignment_Failure_Audited.png | Alignment failure routed to audit persistence. |
| FINAL-003_Failed_Assessment_Record.png | Failed state, attempt 1, recorded HTTP 503 and no authorization. |
| FINAL-003_Controlled_Retry.png | Retry executed; unexpectedly routed to human review. |
| FINAL-003_Retry_Pending_Review_Record.png | Attempt 2 completed; unexpected weak evidence matches indicated version mismatch. |
| Troubleshooting/Alignment_v1.0_Unexpected_Health_Response.png | Health response lacked the version field; consistent with older engine. |
| Alignment_v1.1_Version_Verification.png | Health response confirmed engine version 1.1.0. |
| FINAL-004_Corrected_Routine_Workflow.png | Routine routing after restoring correct alignment version. |
| FINAL-004_Corrected_Audit_Record.png | Aligned, three evidence sections, P3, routine advisory. |
| FINAL-005_Audit_Service_Failure.png | Audit registration error bypassed all assessment engines; response payload not shown. |
| FINAL-003_Controlled_Retry_Audit_History.png | Original failure and retry events preserved. |
| FINAL-003_Reviewer_Rejection.png | Rejection submission HTTP 200; reviewed state. |
| FINAL-003_Reviewer_Rejection_Audit_Trail.png | Rejection event and justification recorded. |
| FINAL-006_Override_Test_Workflow.png | Human review branch executed. |
| FINAL-006_Pending_Override_Record.png | Pending review with generalist classification, Requires Review alignment and P3. |
| FINAL-006_Reviewer_Override.png | Override submission HTTP 200; reviewed state. |
| FINAL-006_Reviewer_Override_Audit_Trail.png | Override to generalist handling recorded with justification; original assessment preserved and production authorization false. |
