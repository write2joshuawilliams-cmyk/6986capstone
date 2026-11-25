@echo off
cd /d "%~dp0"
py -3.13 -m venv .venv
if errorlevel 1 goto failed
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 goto failed
echo Installation complete.
pause
exit /b 0
:failed
echo Installation failed.
pause
exit /b 1
