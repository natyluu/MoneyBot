# Guía de Uso: Backtesting y Trading en Vivo con MT5

Esta guía explica cómo usar el sistema completo de backtesting y trading en vivo conectado a MetaTrader 5.

## 📋 Requisitos Previos

1. **MetaTrader 5 instalado** en tu computadora
2. **Cuenta en Zeven** (recomendado empezar con cuenta DEMO)
3. **Python 3.8+** instalado
4. **Archivos CSV de datos históricos** en la carpeta `data/`

## 🚀 Instalación

### 1. Instalar Dependencias

```bash
pip install -r requirements.txt
```

Esto instalará:
- `pandas` y `numpy` para manejo de datos
- `python-dotenv` para variables de entorno
- `MetaTrader5` para conexión con MT5

### 2. Configurar Credenciales MT5

Crea un archivo `.env` en la raíz del proyecto (copia desde `.env.example`):

```bash
cp .env.example .env
```

Edita `.env` con tus credenciales:

```env
MT5_LOGIN=1234567
MT5_PASSWORD=tu_password
MT5_SERVER=ZevenGlobal-Demo
MT5_SYMBOL=XAUUSD
RISK_PER_TRADE=0.01
MAX_CONCURRENT_TRADES=3
MIN_RR=2.0
```

**⚠️ IMPORTANTE:**
- NUNCA subas el archivo `.env` a Git (está en `.gitignore`)
- Usa cuenta DEMO primero para probar
- Verifica el nombre exacto del símbolo en MT5 (puede ser `XAUUSD` o `XAUUSD.m`)

## 📊 Backtesting

### Preparar Datos Históricos

Coloca archivos CSV en la carpeta `data/` con formato:
- `XAUUSD_1d.csv` (diario)
- `XAUUSD_4h.csv` (4 horas)
- `XAUUSD_1h.csv` (1 hora)
- `XAUUSD_15m.csv` (15 minutos)
- `XAUUSD_5m.csv` (5 minutos)
- `XAUUSD_3m.csv` (3 minutos)
- `XAUUSD_1m.csv` (1 minuto)

Cada CSV debe tener columnas: `timestamp,open,high,low,close,volume`

### Ejecutar Backtest

```bash
python backtest/backtest.py
```

O desde Python:

```python
from backtest.backtest import (
    load_multi_timeframe_data,
    synchronize_timeframes,
    run_backtest,
    print_backtest_summary
)

# 1. Carga datos
data_dict = load_multi_timeframe_data("XAUUSD")

# 2. Sincroniza timeframes
synced_data = synchronize_timeframes(data_dict, base_timeframe="M1")

# 3. Ejecuta backtest
results = run_backtest(
    synced_data,
    initial_capital=10000,
    risk_per_trade=0.01,  # 1% de riesgo
    commission=0.0001     # 0.01% de comisión
)

# 4. Muestra resultados
print_backtest_summary(results)
```

### Resultados del Backtest

El backtest mostrará:
- **Capital**: Inicial, final, retorno total
- **Operaciones**: Total, ganadoras, perdedoras, winrate
- **Métricas**: Profit Factor, Max Drawdown, Risk:Reward promedio
- **Detalles**: Lista de todas las operaciones

## 🔴 Trading en Vivo con MT5

### 1. Verificar Conexión

Antes de ejecutar el bot, verifica que MT5 esté abierto y conectado:

```python
from live.mt5_trading import init_mt5

if init_mt5():
    print("✅ Conexión exitosa")
else:
    print("❌ Error de conexión")
```

### 2. Ejecutar Bot de Trading

```bash
python live/mt5_trading.py
```

O desde Python:

```python
from live.mt5_trading import run_auto_trading_loop

# Inicia el bot
run_auto_trading_loop(
    analysis_interval=300,  # Análisis cada 5 minutos
    update_interval=60       # Actualización cada 1 minuto
)
```

### 3. Qué Hace el Bot

