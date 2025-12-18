"""
live/mt5_trading.py - Conexión a MetaTrader 5 para Trading en Vivo

Este módulo conecta Python con MetaTrader 5 (MT5) para operar directamente
en el broker Zeven con la estrategia institucional ICT.

Para una trader ICT novata en Python:
- Este archivo conecta tu bot de Python con MetaTrader 5
- Obtiene datos en tiempo real del mercado
- Genera señales usando tu estrategia ICT
- Envía órdenes BUY/SELL automáticamente al broker
- Gestiona tus posiciones abiertas

IMPORTANTE:
- Siempre prueba primero en cuenta DEMO
- No pongas credenciales reales en el código (usa .env)
- El trading automático conlleva riesgo real de pérdida
"""

import sys
import os

# FORZAR UNBUFFERED OUTPUT INMEDIATAMENTE
# Esto debe ser lo primero que se ejecuta
sys.stdout.reconfigure(line_buffering=True) if hasattr(sys.stdout, 'reconfigure') else None
sys.stderr.reconfigure(line_buffering=True) if hasattr(sys.stderr, 'reconfigure') else None

# Configurar encoding UTF-8 para Windows (permite mostrar emojis)
# También desactivar el buffer para que los mensajes se muestren inmediatamente
if sys.platform == 'win32':
    import io
    # Desactivar buffer para ver mensajes en tiempo real
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace', line_buffering=True)
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace', line_buffering=True)
    # Forzar que Python no use buffer
    os.environ['PYTHONUNBUFFERED'] = '1'
    # Forzar flush inmediato después de cada print
    original_print = print
    def unbuffered_print(*args, **kwargs):
        original_print(*args, **kwargs)
        sys.stdout.flush()
        sys.stderr.flush()
    print = unbuffered_print

# MENSAJE INMEDIATO PARA VERIFICAR QUE EL CÓDIGO SE EJECUTA
print("🔧 Bot iniciando...", flush=True)
sys.stdout.flush()

# Agregar el directorio raíz al path para que Python encuentre los módulos
# Esto permite importar config y otros módulos desde cualquier ubicación
# Obtener el directorio del script (funciona incluso cuando se ejecuta con exec())
try:
    # Intenta obtener __file__ (funciona cuando se ejecuta directamente)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
except NameError:
    # Si __file__ no está definido (ej: cuando se ejecuta con exec), usar el directorio actual
    script_dir = os.getcwd()
    # Si estamos en la carpeta live, subir un nivel
    if os.path.basename(script_dir) == 'live':
        project_root = os.path.dirname(script_dir)
    else:
        project_root = script_dir
    # Verificar que config.py existe en project_root
    if not os.path.exists(os.path.join(project_root, 'config.py')):
        # Si no está, intentar el directorio actual
        project_root = os.getcwd()

# Normalizar la ruta para evitar problemas con caracteres especiales
project_root = os.path.normpath(project_root)

# Debug: verificar que config.py existe (solo mostrar advertencia, no salir)
config_path = os.path.join(project_root, "config.py")
if not os.path.exists(config_path):
    print(f"⚠️ ADVERTENCIA: No se encontró config.py en: {config_path}")
    print(f"   Intentando buscar en otros lugares...")
    # Intentar buscar en el directorio actual de trabajo
    current_dir_config = os.path.join(os.getcwd(), "config.py")
    if os.path.exists(current_dir_config):
        print(f"   ✓ Encontrado en: {current_dir_config}")
        project_root = os.getcwd()
        config_path = current_dir_config
    else:
        print(f"   ❌ No se encontró config.py en ningún lugar")
        print(f"   Directorio del script: {script_dir}")
        print(f"   Directorio raíz calculado: {project_root}")
        print(f"   Directorio actual de trabajo: {os.getcwd()}")
        sys.exit(1)

# Agregar al path (múltiples ubicaciones para asegurar que funcione)
paths_to_add = [project_root, os.getcwd()]
for path in paths_to_add:
    path = os.path.normpath(path)
    if path and path not in sys.path:
        sys.path.insert(0, path)

# Cargar config.py de manera robusta
import importlib.util
config_paths = [
    os.path.join(project_root, "config.py"),
    os.path.join(os.getcwd(), "config.py"),
    "config.py"
]
config_loaded = False
config_module = None

for cfg_path in config_paths:
    if os.path.exists(cfg_path):
        try:
            spec = importlib.util.spec_from_file_location("config", cfg_path)
            config_module = importlib.util.module_from_spec(spec)
            sys.modules["config"] = config_module
            spec.loader.exec_module(config_module)
            config_loaded = True
            print(f"✓ Config cargado desde: {cfg_path}")
            break
        except Exception as e:
            print(f"⚠️ Error al cargar {cfg_path}: {e}")
            continue

if not config_loaded:
    # Último intento: import normal
    try:
        import config as config_module
        config_loaded = True
    except ImportError:
        print(f"❌ ERROR: No se pudo cargar config.py")
        print(f"   Buscado en: {config_paths}")
        print(f"   Directorio actual: {os.getcwd()}")
        print(f"   Project root: {project_root}")
        sys.exit(1)

# Ahora podemos importar las variables desde config
MT5_LOGIN = config_module.MT5_LOGIN
MT5_PASSWORD = config_module.MT5_PASSWORD
MT5_SERVER = config_module.MT5_SERVER
MT5_SYMBOL = config_module.MT5_SYMBOL
RISK_PER_TRADE = config_module.RISK_PER_TRADE
MAX_CONCURRENT_TRADES = config_module.MAX_CONCURRENT_TRADES
MIN_RR = config_module.MIN_RR

# Configuración News Risk Gate
SPREAD_MAX = config_module.SPREAD_MAX
ATR_MAX_RATIO = config_module.ATR_MAX_RATIO
DAILY_DD_LIMIT = config_module.DAILY_DD_LIMIT
NEWS_USD_WINDOW_MINUTES = config_module.NEWS_USD_WINDOW_MINUTES
NEWS_MIN_EVENTS_FOR_CLUSTER = config_module.NEWS_MIN_EVENTS_FOR_CLUSTER
NEWS_BLOCK_PRE_MINUTES = config_module.NEWS_BLOCK_PRE_MINUTES
NEWS_BLOCK_POST_MINUTES = config_module.NEWS_BLOCK_POST_MINUTES
NEWS_COOLDOWN_MINUTES = config_module.NEWS_COOLDOWN_MINUTES
EIA_BLOCK_PRE_MINUTES = config_module.EIA_BLOCK_PRE_MINUTES
EIA_BLOCK_POST_MINUTES = config_module.EIA_BLOCK_POST_MINUTES
HIGH_NEWS_BLOCK_PRE_MINUTES = config_module.HIGH_NEWS_BLOCK_PRE_MINUTES
HIGH_NEWS_BLOCK_POST_MINUTES = config_module.HIGH_NEWS_BLOCK_POST_MINUTES
HIGH_NEWS_COOLDOWN_MINUTES = config_module.HIGH_NEWS_COOLDOWN_MINUTES
NEWS_BLOCK_POST_MINUTES = config_module.NEWS_BLOCK_POST_MINUTES
NEWS_COOLDOWN_MINUTES = config_module.NEWS_COOLDOWN_MINUTES
EIA_BLOCK_PRE_MINUTES = config_module.EIA_BLOCK_PRE_MINUTES
EIA_BLOCK_POST_MINUTES = config_module.EIA_BLOCK_POST_MINUTES

import MetaTrader5 as mt5
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# Importar News Risk Gate
try:
    from news.provider import get_news_provider
    from risk.news_gate import should_block_new_entries
    from utils.indicators import calculate_atr, calculate_atr_ratio
    NEWS_GATE_AVAILABLE = True
