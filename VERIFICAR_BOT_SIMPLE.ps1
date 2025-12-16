# Script simple para verificar y ejecutar el bot
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "VERIFICACIÓN RÁPIDA Y EJECUCIÓN DEL BOT" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

# Cambiar al directorio del proyecto
$projectDir = "C:\BOT\trading-bot-windows-20251210 on 'Mac'"
if (-not (Test-Path $projectDir)) {
    Write-Host "ERROR: Directorio no encontrado: $projectDir" -ForegroundColor Red
    exit 1
}

Set-Location $projectDir
Write-Host "Directorio: $(Get-Location)" -ForegroundColor Green
Write-Host ""

# Verificaciones rápidas
Write-Host "Verificando archivos..." -ForegroundColor Yellow
$filesOK = $true
if (-not (Test-Path "config.py")) { Write-Host "  ❌ config.py NO existe" -ForegroundColor Red; $filesOK = $false }
if (-not (Test-Path ".env")) { Write-Host "  ❌ .env NO existe" -ForegroundColor Red; $filesOK = $false }
if (-not (Test-Path "live\mt5_trading.py")) { Write-Host "  ❌ live\mt5_trading.py NO existe" -ForegroundColor Red; $filesOK = $false }
if ($filesOK) { Write-Host "  ✓ Archivos principales encontrados" -ForegroundColor Green }
Write-Host ""

Write-Host "Verificando Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  ✓ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  ❌ Python no encontrado" -ForegroundColor Red
    exit 1
}
Write-Host ""

Write-Host "Verificando MT5..." -ForegroundColor Yellow
$mt5Process = Get-Process -Name "terminal64" -ErrorAction SilentlyContinue
if ($mt5Process) {
    Write-Host "  ✓ MetaTrader 5 está abierto" -ForegroundColor Green
} else {
    Write-Host "  ⚠️ MetaTrader 5 NO está abierto" -ForegroundColor Yellow
    Write-Host "     Abre MT5 antes de continuar" -ForegroundColor Gray
    Read-Host "Presiona Enter para continuar de todos modos"
}
Write-Host ""

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "INICIANDO BOT..." -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Presiona Ctrl+C para detener el bot" -ForegroundColor Yellow
Write-Host ""

# Configurar unbuffered output
$env:PYTHONUNBUFFERED = "1"

# Iniciar el bot
python -u live\mt5_trading.py




