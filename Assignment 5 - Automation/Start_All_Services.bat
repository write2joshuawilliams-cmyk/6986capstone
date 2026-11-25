@echo off
setlocal
cd /d "%~dp0"
set "ROOT=%~dp0"
where n8n >nul 2>&1 || (echo n8n not found on PATH & pause & exit /b 1)
if not exist "%ROOT%API\start_api_venv.bat" (echo Missing API\start_api_venv.bat & pause & exit /b 1)
if not exist "%ROOT%Alignment_v1.1\start_alignment.bat" (echo Missing Alignment_v1.1\start_alignment.bat & pause & exit /b 1)
if not exist "%ROOT%Priority_v1.0\start_priority.bat" (echo Missing Priority_v1.0\start_priority.bat & pause & exit /b 1)
if not exist "%ROOT%Audit_v1.0\start_audit.bat" (echo Missing Audit_v1.0\start_audit.bat & pause & exit /b 1)
if not exist "%ROOT%Dashboard_v1.1\start_dashboard.bat" (echo Missing Dashboard_v1.1\start_dashboard.bat & pause & exit /b 1)
powershell -NoProfile -Command "$p=@(8000,8001,8002,8003,8004,5678); if(Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue | Where-Object { $_.LocalPort -in $p }) { exit 1 }"
if errorlevel 1 (echo A required port is already listening or port check failed. Stop existing services and retry. & pause & exit /b 1)
set "NODE_OPTIONS=--use-system-ca"
set "N8N_LISTEN_ADDRESS=127.0.0.1"
set "N8N_DIAGNOSTICS_ENABLED=false"
set "N8N_VERSION_NOTIFICATIONS_ENABLED=false"
set "N8N_TEMPLATES_ENABLED=false"
start "IT Work Triage 8000" /D "%ROOT%API" cmd /k call start_api_venv.bat
start "IT Work Triage 8001" /D "%ROOT%Alignment_v1.1" cmd /k call start_alignment.bat
start "IT Work Triage 8002" /D "%ROOT%Priority_v1.0" cmd /k call start_priority.bat
start "IT Work Triage 8003" /D "%ROOT%Audit_v1.0" cmd /k call start_audit.bat
start "IT Work Triage 8004" /D "%ROOT%Dashboard_v1.1" cmd /k call start_dashboard.bat
start "IT Work Triage n8n 5678" cmd /k n8n start
echo Startup commands launched. Check each window and health endpoint.
echo Confirm v3.1 is published in n8n.
echo Manually open http://127.0.0.1:8004/ after services are ready.
pause