except ImportError as e:
    NEWS_GATE_AVAILABLE = False
    if logger:
        logger.warning(f"News Risk Gate no disponible: {e}")

# Cargar strategy de manera similar
try:
    from strategy.ict_hybrid_strategy import ICTHybridStrategy
except ImportError:
    # Intentar cargar desde path absoluto
    strategy_path = os.path.join(project_root, "strategy", "ict_hybrid_strategy.py")
    if os.path.exists(strategy_path):
        spec = importlib.util.spec_from_file_location("ict_hybrid_strategy", strategy_path)
        strategy_module = importlib.util.module_from_spec(spec)
        sys.modules["strategy.ict_hybrid_strategy"] = strategy_module
        spec.loader.exec_module(strategy_module)
        ICTHybridStrategy = strategy_module.ICTHybridStrategy
    else:
        print(f"❌ ERROR: No se encontró strategy/ict_hybrid_strategy.py")
        sys.exit(1)

# Importar módulos del sistema profesional
try:
    from utils.logger import logger
    from utils.database import TradingDatabase
    from live.position_manager import PositionManager
    from live.trade_analyzer import TradeAnalyzer
    from live.telegram_alerts import TelegramAlerts
except ImportError as e:
    # Intentar cargar desde paths absolutos
    try:
        utils_logger_path = os.path.join(project_root, "utils", "logger.py")
        if os.path.exists(utils_logger_path):
            spec = importlib.util.spec_from_file_location("logger", utils_logger_path)
            logger_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(logger_module)
            logger = logger_module.logger
        else:
            logger = None
        
        utils_db_path = os.path.join(project_root, "utils", "database.py")
        if os.path.exists(utils_db_path):
            spec = importlib.util.spec_from_file_location("database", utils_db_path)
            db_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(db_module)
            TradingDatabase = db_module.TradingDatabase
        else:
            TradingDatabase = None
        
        pos_mgr_path = os.path.join(project_root, "live", "position_manager.py")
        if os.path.exists(pos_mgr_path):
            spec = importlib.util.spec_from_file_location("position_manager", pos_mgr_path)
            pos_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(pos_module)
            PositionManager = pos_module.PositionManager
        else:
            PositionManager = None
        
        trade_analyzer_path = os.path.join(project_root, "live", "trade_analyzer.py")
        if os.path.exists(trade_analyzer_path):
            spec = importlib.util.spec_from_file_location("trade_analyzer", trade_analyzer_path)
            analyzer_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(analyzer_module)
            TradeAnalyzer = analyzer_module.TradeAnalyzer
        else:
            TradeAnalyzer = None
    except Exception as import_error:
        print(f"⚠️ Advertencia: No se pudieron cargar módulos profesionales: {import_error}")
        logger = None
        TradingDatabase = None
        PositionManager = None
        TradeAnalyzer = None
        TelegramAlerts = None


# Mapeo de timeframes ICT a timeframes MT5
# MT5 usa códigos numéricos para los timeframes
TIMEFRAME_MT5 = {
    "M1": mt5.TIMEFRAME_M1,      # 1 minuto
    "M3": mt5.TIMEFRAME_M3,      # 3 minutos (si está disponible)
    "M5": mt5.TIMEFRAME_M5,      # 5 minutos
    "M15": mt5.TIMEFRAME_M15,    # 15 minutos
    "H1": mt5.TIMEFRAME_H1,      # 1 hora
    "H4": mt5.TIMEFRAME_H4,      # 4 horas
    "D1": mt5.TIMEFRAME_D1       # 1 día
}


def init_mt5() -> bool:
    """
    Inicializa la conexión con MetaTrader 5.
    
    ¿Qué hace esta función?
    1. Inicia MT5 desde Python
    2. Se conecta a tu cuenta usando tus credenciales
    3. Verifica que el símbolo (XAUUSD) esté disponible
    4. Retorna True si todo está bien, False si hay error
    
    Returns:
        True si la conexión fue exitosa, False en caso contrario
    """
    print("🔌 Inicializando conexión con MetaTrader 5...")
    
    # Inicializa MT5
    if not mt5.initialize():
        print(f"❌ Error al inicializar MT5: {mt5.last_error()}")
        return False
    
    print("✓ MT5 inicializado")
    
    # Conecta a la cuenta
    if not mt5.login(MT5_LOGIN, password=MT5_PASSWORD, server=MT5_SERVER):
        print(f"❌ Error al conectar a MT5: {mt5.last_error()}")
        print(f"   Login: {MT5_LOGIN}")
        print(f"   Server: {MT5_SERVER}")
        mt5.shutdown()
        return False
    
    print(f"✓ Conectado a cuenta {MT5_LOGIN} en servidor {MT5_SERVER}")
    
    # Verifica que el símbolo esté disponible
    symbol_info = mt5.symbol_info(MT5_SYMBOL)
    if symbol_info is None:
        print(f"❌ Símbolo {MT5_SYMBOL} no encontrado")
        print("   Intenta con XAUUSD.m o verifica el nombre exacto en MT5")
        mt5.shutdown()
        return False
    
    # Activa el símbolo para trading
    if not symbol_info.visible:
        if not mt5.symbol_select(MT5_SYMBOL, True):
            print(f"❌ No se pudo activar el símbolo {MT5_SYMBOL}")
            mt5.shutdown()
            return False
    
    print(f"✓ Símbolo {MT5_SYMBOL} activado y disponible")
    
    # Muestra información de la cuenta
    account_info = mt5.account_info()
    if account_info:
        print(f"\n📊 Información de la cuenta:")
        print(f"   Balance: ${account_info.balance:,.2f}")
        print(f"   Equity: ${account_info.equity:,.2f}")
        print(f"   Margen libre: ${account_info.margin_free:,.2f}")
        print(f"   Leverage: 1:{account_info.leverage}")
    
    return True


def fetch_candles(symbol: str, timeframe: str, count: int = 500) -> Optional[pd.DataFrame]:
    """
    Obtiene velas (velas de precio) desde MetaTrader 5.
    
    ¿Qué son las velas?
    Cada vela representa el precio durante un período de tiempo:
    - open: Precio de apertura
    - high: Precio máximo
    - low: Precio mínimo
    - close: Precio de cierre
    - volume: Volumen negociado
    
    Args:
        symbol: Símbolo a obtener (ej: "XAUUSD")
        timeframe: Timeframe a obtener ("M1", "M5", "H1", etc.)
        count: Número de velas a obtener (default: 500)
    
    Returns:
        DataFrame con las velas o None si hay error
    """
    # Convierte el timeframe a código MT5
    if timeframe not in TIMEFRAME_MT5:
        print(f"❌ Timeframe {timeframe} no válido")
        return None
    
    mt5_timeframe = TIMEFRAME_MT5[timeframe]
    
    # Obtiene las velas desde MT5
    # copy_rates_from_pos obtiene las últimas N velas desde la posición 0 (más reciente)
    rates = mt5.copy_rates_from_pos(symbol, mt5_timeframe, 0, count)
    
    if rates is None or len(rates) == 0:
        print(f"⚠️ No se pudieron obtener velas para {symbol} {timeframe}")
        return None
    
    # Convierte a DataFrame de pandas
    df = pd.DataFrame(rates)
    
    # Convierte el timestamp a datetime
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df.set_index('time', inplace=True)
    
    # Renombra columnas para que coincidan con nuestro formato
    df.rename(columns={
        'open': 'open',
        'high': 'high',
        'low': 'low',
        'close': 'close',
        'tick_volume': 'volume'
    }, inplace=True)
    
    # Asegura que tenga todas las columnas necesarias
    required_cols = ['open', 'high', 'low', 'close', 'volume']
    if not all(col in df.columns for col in required_cols):
        print(f"⚠️ Faltan columnas en los datos de {symbol} {timeframe}")
        return None
    
    return df[required_cols]


