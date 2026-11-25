# Assignment 5 — Automation and Decision Support Integration

Final prototype configuration, November 25, 2026. Academic demonstration using synthetic data only.

## Component map

| Component | Version / port | Source |
|---|---|---|
| Classification | NB-v1 / 8000 | [API](IT_Work_Triage_Alignment_v1/API/) |
| Document alignment | 1.1.0 / 8001 | [Alignment](IT_Work_Triage_Alignment_v1/Alignment_v1.1/) |
| Priority | 1.0.0 / 8002 | [Priority](IT_Work_Triage_Alignment_v1/Priority_v1.0/) |
| Audit and human review | 1.0.0 / 8003 | [Audit](Audit_v1.0/) |
| Dashboard | 1.2.0 / 8004 | [Dashboard](Dashboard_v1.1/) |
| n8n | 2.49.5 / 5678 | [Tested v3.1 export](IT_Work_Triage_v3/IT%20Work%20Triage%20v3.1%20-%20Version%20Guarded%20TESTED.json) |
| Startup launcher | 1.2 | [Start_All_Services_v1_2.bat](Start_All_Services_v1_2.bat) |

The Dashboard_v1.1 directory intentionally retains its existing name for launcher compatibility; its installed source is v1.2.0.

## Windows setup and reproduction

1. Clone/download the repository. Install Python 3.13 (Windows py launcher), Node.js with system CA support and n8n 2.49.5. Ensure n8n is on PATH. Dependency installation may require network access; runtime assessment stays local.
2. Run the installation batch files in the four service directories: [install_api.bat](IT_Work_Triage_Alignment_v1/API/install_api.bat), [install_alignment.bat](IT_Work_Triage_Alignment_v1/Alignment_v1.1/install_alignment.bat), [install_priority.bat](IT_Work_Triage_Alignment_v1/Priority_v1.0/install_priority.bat), [install_audit.bat](Audit_v1.0/install_audit.bat). Each creates a local virtual environment and installs its requirements. The dashboard uses Python's standard library.
3. Run Start_All_Services_v1_2.bat from this directory. It uses the actual nested service paths, starts separate command windows, skips occupied ports and reports listeners. It does not install dependencies or publish workflows. Verify that the correct services, not merely arbitrary listeners, occupy the ports.
4. Open `http://127.0.0.1:5678/`, import the tested v3.1 JSON above and publish it locally. The production webhook is POST `http://127.0.0.1:5678/webhook/it-work-triage-v31`. Do not use a browser GET to test that endpoint. For manual n8n test execution use the test webhook only when listening.
5. Manually type `http://127.0.0.1:8004/` in the browser. Confirm NB-v1, alignment 1.1.0, priority 1.0.0 and audit 1.0.0 show Ready. Run a synthetic routine example to verify the published webhook and audit persistence. Keep command windows open; stop them with Ctrl+C when finished.

The frozen model is included with the API; its expected SHA-256 is `e7e440cacfc5926e4eab482bc9baad188eebedf2dbab22b21b3d49fcffac4239`. Do not retrain on the held-out set.

## Decision flow

Validated intake registers an audit attempt. The workflow checks component health/versions, calls the frozen classifier, retrieves local document evidence, assigns a deterministic priority, combines results, and commits the advisory assessment before returning it. Identical request IDs/payloads return existing records; conflicting payloads are blocked. Review-required cases are held for human decisions with justification. Failed assessments can be explicitly retried after restoring services. The original assessment and subsequent review are kept separately. Production authorization remains false.

The dashboard displays history, evidence citations and passages, priority explanations, review controls, audit events and a P1–P4 ranked list. Unassessed/undetermined items remain visible. Reviewed and regression-test records are included; the list is not a task completion or approval queue.

## Evidence and testing

- [API demonstrations](Evidence/API%20Evidence/)
- [Alignment v1.0 development evidence](Evidence/Alignment_v1.0%20Evidence/) and [v1.1 regression evidence](Evidence/Alignment_v1.1%20Evidence/)
- [Priority regression evidence](Evidence/Priority_v1.0%20Evidence/)
- [Audit regression evidence](Evidence/Audit_v1.0%20Evidence/)
- [Combined workflow v2 evidence](IT_Work_Triage_v2/Evidence/)
- [Audited workflow v3 evidence](Evidence/Triage_v3/)
- [Version-guarded v3.1 evidence](Evidence/Triage_Guarded_v3_1_Evidence/)
- [Dashboard v1.0 evidence](Evidence/Dashboard_v1_0_Testing_Evidence/)
- [Final startup, duplicate notification and priority-list evidence](Evidence/Final_Prototype_Testing_Evidence/)

Alignment regression: 9/9; priority regression: 11/11; audit regression: 9/9 groups. The three planned version-guard scenarios passed (correct versions, outdated alignment blocked, recovery). Other component mismatches were not individually exercised. Dashboard v1.0: 14 planned checks passed; final priority list: 11 planned checks passed in demonstrations. These checks are not independent accuracy studies. Earlier versions and screenshots demonstrate development history, not the final configuration.

## Superseded files and limitations

Use only Start_All_Services_v1_2.bat for current startup. Earlier launchers remain for history, including the copy inside Dashboard_v1.1; they may contain obsolete paths. Alignment v1.0, workflow v1/v2/v3 and the original dashboard are historical. No automatic production work, authentication/RBAC, tamper-resistant logging or independent alignment accuracy validation is claimed. Health checks are not cryptographic verification of all services. Abruptly interrupted processing can require manual recovery. Never expose these services to a network or publish runtime databases, credentials, private documents or personal information.
