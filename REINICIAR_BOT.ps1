# Script para reiniciar el bot de trading desde cero
# Ejecuta este script en PowerShell dentro de Windows (Parallels)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "REINICIAR BOT DE TRADING" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 1. Verificar que estamos en el directorio correcto
$projectPath = "C:\BOT\trading-bot-windows-20251210 on 'Mac'"
if (-not (Test-Path $projectPath)) {
    Write-Host "❌ No se encontró el directorio del proyecto" -ForegroundColor Red
    Write-Host "   Buscando en: $projectPath" -ForegroundColor Yellow
    exit 1
}

Set-Location $projectPath
Write-Host "✓ Directorio del proyecto: $projectPath" -ForegroundColor Green
Write-Host ""

# 2. Detener procesos de Python que puedan estar corriendo
Write-Host "2. Deteniendo procesos anteriores..." -ForegroundColor Yellow
$pythonProcesses = Get-Process python* -ErrorAction SilentlyContinue | Where-Object { 
    $_.Path -like "*python*" -and $_.CommandLine -like "*mt5_trading*"
}

if ($pythonProcesses) {
    foreach ($proc in $pythonProcesses) {
        Write-Host "   Deteniendo proceso PID: $($proc.Id)" -ForegroundColor Gray
        Stop-Process -Id $proc.Id -Force -ErrorAction SilentlyContinue
    }
    Start-Sleep -Seconds 2
    Write-Host "   ✓ Procesos detenidos" -ForegroundColor Green
} else {
    Write-Host "   ✓ No hay procesos anteriores corriendo" -ForegroundColor Green
}
Write-Host ""

# 3. Verificar que MetaTrader 5 esté abierto
Write-Host "3. Verificando MetaTrader 5..." -ForegroundColor Yellow
$mt5Process = Get-Process terminal64 -ErrorAction SilentlyContinue

if ($mt5Process) {
    Write-Host "   ✓ MetaTrader 5 está ejecutándose" -ForegroundColor Green
} else {
    Write-Host "   ⚠ MetaTrader 5 NO está ejecutándose" -ForegroundColor Yellow
    Write-Host "   ⚠ IMPORTANTE: Abre MetaTrader 5 antes de continuar" -ForegroundColor Red
    Write-Host ""
    $continue = Read-Host "   ¿Deseas continuar de todos modos? (S/N)"
    if ($continue -ne "S" -and $continue -ne "s") {
        Write-Host "   Abortando..." -ForegroundColor Yellow
        exit 1
    }
}
Write-Host ""

# 4. Verificar archivo .env
Write-Host "4. Verificando configuración (.env)..." -ForegroundColor Yellow
$envFile = Join-Path $projectPath ".env"

if (Test-Path $envFile) {
    Write-Host "   ✓ Archivo .env encontrado" -ForegroundColor Green
    
    # Leer y mostrar configuración (sin mostrar contraseña completa)
    $envContent = Get-Content $envFile -Raw
    if ($envContent -match "MT5_LOGIN=(\d+)") {
        Write-Host "   ✓ MT5_LOGIN configurado" -ForegroundColor Green
    } else {
        Write-Host "   ⚠ MT5_LOGIN no encontrado en .env" -ForegroundColor Yellow
    }
    
    if ($envContent -match "MT5_PASSWORD=.+") {
        Write-Host "   ✓ MT5_PASSWORD configurado" -ForegroundColor Green
    } else {
        Write-Host "   ⚠ MT5_PASSWORD no encontrado en .env" -ForegroundColor Yellow
    }
    
    if ($envContent -match "MT5_SERVER=.+") {
        $server = ($envContent | Select-String -Pattern "MT5_SERVER=(.+)").Matches.Groups[1].Value
        Write-Host "   ✓ MT5_SERVER: $server" -ForegroundColor Green
    } else {
        Write-Host "   ⚠ MT5_SERVER no encontrado en .env" -ForegroundColor Yellow
    }
} else {
    Write-Host "   ❌ Archivo .env NO encontrado" -ForegroundColor Red
    Write-Host "   Necesitas crear el archivo .env con tus credenciales" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "   Ejecuta: python setup_mt5.py" -ForegroundColor Cyan
    Write-Host "   O crea manualmente el archivo .env" -ForegroundColor Cyan
    exit 1
}
Write-Host ""

# 5. Verificar Python
Write-Host "5. Verificando Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    if ($pythonVersion -match "Python 3\.(1[2-9]|[2-9])") {
        Write-Host "   ✓ Python encontrado: $pythonVersion" -ForegroundColor Green
    } else {
        Write-Host "   ⚠ Versión de Python: $pythonVersion" -ForegroundColor Yellow
        Write-Host "   Intentando con py -3.12..." -ForegroundColor Gray
        $pythonCmd = "py -3.12"
    }
} catch {
    Write-Host "   ⚠ Python no encontrado en PATH" -ForegroundColor Yellow
    Write-Host "   Intentando con py -3.12..." -ForegroundColor Gray
    $pythonCmd = "py -3.12"
}

if (-not $pythonCmd) {
    $pythonCmd = "python"
}
Write-Host ""

# 6. Verificar dependencias
Write-Host "6. Verificando dependencias..." -ForegroundColor Yellow
try {
    $testImport = & $pythonCmd -c "import MetaTrader5; import pandas; print('OK')" 2>&1
    if ($testImport -eq "OK") {
        Write-Host "   ✓ Dependencias instaladas correctamente" -ForegroundColor Green
    } else {
        Write-Host "   ⚠ Algunas dependencias pueden faltar" -ForegroundColor Yellow
        Write-Host "   Instalando dependencias..." -ForegroundColor Gray
        & $pythonCmd -m pip install -r requirements.txt --quiet
    }
} catch {
    Write-Host "   ⚠ Error al verificar dependencias" -ForegroundColor Yellow
    Write-Host "   Instalando dependencias..." -ForegroundColor Gray
    & $pythonCmd -m pip install -r requirements.txt --quiet
}
Write-Host ""

# 7. Probar conexión con MT5
Write-Host "7. Probando conexión con MT5..." -ForegroundColor Yellow
try {
    $testResult = & $pythonCmd test_mt5_connection.py 2>&1
    if ($LASTEXITCODE -eq 0 -or $testResult -match "✓|✅|exitoso|conectado") {
        Write-Host "   ✓ Conexión con MT5 exitosa" -ForegroundColor Green
    } else {
        Write-Host "   ⚠ Advertencia en la prueba de conexión" -ForegroundColor Yellow
        Write-Host "   Verifica que MT5 esté abierto y conectado" -ForegroundColor Gray
    }
} catch {
    Write-Host "   ⚠ No se pudo probar la conexión" -ForegroundColor Yellow
}
Write-Host ""

# 8. Iniciar el bot
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "INICIANDO BOT DE TRADING" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Presiona Ctrl+C para detener el bot" -ForegroundColor Yellow
Write-Host ""

# Ejecutar el bot
try {
    & $pythonCmd live/mt5_trading.py
} catch {
    Write-Host ""
    Write-Host "❌ Error al ejecutar el bot: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "Verifica:" -ForegroundColor Yellow
    Write-Host "   1. Que MetaTrader 5 esté abierto y conectado" -ForegroundColor Gray
    Write-Host "   2. Que el archivo .env tenga las credenciales correctas" -ForegroundColor Gray
    Write-Host "   3. Que todas las dependencias estén instaladas" -ForegroundColor Gray
}