def build_multitimeframe_context(symbol: str = None) -> Dict[str, pd.DataFrame]:
    """
    Construye el contexto multi-temporal obteniendo datos de todos los timeframes.
    
    Como trader ICT, necesitas analizar el mercado en múltiples timeframes:
    - D1: Para ver la tendencia macro
    - H4: Para ver estructura institucional
    - H1: Para zonas activas
    - M15/M5: Para BOS/CHoCH y barridas
    - M3/M1: Para confirmar entradas
    
    Esta función obtiene datos de todos estos timeframes desde MT5.
    
    Args:
        symbol: Símbolo a obtener (default: desde config)
    
    Returns:
        Diccionario con DataFrames de cada timeframe:
        {
            "D1": df_d1,
            "H4": df_h4,
            "H1": df_h1,
            "M15": df_m15,
            "M5": df_m5,
            "M3": df_m3,
            "M1": df_m1
        }
    """
    symbol = symbol or MT5_SYMBOL
    
    # Forzar flush antes de imprimir
    sys.stdout.flush()
    sys.stderr.flush()
    
    print(f"📊 Obteniendo datos multi-temporales para {symbol}...", flush=True)
    sys.stdout.flush()
    
    # Timeframes a obtener (de mayor a menor)
    timeframes = ["D1", "H4", "H1", "M15", "M5", "M3", "M1"]
    
    # Número de velas a obtener por timeframe
    # Timeframes mayores necesitan menos velas (ej: D1 solo necesita ~100 días)
    counts = {
        "D1": 100,
        "H4": 200,
        "H1": 300,
        "M15": 500,
        "M5": 500,
        "M3": 500,
        "M1": 500
    }
    
    context = {}
    
    for tf in timeframes:
        df = fetch_candles(symbol, tf, counts.get(tf, 500))
        if df is not None and len(df) > 10:
            context[tf] = df
            print(f"   ✓ {tf}: {len(df)} velas", flush=True)
            sys.stdout.flush()
        else:
            print(f"   ⚠️ {tf}: No se pudieron obtener datos suficientes", flush=True)
            sys.stdout.flush()
    
    print(f"✓ Contexto construido con {len(context)} timeframes", flush=True)
    sys.stdout.flush()
    return context


def calculate_lot_size(balance: float, risk_pct: float, entry_price: float, 
                       stop_loss: float, direction: str, symbol: str = None) -> float:
    """
    Calcula el tamaño de la posición (lotes) basado en el riesgo.
    
    ¿Qué es un lote?
    Un lote es la unidad de trading. Para XAUUSD:
    - 1 lote estándar = 100 onzas de oro
    - 1 mini lote = 10 onzas
    - 1 micro lote = 1 onza
    
    Esta función calcula cuántos lotes puedes operar basado en:
    - Tu balance (cuánto dinero tienes)
    - Tu riesgo por operación (ej: 1% del balance)
    - La distancia al stop loss (cuánto puedes perder)
    - El margen disponible
    
    Args:
        balance: Balance de tu cuenta
        risk_pct: Porcentaje de riesgo (ej: 0.01 = 1%)
        entry_price: Precio de entrada
        stop_loss: Precio de stop loss
        direction: "BUY" o "SELL"
        symbol: Símbolo a operar (para calcular margen)
    
    Returns:
        Tamaño de la posición en lotes
    """
    symbol = symbol or MT5_SYMBOL
    
    # Calcula cuánto dinero estás dispuesto a arriesgar
    risk_amount = balance * risk_pct
    
    # Calcula la distancia al stop loss en puntos
    if direction == "BUY":
        risk_distance = entry_price - stop_loss
    else:  # SELL
        risk_distance = stop_loss - entry_price
    
    if risk_distance <= 0:
        return 0.0
    
    # Obtiene información del símbolo para calcular correctamente
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        # Fallback: usa cálculo básico
        point_value = 1.0
        lot_size = risk_amount / (risk_distance * point_value)
    else:
        # Calcula usando el tick value real del símbolo
        # Para XAUUSD, generalmente 1 lote = 100 onzas
        # El tick value es el valor de 1 tick por lote
        tick_value = symbol_info.trade_tick_value
        tick_size = symbol_info.trade_tick_size
        
        # Calcula cuántos ticks hay en la distancia de riesgo
        ticks_in_risk = risk_distance / tick_size if tick_size > 0 else risk_distance
        
        # Calcula el tamaño de lote basado en el riesgo
        # risk_amount = lot_size * ticks_in_risk * tick_value
        if ticks_in_risk > 0 and tick_value > 0:
            lot_size = risk_amount / (ticks_in_risk * tick_value)
        else:
            # Fallback
            lot_size = risk_amount / risk_distance
    
    # Obtiene información de la cuenta para verificar margen
    account_info = mt5.account_info()
    if account_info:
        margin_free = account_info.margin_free
        
        # Calcula el margen requerido para 1 lote
        if symbol_info:
            margin_required = symbol_info.margin_initial
            if margin_required > 0:
                # Verifica cuántos lotes puedes permitirte con el margen disponible
                max_lots_by_margin = margin_free / margin_required
                # Usa el menor entre el cálculo por riesgo y el disponible por margen
                lot_size = min(lot_size, max_lots_by_margin * 0.9)  # 90% para seguridad
    
    # Redondea según el volumen mínimo del símbolo
    if symbol_info:
        volume_min = symbol_info.volume_min
        volume_step = symbol_info.volume_step
        if volume_step > 0:
            # Redondea al step más cercano
            lot_size = round(lot_size / volume_step) * volume_step
        # Asegura el mínimo
        if lot_size < volume_min:
            lot_size = volume_min
    else:
        # Fallback: redondea a 2 decimales
        lot_size = round(lot_size, 2)
        if lot_size < 0.01:
            lot_size = 0.01
    
    return lot_size


