# 📚 MANUAL COMPLETO DEL BOT - MoneyBot

## Guía Completa de Estructura y Funcionalidad

---

## 📁 ESTRUCTURA GENERAL DEL PROYECTO

```
MoneyBot/
├── 📂 live/                    # Trading en tiempo real
├── 📂 strategy/                # Estrategias de trading
├── 📂 utils/                   # Utilidades y herramientas
├── 📂 backtest/                # Motor de backtesting
├── 📂 data/                     # Datos históricos y base de datos
├── 📂 logs/                     # Archivos de log
├── 📄 config.py                 # Configuración centralizada
├── 📄 .env                      # Credenciales (NO se sube a Git)
├── 📄 requirements.txt          # Dependencias Python
└── 📄 README.md                 # Documentación principal
```

---

## 📂 CARPETA: `live/` - Trading en Tiempo Real

**Propósito:** Contiene todos los módulos necesarios para operar en vivo con MetaTrader 5.

### 📄 `mt5_trading.py` - **ARCHIVO PRINCIPAL DEL BOT**

**Función:** Es el corazón del bot. Ejecuta el loop principal de trading.

**¿Qué hace?**
- ✅ Conecta con MetaTrader 5
- ✅ Obtiene datos de mercado en tiempo real
- ✅ Ejecuta la estrategia cada 3 minutos
- ✅ Genera señales de trading
- ✅ Ejecuta órdenes BUY/SELL automáticamente
- ✅ Gestiona posiciones abiertas cada 30 segundos
- ✅ Envía alertas a Telegram
- ✅ Guarda todo en la base de datos

**Cómo ejecutarlo:**
```bash
python -u live/mt5_trading.py
```

**Frecuencias:**
- Análisis completo: Cada 180 segundos (3 minutos)
- Actualización de posiciones: Cada 30 segundos
- Reportes a Telegram: Cada hora

---

### 📄 `position_manager.py` - Gestor de Posiciones

**Función:** Gestiona las posiciones abiertas automáticamente.

**¿Qué hace?**
- ✅ Monitorea posiciones abiertas cada 30 segundos
- ✅ Mueve Stop Loss a Break-Even cuando alcanza 80% del TP1
- ✅ Ejecuta cierres parciales automáticos:
  - 50% de la posición al alcanzar TP1
  - 25% adicional al alcanzar TP2
- ✅ Detecta cuando una posición se cierra
- ✅ Actualiza la base de datos con cambios

**Funciones principales:**
- `check_closed_positions()`: Detecta posiciones cerradas
- `update_positions()`: Actualiza SL a break-even y cierres parciales
- `move_sl_to_breakeven()`: Mueve SL al precio de entrada

---

### 📄 `telegram_alerts.py` - Sistema de Alertas

**Función:** Envía notificaciones a Telegram sobre todas las actividades del bot.

**¿Qué notifica?**
- 🚀 **Inicio del bot**: Cuando el bot se inicia (con info de cuenta)
- 👤 **Cierre del bot**: Cuando el bot se detiene (con razón y uptime)
- 📊 **Señales generadas**: Cuando se detecta una oportunidad de trading
- ✅ **Trades ejecutados**: Cuando se abre una posición
- 📉 **Trades cerrados**: Cuando se cierra una posición (con P&L)
- ⚙️ **Actualizaciones**: SL a BE, cierres parciales
- 📈 **Reportes horarios**: Métricas cada hora
- 📊 **Reportes diarios**: Resumen completo del día

**Funciones principales:**
- `send_bot_started()`: Notifica inicio del bot
- `send_bot_stopped()`: Notifica cierre del bot
- `send_signal()`: Envía señal de trading
- `send_trade_opened()`: Notifica trade abierto
- `send_trade_closed()`: Notifica trade cerrado
- `send_daily_report()`: Envía reporte diario
- `send_operations_report()`: Envía reporte de operaciones

