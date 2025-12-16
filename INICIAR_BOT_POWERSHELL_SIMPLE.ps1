# Script PowerShell simple para iniciar el bot con output inmediato
# Versión simplificada que funciona mejor

# Configurar encoding
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

# Cambiar al directorio
$projectDir = "C:\BOT\trading-bot-windows-20251210 on 'Mac'"
Set-Location $projectDir

# Configurar variables de entorno
$env:PYTHONUNBUFFERED = "1"
$env:PYTHONIOENCODING = "utf-8"

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "INICIANDO BOT DE TRADING" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Presiona Ctrl+C para detener" -ForegroundColor Yellow
Write-Host ""

# Ejecutar Python directamente con redirección a archivo y mostrar en tiempo real
$scriptBlock = {
    param($dir)
    Set-Location $dir
    $env:PYTHONUNBUFFERED = "1"
    python -u live\mt5_trading.py 2>&1 | ForEach-Object {
        Write-Host $_ -NoNewline
        [Console]::Out.Flush()
    }
}

# Ejecutar en el contexto actual
& $scriptBlock $projectDir

Write-Host ""
Write-Host "Bot detenido" -ForegroundColor Cyan
Read-Host "Presiona Enter para salir"




