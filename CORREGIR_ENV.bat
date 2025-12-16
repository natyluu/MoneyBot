@echo off
chcp 65001 >nul 2>&1
echo =====================================================================
echo CORREGIR ARCHIVO .env
echo =====================================================================
echo.

cd /d "C:\BOT\trading-bot-windows-20251210 on 'Mac'"

if not exist ".env" (
    echo ERROR: El archivo .env no existe
    pause
    exit /b 1
)

echo [ADVERTENCIA] El archivo .env actual tiene errores
echo.
echo Contenido actual (con error):
type .env
echo.
echo.
echo Corrigiendo archivo .env...
echo.

REM Crear archivo .env correcto
(
echo MT5_LOGIN=94342
echo MT5_PASSWORD=Santos2025!
echo MT5_SERVER=ZevenGlobal-Live
echo MT5_SYMBOL=XAUUSD.vip
echo RISK_PER_TRADE=0.01
echo MAX_CONCURRENT_TRADES=3
echo MIN_RR=2.0
) > .env

if exist ".env" (
    echo [OK] Archivo .env corregido exitosamente
    echo.
    echo Contenido corregido:
    type .env
) else (
    echo [ERROR] No se pudo corregir el archivo .env
    pause
    exit /b 1
)

echo.
echo =====================================================================
echo ARCHIVO .env CORREGIDO
echo =====================================================================
echo.
echo Ahora puedes iniciar el bot con:
echo    python -u live\mt5_trading.py
echo.
pause




