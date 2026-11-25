# IT Work Triage — Dashboard v1.2.0

INAI 6986 / Assignment 5. This directory retains the name Dashboard_v1.1 for compatibility with the tested launcher. The HTML identifies the current application as v1.2.0.

## Startup

Follow the [Assignment 5 setup guide](../README.md). Start the four local APIs and n8n; publish the [tested v3.1 workflow](../IT_Work_Triage_v3/IT%20Work%20Triage%20v3.1%20-%20Version%20Guarded%20TESTED.json). Use the [master launcher v1.2](../Start_All_Services_v1_2.bat), or run start_dashboard.bat after other services are ready. Python 3.13 standard library only. Manually type `http://127.0.0.1:8004/`; do not append tracking parameters. The dashboard uses the local production POST webhook, not the test webhook.

## Features

Work-item intake, automatic request IDs, service readiness and version indicators, assessment history, frozen classification and uncalibrated confidence, priority justification, policy/SOP/strategy citations and retrieved passages, human acceptance/rejection/override with justification, explicit retry and audit history. Identical duplicate submissions display a notification and preserve the existing record; changed payloads with the same ID are blocked.

The prioritized list ranks stored records P1 through P4, then unranked, with older assessments first within each group where available. It displays counts, filters, clickable work items, domain, assessment state, review decision, attempt and provisional priority. It includes historical and regression-test records; it is advisory, not an execution queue.

## Demonstrated tests

See [dashboard v1.0 testing](../Evidence/Dashboard_v1_0_Testing_Evidence/) and [final prototype testing](../Evidence/Final_Prototype_Testing_Evidence/). Demonstrations verified routine and high-risk requests, evidence display, human review decisions, duplicates, failure and retry. The final extension demonstrated priority list updates, P4, filtering and navigation. Startup was exercised on Windows with the corrected launcher. The duplicate notice was verified near the submission form; exact automatic scrolling behavior was not independently established.

## Limitations

The local Python server proxies fixed local endpoints. Service health cards do not prove webhook registration. Reviewer names are self-reported; no authentication, RBAC, TLS or tamper-resistant logs. Synthetic documents and rule-based matching are not verified compliance. Unmapped is not approval. A timeout may leave a processing record; inspect history before retrying. No production authorization. Keep all services loopback-only and do not publish runtime data.
