# Upload Instructions

Upload the contents of this package into the root of:

https://github.com/write2joshuawilliams-cmyk/6986capstone

## Important

1. Replace the current `README.md` with the included on-premises version.
2. Replace the current `.gitignore` with the included version.
3. Upload the folders `configs`, `scripts`, `evaluation`, `artifacts`, and `n8n`.
4. Do not upload raw source documents.
5. After upload, verify the repository homepage shows the folders and that each file opens.
6. Run at least the parsing/baseline scripts in the approved environment before claiming them as executed.
7. The `gold_set_pilot_25.csv` rows are marked Draft. Change a row to Frozen only after the label/source have been reviewed and the freeze timestamp has been recorded.

## What this fixes from instructor feedback

- visible working repository structure
- README with on-premises architecture
- extraction/parsing code
- chunking code and configs
- keyword baseline code
- on-premises vector retrieval code
- corpus-profile evidence
- pilot gold-set artifact
- explicit raw-data exclusion
- no Azure OpenAI dependency
