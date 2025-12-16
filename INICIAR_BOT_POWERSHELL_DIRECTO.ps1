# Script PowerShell directo - La forma más simple
# Ejecuta el bot y muestra output usando Tee-Object

# Configurar encoding UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

# Cambiar al directorio
cd "C:\BOT\trading-bot-windows-20251210 on 'Mac'"

# Configurar variables de entorno
$env:PYTHONUNBUFFERED = "1"
$env:PYTHONIOENCODING = "utf-8"

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "INICIANDO BOT DE TRADING - POWERSHELL" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "IMPORTANTE: MetaTrader 5 debe estar ABIERTO" -ForegroundColor Yellow
Write-Host "Presiona Ctrl+C para detener el bot" -ForegroundColor Yellow
Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

# Ejecutar Python y mostrar output en tiempo real usando Tee-Object
python -u live\mt5_trading.py 2>&1 | Tee-Object -FilePath "bot_output.txt" | ForEach-Object {
    Write-Host $_
    [Console]::Out.Flush()
}

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "Bot detenido" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Output guardado en: bot_output.txt" -ForegroundColor Gray
Read-Host "Presiona Enter para salir"




