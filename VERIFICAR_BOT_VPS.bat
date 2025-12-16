@echo off
REM ========================================
REM   VERIFICAR ESTADO DEL BOT EN VPS
REM ========================================
chcp 65001 >nul 2>&1
echo.
echo ========================================
echo   VERIFICACIÓN DEL BOT DE TRADING
echo ========================================
echo.

REM Verificar directorio
cd /d "C:\BOT\trading-bot" 2>nul
if errorlevel 1 (
    echo [ERROR] Directorio del proyecto no encontrado
    echo Ruta esperada: C:\BOT\trading-bot
    echo.
) else (
    echo [OK] Directorio del proyecto encontrado
    echo.
)

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no está instalado o no está en PATH
    echo.
) else (
    echo [OK] Python instalado:
    python --version
    echo.
)

REM Verificar archivos principales
if exist "live\mt5_trading.py" (
    echo [OK] Archivo mt5_trading.py encontrado
) else (
    echo [ERROR] Archivo mt5_trading.py NO encontrado
)
echo.

if exist "config.py" (
    echo [OK] Archivo config.py encontrado
) else (
    echo [ERROR] Archivo config.py NO encontrado
)
echo.

if exist ".env" (
    echo [OK] Archivo .env encontrado
) else (
    echo [ADVERTENCIA] Archivo .env NO encontrado
    echo Necesitas crear este archivo con tus credenciales
)
echo.

REM Verificar módulos Python
echo Verificando módulos Python...
python -c "import MetaTrader5; print('[OK] MetaTrader5 instalado')" 2>nul || echo [ERROR] MetaTrader5 NO instalado
python -c "import pandas; print('[OK] pandas instalado')" 2>nul || echo [ERROR] pandas NO instalado
python -c "import numpy; print('[OK] numpy instalado')" 2>nul || echo [ERROR] numpy NO instalado
python -c "import dotenv; print('[OK] python-dotenv instalado')" 2>nul || echo [ERROR] python-dotenv NO instalado
echo.

REM Verificar procesos
echo ========================================
echo   PROCESOS ACTIVOS
echo ========================================
echo.

tasklist | findstr /i python >nul
if errorlevel 1 (
    echo [INFO] No hay procesos Python activos
) else (
    echo [INFO] Procesos Python activos:
    tasklist | findstr /i python
)
echo.

tasklist | findstr /i terminal64 >nul
if errorlevel 1 (
    echo [ADVERTENCIA] MetaTrader 5 NO está abierto
    echo El bot necesita MT5 abierto y conectado
) else (
    echo [OK] MetaTrader 5 está abierto
    tasklist | findstr /i terminal64
)
echo.

REM Verificar conexión MT5 (si está abierto)
tasklist | findstr /i terminal64 >nul
if not errorlevel 1 (
    echo ========================================
    echo   PROBANDO CONEXIÓN MT5
    echo ========================================
    echo.
    python -c "import MetaTrader5 as mt5; mt5.initialize(); print('[OK] MT5 inicializado') if mt5.initialize() else print('[ERROR] No se pudo inicializar MT5'); mt5.shutdown()" 2>nul
    echo.
)

echo ========================================
echo   VERIFICACIÓN COMPLETA
echo ========================================
echo.
pause

