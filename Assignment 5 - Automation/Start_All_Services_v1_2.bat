@echo off
setlocal EnableExtensions
cd /d "%~dp0"
set "ROOT=%~dp0"
set "NODE_OPTIONS=--use-system-ca"
set "N8N_LISTEN_ADDRESS=127.0.0.1"
set "N8N_DIAGNOSTICS_ENABLED=false"
set "N8N_VERSION_NOTIFICATIONS_ENABLED=false"
set "N8N_TEMPLATES_ENABLED=false"
echo === IT Work Triage startup v1.2 ===
call :launch 8000 "IT_Work_Triage_Alignment_v1\API" start_api_venv.bat
call :launch 8001 "IT_Work_Triage_Alignment_v1\Alignment_v1.1" start_alignment.bat
call :launch 8002 "IT_Work_Triage_Alignment_v1\Priority_v1.0" start_priority.bat
call :launch 8003 "Audit_v1.0" start_audit.bat
call :listening 5678
if not errorlevel 1 (
  echo [5678] Already listening - skipped.
) else (
  where n8n >nul 2>&1
  if errorlevel 1 (
    echo [5678] ERROR: n8n not found on PATH.
  ) else (
    echo [5678] Launching n8n...
    start "IT Work Triage n8n 5678" cmd /k n8n start
  )
)
call :launch 8004 "Dashboard_v1.1" start_dashboard.bat
echo Waiting up to 60 seconds for listeners...
powershell -NoProfile -Command "$ports=@(8000,8001,8002,8003,5678,8004); $end=(Get-Date).AddSeconds(60); do { $live=@(Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue | Select-Object -ExpandProperty LocalPort); $missing=@($ports | Where-Object { $_ -notin $live }); if($missing.Count -eq 0){break}; Start-Sleep -Seconds 2 } while((Get-Date) -lt $end); foreach($p in $ports){if($p -in $live){Write-Host ('[{0}] LISTENING' -f $p) -ForegroundColor Green}else{Write-Host ('[{0}] NOT LISTENING - check service window' -f $p) -ForegroundColor Red}}"
echo Verify service versions in the dashboard and confirm v3.1 is published in n8n.
echo Manually open http://127.0.0.1:8004/
pause
exit /b

:launch
call :listening %~1
if not errorlevel 1 (
  echo [%~1] Already listening - skipped.
  exit /b 0
)
if not exist "%ROOT%%~2\%~3" (
  echo [%~1] ERROR: Missing "%ROOT%%~2\%~3"
  exit /b 1
)
echo [%~1] Launching %~2\%~3...
start "IT Work Triage %~1" /D "%ROOT%%~2" cmd /k call %~3
exit /b 0

:listening
powershell -NoProfile -Command "if(Get-NetTCPConnection -LocalPort %~1 -State Listen -ErrorAction SilentlyContinue){exit 0}else{exit 1}"
exit /b %errorlevel%
