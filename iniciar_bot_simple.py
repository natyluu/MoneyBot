"""
Script simple para iniciar el bot - Ejecuta desde el directorio raíz
"""
import sys
import os

# Cambiar al directorio del proyecto
project_dir = r"C:\BOT\trading-bot-windows-20251210 on 'Mac'"
os.chdir(project_dir)

# Agregar al path
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

# Verificar que config.py existe
config_file = os.path.join(project_dir, "config.py")
if not os.path.exists(config_file):
    print(f"❌ ERROR: No se encontró config.py en: {config_file}")
    sys.exit(1)

# Cargar config.py manualmente
import importlib.util
spec = importlib.util.spec_from_file_location("config", config_file)
config = importlib.util.module_from_spec(spec)
sys.modules["config"] = config
spec.loader.exec_module(config)

# Cargar las variables necesarias
MT5_LOGIN = config.MT5_LOGIN
MT5_PASSWORD = config.MT5_PASSWORD
MT5_SERVER = config.MT5_SERVER
MT5_SYMBOL = config.MT5_SYMBOL
RISK_PER_TRADE = config.RISK_PER_TRADE
MAX_CONCURRENT_TRADES = config.MAX_CONCURRENT_TRADES
MIN_RR = config.MIN_RR

# Ahora importar lo necesario para el bot
import MetaTrader5 as mt5
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# Cargar la estrategia
strategy_file = os.path.join(project_dir, "strategy", "ict_hybrid_strategy.py")
if os.path.exists(strategy_file):
    spec = importlib.util.spec_from_file_location("ict_hybrid_strategy", strategy_file)
    strategy_module = importlib.util.module_from_spec(spec)
    sys.modules["strategy.ict_hybrid_strategy"] = strategy_module
    spec.loader.exec_module(strategy_module)
    ICTHybridStrategy = strategy_module.ICTHybridStrategy
else:
    print(f"❌ ERROR: No se encontró strategy/ict_hybrid_strategy.py")
    sys.exit(1)

# Ahora ejecutar el código del bot (copiamos las funciones principales)
print("=" * 70)
print("🚀 INICIANDO BOT DE TRADING AUTOMÁTICO")
print("=" * 70)

# Importar las funciones del bot
bot_file = os.path.join(project_dir, "live", "mt5_trading.py")
if not os.path.exists(bot_file):
    print(f"❌ ERROR: No se encontró live/mt5_trading.py")
    sys.exit(1)

# Leer y ejecutar el bot, pero saltando las importaciones problemáticas
with open(bot_file, 'r', encoding='utf-8') as f:
    code = f.read()
    
# Reemplazar las importaciones problemáticas
code = code.replace('from config import (', '# from config import (')
code = code.replace('from strategy.ict_hybrid_strategy import ICTHybridStrategy', '# from strategy.ict_hybrid_strategy import ICTHybridStrategy')

# Ejecutar el código
exec(compile(code, bot_file, 'exec'), {
    'MT5_LOGIN': MT5_LOGIN,
    'MT5_PASSWORD': MT5_PASSWORD,
    'MT5_SERVER': MT5_SERVER,
    'MT5_SYMBOL': MT5_SYMBOL,
    'RISK_PER_TRADE': RISK_PER_TRADE,
    'MAX_CONCURRENT_TRADES': MAX_CONCURRENT_TRADES,
    'MIN_RR': MIN_RR,
    'ICTHybridStrategy': ICTHybridStrategy,
    'mt5': mt5,
    'pd': pd,
    'np': np,
    'time': time,
    'datetime': datetime,
    'timedelta': timedelta,
    'Dict': Dict,
    'List': List,
    'Optional': Optional,
    'sys': sys,
    'os': os,
    '__name__': '__main__'
})




