@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
 echo Run install_alignment.bat first.
 pause
 exit /b 1
)
.venv\Scripts\python.exe test_alignment.py > regression_results.txt 2>&1
set RESULT=%ERRORLEVEL%
type regression_results.txt
pause
exit /b %RESULT%
