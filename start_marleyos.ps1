$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Write-Host "=== Inicializando MarleyOS Engine ==="

Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match 'module_2_mcp[\\/]telemetry_feeder\.py' } | ForEach-Object {
    Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue
}

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    $python = Get-Command py -ErrorAction SilentlyContinue
}
if (-not $python) {
    throw "Python não encontrado. Instale Python 3 ou adicione-o ao PATH."
}

Write-Host "[1/3] Executando testes unitários..."
& $python.Source test_pipeline.py
if ($LASTEXITCODE -ne 0) {
    throw "A suíte de testes falhou. O dashboard não será iniciado."
}

Write-Host "[2/3] Subindo Cockpit Web na porta 8080..."
$server = Start-Process -FilePath $python.Source `
    -ArgumentList "dashboard/server.py" `
    -WorkingDirectory $PSScriptRoot `
    -PassThru

$ready = $false
foreach ($attempt in 1..20) {
    try {
        $response = Invoke-WebRequest -Uri "http://127.0.0.1:8080" -UseBasicParsing -TimeoutSec 1
        if ($response.StatusCode -eq 200) {
            $ready = $true
            break
        }
    } catch {
        Start-Sleep -Milliseconds 250
    }

    if ($server.HasExited) {
        throw "O servidor encerrou antes de ficar disponível."
    }
}

if (-not $ready) {
    Stop-Process -Id $server.Id -Force -ErrorAction SilentlyContinue
    throw "O dashboard não respondeu em http://localhost:8080."
}

$feeder = Start-Process -FilePath $python.Source `
    -ArgumentList "module_2_mcp/telemetry_feeder.py" `
    -WorkingDirectory $PSScriptRoot `
    -WindowStyle Hidden `
    -PassThru
Start-Sleep -Milliseconds 250
$feeder.Refresh()
if ($feeder.HasExited) {
    throw "O Telemetry Feeder encerrou inesperadamente."
}

Write-Host "[3/3] MarleyOS ativo!"
Write-Host "Acesse o Cockpit no navegador: http://localhost:8080"
Write-Host "Telemetry Feeder ativo (PID: $($feeder.Id))"