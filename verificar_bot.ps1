# Script de verificación del bot de trading
# Ejecuta este script en PowerShell para verificar que el bot está funcionando

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "VERIFICACIÓN DEL BOT DE TRADING" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 1. Verificar si el proceso de Python está corriendo
Write-Host "1. Verificando procesos de Python..." -ForegroundColor Yellow
$pythonProcesses = Get-Process python* -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -like "*mt5_trading*" -or $_.CommandLine -like "*mt5_trading*" }

if ($pythonProcesses) {
    Write-Host "   ✓ Proceso de Python encontrado" -ForegroundColor Green
    foreach ($proc in $pythonProcesses) {
        Write-Host "      PID: $($proc.Id) | CPU: $($proc.CPU) | Memoria: $([math]::Round($proc.WorkingSet64/1MB, 2)) MB" -ForegroundColor Gray
    }
} else {
    Write-Host "   ⚠ No se encontró proceso de Python ejecutando mt5_trading.py" -ForegroundColor Yellow
    Write-Host "      Esto puede ser normal si el bot se detuvo o está en otra ventana" -ForegroundColor Gray
}

Write-Host ""

# 2. Verificar conexión con MT5
Write-Host "2. Verificando conexión con MetaTrader 5..." -ForegroundColor Yellow
$mt5Process = Get-Process terminal64 -ErrorAction SilentlyContinue

if ($mt5Process) {
    Write-Host "   ✓ MetaTrader 5 está ejecutándose" -ForegroundColor Green
    Write-Host "      PID: $($mt5Process.Id)" -ForegroundColor Gray
} else {
    Write-Host "   ⚠ MetaTrader 5 no está ejecutándose" -ForegroundColor Yellow
    Write-Host "      El bot necesita MT5 abierto para funcionar" -ForegroundColor Gray
}

Write-Host ""

# 3. Verificar archivos del proyecto
Write-Host "3. Verificando archivos del proyecto..." -ForegroundColor Yellow
$projectPath = "C:\BOT\trading-bot-windows-20251210 on 'Mac'"

if (Test-Path $projectPath) {
    Write-Host "   ✓ Directorio del proyecto encontrado" -ForegroundColor Green
    
    $envFile = Join-Path $projectPath ".env"
    $mt5File = Join-Path $projectPath "live\mt5_trading.py"
    
    if (Test-Path $envFile) {
        Write-Host "   ✓ Archivo .env encontrado" -ForegroundColor Green
    } else {
        Write-Host "   ⚠ Archivo .env no encontrado" -ForegroundColor Yellow
    }
    
    if (Test-Path $mt5File) {
        Write-Host "   ✓ Archivo mt5_trading.py encontrado" -ForegroundColor Green
    } else {
        Write-Host "   ⚠ Archivo mt5_trading.py no encontrado" -ForegroundColor Yellow
    }
} else {
    Write-Host "   ⚠ Directorio del proyecto no encontrado: $projectPath" -ForegroundColor Yellow
}

Write-Host ""

# 4. Verificar última actividad (si hay logs)
Write-Host "4. Recomendaciones:" -ForegroundColor Yellow
Write-Host "   • Si el bot está corriendo, deberías ver mensajes cada 30 segundos" -ForegroundColor Gray
Write-Host "   • El bot hace análisis completos cada 5 minutos" -ForegroundColor Gray
Write-Host "   • Verifica la ventana de PowerShell donde ejecutaste el bot" -ForegroundColor Gray
Write-Host "   • Si no ves actividad, el bot puede estar esperando el próximo ciclo" -ForegroundColor Gray

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Para ver el bot en acción:" -ForegroundColor Cyan
Write-Host "  1. Abre la ventana de PowerShell donde ejecutaste el bot" -ForegroundColor White
Write-Host "  2. Deberías ver mensajes cada 30 segundos indicando que está activo" -ForegroundColor White
Write-Host "  3. Cada 5 minutos verás un análisis completo" -ForegroundColor White
Write-Host "========================================" -ForegroundColor Cyan