El bot automáticamente:
1. **Obtiene datos** del mercado en tiempo real desde MT5
2. **Ejecuta análisis** multi-temporal (D1, H4, H1, M15, M5, M3, M1)
3. **Genera señales** usando la estrategia ICT
4. **Verifica condiciones** (RR mínimo, máximo de operaciones, etc.)
5. **Envía órdenes** automáticamente al broker
6. **Gestiona posiciones** (muestra P&L, SL, TP)

### 4. Detener el Bot

Presiona `Ctrl+C` para detener el bot de forma segura.

## ⚙️ Configuración Avanzada

### Ajustar Riesgo por Operación

En `.env`:
```env
RISK_PER_TRADE=0.02  # 2% de riesgo por operación
```

### Cambiar Risk:Reward Mínimo

En `.env`:
```env
MIN_RR=2.5  # Requiere mínimo 1:2.5
```

### Límite de Operaciones Simultáneas

En `.env`:
```env
MAX_CONCURRENT_TRADES=5  # Máximo 5 operaciones a la vez
```

## 📝 Funciones Principales

### Backtesting

- `load_multi_timeframe_data()`: Carga CSV de múltiples timeframes
- `synchronize_timeframes()`: Sincroniza timeframes para análisis
- `run_backtest()`: Ejecuta el backtest completo
- `print_backtest_summary()`: Muestra resultados

### Trading MT5

- `init_mt5()`: Inicializa conexión con MT5
- `fetch_candles()`: Obtiene velas desde MT5
- `build_multitimeframe_context()`: Construye contexto multi-temporal
- `calculate_lot_size()`: Calcula tamaño de posición
- `send_order()`: Envía orden al broker
- `update_open_positions()`: Muestra posiciones abiertas
- `run_auto_trading_loop()`: Loop principal de trading

## ⚠️ Advertencias Importantes

1. **Siempre prueba en DEMO primero**
   - Usa cuenta demo durante al menos 1-2 semanas
   - Valida que el bot funcione correctamente
   - Ajusta parámetros según resultados

2. **Gestión de Riesgo**
   - No arriesgues más del 1-2% por operación
   - Usa stop loss siempre
   - No operes con dinero que no puedas perder

3. **Monitoreo**
   - Revisa el bot regularmente
   - Verifica que las órdenes se ejecuten correctamente
   - Ajusta parámetros según condiciones de mercado

4. **Backtesting vs Real**
   - Los resultados de backtesting no garantizan resultados futuros
   - El mercado real tiene slippage, spreads, y latencia
   - Siempre hay riesgo de pérdida

## 🔧 Solución de Problemas

### Error: "No se pudo inicializar MT5"
- Verifica que MetaTrader 5 esté instalado y abierto
- Asegúrate de tener permisos de administrador si es necesario

### Error: "Símbolo no encontrado"
- Verifica el nombre exacto del símbolo en MT5
- Puede ser `XAUUSD` o `XAUUSD.m`
- Activa el símbolo en MT5 (clic derecho → Mostrar)

### Error: "Orden rechazada"
- Verifica que tengas suficiente margen
- Revisa que el símbolo esté disponible para trading
- Verifica que los precios SL/TP sean válidos

### No se generan señales
- Verifica que tengas datos suficientes de todos los timeframes
- Revisa que la estrategia tenga las confirmaciones necesarias
- Ajusta `MIN_RR` si es muy restrictivo

## 📚 Próximos Pasos

1. **Cierres Parciales**: Modifica `send_order()` para cerrar parcialmente en TP1
2. **Mover SL a BE**: Implementa lógica para mover stop loss a break even
3. **Piramidación**: Agrega lógica para agregar a posiciones ganadoras
4. **Notificaciones**: Integra alertas (email, Telegram, etc.)
5. **Dashboard**: Crea interfaz web para monitoreo

## 📞 Soporte

Para más información, consulta:
- `backtest/backtest.py` - Código del backtesting
- `live/mt5_trading.py` - Código del trading en vivo
- Documentación de MetaTrader 5: https://www.mql5.com/en/docs













