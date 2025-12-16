@echo off
chcp 65001 >nul 2>&1
echo =====================================================================
echo CREAR ARCHIVO .env EN WINDOWS
echo =====================================================================
echo.

cd /d "C:\BOT\trading-bot-windows-20251210 on 'Mac'"

REM Verificar si .env ya existe
if exist ".env" (
    echo [ADVERTENCIA] El archivo .env ya existe
    echo.
    echo Contenido actual:
    type .env
    echo.
    echo Deseas sobrescribirlo? (S/N)
    set /p respuesta=
    if /i not "%respuesta%"=="S" (
        echo Cancelado.
        pause
        exit /b 0
    )
)

echo.
echo Creando archivo .env...
echo.

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
    echo [OK] Archivo .env creado exitosamente
    echo.
    echo Contenido:
    type .env
) else (
    echo [ERROR] No se pudo crear el archivo .env
    pause
    exit /b 1
)

echo.
echo =====================================================================
echo ARCHIVO .env CREADO
echo =====================================================================
echo.
echo IMPORTANTE: Verifica que las credenciales sean correctas
echo.
pause