**Configuración:**
- Requiere `TELEGRAM_BOT_TOKEN` y `TELEGRAM_CHAT_ID` en `.env`
- Puede ser un chat individual o un grupo

---

### 📄 `trade_analyzer.py` - Analizador de Trades

**Función:** Analiza el performance de los trades cerrados.

**¿Qué analiza?**
- 📊 Métricas de performance (win rate, profit factor, etc.)
- 📈 Análisis de trades ganadores vs perdedores
- 📉 Drawdown máximo
- 💰 P&L total y promedio
- 📊 Risk:Reward promedio

**Funciones principales:**
- `generate_daily_report()`: Genera reporte diario completo
- `analyze_trade()`: Analiza un trade individual
- `get_performance_metrics()`: Obtiene métricas generales

---

### 📄 `paper_trader.py` - Simulador de Trading

**Función:** Simula operaciones sin riesgo real (para pruebas).

**¿Qué hace?**
- ✅ Simula operaciones sin usar dinero real
- ✅ Calcula P&L teórico
- ✅ Permite probar estrategias sin riesgo

**Uso:** Principalmente para desarrollo y pruebas.

---

### 📄 `ict_live_trader.py` - Trader ICT Específico

**Función:** Implementación específica para estrategia ICT (versión alternativa).

**Uso:** Versión alternativa del trader, puede usarse en lugar de `mt5_trading.py`.

---

### 📄 `live_trader.py` - Trader Genérico

**Función:** Clase base para traders en vivo.

**Uso:** Base para implementaciones específicas.

---

### 📄 `alert_system.py` - Sistema de Alertas Genérico

**Función:** Sistema base de alertas (puede usarse para otros canales además de Telegram).

---

## 📂 CARPETA: `strategy/` - Estrategias de Trading

**Propósito:** Contiene todas las estrategias de trading implementadas.

### 📄 `ict_hybrid_strategy.py` - **ESTRATEGIA PRINCIPAL**

**Función:** Implementa la estrategia ICT Híbrida multi-temporal.

**¿Cómo funciona?**

1. **Análisis Multi-Temporal:**
   - **D1**: Detecta tendencia macro, zonas de liquidez mayor, FVG grandes
   - **H4**: Detecta BOS/CHoCH institucionales, acumulación/redistribución
   - **H1**: Valida zonas institucionales activas
   - **M15/M5**: Detecta BOS/CHoCH limpios, barridas de liquidez
   - **M1/M3**: Confirma entrada tipo sniper

2. **Confirmaciones Requeridas (mínimo 3 de 5):**
   - ✅ Sweep de liquidez
   - ✅ Mitigación de OB o FVG
   - ✅ BOS/CHoCH interno
   - ✅ Vela institucional con volumen
   - ✅ Divergencia RSI (opcional)

3. **Generación de Señal:**
   - Analiza todos los timeframes
   - Busca confluencias
   - Calcula niveles de entrada, SL y TPs
   - Retorna señal estructurada

**Funciones principales:**
- `generate_signal()`: Genera señal de trading
- `analyze_D1()`: Análisis diario
- `analyze_H4()`: Análisis de 4 horas
- `analyze_H1()`: Análisis de 1 hora
- `analyze_M15_M5()`: Análisis de 15 y 5 minutos
- `find_sniper_entry()`: Busca entrada tipo sniper

---

### 📄 `ict_utils.py` - Utilidades ICT

**Función:** Funciones auxiliares para análisis ICT.

**Contiene:**
- `detect_swings()`: Detecta puntos de swing
- `detect_bos_choch()`: Detecta cambios de estructura
- `detect_liquidity_sweeps()`: Detecta barridas de liquidez
- `detect_fair_value_gaps()`: Detecta FVG
- `detect_order_blocks()`: Detecta Order Blocks
- `detect_mitigation_blocks()`: Detecta mitigaciones
- Y muchas más funciones de análisis ICT

---

