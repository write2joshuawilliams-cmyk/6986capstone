# Reviewer-label sensitivity (CA-06)
Post-test analysis of original saved predictions. No training, inference, relabeling or changes to the original evaluation. Both label interpretations remain visible. The professor's alternative result is reproduced: 16/18 recall, 2 false positives, 90% accuracy; neither reference meets the 90% recall target. Wilson intervals do not account for author or selection bias. The review workbook records November 23, 2026; the actual review date remains disputed and is not corrected here. The reviewer's labels are an alternative reference, not independently adjudicated ground truth.

The included results were calculated from the available original prediction CSV, frozen test CSV and final review workbook, with exact SHA-256 checks and matching IDs, texts, domains and final labels. To reproduce, extract into repository root. Python 3.13 and openpyxl are sufficient. Move the included results folder aside before executing (the script refuses to overwrite). From repository root:

```powershell
& '.\Assignment 5 - Automation\IT_Work_Triage_Alignment_v1\API\.venv\Scripts\python.exe' '.\Supplemental Evaluation\Reviewer_Label_Sensitivity\score_reviewer_sensitivity.py'
```

The script aborts on any input hash mismatch. Investigate differences rather than bypass the check. Original evidence files are not duplicated. AI assistance: ChatGPT prepared and executed this analysis against available source files; student should inspect and reproduce results before submission.
