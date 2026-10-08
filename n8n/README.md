# n8n Operationalization

This folder will contain the exported n8n workflow after Technical Milestone 3.

Planned flow:

1. Intake review document or scenario.
2. Parse reviewable sections.
3. Retrieve top-k passages from the selected on-premises index.
4. Send retrieved evidence and review text to the approved local LLM.
5. Produce structured findings with source citations.
6. Route Potential Policy Conflict, Missing Requirement, low-confidence, or ambiguous findings to human review.
7. Record audit fields and reviewer override decisions.

No workflow is claimed as complete until an exported `.json` file is added here and tested.
