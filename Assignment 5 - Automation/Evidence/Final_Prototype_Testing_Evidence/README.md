# Final prototype testing evidence

INAI 6986 — Assignment 5: Automation and Decision Support Integration

Date: November 25, 2026 (local date). This package supplements the earlier dashboard v1.0 and workflow evidence; it does not duplicate them. All screenshots use synthetic demonstration work items.

## Evidence index

| Screenshot | What it demonstrates |
|---|---|
| Dashboard_v1.1.1_Duplicate_Notification_Passed | Explicit duplicate message displayed after resubmission. |
| Final_Startup_Service_Readiness | Dashboard reachable; four backend health/version indicators ready. |
| Final_Startup_Assessment_Audit_History | New assessment recorded after reported restart; aligned strategic evidence and events 64–65. |
| Dashboard_v1.2_Priority_List_Initial_20_Items | Ranked list, counts (P1=1, P2=6, P3=13, P4=0), review status and attempt fields. |
| Dashboard_v1.2_P4_Low_Priority_Assessment | P4 recommendation with unmapped evidence, pending review, production authorization false. |
| Dashboard_v1.2_Priority_Filter_P4_Passed | New item visible; 21 stored records; P4 filter returns one provisional item awaiting review. |
| Dashboard_v1.2_Work_Item_Navigation_Passed | Selecting P1 record displays matching historical assessment. |

## Troubleshooting

The Troubleshooting directory retains the missing-notification observations (events 61 and 62), preserved original record and HTTP 409 blocked response. The 409 alone does not establish the precise cause. A later screenshot confirms visible duplicate feedback.

Two startup troubleshooting screenshots contain local account/path information and desktop details. They are intentionally excluded from the public-ready ZIP and provided separately for private retention.

## Limitations

The startup evidence verifies service readiness and a new recorded assessment after the user reported successful startup; it does not show all six launcher port checks or independently prove a clean shutdown. The priority list screenshots demonstrate a visible ranked list and selected filters, not exhaustive ordering or pagination validation. Stored records include synthetic regression fixtures and reviewed items, and are not an operational task completion queue. Priority and reviewer decisions do not authorize production work. Reviewer identities are self-reported; model scores are uncalibrated; document alignment uses synthetic material. No runtime database is included.
