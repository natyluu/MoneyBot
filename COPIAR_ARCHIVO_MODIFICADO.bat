@echo off
chcp 65001 >nul 2>&1
echo =====================================================================
echo COPIAR ARCHIVO MODIFICADO A WINDOWS
echo =====================================================================
echo.

REM Copiar el archivo de estrategia modificado
echo Copiando strategy\ict_hybrid_strategy.py...
xcopy "\\Mac\Home\bot de trader\strategy\ict_hybrid_strategy.py" "C:\BOT\trading-bot-windows-20251210 on 'Mac'\strategy\" /Y

if errorlevel 1 (
    echo.
    echo ERROR: No se pudo copiar el archivo
    echo.
    echo SOLUCIONES:
    echo   1. Verifica que puedas acceder a \\Mac\Home\bot de trader
    echo   2. Verifica que el archivo existe en Mac
    echo   3. Copia manualmente desde el Explorador
    echo.
    pause
    exit /b 1
)

echo.
echo [OK] Archivo copiado exitosamente
echo.
echo El bot ahora requiere solo 1 confirmacion en lugar de 3
echo.
echo IMPORTANTE: Reinicia el bot para que los cambios surtan efecto
echo.
pause




