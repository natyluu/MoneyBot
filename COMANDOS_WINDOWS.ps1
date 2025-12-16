# COMANDOS_WINDOWS.ps1 - Script PowerShell para Windows
# Ejecuta este script en PowerShell después de instalar Python

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  INSTALANDO DEPENDENCIAS PARA MT5" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Verifica Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python encontrado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ ERROR: Python no está instalado" -ForegroundColor Red
    Write-Host "Descarga Python desde: https://www.python.org/downloads/" -ForegroundColor Yellow
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-Host ""
Write-Host "Instalando dependencias..." -ForegroundColor Yellow
pip install MetaTrader5 python-dotenv pandas numpy

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ ERROR al instalar dependencias" -ForegroundColor Red
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  CONFIGURANDO CREDENCIALES" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
python setup_mt5.py

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  PROBANDO CONEXIÓN" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "⚠️ IMPORTANTE: Abre MetaTrader 5 y conéctate a tu cuenta antes de continuar" -ForegroundColor Yellow
Read-Host "Presiona Enter cuando MT5 esté abierto y conectado"

python test_mt5_connection.py

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  LISTO PARA EJECUTAR EL BOT" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Para ejecutar el bot, usa:" -ForegroundColor Green
Write-Host "  python live\mt5_trading.py" -ForegroundColor White
Write-Host ""
Read-Host "Presiona Enter para salir"










