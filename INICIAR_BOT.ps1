# Script para iniciar el bot con salida en tiempo real
# Ejecuta: .\INICIAR_BOT.ps1

$env:PYTHONUNBUFFERED = "1"
Set-Location "C:\BOT\trading-bot-windows-20251210 on 'Mac'"
python -u live\mt5_trading.py




