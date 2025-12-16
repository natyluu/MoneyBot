# Script de diagnóstico completo para el bot de trading
# Ejecuta este script en PowerShell para verificar que todo está configurado correctamente

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "🔍 DIAGNÓSTICO COMPLETO DEL BOT DE TRADING" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

# 1. Verificar directorio actual
Write-Host "1️⃣ VERIFICANDO DIRECTORIO ACTUAL..." -ForegroundColor Yellow
$currentDir = Get-Location
Write-Host "   Directorio actual: $currentDir" -ForegroundColor Gray
Write-Host ""

# 2. Verificar archivos necesarios
Write-Host "2️⃣ VERIFICANDO ARCHIVOS NECESARIOS..." -ForegroundColor Yellow
$filesToCheck = @(
    "config.py",
    ".env",
    "live\mt5_trading.py",
    "strategy\ict_hybrid_strategy.py"
)

$allFilesExist = $true
foreach ($filePath in $filesToCheck) {
    $fullPath = Join-Path $currentDir $filePath
    $exists = Test-Path $fullPath
    if ($exists) {
        Write-Host "   ✓ $filePath : EXISTE" -ForegroundColor Green
    } else {
        Write-Host "   ❌ $filePath : NO EXISTE" -ForegroundColor Red
        Write-Host "      Ruta completa: $fullPath" -ForegroundColor Gray
        $allFilesExist = $false
    }
}

if (-not $allFilesExist) {
    Write-Host ""
    Write-Host "⚠️ ADVERTENCIA: Faltan algunos archivos. El bot puede no funcionar correctamente." -ForegroundColor Yellow
}
Write-Host ""

# 3. Verificar Python
Write-Host "3️⃣ VERIFICANDO PYTHON..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "   Versión de Python: $pythonVersion" -ForegroundColor Green
    
    $pythonExe = (Get-Command python -ErrorAction SilentlyContinue).Source
    if ($pythonExe) {
        Write-Host "   Ejecutable: $pythonExe" -ForegroundColor Gray
    }
} catch {
    Write-Host "   ❌ Python NO está instalado o no está en el PATH" -ForegroundColor Red
}
Write-Host ""

# 4. Verificar módulos instalados
Write-Host "4️⃣ VERIFICANDO MÓDULOS INSTALADOS..." -ForegroundColor Yellow
$modulesToCheck = @("MetaTrader5", "pandas", "numpy", "dotenv")

foreach ($moduleName in $modulesToCheck) {
    try {
        $result = python -c "import $moduleName; print('OK')" 2>&1
        if ($result -match "OK") {
            # Intentar obtener versión
            $versionResult = python -c "import $moduleName; print(getattr($moduleName, '__version__', 'N/A'))" 2>&1
            if ($versionResult -and $versionResult -ne "") {
                Write-Host "   ✓ $moduleName : INSTALADO (versión: $versionResult)" -ForegroundColor Green
            } else {
                Write-Host "   ✓ $moduleName : INSTALADO" -ForegroundColor Green
            }
        } else {
            Write-Host "   ❌ $moduleName : NO INSTALADO" -ForegroundColor Red
        }
    } catch {
        Write-Host "   ❌ $moduleName : NO INSTALADO" -ForegroundColor Red
    }
}
Write-Host ""