### 📄 `base_strategy.py` - Clase Base de Estrategia

**Función:** Clase abstracta base para todas las estrategias.

**Uso:** Define la interfaz que deben implementar todas las estrategias.

---

### 📄 `moving_average_strategy.py` - Estrategia de Medias Móviles

**Función:** Estrategia alternativa basada en medias móviles.

**Uso:** Estrategia de ejemplo/alternativa.

---

### 📄 `example_ict_usage.py` - Ejemplo de Uso ICT

**Función:** Ejemplos de cómo usar la estrategia ICT.

**Uso:** Referencia y aprendizaje.

---

## 📂 CARPETA: `utils/` - Utilidades

**Propósito:** Herramientas y funciones auxiliares usadas en todo el proyecto.

### 📄 `database.py` - Base de Datos SQLite

**Función:** Gestiona la base de datos SQLite para almacenar datos históricos.

**¿Qué almacena?**
- 📊 **Señales generadas**: Todas las señales que genera el bot
- 💼 **Trades ejecutados**: Todas las operaciones abiertas y cerradas
- 📈 **Posiciones abiertas**: Estado actual de posiciones
- 📊 **Métricas diarias**: Performance por día

**Tablas:**
- `signals`: Señales generadas
- `trades`: Trades ejecutados
- `positions`: Posiciones abiertas
- `daily_metrics`: Métricas diarias

**Funciones principales:**
- `save_signal()`: Guarda una señal
- `save_trade()`: Guarda un trade
- `save_position()`: Guarda una posición
- `update_position()`: Actualiza una posición
- `close_trade()`: Cierra un trade
- `get_performance_metrics()`: Obtiene métricas
- `get_today_trades()`: Obtiene trades del día
- `get_open_positions()`: Obtiene posiciones abiertas

**Ubicación de la BD:** `data/trading_bot.db`

---

### 📄 `logger.py` - Sistema de Logging

**Función:** Sistema profesional de logging con rotación de archivos.

**¿Qué hace?**
- ✅ Registra todos los eventos del bot
- ✅ Crea archivos de log rotativos (máximo 10MB, 7 backups)
- ✅ Muestra logs en consola y archivo
- ✅ Formato estructurado con timestamps

**Niveles de log:**
- `DEBUG`: Información detallada
- `INFO`: Información general
- `WARNING`: Advertencias
- `ERROR`: Errores
- `CRITICAL`: Errores críticos

**Ubicación de logs:** `logs/bot_YYYYMMDD.log`

---

### 📄 `indicators.py` - Indicadores Técnicos

**Función:** Implementa indicadores técnicos usados en las estrategias.

**Indicadores incluidos:**
- RSI (Relative Strength Index)
- Medias móviles
- Y otros indicadores comunes

---

### 📄 `data_loader.py` - Cargador de Datos

**Función:** Carga datos históricos desde archivos o APIs.

**Uso:** Para backtesting y análisis histórico.

---

### 📄 `multi_timeframe_loader.py` - Cargador Multi-Temporal

**Función:** Carga datos de múltiples timeframes simultáneamente.

**Uso:** Para análisis multi-temporal.

---

### 📄 `generate_sample_data.py` - Generador de Datos de Prueba

**Función:** Genera datos de ejemplo para pruebas.

**Uso:** Desarrollo y testing.

---

## 📂 CARPETA: `backtest/` - Motor de Backtesting

**Propósito:** Permite probar estrategias con datos históricos sin riesgo.

### 📄 `backtest_engine.py` - Motor de Backtesting

**Función:** Motor principal para ejecutar backtests.

**¿Qué hace?**
- ✅ Simula operaciones con datos históricos
- ✅ Calcula métricas de performance
- ✅ Genera reportes de resultados

---

### 📄 `ict_backtest_engine.py` - Motor de Backtesting ICT

**Función:** Motor específico para backtesting de estrategia ICT.

---

### 📄 `backtest.py` - Backtest Genérico

