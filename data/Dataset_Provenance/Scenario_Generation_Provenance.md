# Scenario generation provenance

Retrospective record prepared November 25, 2026 for INAI 6986. This is not an original prompt transcript or a pre-training protocol.

## Authorship and evidence
The project author used OpenAI ChatGPT to assist with synthetic scenario generation and drafting the dataset specification and labeling guide. The author is responsible for the final dataset and labels. The original 200 cases are synthetic, not a sample of agency tickets. Only the 40 held-out cases received independent label review; the author adjudicated the two disagreements (BDR-006 and BDR-017). A separate 20-case supplemental set was independently authored by Johnathan Smythe, without AI assistance or consultation of existing project materials, according to the project author's account. The independent set is not part of the original 200.

## Reconstructed generation brief (not verbatim historical prompts)
Based on the preserved specification, labeling guide and workbook notes, the following describes the documented generation requirements. Exact prompt wording, complete conversation sequence, AI model version, sampling settings and generation timestamps were not recovered. The brief cannot recreate the same dataset and must not be represented as an original prompt.

- Generate realistic synthetic IT work items for a small generalist team across Infrastructure, Security/Policy, Backup/DR and Procurement/Vendor/RFP.
- Use information plausibly available at intake; omit explicit label-revealing statements and sensitive identifiers. Vary vocabulary, sentence length and context.
- Assign label 0 when work is within established procedure and authority; label 1 when specialist, vendor, security, architecture, procurement or management review is required. Use Hold when context is insufficient rather than guessing.
- Record a short rationale, stable ID, domain, source and review metadata. Keep priority, capacity, strategic alignment, rationale and reviewer information outside classifier features.
- Start with 40 balanced cases; expand coverage in two 40-case batches; then add 80 hardening cases containing mixed cues and borderline decisions. Maintain class and domain balance. Review duplicates, wording and labels before freezing test data.

## Contemporaneous workbook evidence

### Williams_INAI6986_40_Scenario_Pilot_Dataset(1).xlsx — Summary / Labeling_Rules

The workbook records 40 draft scenarios, 10 per domain, five of each label per domain, with priority data separated. Independent review is required; the review log is blank.

### Williams_INAI6986_Batch2_40_Scenarios(1).xlsx — Design_Notes

- **Purpose:** Batch 2 fills weak coverage areas from the scenario coverage matrix rather than simply paraphrasing the pilot.
- **Balance:** 40 scenarios: 10 per domain, 5 routine and 5 escalation in each domain.
- **Review status:** All labels are Draft until independently reviewed.
- **Leakage control:** label_rationale, priority-guide fields, reviewer information, and strategic-alignment annotations are not classifier inputs.
- **Priority guide:** Priority fields remain blank for human scoring and are stored separately from classifier fields.
- **Next decision:** After Batch 2 review, assess reviewer agreement, duplicate/near-duplicate risk, wording diversity, and remaining coverage gaps before generating Batch 3.
- **200 target:** 200 remains a planning target, not a locked requirement.

### Williams_INAI6986_Batch3_40_Scenarios(1).xlsx — Design_Notes

- **Purpose:** Batch 3 broadens scenario coverage after the first 80 rows, with added emphasis on lifecycle, resilience, audit/logging, retention, security requirements, contract scope, and support commitments.
- **Balance:** 40 scenarios: 10 per domain, 5 routine and 5 escalation in each domain.
- **Review status:** All labels are Draft until independently reviewed.
- **Leakage control:** label_rationale, priority-guide fields, reviewer information, and strategic-alignment annotations are not classifier inputs.
- **Priority guide:** Priority fields remain blank for human scoring and are stored separately from classifier fields.
- **Next decision:** After Batch 3, the working dataset reaches 120 rows. Review diversity and agreement before deciding whether the final 80 scenarios should preserve exact balance or target remaining subtopic gaps more heavily.
- **200 target:** 200 remains a planning target, not a locked requirement.

### Williams_INAI6986_Final80_Hardening_Scenarios(1).xlsx — Design_Notes

- **Purpose:** These final 80 rows are designed as hardening scenarios rather than another easy balanced batch.
- **Difficulty:** Many rows are marked Borderline because they contain both routine and risk cues. Borderline means near the decision boundary, not intentionally unresolvable.
- **Signal design:** Mixed-signal cases deliberately use words such as vendor, production, firewall, backup, or MFA in both classes so the model cannot rely on a single keyword.
- **Balance:** 80 scenarios: 20 per domain, 10 routine and 10 escalation in each domain.
- **Project total:** Combined with Pilot, Batch 2, and Batch 3, the working target reaches 200 rows: 50 per domain and 25/25 labels in each domain.
- **Review requirement:** Do not treat 200 as final until scenario wording, duplicates, labels, and independent-review disagreements are checked.
- **Leakage control:** Difficulty, signal_type, rationale, reviewer fields, and priority-guide values are metadata only and must not be classifier inputs.
- **Next step:** Merge all four dataset workbooks into one master dataset, run duplicate/near-duplicate review, then conduct independent label review before freezing any held-out test set.

## Limitations and deviations
The written controls did not eliminate style shortcuts. Stopword-only Naive Bayes matched the frozen model's original test recall (85%); independently authored cases yielded only 55.56% recall for the frozen model. These findings indicate substantial generalization risk, not proof of one exclusive cause. The original keyword baseline was finalized with test text visible. A blind-review workbook exists with no author labels or rationales, but actual reviewer blinding has not been confirmed. The review date is disputed between the author's recollection (October 23) and the committed record (November 23); retain both until reconciled. No historical prompts are fabricated. The retrospective record changes neither data nor model.

## AI disclosure
ChatGPT assisted with the original design and synthetic scenario generation and with drafting this retrospective record. The author must verify the account against original materials. No private operational data is needed for this record.