# 5. Verificar .env
Write-Host "5️⃣ VERIFICANDO ARCHIVO .env..." -ForegroundColor Yellow
$envPath = Join-Path $currentDir ".env"
if (Test-Path $envPath) {
    Write-Host "   ✓ .env existe en: $envPath" -ForegroundColor Green
    try {
        $envContent = Get-Content $envPath -Encoding UTF8
        Write-Host "   ✓ .env tiene $($envContent.Count) líneas" -ForegroundColor Gray
        
        $requiredVars = @("MT5_LOGIN", "MT5_PASSWORD", "MT5_SERVER", "MT5_SYMBOL")
        $envVars = @{}
        
        foreach ($line in $envContent) {
            $line = $line.Trim()
            if ($line -and -not $line.StartsWith("#") -and $line.Contains("=")) {
                $parts = $line.Split("=", 2)
                if ($parts.Length -eq 2) {
                    $key = $parts[0].Trim()
                    $value = $parts[1].Trim()
                    # Eliminar comillas si las hay
                    if ($value.StartsWith('"') -and $value.EndsWith('"')) {
                        $value = $value.Substring(1, $value.Length - 2)
                    } elseif ($value.StartsWith("'") -and $value.EndsWith("'")) {
                        $value = $value.Substring(1, $value.Length - 2)
                    }
                    $envVars[$key] = $value
                }
            }
        }
        
        Write-Host ""
        Write-Host "   Variables encontradas en .env:" -ForegroundColor Gray
        foreach ($var in $requiredVars) {
            if ($envVars.ContainsKey($var)) {
                if ($var -eq "MT5_PASSWORD") {
                    $hiddenValue = "*" * $envVars[$var].Length
                    Write-Host "   ✓ $var : $hiddenValue (oculto)" -ForegroundColor Green
                } else {
                    Write-Host "   ✓ $var : $($envVars[$var])" -ForegroundColor Green
                }
            } else {
                Write-Host "   ❌ $var : NO ENCONTRADO" -ForegroundColor Red
            }
        }
    } catch {
        Write-Host "   ❌ Error al leer .env: $_" -ForegroundColor Red
    }
} else {
    Write-Host "   ❌ .env NO EXISTE en: $envPath" -ForegroundColor Red
}
Write-Host ""

# 6. Verificar config.py
Write-Host "6️⃣ VERIFICANDO config.py..." -ForegroundColor Yellow
$configPath = Join-Path $currentDir "config.py"
if (Test-Path $configPath) {
    try {
        # Intentar importar config usando Python
        $configTest = python -c "import sys; sys.path.insert(0, '.'); import importlib.util; spec = importlib.util.spec_from_file_location('config', 'config.py'); config = importlib.util.module_from_spec(spec); spec.loader.exec_module(config); print('OK')" 2>&1
        if ($configTest -match "OK") {
            Write-Host "   ✓ config.py se puede importar correctamente" -ForegroundColor Green
            
            # Verificar variables importantes
            $requiredConfigVars = @("MT5_LOGIN", "MT5_PASSWORD", "MT5_SERVER", "MT5_SYMBOL", "RISK_PER_TRADE", "MAX_CONCURRENT_TRADES", "MIN_RR")
            Write-Host ""
            Write-Host "   Variables de configuración:" -ForegroundColor Gray
            foreach ($var in $requiredConfigVars) {
                $varTest = python -c "import sys; sys.path.insert(0, '.'); import importlib.util; spec = importlib.util.spec_from_file_location('config', 'config.py'); config = importlib.util.module_from_spec(spec); spec.loader.exec_module(config); print(getattr(config, '$var', 'NOT_FOUND'))" 2>&1
                if ($varTest -and $varTest -ne "NOT_FOUND" -and -not $varTest.Contains("Error")) {
                    if ($var -eq "MT5_PASSWORD") {
                        $hiddenValue = "*" * $varTest.Trim().Length
                        Write-Host "   ✓ $var : $hiddenValue (oculto)" -ForegroundColor Green
                    } else {
                        Write-Host "   ✓ $var : $($varTest.Trim())" -ForegroundColor Green
                    }
                } else {
                    Write-Host "   ❌ $var : NO DEFINIDO" -ForegroundColor Red
                }
            }
        } else {
            Write-Host "   ❌ Error al importar config.py: $configTest" -ForegroundColor Red
        }
    } catch {
        Write-Host "   ❌ Error al verificar config.py: $_" -ForegroundColor Red
    }
} else {
    Write-Host "   ❌ config.py NO EXISTE" -ForegroundColor Red
}
Write-Host ""