**Función:** Implementación genérica de backtesting.

---

### 📄 `run_backtest.py` - Ejecutor de Backtest

**Función:** Script para ejecutar backtests fácilmente.

**Uso:**
```bash
python backtest/run_backtest.py
```

---

### 📄 `run_ict_backtest.py` - Ejecutor de Backtest ICT

**Función:** Script específico para ejecutar backtests de estrategia ICT.

---

## 📂 CARPETA: `data/` - Datos

**Propósito:** Almacena datos históricos y la base de datos.

**Contenido:**
- `trading_bot.db`: Base de datos SQLite con trades y señales
- Archivos CSV con datos históricos (opcional)

**Nota:** Esta carpeta puede contener datos sensibles. Los archivos `.db` están en `.gitignore`.

---

## 📂 CARPETA: `logs/` - Logs

**Propósito:** Almacena archivos de log del bot.

**Contenido:**
- `bot_YYYYMMDD.log`: Archivos de log diarios
- Rotación automática (máximo 7 días)

**Nota:** Los archivos `.log` están en `.gitignore`.

---

## 📄 ARCHIVOS EN LA RAÍZ

### 📄 `config.py` - Configuración Centralizada

**Función:** Archivo central de configuración.

**¿Qué contiene?**
- Credenciales de MT5 (cargadas desde `.env`)
- Configuración de riesgo
- Configuración de Telegram
- Parámetros de la estrategia

**Variables principales:**
- `MT5_LOGIN`: Número de cuenta MT5
- `MT5_PASSWORD`: Contraseña MT5
- `MT5_SERVER`: Servidor MT5 (Demo o Live)
- `MT5_SYMBOL`: Símbolo a operar (ej: XAUUSD.vip)
- `RISK_PER_TRADE`: Riesgo por operación (ej: 0.01 = 1%)
- `MAX_CONCURRENT_TRADES`: Máximo de operaciones simultáneas
- `MIN_RR`: Risk:Reward mínimo requerido
- `TELEGRAM_BOT_TOKEN`: Token del bot de Telegram
- `TELEGRAM_CHAT_ID`: ID del chat/grupo de Telegram

---

### 📄 `.env` - Credenciales (NO SE SUBE A GIT)

**Función:** Almacena credenciales sensibles de forma segura.

**Contenido:**
```env
MT5_LOGIN=94342
MT5_PASSWORD=TuContraseña
MT5_SERVER=ZevenGlobal-Live
MT5_SYMBOL=XAUUSD.vip
RISK_PER_TRADE=0.01
MAX_CONCURRENT_TRADES=3
MIN_RR=1.5
TELEGRAM_BOT_TOKEN=tu_token
TELEGRAM_CHAT_ID=tu_chat_id
```

**⚠️ IMPORTANTE:**
- ❌ NUNCA se sube a Git (está en `.gitignore`)
- ✅ Debes crearlo manualmente en cada máquina
- ✅ Usa scripts `CREAR_ENV_EN_VPS.bat` o `CREAR_ENV_EN_VPS.ps1` en Windows

---

### 📄 `requirements.txt` - Dependencias Python

**Función:** Lista todas las librerías necesarias para el bot.

**Contenido:**
```
MetaTrader5>=5.0.45
pandas>=2.0.0
numpy>=1.24.0
python-dotenv>=1.0.0
requests>=2.31.0
```

**Instalación:**
```bash
pip install -r requirements.txt
```

---

### 📄 `README.md` - Documentación Principal

**Función:** Documentación general del proyecto.

**Contenido:**
- Descripción del bot
- Características principales
- Instrucciones de instalación
- Guía de uso básica

---

## 🔄 FLUJO DE FUNCIONAMIENTO DEL BOT

### 1. Inicio del Bot

