@echo off
cd /d "%~dp0"
echo Starting INAI 6986 Model API...
echo.
python -m uvicorn app:app --host 127.0.0.1 --port 8000
pause
