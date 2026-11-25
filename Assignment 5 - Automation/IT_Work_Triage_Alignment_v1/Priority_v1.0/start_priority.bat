@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
 echo Run install_priority.bat first.
 pause
 exit /b 1
)
.venv\Scripts\python.exe -m uvicorn priority_api:app --host 127.0.0.1 --port 8002
pause
