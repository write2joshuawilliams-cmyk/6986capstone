@echo off
cd /d "%~dp0"
.venv\Scripts\python.exe test_audit.py > audit_regression_results.txt 2>&1
set RESULT=%ERRORLEVEL%
type audit_regression_results.txt
pause
exit /b %RESULT%
