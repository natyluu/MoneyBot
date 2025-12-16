@echo off
REM Script simple y directo para iniciar el bot
chcp 65001 >nul 2>&1
cd /d "C:\BOT\trading-bot-windows-20251210 on 'Mac'"
set PYTHONUNBUFFERED=1
python -u live\mt5_trading.py
pause




