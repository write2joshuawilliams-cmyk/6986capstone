@echo off
setlocal EnableExtensions
cd /d "%~dp0"
set "ROOT=%~dp0"
set "NODE_OPTIONS=--use-system-ca"
set "N8N_LISTEN_ADDRESS=127.0.0.1"
set "N8N_DIAGNOSTICS_ENABLED=false"
set "N8N_VERSION_NOTIFICATIONS_ENABLED=false"
set "N8N_TEMPLATES_ENABLED=false"
echo === IT Work Triage startup ===
call :launch 8000 API start_api_venv.bat
call :launch 8001 Alignment_v1.1 start_alignment.bat
call :launch 8002 Priority_v1.0 start_priority.bat
call :launch 8003 Audit_v1.0 start_audit.bat
call :launch 5678 . n8n
call :launch 8004 Dashboard_v1.1 start_dashboard.bat
echo Waiting up to 60 seconds for listeners...
powershell -NoProfile -Command "$ports=8000,8001,8002,8003,8004,5678; $end=(Get-Date).AddSeconds(60); do { $live=@(Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue | Select-Object -ExpandProperty LocalPort -Unique); $missing=@($ports | Where-Object { $_ -notin $live }); if($missing.Count -eq 0){break}; Start-Sleep -Seconds 2 } while((Get-Date) -lt $end); foreach($port in $ports){if($port -in $live){Write-Host ($port.ToString()+' LISTENING') -ForegroundColor Green}else{Write-Host ($port.ToString()+' NOT LISTENING') -ForegroundColor Red}}"
echo Listener checks do not verify service identity, health, or version.
echo Confirm dashboard health indicators and published n8n v3.1 workflow.
echo Open http://127.0.0.1:8004/ manually.
pause
exit /b

:launch
powershell -NoProfile -Command "if(Get-NetTCPConnection -LocalPort %1 -State Listen -ErrorAction SilentlyContinue){exit 0}else{exit 1}"
if not errorlevel 1 (
 echo [%1] Already listening - skipped. Verify correct service and version.
 exit /b 0
)
if /i "%3"=="n8n" (
 where n8n >nul 2>&1
 if errorlevel 1 (
  echo [%1] ERROR: n8n not found on PATH.
  exit /b 1
 )
 echo [%1] Launching n8n...
 start "IT Work Triage %1" /D "%ROOT%." "%ComSpec%" /k "n8n start"
 exit /b 0
)
if not exist "%ROOT%%2\%3" (
 echo [%1] ERROR: Missing "%ROOT%%2\%3"
 exit /b 1
)
echo [%1] Launching %2\%3...
start "IT Work Triage %1" /D "%ROOT%%2" "%ComSpec%" /k "call %3"
if errorlevel 1 echo [%1] ERROR: Could not launch command window.
exit /b 0