def send_order(direction: str, entry_price: float, stop_loss: float,
              take_profit: float, lot_size: float, symbol: str = None,
              comment: str = "ICT Strategy") -> Optional[int]:
    """
    Envía una orden de trading a MetaTrader 5.
    
    ¿Qué hace esta función?
    Envía una orden al broker para comprar o vender XAUUSD.
    La orden incluye:
    - Dirección (BUY o SELL)
    - Precio de entrada
    - Stop Loss (protección contra pérdidas)
    - Take Profit (objetivo de ganancia)
    - Tamaño de la posición (lotes)
    
    Args:
        direction: "BUY" (compra) o "SELL" (venta)
        entry_price: Precio de entrada deseado
        stop_loss: Precio de stop loss
        take_profit: Precio de take profit (puede ser TP1, TP2 o TP Final)
        lot_size: Tamaño de la posición en lotes
        symbol: Símbolo a operar (default: desde config)
        comment: Comentario para la orden
    
    Returns:
        Ticket de la orden si fue exitosa, None si hubo error
    """
    symbol = symbol or MT5_SYMBOL
    
    # Obtiene información del símbolo
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        print(f"❌ No se pudo obtener información del símbolo {symbol}")
        return None
    
    # Obtiene el precio actual del mercado
    tick = mt5.symbol_info_tick(symbol)
    if tick is None:
        print(f"❌ No se pudo obtener el precio actual de {symbol}")
        return None
    
    # Determina el tipo de orden según la dirección
    if direction == "BUY":
        order_type = mt5.ORDER_TYPE_BUY
        price = tick.ask  # Para comprar, usas el precio ask (precio de venta del broker)
    else:  # SELL
        order_type = mt5.ORDER_TYPE_SELL
        price = tick.bid  # Para vender, usas el precio bid (precio de compra del broker)
    
    # Verifica margen disponible antes de enviar
    account_info = mt5.account_info()
    if account_info:
        margin_free = account_info.margin_free
        
        # Calcula margen requerido para esta operación
        if symbol_info.margin_initial > 0:
            margin_required = lot_size * symbol_info.margin_initial
            
            if margin_required > margin_free:
                print(f"⚠️ Margen insuficiente: Requerido ${margin_required:.2f}, Disponible ${margin_free:.2f}")
                # Intenta reducir el tamaño de lote
                max_lots = (margin_free / symbol_info.margin_initial) * 0.9  # 90% para seguridad
                if max_lots >= symbol_info.volume_min:
                    lot_size = max_lots
                    # Redondea al step
                    if symbol_info.volume_step > 0:
                        lot_size = round(lot_size / symbol_info.volume_step) * symbol_info.volume_step
                    print(f"   Ajustando tamaño a {lot_size:.2f} lotes")
                else:
                    print(f"   ❌ No hay suficiente margen incluso para el lote mínimo")
                    return None
    
    # Prepara la solicitud de orden
    request = {
        "action": mt5.TRADE_ACTION_DEAL,  # Orden de mercado (ejecución inmediata)
        "symbol": symbol,
        "volume": lot_size,
        "type": order_type,
        "price": price,
        "sl": stop_loss,  # Stop Loss
        "tp": take_profit,  # Take Profit
        "deviation": 20,  # Desviación máxima permitida en puntos
        "magic": 234000,  # Número mágico para identificar órdenes del bot
        "comment": comment,
        "type_time": mt5.ORDER_TIME_GTC,  # Good Till Cancel (válida hasta cancelar)
        "type_filling": mt5.ORDER_FILLING_IOC,  # Immediate or Cancel
    }
    
    # Envía la orden
    result = mt5.order_send(request)
    
    if result is None:
        print(f"❌ Error al enviar orden: {mt5.last_error()}")
        return None
    
    # Verifica el resultado
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"❌ Orden rechazada: {result.retcode} - {result.comment}")
        return None
    
    print(f"✅ Orden {direction} ejecutada exitosamente")
    print(f"   Ticket: {result.order}")
    print(f"   Precio: ${price:.2f}")
    print(f"   Lotes: {lot_size}")
    print(f"   SL: ${stop_loss:.2f}")
    print(f"   TP: ${take_profit:.2f}")
    
    return result.order


def get_current_spread(symbol: str = None) -> float:
    """
    Obtiene el spread actual del símbolo.
    
    Args:
        symbol: Símbolo (default: MT5_SYMBOL)
    
    Returns:
        Spread en puntos
    """
    symbol = symbol or MT5_SYMBOL
    tick = mt5.symbol_info_tick(symbol)
    if tick:
        return tick.ask - tick.bid
    return 0.0


def get_atr_ratio(symbol: str = None, period: int = 14, lookback: int = 50) -> float:
    """
    Calcula el ratio ATR actual / ATR promedio.
    
    Args:
        symbol: Símbolo (default: MT5_SYMBOL)
        period: Período para ATR (default: 14)
        lookback: Período para calcular promedio (default: 50)
    
    Returns:
        Ratio ATR (ej: 1.5 significa que ATR actual es 1.5x el promedio)
    """
    symbol = symbol or MT5_SYMBOL
    
    try:
        # Obtiene datos H1 para calcular ATR
        df = fetch_candles(symbol, "H1", lookback + period)
        if df is None or len(df) < lookback + period:
            return 1.0
        
        # Calcula ATR
        from utils.indicators import calculate_atr
        atr = calculate_atr(df['high'], df['low'], df['close'], period)
        
        if len(atr) < 2:
            return 1.0
        
        # ATR actual (último valor)
        current_atr = atr.iloc[-1]
        
        # ATR promedio (últimos lookback valores)
        avg_atr = atr.iloc[-lookback:].mean()
        
        if avg_atr == 0:
            return 1.0
        
        return current_atr / avg_atr
    except Exception as e:
        if logger:
            logger.warning(f"Error al calcular ATR ratio: {e}")
        return 1.0


def update_open_positions(symbol: str = None) -> List[Dict]:
    """
    Obtiene y muestra información de todas las posiciones abiertas.
    
    Esta función te muestra:
    - Cuántas posiciones tienes abiertas
    - El P&L (ganancia/pérdida) de cada una
    - Los niveles de SL y TP
    - El ticket (ID) de cada posición
    
    Args:
        symbol: Símbolo a verificar (None = todos los símbolos)
    
    Returns:
        Lista de diccionarios con información de cada posición
    """
    symbol = symbol or MT5_SYMBOL
    
    # Obtiene todas las posiciones abiertas
    positions = mt5.positions_get(symbol=symbol)
    
    if positions is None:
        error = mt5.last_error()
        error_code = error[0] if error else None
        
        # RES_S_OK significa que no hay posiciones (no es un error)
        if error_code == mt5.RES_S_OK:
            # No hay posiciones abiertas
            return []
        # Error -4 (Terminal: Not found) puede ser temporal, no es crítico
        elif error_code == -4:
            # Error temporal de MT5, intentar de nuevo en el siguiente ciclo
            return []
        else:
            # Otros errores, mostrar solo si son críticos
            if error_code not in [10004]:  # 10004 = No hay posiciones
                print(f"⚠️ Advertencia al obtener posiciones: {error}")
            return []
    
    if len(positions) == 0:
        return []
    
    print(f"\n📊 Posiciones abiertas ({len(positions)}):")
    print("-" * 70)
    
    positions_info = []
    
    for pos in positions:
        # Calcula P&L actual
        current_price = pos.price_current
        profit = pos.profit
        
        position_info = {
            "ticket": pos.ticket,
            "symbol": pos.symbol,
            "type": "BUY" if pos.type == mt5.ORDER_TYPE_BUY else "SELL",
            "volume": pos.volume,
            "entry_price": pos.price_open,
            "current_price": current_price,
            "stop_loss": pos.sl,
            "take_profit": pos.tp,
            "profit": profit,
            "swap": pos.swap,
            "comment": pos.comment
        }
        
        positions_info.append(position_info)
        
        # Muestra información
        direction_str = "📈 BUY" if pos.type == mt5.ORDER_TYPE_BUY else "📉 SELL"
        profit_str = f"${profit:+,.2f}"
        profit_color = "+" if profit >= 0 else ""
        
        print(f"\n{direction_str} | Ticket: {pos.ticket}")
        print(f"   Símbolo: {pos.symbol} | Lotes: {pos.volume}")
        print(f"   Entrada: ${pos.price_open:.2f} | Actual: ${current_price:.2f}")
        print(f"   SL: ${pos.sl:.2f} | TP: ${pos.tp:.2f}")
        print(f"   P&L: {profit_str} | Swap: ${pos.swap:.2f}")
        if pos.comment:
            print(f"   Comentario: {pos.comment}")
    
    print("-" * 70)
    
    return positions_info


