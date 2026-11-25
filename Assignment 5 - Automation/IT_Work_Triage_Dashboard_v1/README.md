# IT Work Triage — Decision Support Dashboard v1.0
Assignment 5 / INAI 6986. Local academic prototype; synthetic data only.

## Start
1. Start classification 8000, alignment v1.1 8001, priority 8002, audit 8003, and n8n 5678 (loopback only).
2. In n8n open the tested v3.1 workflow and Publish/activate it. Confirm production POST path `/webhook/it-work-triage-v31`. No manual Execute is needed for production URL. Preserve prior workflow exports.
3. Extract this package to `Assignment 5 - Automation/Dashboard_v1.0`. Run `start_dashboard.bat`. No pip installation needed (Python 3.13 standard library only).
4. Open http://localhost:8004. Check four service indicators. Submit Routine example, inspect details and audit events. Submit Vendor example and record a simulated reviewer decision. Refresh history. For failed records use the explicit retry button after restoring the failed service; it sends the original work item unchanged. Do not retry processing or reviewed records.

## Architecture
Browser talks only to a loopback Python HTTP server; fixed local proxy routes send intake to n8n production webhook and read records/events or send review decisions to the audit API. No external services or dependencies. The dashboard does not replace the workflow or duplicate its rules. Service cards check health and versions; n8n registration is verified only by submitting a request. The stored record is authoritative, including the separate original assessment and reviewer decision. Confidence is uncalibrated. No production authorization. Reviewer identities are self-reported; no authentication, RBAC, TLS or tamper-resistant logs. Keep all services loopback-only and never expose to a network. No real work items or private data. Do not publish runtime databases. A timeout may leave a processing record; inspect history before retrying. Interrupted processing recovery remains a limitation.

## Acceptance tests on Windows
- Existing FINAL-001 / FINAL-002 records visible; review history survives restart.
- New routine example: P3, aligned, routine advisory, three citations.
- New vendor example: P2, potential conflict, pending review; accept escalation with justification; verify event and no production authorization.
- Reuse identical ID/payload: duplicate returned; no repeated assessment. Changed payload: blocked.
- Stop alignment, submit new synthetic item: failed audit state; restore alignment v1.1 and explicitly retry; verify attempt 2 and history.
- Stop audit: assessment blocked; no success claimed. Restore afterward.
- Test filter, evidence, override/reject controls using new pending-review cases.

Development checks are not live n8n/browser validation. Use screenshots and sanitized records for evidence.
