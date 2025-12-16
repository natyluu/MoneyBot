# Script PowerShell para iniciar el bot con output unbuffered forzado
$env:PYTHONUNBUFFERED = "1"
$env:PYTHONIOENCODING = "utf-8"

cd "C:\BOT\trading-bot-windows-20251210 on 'Mac'"

Write-Host "Iniciando bot con output unbuffered..." -ForegroundColor Cyan
Write-Host ""

# Ejecutar Python con -u y redirigir para forzar flush
python -u live\mt5_trading.py




