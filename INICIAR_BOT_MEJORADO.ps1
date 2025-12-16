# Script mejorado de PowerShell para iniciar el bot con diagnóstico

# Configurar encoding UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "INICIANDO BOT DE TRADING - VERSION MEJORADA" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

# Cambiar al directorio del proyecto
$projectDir = "C:\BOT\trading-bot-windows-20251210 on 'Mac'"
if (-not (Test-Path $projectDir)) {
    Write-Host "ERROR: No se encontró el directorio del proyecto" -ForegroundColor Red
    Write-Host "Ruta esperada: $projectDir" -ForegroundColor Red
    Read-Host "Presiona Enter para salir"
    exit 1
}

Set-Location $projectDir
Write-Host "Directorio actual: $(Get-Location)" -ForegroundColor Green
Write-Host ""

# Verificar Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python encontrado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python no está instalado o no está en el PATH" -ForegroundColor Red
    Write-Host "Instala Python 3.12 desde python.org" -ForegroundColor Yellow
    Read-Host "Presiona Enter para salir"
    exit 1
}
Write-Host ""

# Verificar archivo
if (-not (Test-Path "live\mt5_trading.py")) {
    Write-Host "ERROR: No se encontró live\mt5_trading.py" -ForegroundColor Red
    Write-Host "Verifica que estás en el directorio correcto" -ForegroundColor Yellow
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-Host "Archivo encontrado: live\mt5_trading.py" -ForegroundColor Green
Write-Host ""

# Verificar MT5 (opcional)
$mt5Process = Get-Process -Name "terminal64" -ErrorAction SilentlyContinue
if (-not $mt5Process) {
    Write-Host "ADVERTENCIA: MetaTrader 5 no parece estar abierto" -ForegroundColor Yellow
    Write-Host "Asegúrate de abrir MT5 antes de iniciar el bot" -ForegroundColor Yellow
    Write-Host ""
    Start-Sleep -Seconds 3
}

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "INICIANDO BOT..." -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Presiona Ctrl+C para detener el bot" -ForegroundColor Yellow
Write-Host ""

# Configurar variable de entorno para unbuffered output
$env:PYTHONUNBUFFERED = "1"

# Iniciar el bot
try {
    python -u live\mt5_trading.py
} catch {
    Write-Host ""
    Write-Host "ERROR al ejecutar el bot: $_" -ForegroundColor Red
} finally {
    Write-Host ""
    Write-Host "======================================================================" -ForegroundColor Cyan
    Write-Host "Bot detenido" -ForegroundColor Cyan
    Write-Host "======================================================================" -ForegroundColor Cyan
    Read-Host "Presiona Enter para salir"
}