```
1. Se ejecuta: python -u live/mt5_trading.py
2. Carga config.py → Lee .env
3. Conecta a MT5 (init_mt5())
4. Inicializa base de datos
5. Inicializa logger
6. Inicializa Telegram
7. Envía notificación de inicio a Telegram
8. Inicia loop principal
```

### 2. Loop Principal (Cada 3 minutos)

```
1. Obtiene datos multi-temporal de MT5
2. Construye contexto multi-temporal
3. Ejecuta estrategia ICT (generate_signal())
4. Si hay señal válida:
   - Verifica condiciones (RR, límites, margen)
   - Calcula tamaño de lote
   - Ejecuta orden en MT5
   - Guarda en base de datos
   - Envía alerta a Telegram
5. Continúa al siguiente ciclo
```

### 3. Gestión de Posiciones (Cada 30 segundos)

```
1. Obtiene posiciones abiertas de MT5
2. Para cada posición:
   - Verifica si alcanzó 80% del TP1 → Mueve SL a BE
   - Verifica si alcanzó TP1 → Cierra 50% parcial
   - Verifica si alcanzó TP2 → Cierra 25% adicional
   - Actualiza base de datos
3. Detecta posiciones cerradas
4. Envía alertas a Telegram
```

### 4. Reportes (Cada hora)

```
1. Genera reporte de operaciones
2. Calcula métricas de performance
3. Envía reporte a Telegram
```

---

## 🎯 CONFIGURACIÓN DE LÍMITES

### Límites de Trading

- **Máximo de operaciones simultáneas**: 3 (configurable en `.env`)
- **Riesgo por operación**: 1% del balance (configurable en `.env`)
- **Risk:Reward mínimo**: 1:1.5 (configurable en `.env`)

### Confirmaciones Requeridas

- **Mínimo de confirmaciones**: 3 de 5 posibles
- **Confirmaciones disponibles**:
  1. Sweep de liquidez
  2. Mitigación OB/FVG
  3. BOS/CHoCH interno
  4. Vela institucional
  5. Divergencia RSI

---

## 📊 BASE DE DATOS

### Tabla: `signals`

Almacena todas las señales generadas por el bot.

**Campos:**
- `id`: ID único
- `timestamp`: Fecha y hora
- `symbol`: Símbolo (ej: XAUUSD)
- `direction`: BUY o SELL
- `entry_price`: Precio de entrada
- `stop_loss`: Stop Loss
- `take_profit_1`, `take_profit_2`, `take_profit_final`: Take Profits
- `risk_reward`: Ratio Risk:Reward
- `confirmations`: Número de confirmaciones
- `status`: GENERATED, ACCEPTED, REJECTED
- `rejection_reason`: Razón de rechazo (si aplica)

### Tabla: `trades`

Almacena todas las operaciones ejecutadas.

**Campos:**
- `id`: ID único
- `signal_id`: ID de la señal relacionada
- `ticket`: Ticket de MT5
- `symbol`: Símbolo
- `direction`: BUY o SELL
- `entry_time`, `exit_time`: Fechas
- `entry_price`, `exit_price`: Precios
- `lot_size`: Tamaño en lotes
- `stop_loss`, `take_profit`: SL y TP
- `pnl`, `pnl_pct`: Ganancia/pérdida
- `exit_reason`: Razón de cierre

### Tabla: `positions`

Almacena posiciones abiertas actuales.

**Campos:**
- `id`: ID único
- `trade_id`: ID del trade relacionado
- `ticket`: Ticket de MT5
- `symbol`: Símbolo
- `direction`: BUY o SELL
- `entry_time`, `entry_price`: Entrada
- `lot_size`: Tamaño
- `stop_loss`, `take_profit`: SL y TP
- `current_price`: Precio actual
- `unrealized_pnl`: P&L no realizado
- `sl_moved_to_be`: Si el SL ya se movió a BE
- `partial_close_1`, `partial_close_2`: Si ya se hicieron cierres parciales

### Tabla: `daily_metrics`

Almacena métricas diarias de performance.