def run_auto_trading_loop(analysis_interval: int = 300, update_interval: int = 60):
    """
    Loop principal de trading automático.
    
    Esta es la función principal que ejecuta el bot de trading.
    Hace lo siguiente en un loop infinito:
    1. Obtiene datos del mercado en tiempo real
    2. Ejecuta análisis multi-temporal
    3. Genera señales usando tu estrategia ICT
    4. Si hay señal válida, envía orden al broker
    5. Actualiza información de posiciones abiertas
    6. Gestiona posiciones (break-even, cierres parciales)
    7. Analiza trades cerrados
    8. Espera un tiempo antes de repetir
    
    Args:
        analysis_interval: Segundos entre análisis completos (default: 300 = 5 min)
        update_interval: Segundos entre actualizaciones (default: 60 = 1 min)
    """
    # Forzar flush inmediato y múltiples veces para asegurar que se muestre
    for _ in range(3):
        sys.stdout.flush()
        sys.stderr.flush()
    
    # Inicializar sistema de logging
    if logger:
        logger.info("=" * 70)
        logger.info("🚀 INICIANDO BOT DE TRADING AUTOMÁTICO")
        logger.info("=" * 70)
    
    # Inicializar base de datos
    db = None
    if TradingDatabase:
        try:
            db = TradingDatabase()
            if logger:
                logger.info("✅ Base de datos inicializada")
        except Exception as e:
            print(f"⚠️ No se pudo inicializar base de datos: {e}")
            if logger:
                logger.warning(f"No se pudo inicializar base de datos: {e}")
    
    # Inicializar gestor de posiciones
    position_manager = None
    if PositionManager and db:
        try:
            position_manager = PositionManager(db=db)
            if logger:
                logger.info("✅ Gestor de posiciones inicializado")
        except Exception as e:
            print(f"⚠️ No se pudo inicializar gestor de posiciones: {e}")
            if logger:
                logger.warning(f"No se pudo inicializar gestor de posiciones: {e}")
    
    # Inicializar analizador de trades
    trade_analyzer = None
    if TradeAnalyzer and db:
        try:
            trade_analyzer = TradeAnalyzer(db=db)
            if logger:
                logger.info("✅ Analizador de trades inicializado")
        except Exception as e:
            print(f"⚠️ No se pudo inicializar analizador de trades: {e}")
            if logger:
                logger.warning(f"No se pudo inicializar analizador de trades: {e}")
    
    # Inicializar alertas de Telegram
    telegram = None
    if TelegramAlerts and config_module:
        try:
            telegram_token = getattr(config_module, 'TELEGRAM_BOT_TOKEN', '')
            telegram_chat = getattr(config_module, 'TELEGRAM_CHAT_ID', '')
            if telegram_token and telegram_chat:
                telegram = TelegramAlerts(telegram_token, telegram_chat)
                if logger:
                    logger.info("✅ Alertas de Telegram inicializadas")
            else:
                if logger:
                    logger.info("ℹ️ Telegram no configurado (opcional)")
        except Exception as e:
            print(f"⚠️ No se pudo inicializar Telegram: {e}")
            if logger:
                logger.warning(f"No se pudo inicializar Telegram: {e}")
    
    # Imprimir mensajes iniciales con flush forzado
    print("=" * 70, flush=True)
    sys.stdout.flush()
    print("🚀 INICIANDO BOT DE TRADING AUTOMÁTICO", flush=True)
    sys.stdout.flush()
    print("=" * 70, flush=True)
    sys.stdout.flush()
    
    # 1. Inicializa MT5
    if not init_mt5():
        if logger:
            logger.error("No se pudo inicializar MT5. Abortando.")
        print("❌ No se pudo inicializar MT5. Abortando.", flush=True)
        sys.stdout.flush()
        if db:
            db.close()
        return
    
    # Obtener información de la cuenta para la notificación
    account_info_dict = None
    try:
        account_info = mt5.account_info()
        if account_info:
            account_info_dict = {
                "balance": account_info.balance,
                "equity": account_info.equity,
                "margin_free": account_info.margin_free,
                "leverage": account_info.leverage
            }
    except Exception as e:
        if logger:
            logger.warning(f"No se pudo obtener información de cuenta: {e}")
    
    # Enviar notificación de inicio a Telegram
    if telegram:
        try:
            telegram.send_bot_started(account_info_dict)
            print("✅ Notificación de inicio enviada a Telegram", flush=True)
        except Exception as e:
            print(f"⚠️ No se pudo enviar notificación de inicio: {e}", flush=True)
            if logger:
                logger.warning(f"Error al enviar notificación de inicio: {e}")
    
    # Guardar hora de inicio para calcular uptime
    start_time = datetime.now()
    
    # 2. Inicializa la estrategia
    strategy = ICTHybridStrategy()
    
    # 3. Variables de control
    last_analysis_time = None
    last_signal_time = None
    last_status_time = None
    last_position_check_time = None
    
    print(f"\n⚙️ Configuración:", flush=True)
    sys.stdout.flush()
    print(f"   Símbolo: {MT5_SYMBOL}", flush=True)
    sys.stdout.flush()
    print(f"   Riesgo por operación: {RISK_PER_TRADE*100:.1f}%", flush=True)
    sys.stdout.flush()
    print(f"   Máximo de operaciones simultáneas: {MAX_CONCURRENT_TRADES}", flush=True)
    sys.stdout.flush()
    print(f"   Risk:Reward mínimo: 1:{MIN_RR}", flush=True)
    sys.stdout.flush()
    print(f"   Análisis cada: {analysis_interval}s", flush=True)
    sys.stdout.flush()
    print(f"   Actualización cada: {update_interval}s", flush=True)
    sys.stdout.flush()
    print("\n⚠️ Presiona Ctrl+C para detener el bot", flush=True)
    sys.stdout.flush()
    print("=" * 70 + "\n", flush=True)
    sys.stdout.flush()
    
    try:
        while True:
            current_time = datetime.now()
            
            # Ejecuta análisis multi-temporal periódicamente
            if (last_analysis_time is None or 
                (current_time - last_analysis_time).total_seconds() >= analysis_interval):
                
                # Forzar flush múltiples veces antes de imprimir análisis
                for _ in range(5):
                    sys.stdout.flush()
                    sys.stderr.flush()
                
                # Imprimir línea separadora para que sea más visible
                print("\n" + "=" * 70, flush=True)
                sys.stdout.flush()
                print(f"🔍 Análisis multi-temporal ({current_time.strftime('%H:%M:%S')})...", flush=True)
                sys.stdout.flush()
                print("=" * 70, flush=True)
                sys.stdout.flush()
                
                # ========== NEWS RISK GATE ==========
                # Verifica condiciones de mercado antes de generar señales
                blocked_by_news = False
                news_mode = "NORMAL"
                news_reasons = []
                cooldown_until = None
                
                if NEWS_GATE_AVAILABLE:
                    try:
                        # Obtener eventos del día
                        news_provider = get_news_provider()
                        today_utc = datetime.utcnow().date()
                        events_today = news_provider.get_events_for_day(today_utc)
                        
                        # Calcular métricas de mercado
                        current_spread = get_current_spread(MT5_SYMBOL)
                        atr_ratio = get_atr_ratio(MT5_SYMBOL)
                        open_positions = update_open_positions(MT5_SYMBOL)
                        open_positions_count = len(open_positions)
                        
                        # Calcular drawdown diario
                        daily_dd_pct = 0.0
                        if db:
                            daily_dd_pct = db.get_daily_drawdown_pct()
                        
                        # Configuración para News Gate
                        news_config = {
                            'SPREAD_MAX': SPREAD_MAX,
                            'ATR_MAX_RATIO': ATR_MAX_RATIO,
                            'DAILY_DD_LIMIT': DAILY_DD_LIMIT,
                            'NEWS_USD_WINDOW_MINUTES': NEWS_USD_WINDOW_MINUTES,
                            'NEWS_MIN_EVENTS_FOR_CLUSTER': NEWS_MIN_EVENTS_FOR_CLUSTER,
                            'NEWS_BLOCK_PRE_MINUTES': NEWS_BLOCK_PRE_MINUTES,
                            'NEWS_BLOCK_POST_MINUTES': NEWS_BLOCK_POST_MINUTES,
                            'NEWS_COOLDOWN_MINUTES': NEWS_COOLDOWN_MINUTES,
                            'EIA_BLOCK_PRE_MINUTES': EIA_BLOCK_PRE_MINUTES,
                            'EIA_BLOCK_POST_MINUTES': EIA_BLOCK_POST_MINUTES,
                            'HIGH_NEWS_BLOCK_PRE_MINUTES': HIGH_NEWS_BLOCK_PRE_MINUTES,
                            'HIGH_NEWS_BLOCK_POST_MINUTES': HIGH_NEWS_BLOCK_POST_MINUTES,
                            'HIGH_NEWS_COOLDOWN_MINUTES': HIGH_NEWS_COOLDOWN_MINUTES
                        }
                        
                        # Verificar si se deben bloquear nuevas entradas
                        blocked_by_news, news_mode, news_reasons, cooldown_until = should_block_new_entries(
                            now_utc=datetime.utcnow(),
                            symbol=MT5_SYMBOL,
                            events_today=events_today,
                            spread=current_spread,
                            atr_ratio=atr_ratio,
                            open_positions_count=open_positions_count,
                            daily_dd_pct=daily_dd_pct,
                            config=news_config
                        )
                        
                        # Guardar estado en base de datos
                        if db:
                            try:
                                db.save_bot_state(
                                    symbol=MT5_SYMBOL,
                                    news_mode=news_mode,
                                    blocked=blocked_by_news,
                                    reasons=news_reasons,
                                    cooldown_until_utc=cooldown_until,
                                    spread=current_spread,
                                    atr_ratio=atr_ratio,
                                    daily_dd_pct=daily_dd_pct
                                )
                            except Exception as e:
                                if logger:
                                    logger.warning(f"Error al guardar estado del bot: {e}")
                        
                        # Loggear estado
                        if blocked_by_news:
                            if logger:
                                logger.warning(f"🚫 News Risk Gate: Bloqueado - {', '.join(news_reasons)}")
                            print(f"🚫 News Risk Gate: Modo {news_mode} - Bloqueado", flush=True)
                            for reason in news_reasons:
                                print(f"   ⚠️ {reason}", flush=True)
                        elif news_mode != "NORMAL":
                            if logger:
                                logger.info(f"⚠️ News Risk Gate: Modo {news_mode}")
                            print(f"⚠️ News Risk Gate: Modo {news_mode}", flush=True)
                    except Exception as e:
                        if logger:
                            logger.warning(f"Error en News Risk Gate: {e}")
                        print(f"⚠️ Error en News Risk Gate: {e}", flush=True)
                
                # Si está bloqueado, saltar generación de señales pero continuar gestión
                if blocked_by_news:
                    print("⏸️ Generación de señales pausada (News Risk Gate activo)", flush=True)
                    print("   ✅ Continuando gestión de posiciones abiertas...", flush=True)
                    time.sleep(update_interval)
                    continue
                
                # Construye contexto multi-temporal
                context = build_multitimeframe_context()
                
                if not context or len(context) < 3:
                    print("⚠️ No se pudo construir contexto completo. Esperando...")
                    time.sleep(update_interval)
                    continue
                
                # Genera señal usando la estrategia
                signal = strategy.generate_signal(context)
                
                # Forzar flush después del análisis
                sys.stdout.flush()
                sys.stderr.flush()
                
                # Guarda la señal en la base de datos (aceptada o rechazada)
                if signal:
                    signal_id = None
                    if db:
                        try:
                            # Agrega símbolo si no está
                            if "symbol" not in signal:
                                signal["symbol"] = MT5_SYMBOL
                            signal_id = db.save_signal(signal, status="GENERATED")
                        except Exception as e:
                            if logger:
                                logger.warning(f"Error al guardar señal: {e}")
                    
                    # Envía alerta de Telegram si hay señal
                    if telegram and signal.get("signal") in ["BUY", "SELL"]:
                        try:
                            success = telegram.send_signal_alert(signal)
                            if not success:
                                print(f"⚠️ No se pudo enviar alerta de señal a Telegram", flush=True)
                        except Exception as e:
                            print(f"❌ Error al enviar alerta de señal a Telegram: {e}", flush=True)
                            if logger:
                                logger.warning(f"Error al enviar alerta de Telegram: {e}")
                    
                    if signal["signal"] in ["BUY", "SELL"]:
                        # Forzar flush antes de mostrar señal
                        sys.stdout.flush()
                        sys.stderr.flush()
                        
                        # Verifica Risk:Reward mínimo
                        if signal["risk_reward"] < MIN_RR:
                            if logger:
                                logger.info(f"Señal rechazada: RR {signal['risk_reward']:.2f} < mínimo {MIN_RR}")
                            if db:
                                try:
                                    db.save_signal(signal, status="REJECTED", rejection_reason=f"RR insuficiente: {signal['risk_reward']:.2f}")
                                except:
                                    pass
                            print(f"⚠️ Señal rechazada: RR {signal['risk_reward']:.2f} < mínimo {MIN_RR}", flush=True)
                            sys.stdout.flush()
                        else:
                            # Verifica que no haya demasiadas posiciones abiertas
                            positions = update_open_positions()
                            if len(positions) >= MAX_CONCURRENT_TRADES:
                                if logger:
                                    logger.info(f"Máximo de operaciones alcanzado ({MAX_CONCURRENT_TRADES})")
                                if db:
                                    try:
                                        db.save_signal(signal, status="REJECTED", rejection_reason="Máximo de operaciones alcanzado")
                                    except:
                                        pass
                                print(f"⚠️ Máximo de operaciones alcanzado ({MAX_CONCURRENT_TRADES})", flush=True)
                                sys.stdout.flush()
                            else:
                                # Obtiene balance actual
                                account_info = mt5.account_info()
                                if account_info:
                                    balance = account_info.balance
                                    
                                    # Calcula tamaño de posición
                                    lot_size = calculate_lot_size(
                                        balance=balance,
                                        risk_pct=RISK_PER_TRADE,
                                        entry_price=signal["entry_price"],
                                        stop_loss=signal["stop_loss"],
                                        direction=signal["signal"],
                                        symbol=MT5_SYMBOL
                                    )
                                    
                                    if lot_size >= 0.01:
                                        # Guarda señal como aceptada
                                        if db:
                                            try:
                                                signal_id = db.save_signal(signal, status="ACCEPTED")
                                            except Exception as e:
                                                if logger:
                                                    logger.warning(f"Error al guardar señal aceptada: {e}")
                                        
                                        # Envía orden con TP1 primero
                                        ticket = send_order(
                                            direction=signal["signal"],
                                            entry_price=signal["entry_price"],
                                            stop_loss=signal["stop_loss"],
                                            take_profit=signal["take_profit_1"],  # Empieza con TP1
                                            lot_size=lot_size,
                                            comment=f"ICT Strategy - RR:{signal['risk_reward']:.2f}"
                                        )
                                        
                                        if ticket:
                                            # Guarda el trade en la base de datos
                                            if db:
                                                try:
                                                    db.save_trade(
                                                        ticket=ticket,
                                                        signal=signal,
                                                        lot_size=lot_size,
                                                        entry_price=signal["entry_price"],
                                                        stop_loss=signal["stop_loss"],
                                                        take_profit=signal["take_profit_1"],
                                                        signal_id=signal_id
                                                    )
                                                except Exception as e:
                                                    if logger:
                                                        logger.warning(f"Error al guardar trade: {e}")
                                            
                                            # Envía alerta de Telegram
                                            if telegram:
                                                try:
                                                    success = telegram.send_trade_opened(ticket, signal, lot_size)
                                                    if success:
                                                        print(f"✅ Alerta de Telegram enviada para ticket {ticket}", flush=True)
                                                    else:
                                                        print(f"⚠️ No se pudo enviar alerta de Telegram para ticket {ticket}", flush=True)
                                                        if logger:
                                                            logger.warning(f"Fallo al enviar alerta de Telegram para ticket {ticket}")
                                                except Exception as e:
                                                    print(f"❌ Error al enviar alerta de Telegram: {e}", flush=True)
                                                    if logger:
                                                        logger.error(f"Error al enviar alerta de Telegram: {e}", exc_info=True)
                                            else:
                                                print("⚠️ Telegram no está inicializado - No se envió alerta", flush=True)
                                            
                                            if logger:
                                                logger.info(f"✅ Orden ejecutada: Ticket {ticket} | {signal['signal']} | RR: {signal['risk_reward']:.2f}")
                                            print(f"\n✅ Orden ejecutada exitosamente")
                                            print(f"   Señal: {signal['signal']}")
                                            print(f"   Entrada: ${signal['entry_price']:.2f}")
                                            print(f"   SL: ${signal['stop_loss']:.2f}")
                                            print(f"   TP1: ${signal['take_profit_1']:.2f}")
                                            print(f"   RR: 1:{signal['risk_reward']:.2f}")
                                            if signal.get("justifications"):
                                                print(f"   Razones: {', '.join(signal['justifications'][:2])}")
                                            last_signal_time = current_time
                    else:
                        # Señal HOLD o sin dirección
                        if db:
                            try:
                                db.save_signal(signal, status="REJECTED", rejection_reason="No hay señal clara")
                            except:
                                pass
                else:
                    # No se generó señal
                    if logger:
                        logger.debug("No se generó señal en este análisis")
                
                last_analysis_time = current_time
                last_status_time = current_time
            
            # Gestiona posiciones abiertas (break-even, cierres parciales)
            if position_manager and (last_position_check_time is None or 
                (current_time - last_position_check_time).total_seconds() >= 30):  # Cada 30 segundos
                
                try:
                    # Verifica y gestiona posiciones
                    actions = position_manager.check_and_manage_positions(MT5_SYMBOL)
                    
                    # Detecta posiciones cerradas
                    current_positions = mt5.positions_get(symbol=MT5_SYMBOL)
                    open_tickets = [p.ticket for p in (current_positions or [])]
                    closed_trades = position_manager.check_closed_positions(db, open_tickets)
                    
                    # Envía alertas de Telegram para trades cerrados
                    if telegram and closed_trades:
                        for trade_info in closed_trades:
                            try:
                                telegram.send_trade_closed(
                                    trade_info['ticket'],
                                    trade_info['pnl'],
                                    trade_info['pnl_pct'],
                                    trade_info['exit_reason']
                                )
                            except Exception as e:
                                if logger:
                                    logger.warning(f"Error al enviar alerta de trade cerrado: {e}")
                    
                    # Muestra acciones realizadas
                    for action in actions:
                        print(f"⚙️ {action['action']}: Ticket {action['ticket']}", flush=True)
                        # Envía alerta de Telegram
                        if telegram:
                            try:
                                details = f"SL: ${action.get('new_sl', 0):.2f}" if 'new_sl' in action else ""
                                success = telegram.send_position_update(action['action'], action['ticket'], details)
                                if not success:
                                    print(f"⚠️ No se pudo enviar alerta de posición a Telegram", flush=True)
                            except Exception as e:
                                print(f"❌ Error al enviar alerta de posición a Telegram: {e}", flush=True)
                                if logger:
                                    logger.warning(f"Error al enviar alerta de Telegram: {e}")
                except Exception as e:
                    if logger:
                        logger.warning(f"Error al gestionar posiciones: {e}")
                
                last_position_check_time = current_time
            
            # Actualiza posiciones abiertas periódicamente
            if (last_signal_time is None or 
                (current_time - last_signal_time).total_seconds() >= update_interval):
                update_open_positions()
                last_signal_time = current_time
            
            # Envía reporte de operaciones cada 12 horas
            last_report_time = getattr(run_auto_trading_loop, 'last_report_time', None)
            if db and telegram and (last_report_time is None or 
                (current_time - last_report_time).total_seconds() >= 43200):  # Cada 12 horas (43200 segundos)
                
                try:
                    # Envía reporte detallado de operaciones
                    success = telegram.send_operations_report(db, include_open_positions=True)
                    if success:
                        print(f"✅ Reporte de operaciones enviado a Telegram (cada 12 horas)", flush=True)
                    else:
                        print(f"⚠️ No se pudo enviar reporte de operaciones", flush=True)
                    run_auto_trading_loop.last_report_time = current_time
                except Exception as e:
                    print(f"❌ Error al enviar reporte de operaciones: {e}", flush=True)
                    if logger:
                        logger.warning(f"Error al enviar reporte de operaciones: {e}")
            
            # Muestra métricas de performance cada 5 minutos
            if db and (last_status_time is None or 
                (current_time - last_status_time).total_seconds() >= 300):
                
                try:
                    metrics = db.get_performance_metrics()
                    if metrics["total_trades"] > 0:
                        print(f"\n📊 Métricas de Performance:", flush=True)
                        print(f"   Trades: {metrics['total_trades']} | Win Rate: {metrics['win_rate']:.1f}%", flush=True)
                        print(f"   P&L Total: ${metrics['total_pnl']:.2f} | Profit Factor: {metrics['profit_factor']:.2f}", flush=True)
                        if logger:
                            logger.info(f"Métricas: {metrics['total_trades']} trades | WR: {metrics['win_rate']:.1f}% | PF: {metrics['profit_factor']:.2f}")
                        # Envía métricas a Telegram
                        if telegram:
                            try:
                                success = telegram.send_metrics(metrics)
                                if not success:
                                    print(f"⚠️ No se pudo enviar métricas a Telegram", flush=True)
                            except Exception as e:
                                print(f"❌ Error al enviar métricas a Telegram: {e}", flush=True)
                                if logger:
                                    logger.warning(f"Error al enviar métricas a Telegram: {e}")
                except Exception as e:
                    if logger:
                        logger.warning(f"Error al obtener métricas: {e}")
            
            # Muestra mensaje de estado cada 30 segundos para confirmar que está activo
            if (last_status_time is None or 
                (current_time - last_status_time).total_seconds() >= 30):
                # Forzar flush antes de imprimir estado
                sys.stdout.flush()
                sys.stderr.flush()
                
                if last_analysis_time:
                    seconds_until_next = analysis_interval - (current_time - last_analysis_time).total_seconds()
                    minutes_until = int(seconds_until_next // 60)
                    secs_until = int(seconds_until_next % 60)
                    print(f"⏳ Bot activo - Próximo análisis en {minutes_until}m {secs_until}s ({current_time.strftime('%H:%M:%S')})", flush=True)
                else:
                    print(f"⏳ Bot activo - Esperando primer análisis... ({current_time.strftime('%H:%M:%S')})", flush=True)
                
                # Forzar flush después de imprimir
                sys.stdout.flush()
                sys.stderr.flush()
                last_status_time = current_time
            
            # Forzar flush antes de esperar
            sys.stdout.flush()
            sys.stderr.flush()
            
            # Espera antes de la siguiente iteración
            time.sleep(min(update_interval, 10))
    
    except KeyboardInterrupt:
        stop_reason = "Usuario (Ctrl+C)"
        if logger:
            logger.info("Bot detenido por el usuario")
        print("\n\n⏹️ Deteniendo bot de trading...")
    except Exception as e:
        stop_reason = f"Error: {str(e)}"
        if logger:
            logger.error(f"Error en el loop de trading: {e}", exc_info=True)
        print(f"\n❌ Error en el loop de trading: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Calcular tiempo de actividad
        uptime_str = None
        try:
            if 'start_time' in locals():
                uptime = datetime.now() - start_time
                hours = int(uptime.total_seconds() // 3600)
                minutes = int((uptime.total_seconds() % 3600) // 60)
                seconds = int(uptime.total_seconds() % 60)
                if hours > 0:
                    uptime_str = f"{hours}h {minutes}m {seconds}s"
                elif minutes > 0:
                    uptime_str = f"{minutes}m {seconds}s"
                else:
                    uptime_str = f"{seconds}s"
        except:
            pass
        
        # Enviar notificación de cierre a Telegram
        if telegram:
            try:
                reason = stop_reason if 'stop_reason' in locals() else "Desconocido"
                telegram.send_bot_stopped(reason, uptime_str)
                print("✅ Notificación de cierre enviada a Telegram", flush=True)
            except Exception as e:
                print(f"⚠️ No se pudo enviar notificación de cierre: {e}", flush=True)
                if logger:
                    logger.warning(f"Error al enviar notificación de cierre: {e}")
        # Genera reporte final detallado
        if db:
            try:
                # Obtiene métricas del día
                today_metrics = db.get_performance_metrics(today_only=True)
                
                # Obtiene trades del día
                today_trades = db.get_today_closed_trades()
                
                # Obtiene posiciones abiertas
                open_positions = db.get_open_positions()
                
                # Crea reporte completo
                final_report = {
                    "date": datetime.now().date(),
                    "metrics": today_metrics,
                    "today_trades": today_trades,
                    "open_positions": open_positions
                }
                
                if trade_analyzer:
                    daily_report = trade_analyzer.generate_daily_report()
                    final_report["summary"] = daily_report.get("summary", "")
                
                print(f"\n📊 Reporte Final: {final_report.get('summary', 'Sin datos')}", flush=True)
                
                # Envía reporte detallado a Telegram
                if telegram:
                    try:
                        success = telegram.send_daily_report(final_report)
                        if success:
                            print(f"✅ Reporte diario detallado enviado a Telegram", flush=True)
                        else:
                            print(f"⚠️ No se pudo enviar reporte diario a Telegram", flush=True)
                    except Exception as e:
                        print(f"❌ Error al enviar reporte a Telegram: {e}", flush=True)
                        if logger:
                            logger.warning(f"Error al enviar reporte a Telegram: {e}")
            except Exception as e:
                if logger:
                    logger.warning(f"Error al generar reporte final: {e}")
        
        # Cierra conexión con MT5
        if logger:
            logger.info("Cerrando conexión con MT5")
        print("\n🔌 Cerrando conexión con MT5...")
        mt5.shutdown()
        
        # Cierra base de datos
        if db:
            try:
                db.close()
            except:
                pass
        
        print("✅ Bot detenido")
        if logger:
            logger.info("Bot detenido correctamente")


if __name__ == "__main__":
    # Ejecuta el bot de trading automático
    # analysis_interval: 180 segundos (3 minutos) - Análisis completo más frecuente
    # update_interval: 30 segundos - Actualización de posiciones más frecuente
    run_auto_trading_loop(analysis_interval=180, update_interval=30)


# ============================================================================
# DOCUMENTACIÓN: CÓMO FUNCIONA EL SISTEMA
# ============================================================================
"""
🔵 CÓMO SE CONECTA EL BOT A MT5 (ZEVEN)

1. Inicialización (init_mt5()):
   - Python llama a mt5.initialize() para iniciar la conexión
   - Se conecta usando tus credenciales (login, password, server)
   - Verifica que el símbolo XAUUSD esté disponible
   - Activa el símbolo para trading

2. Obtención de Datos (fetch_candles()):
   - Usa mt5.copy_rates_from_pos() para obtener velas históricas
   - Convierte los datos a DataFrame de pandas
   - Formatea las columnas (open, high, low, close, volume)

3. Construcción del Contexto (build_multitimeframe_context()):
   - Obtiene datos de todos los timeframes necesarios (D1, H4, H1, M15, M5, M3, M1)
   - Cada timeframe se obtiene por separado desde MT5
   - Se combinan en un diccionario para el análisis


🔵 CÓMO SE CONSTRUYE EL CONTEXTO INSTITUCIONAL MULTI-TEMPORAL

1. Análisis por Timeframe:
   - D1: Se ejecuta analyze_D1() para detectar tendencia macro, zonas de liquidez mayor, FVG grandes
   - H4: Se ejecuta analyze_H4() para detectar BOS/CHoCH, acumulación/redistribución, FVG activos
   - H1: Se ejecuta analyze_H1() para aterrizar zonas institucionales activas
   - M15/M5: Se ejecuta analyze_M15_M5() para detectar BOS/CHoCH limpios y barridas
   - M3/M1: Se usa para confirmar entradas tipo sniper

2. Generación de Señal (generate_signal()):
   - Toma el contexto multi-temporal completo
   - Ejecuta find_sniper_entry() que busca:
     * Sweep de liquidez
     * Mitigación de OB o FVG
     * BOS/CHoCH interno
     * Vela institucional con volumen
     * Divergencia RSI (opcional)
   - Retorna una señal estructurada con precios de entrada, SL, TPs


🔵 CÓMO SE GENERA LA SEÑAL CON generate_signal()

La función generate_signal() en la estrategia ICT:
1. Recibe un diccionario con DataFrames de cada timeframe
2. Ejecuta análisis multi-temporal (analyze_D1, analyze_H4, etc.)
3. Busca entrada tipo sniper en M1/M3
4. Verifica confirmaciones (sweep, mitigación, BOS/CHoCH, vela institucional)
5. Calcula niveles de entrada, SL y TPs basados en estructura
6. Retorna diccionario con toda la información de la señal


🔵 CÓMO SE ENVÍA LA ORDEN AUTOMÁTICA

1. Verificación de Condiciones:
   - Risk:Reward >= MIN_RR (default: 1:2)
   - No exceder MAX_CONCURRENT_TRADES
   - Tener suficiente balance

2. Cálculo de Tamaño (calculate_lot_size()):
   - Calcula cuánto dinero arriesgar (balance * RISK_PER_TRADE)
   - Calcula distancia al SL
   - Calcula tamaño de posición en lotes

3. Envío de Orden (send_order()):
   - Prepara solicitud con mt5.order_send()
   - Incluye: dirección, precio, SL, TP, tamaño
   - MT5 ejecuta la orden en el mercado
   - Retorna ticket de la orden si es exitosa


🔵 CÓMO HACER UPGRADE DEL SISTEMA

1. CIERRES PARCIALES:
   - Modifica send_order() para enviar múltiples órdenes
   - Envía orden principal con TP1
   - Cuando se alcanza TP1, modifica la orden para mover SL a BE
   - Envía orden adicional para TP2 con tamaño parcial
   - Repite para TP Final

2. MOVER SL A BREAK EVEN (BE):
   - Usa mt5.order_modify() para modificar órdenes existentes
   - Cuando precio alcanza TP1, mueve SL a precio de entrada
   - Protege la operación de pérdidas

3. PIRAMIDACIÓN:
   - Detecta cuando una operación está en ganancia
   - Envía orden adicional en la misma dirección
   - Usa tamaño menor para la segunda posición
   - Gestiona ambas posiciones independientemente

Ejemplo de código para cierres parciales:
```python
# Cuando se alcanza TP1, cierra parcialmente
if current_price >= tp1:
    # Cierra 50% de la posición
    close_partial_position(ticket, volume=position.volume * 0.5)
    # Mueve SL a break even
    modify_order(ticket, sl=entry_price)
```

Ejemplo para mover SL a BE:
```python
# Modifica orden para mover SL a break even
request = {
    "action": mt5.TRADE_ACTION_SLTP,
    "symbol": symbol,
    "position": ticket,
    "sl": entry_price,  # Mueve SL a precio de entrada
    "tp": current_tp
}
mt5.order_send(request)
```
"""









