# Assignment 5 — Combined workflow v2 testing evidence

Date: 2026-11-24

Seven screenshots document the successful execution paths observed in the local n8n workflow. Three additional screenshots under Troubleshooting preserve the initial webhook registration issue and unsuccessful attempts to simulate a model outage. The latter are not counted as passed failure tests.

| Screenshot | Observed path |
|---|---|
| COMBINED-001 | Routine Advisory |
| COMBINED-003 (human review) | Human Review Required |
| COMBINED-003 (duplicate) | Duplicate - No Action |
| COMBINED-004 | Reject Bad Input |
| COMBINED-007 | Model Unavailable |
| COMBINED-008 | Alignment Unavailable |
| COMBINED-009 | Priority Unavailable |

The screenshots support routing verification, not verification of every returned JSON field or HTTP status. Actual reviewer interaction, persistent audit logging, and safe retries after downstream failures remain outstanding. Request IDs reflect the test sequence in the conversation; the screenshots do not independently display those IDs. Images were converted to PNG without resizing or annotation. Review screenshots for public disclosure before publishing.