# 7. Verificar MT5
Write-Host "7️⃣ VERIFICANDO CONEXIÓN CON MT5..." -ForegroundColor Yellow
try {
    $mt5Test = python -c "import MetaTrader5 as mt5; result = mt5.initialize(); print('OK' if result else 'FAIL'); mt5.shutdown() if result else None" 2>&1
    if ($mt5Test -match "OK") {
        Write-Host "   ✓ MT5 se puede inicializar" -ForegroundColor Green
        
        # Obtener información del terminal
        $mt5Info = python -c "import MetaTrader5 as mt5; mt5.initialize(); info = mt5.terminal_info(); print(f'{info.name}|{info.build}|{info.path}'); mt5.shutdown()" 2>&1
        if ($mt5Info -and -not $mt5Info.Contains("Error")) {
            $infoParts = $mt5Info.Split("|")
            if ($infoParts.Length -eq 3) {
                Write-Host "   ✓ Terminal MT5: $($infoParts[0])" -ForegroundColor Gray
                Write-Host "   ✓ Versión: $($infoParts[1])" -ForegroundColor Gray
                Write-Host "   ✓ Ruta: $($infoParts[2])" -ForegroundColor Gray
            }
        }
    } else {
        Write-Host "   ❌ MT5 NO se puede inicializar" -ForegroundColor Red
        Write-Host "      POSIBLES CAUSAS:" -ForegroundColor Yellow
        Write-Host "      - MetaTrader 5 no está instalado" -ForegroundColor Gray
        Write-Host "      - MetaTrader 5 no está abierto" -ForegroundColor Gray
        Write-Host "      - MetaTrader 5 está en otra ubicación" -ForegroundColor Gray
    }
} catch {
    Write-Host "   ⚠️ MetaTrader5 no está instalado (no se puede verificar)" -ForegroundColor Yellow
}
Write-Host ""

# 8. Verificar estrategia
Write-Host "8️⃣ VERIFICANDO ESTRATEGIA..." -ForegroundColor Yellow
$strategyPath = Join-Path $currentDir "strategy\ict_hybrid_strategy.py"
if (Test-Path $strategyPath) {
    try {
        $strategyTest = python -c "import sys; sys.path.insert(0, '.'); from strategy.ict_hybrid_strategy import ICTHybridStrategy; strategy = ICTHybridStrategy(); print('OK')" 2>&1
        if ($strategyTest -match "OK") {
            Write-Host "   ✓ ICTHybridStrategy se puede importar e instanciar" -ForegroundColor Green
        } else {
            Write-Host "   ❌ Error al importar estrategia: $strategyTest" -ForegroundColor Red
        }
    } catch {
        Write-Host "   ❌ Error al verificar estrategia: $_" -ForegroundColor Red
    }
} else {
    Write-Host "   ❌ Estrategia no encontrada en: $strategyPath" -ForegroundColor Red
}
Write-Host ""

# 9. Verificar mt5_trading.py
Write-Host "9️⃣ VERIFICANDO live\mt5_trading.py..." -ForegroundColor Yellow
$mt5TradingPath = Join-Path $currentDir "live\mt5_trading.py"
if (Test-Path $mt5TradingPath) {
    try {
        $syntaxTest = python -m py_compile "live\mt5_trading.py" 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "   ✓ live\mt5_trading.py se puede leer y parsear correctamente" -ForegroundColor Green
        } else {
            Write-Host "   ❌ Error de sintaxis en mt5_trading.py: $syntaxTest" -ForegroundColor Red
        }
    } catch {
        Write-Host "   ❌ Error al verificar mt5_trading.py: $_" -ForegroundColor Red
    }
} else {
    Write-Host "   ❌ live\mt5_trading.py NO EXISTE" -ForegroundColor Red
}
Write-Host ""

# 10. Resumen
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "📋 RESUMEN Y RECOMENDACIONES" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "✅ Si todos los checks pasaron, el bot debería funcionar." -ForegroundColor Green
Write-Host ""
Write-Host "🔧 COMANDO PARA INICIAR EL BOT:" -ForegroundColor Yellow
Write-Host "   cd `"$currentDir`"" -ForegroundColor Gray
Write-Host "   python -u live\mt5_trading.py" -ForegroundColor Gray
Write-Host ""
Write-Host "⚠️ IMPORTANTE:" -ForegroundColor Yellow
Write-Host "   1. Asegúrate de que MetaTrader 5 esté ABIERTO" -ForegroundColor Gray
Write-Host "   2. Asegúrate de estar conectado a tu cuenta en MT5" -ForegroundColor Gray
Write-Host "   3. Usa el flag -u para ver mensajes en tiempo real" -ForegroundColor Gray
Write-Host "   4. Si hay errores, revisa los mensajes de arriba" -ForegroundColor Gray
Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan




