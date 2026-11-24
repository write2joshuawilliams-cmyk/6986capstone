Write-Host "Health check:"
Invoke-RestMethod -Method Get -Uri "http://127.0.0.1:8000/health" | ConvertTo-Json -Depth 5

Write-Host "`nRoutine sample:"
$routine = @{
    request_id = "DEMO-ROUTINE-001"
    domain = "Infrastructure"
    scenario_text = "Apply an approved operating system patch during the documented maintenance window using the existing change procedure."
} | ConvertTo-Json

Invoke-RestMethod -Method Post `
    -Uri "http://127.0.0.1:8000/score" `
    -ContentType "application/json" `
    -Body $routine | ConvertTo-Json -Depth 5

Write-Host "`nEscalation sample:"
$escalate = @{
    request_id = "DEMO-ESC-001"
    domain = "Backup/DR"
    scenario_text = "Request to reduce backup retention from 90 days to 14 days to reclaim storage capacity."
} | ConvertTo-Json

Invoke-RestMethod -Method Post `
    -Uri "http://127.0.0.1:8000/score" `
    -ContentType "application/json" `
    -Body $escalate | ConvertTo-Json -Depth 5

Write-Host "`nDuplicate test:"
Invoke-RestMethod -Method Post `
    -Uri "http://127.0.0.1:8000/score" `
    -ContentType "application/json" `
    -Body $escalate | ConvertTo-Json -Depth 5
