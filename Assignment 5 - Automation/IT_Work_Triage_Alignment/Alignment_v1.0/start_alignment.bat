@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
 echo Run install_alignment.bat first.
 pause
 exit /b 1
)
.venv\Scripts\python.exe -m uvicorn alignment_api:app --host 127.0.0.1 --port 8001
pause
