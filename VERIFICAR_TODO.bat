@echo off
REM Script completo de verificación - Muestra TODO lo que falta
chcp 65001 >nul 2>&1

echo ======================================================================
echo VERIFICACION COMPLETA - QUE FALTA PARA INICIAR EL BOT
echo ======================================================================
echo.

REM Cambiar al directorio
cd /d "C:\BOT\trading-bot-windows-20251210 on 'Mac'" 2>nul
if errorlevel 1 (
    echo [ERROR CRITICO] No se pudo cambiar al directorio del proyecto
    echo.
    echo La ruta "C:\BOT\trading-bot-windows-20251210 on 'Mac'" no existe
    echo.
    echo SOLUCION: Verifica que el proyecto este copiado en Windows
    echo.
    pause
    exit /b 1
)

echo [OK] Directorio: %CD%
echo.

REM ======================================================================
echo 1. VERIFICANDO ARCHIVOS NECESARIOS
echo ======================================================================
echo.

set FALTAN_ARCHIVOS=0

if exist "config.py" (
    echo [OK] config.py existe
) else (
    echo [FALTA] config.py NO existe
    set /a FALTAN_ARCHIVOS+=1
)

if exist ".env" (
    echo [OK] .env existe
    echo.
    echo Contenido de .env:
    type .env
    echo.
) else (
    echo [FALTA] .env NO existe - CRITICO
    echo.
    echo SOLUCION: Crea el archivo .env con tus credenciales
    echo.
    set /a FALTAN_ARCHIVOS+=1
)

if exist "live\mt5_trading.py" (
    echo [OK] live\mt5_trading.py existe
) else (
    echo [FALTA] live\mt5_trading.py NO existe
    set /a FALTAN_ARCHIVOS+=1
)

if exist "strategy\ict_hybrid_strategy.py" (
    echo [OK] strategy\ict_hybrid_strategy.py existe
) else (
    echo [FALTA] strategy\ict_hybrid_strategy.py NO existe
    set /a FALTAN_ARCHIVOS+=1
)

echo.

REM ======================================================================
echo 2. VERIFICANDO PYTHON
echo ======================================================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo [FALTA] Python NO esta instalado o no esta en el PATH
    echo.
    echo SOLUCION: Instala Python 3.12 desde python.org
    echo           Marca "Add Python to PATH" durante la instalacion
    echo.
    set /a FALTAN_ARCHIVOS+=1
) else (
    echo [OK] Python esta instalado:
    python --version
    echo.
)

REM ======================================================================
echo 3. VERIFICANDO MODULOS PYTHON
echo ======================================================================
echo.

python -c "import MetaTrader5; print('[OK] MetaTrader5 instalado')" 2>nul || (
    echo [FALTA] MetaTrader5 NO instalado
    echo SOLUCION: pip install MetaTrader5
    set /a FALTAN_ARCHIVOS+=1
)

python -c "import pandas; print('[OK] pandas instalado')" 2>nul || (
    echo [FALTA] pandas NO instalado
    echo SOLUCION: pip install pandas
    set /a FALTAN_ARCHIVOS+=1
)

python -c "import numpy; print('[OK] numpy instalado')" 2>nul || (
    echo [FALTA] numpy NO instalado
    echo SOLUCION: pip install numpy
    set /a FALTAN_ARCHIVOS+=1
)

python -c "import dotenv; print('[OK] python-dotenv instalado')" 2>nul || (
    echo [FALTA] python-dotenv NO instalado
    echo SOLUCION: pip install python-dotenv
    set /a FALTAN_ARCHIVOS+=1
)

echo.

REM ======================================================================
echo 4. VERIFICANDO METATRADER 5
echo ======================================================================
echo.

tasklist /FI "IMAGENAME eq terminal64.exe" 2>NUL | find /I /N "terminal64.exe">NUL
if errorlevel 1 (
    echo [ADVERTENCIA] MetaTrader 5 NO esta abierto
    echo.
    echo SOLUCION: Abre MetaTrader 5 y conectate a tu cuenta (94342)
    echo.
) else (
    echo [OK] MetaTrader 5 esta abierto
    echo.
)

REM ======================================================================
echo 5. RESUMEN
echo ======================================================================
echo.

if %FALTAN_ARCHIVOS% EQU 0 (
    echo [OK] Todos los archivos necesarios existen
    echo.
    echo El bot deberia poder iniciarse.
    echo.
    echo SIGUIENTE PASO:
    echo 1. Abre MetaTrader 5 y conectate
    echo 2. Ejecuta: INICIAR_BOT_FINAL.bat
    echo.
) else (
    echo [ATENCION] Faltan %FALTAN_ARCHIVOS% archivos o componentes
    echo.
    echo Revisa los mensajes de arriba para ver que falta.
    echo.
)

echo ======================================================================
pause