**Campos:**
- `date`: Fecha
- `total_signals`: Total de señales
- `accepted_signals`: Señales aceptadas
- `rejected_signals`: Señales rechazadas
- `trades_opened`: Trades abiertos
- `trades_closed`: Trades cerrados
- `total_pnl`: P&L total
- `win_rate`: Tasa de acierto
- `profit_factor`: Factor de ganancia
- `max_drawdown`: Drawdown máximo
- `avg_risk_reward`: Risk:Reward promedio

---

## 🔧 COMANDOS ÚTILES

### Verificar Sistema

```bash
python VERIFICAR_SISTEMA_PROFESIONAL.py
```

### Probar Conexión MT5

```bash
python test_mt5_connection.py
```

### Probar Telegram

```bash
python test_telegram.py
```

### Iniciar el Bot

```bash
python -u live/mt5_trading.py
```

### Ver Logs en Tiempo Real

```bash
tail -f logs/bot_$(date +%Y%m%d).log
```

---

## 📱 TELEGRAM

### Configuración

1. Crea un bot con [@BotFather](https://t.me/BotFather)
2. Obtén el token del bot
3. Crea un grupo o usa un chat individual
4. Obtén el Chat ID (puede ser negativo para grupos)
5. Agrega ambos al `.env`

### Comandos para Obtener Chat ID

```bash
# Enviar mensaje al bot, luego:
curl https://api.telegram.org/bot<TU_TOKEN>/getUpdates
```

---

## ⚠️ SEGURIDAD

### Archivos que NUNCA se suben a Git

- `.env`: Credenciales
- `ENV_VPS_COPIA.txt`: Copia de credenciales
- `data/*.db`: Base de datos
- `logs/*.log`: Logs
- `__pycache__/`: Caché de Python

### Mejores Prácticas

1. ✅ Usa cuenta DEMO para pruebas
2. ✅ Nunca subas `.env` a Git
3. ✅ Mantén tus credenciales seguras
4. ✅ Revisa los logs regularmente
5. ✅ Monitorea las operaciones en Telegram

---

## 🐛 SOLUCIÓN DE PROBLEMAS

### El bot no se conecta a MT5

1. Verifica que MT5 esté abierto
2. Verifica credenciales en `.env`
3. Ejecuta `python test_mt5_connection.py`

### No se envían alertas a Telegram

1. Verifica `TELEGRAM_BOT_TOKEN` y `TELEGRAM_CHAT_ID` en `.env`
2. Envía un mensaje al bot primero (para iniciar conversación)
3. Ejecuta `python test_telegram.py`

### El bot no ejecuta operaciones

1. Verifica que haya señales válidas (mínimo 3 confirmaciones)
2. Verifica límites (MAX_CONCURRENT_TRADES)
3. Verifica margen disponible
4. Verifica Risk:Reward mínimo (MIN_RR)

---

## 📚 RECURSOS ADICIONALES

- **README.md**: Documentación general
- **README_MT5.md**: Guía específica de MT5
- **README_LIVE.md**: Documentación de módulos live
- **README_ICT.md**: Documentación de estrategia ICT
- **README_BACKTEST.md**: Documentación de backtesting

---

## 🎓 GLOSARIO

- **BOS**: Break of Structure (Ruptura de Estructura)
- **CHoCH**: Change of Character (Cambio de Carácter)
- **FVG**: Fair Value Gap (Gap de Valor Justo)
- **OB**: Order Block (Bloque de Órdenes)
- **SL**: Stop Loss
- **TP**: Take Profit
- **BE**: Break Even (Punto de equilibrio)
- **RR**: Risk:Reward (Riesgo:Recompensa)
- **P&L**: Profit and Loss (Ganancia y Pérdida)

---

**Última actualización:** 2025-01-15

**Versión del Bot:** 1.0

---

¿Tienes preguntas sobre alguna parte específica del bot? Revisa la documentación o abre un issue en GitHub.






