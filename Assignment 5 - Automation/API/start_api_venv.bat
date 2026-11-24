@echo off
cd /d "%~dp0"

echo Starting IT Work Triage Model API...

.venv\Scripts\python.exe -m uvicorn app:app --host 127.0.0.1 --port 8000

pause