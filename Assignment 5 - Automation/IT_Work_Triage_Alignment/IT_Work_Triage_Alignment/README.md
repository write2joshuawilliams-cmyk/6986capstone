# IT Work Triage — Local Policy, SOP and Strategic Alignment

Academic prototype. All nine source documents are fictional and are not agency policies. The original classifier and its frozen test set are not changed or used by this service.

## Windows setup
1. Extract the ZIP. Double-click `install_alignment.bat` (requires Python 3.13).
2. Double-click `start_alignment.bat`. Keep the window open.
3. Visit http://127.0.0.1:8001/health and http://127.0.0.1:8001/docs.

## Interface
POST `/align` with JSON `request_id`, `scenario_text`, and optional `domain`. The response groups retrieved sections into policy, SOP and strategy, including exact source passages, citations and rule-based status. TF-IDF ranks sections matched by relevance expressions; neither the score nor status is a probability or a legal compliance determination. `Aligned` means explicit textual indicators only; `Potential Conflict` means a predefined risk cue was matched; `Requires Review` means applicable guidance lacks sufficient affirmative evidence; `Unmapped` means no rule identified relevant guidance. Status precedence: Potential Conflict > Requires Review > Aligned > Unmapped. Human approval remains required under normal controls. Domain is returned for context and does not filter the corpus.

No sensitive data. No persistent storage of requests in this standalone service. Keep localhost only. The sample tests are synthetic examples, not frozen classifier test cases. The service is not yet integrated with n8n. Update documents and rules under version control; revalidate before use. The `build_corpus.py` script recreates the initial synthetic corpus. The accompanying test script exercises the interface using FastAPI TestClient (requires optional `httpx` for developer testing).
