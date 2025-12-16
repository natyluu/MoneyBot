"""
config.py - Archivo de configuración centralizado

Este archivo contiene todas las configuraciones que usa el bot de trading.
Es como el "tablero de control" donde ajustas parámetros sin tocar el código principal.
"""

# Configuración de la API de trading (cuando operes en vivo)
API_KEY = "tu_api_key_aqui"  # Tu clave de API del broker
API_SECRET = "tu_api_secret_aqui"  # Tu secreto de API
BASE_URL = "https://api.broker.com"  # URL base de la API del broker

# Configuración de la estrategia
SYMBOL = "BTCUSDT"  # Par de trading (Bitcoin/USDT en este ejemplo)
TIMEFRAME = "1h"  # Marco temporal: 1m, 5m, 15m, 1h, 4h, 1d, etc.

# Parámetros de la estrategia (ajusta estos según tu estrategia)
# Ejemplo: Media móvil simple
FAST_MA_PERIOD = 10  # Período de la media móvil rápida (ej: 10 velas)
SLOW_MA_PERIOD = 30  # Período de la media móvil lenta (ej: 30 velas)

# Gestión de riesgo
MAX_POSITION_SIZE = 0.1  # Tamaño máximo de posición (10% del capital)
STOP_LOSS_PCT = 0.02  # Stop loss del 2% (salir si pierdes 2%)
TAKE_PROFIT_PCT = 0.04  # Take profit del 4% (salir si ganas 4%)

# Configuración del backtest
INITIAL_CAPITAL = 10000  # Capital inicial para el backtest (ej: $10,000)
COMMISSION = 0.001  # Comisión del broker (0.1% en este ejemplo)
START_DATE = "2023-01-01"  # Fecha de inicio del backtest
END_DATE = "2024-01-01"  # Fecha de fin del backtest

# Configuración de datos
DATA_DIR = "data"  # Carpeta donde se guardan los datos históricos

# ==================== CONFIGURACIÓN METATRADER 5 (MT5) ====================
# Estas credenciales se cargan desde el archivo .env para mayor seguridad
# NO pongas credenciales reales directamente en este archivo

import os

# Función para leer .env manualmente si load_dotenv() falla
def load_env_manual():
    """Lee el archivo .env manualmente y carga las variables"""
    env_vars = {}
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    
    if os.path.exists(env_path):
        try:
            with open(env_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    # Ignora líneas vacías y comentarios
                    if not line or line.startswith('#'):
                        continue
                    # Separa clave=valor
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        # Elimina comillas si las hay
                        if value.startswith('"') and value.endswith('"'):
                            value = value[1:-1]
                        elif value.startswith("'") and value.endswith("'"):
                            value = value[1:-1]
                        env_vars[key] = value
        except Exception as e:
            print(f"⚠️ Advertencia: No se pudo leer .env manualmente: {e}")
    
    return env_vars

# Intenta cargar con python-dotenv primero
env_vars = {}

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

# Siempre lee manualmente como respaldo (por si dotenv falla silenciosamente)
env_vars = load_env_manual()

# Carga las variables manualmente en os.environ (sobrescribe si ya existen)
for key, value in env_vars.items():
    os.environ[key] = value

def get_env(key, default=""):
    """Obtiene una variable de entorno, priorizando lectura manual"""
    # Primero intenta desde env_vars (lectura manual, más confiable)
    if key in env_vars:
        return env_vars[key]
    # Si no está en env_vars, intenta desde os.environ (puede venir de dotenv)
    value = os.getenv(key, default)
    if value:
        return value
    # Si no está en ningún lado, devuelve el default
    return default

# Credenciales de MT5 (cargadas desde .env)
MT5_LOGIN = int(get_env("MT5_LOGIN", "0"))  # Tu número de cuenta MT5
MT5_PASSWORD = get_env("MT5_PASSWORD", "")  # Tu contraseña MT5
MT5_SERVER = get_env("MT5_SERVER", "ZevenGlobal-Demo")  # Servidor MT5 (Demo o Real)
MT5_SYMBOL = get_env("MT5_SYMBOL", "XAUUSD")  # Símbolo a operar (puede ser XAUUSD o XAUUSD.m)

# Configuración de riesgo para trading en vivo
RISK_PER_TRADE = float(get_env("RISK_PER_TRADE", "0.01"))  # 1% de riesgo por operación
MAX_CONCURRENT_TRADES = int(get_env("MAX_CONCURRENT_TRADES", "3"))  # Máximo de operaciones simultáneas
MIN_RR = float(get_env("MIN_RR", "1.5"))  # Risk:Reward mínimo requerido (1:1.5)

# Configuración de Telegram (opcional)
TELEGRAM_BOT_TOKEN = get_env("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = get_env("TELEGRAM_CHAT_ID", "")

