# Script PowerShell para iniciar el bot con mensajes visibles inmediatamente
# Este script configura PowerShell para mostrar mensajes en tiempo real

# Configurar encoding UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

# Cambiar al directorio del proyecto
$projectDir = "C:\BOT\trading-bot-windows-20251210 on 'Mac'"
if (-not (Test-Path $projectDir)) {
    Write-Host "ERROR: Directorio no encontrado: $projectDir" -ForegroundColor Red
    Read-Host "Presiona Enter para salir"
    exit 1
}

Set-Location $projectDir

# Configurar variables de entorno para unbuffered output
$env:PYTHONUNBUFFERED = "1"
$env:PYTHONIOENCODING = "utf-8"

# Configurar PowerShell para output inmediato
$PSDefaultParameterValues['Out-Default:OutVariable'] = $null
$PSDefaultParameterValues['*:Encoding'] = 'utf8'

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "INICIANDO BOT DE TRADING - POWERSHELL" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Directorio: $(Get-Location)" -ForegroundColor Green
Write-Host ""
Write-Host "IMPORTANTE: MetaTrader 5 debe estar ABIERTO" -ForegroundColor Yellow
Write-Host ""
Write-Host "Presiona Ctrl+C para detener el bot" -ForegroundColor Yellow
Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

# Forzar que Python no use buffer y ejecutar
# Usar Start-Process con redirección para forzar output inmediato
$process = Start-Process -FilePath "python" -ArgumentList "-u", "live\mt5_trading.py" -NoNewWindow -PassThru -RedirectStandardOutput "bot_output.txt" -RedirectStandardError "bot_error.txt"

# Mostrar output en tiempo real
$job = Start-Job -ScriptBlock {
    param($outputFile)
    Get-Content $outputFile -Wait -Tail 0
} -ArgumentList "bot_output.txt"

# También mostrar errores
$errorJob = Start-Job -ScriptBlock {
    param($errorFile)
    Get-Content $errorFile -Wait -Tail 0
} -ArgumentList "bot_error.txt"

# Esperar y mostrar output
try {
    while (-not $process.HasExited) {
        # Mostrar output del job
        $output = Receive-Job $job
        if ($output) {
            Write-Host $output
        }
        
        # Mostrar errores del job
        $errors = Receive-Job $errorJob
        if ($errors) {
            Write-Host $errors -ForegroundColor Red
        }
        
        Start-Sleep -Milliseconds 100
    }
    
    # Mostrar output final
    $finalOutput = Receive-Job $job
    if ($finalOutput) {
        Write-Host $finalOutput
    }
    
    $finalErrors = Receive-Job $errorJob
    if ($finalErrors) {
        Write-Host $finalErrors -ForegroundColor Red
    }
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
} finally {
    # Limpiar jobs
    Stop-Job $job, $errorJob -ErrorAction SilentlyContinue
    Remove-Job $job, $errorJob -ErrorAction SilentlyContinue
}

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "Bot detenido" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Read-Host "Presiona Enter para salir"




