@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
 echo Run install_priority.bat first.
 pause
 exit /b 1
)
.venv\Scripts\python.exe test_priority.py > priority_regression_results.txt 2>&1
set RESULT=%ERRORLEVEL%
type priority_regression_results.txt
pause
exit /b %RESULT%
