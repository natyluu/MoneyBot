# 💰 MoneyBot - Automated Trading Bot

Bot de trading automatizado con integración de MetaTrader 5, estrategia ICT Híbrida y alertas de Telegram.

## 🚀 Características Principales

- ✅ **Integración con MetaTrader 5** - Trading en vivo con MT5
- ✅ **Estrategia ICT Híbrida** - Análisis multi-temporal institucional
- ✅ **Alertas de Telegram** - Notificaciones en tiempo real de señales, trades y reportes
- ✅ **Sistema de Logging Profesional** - Logs rotativos con historial completo
- ✅ **Base de Datos SQLite** - Almacenamiento persistente de trades y métricas
- ✅ **Gestión Avanzada de Posiciones** - SL a break-even, cierres parciales automáticos
- ✅ **Análisis de Trades** - Reportes de performance y análisis post-trade
- ✅ **Reportes Automáticos** - Reportes horarios y diarios vía Telegram

## 📋 Requisitos

- Python 3.8+
- MetaTrader 5 instalado y configurado
- Cuenta de trading en MT5
- Token de bot de Telegram (opcional, para alertas)

## 🔧 Instalación

1. Clona el repositorio:
```bash
git clone git@github.com:natyluu/MoneyBot.git
cd MoneyBot
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

3. Configura el archivo `.env`:
```env
MT5_LOGIN=tu_login
MT5_PASSWORD=tu_password
MT5_SERVER=tu_servidor
MT5_SYMBOL=XAUUSD.vip
RISK_PER_TRADE=0.01
MAX_CONCURRENT_TRADES=3
MIN_RR=1.5
TELEGRAM_BOT_TOKEN=tu_token
TELEGRAM_CHAT_ID=tu_chat_id
```

## 🎯 Uso

### Iniciar el Bot

```bash
python -u live/mt5_trading.py
```

### Verificar Sistema

```bash
python VERIFICAR_SISTEMA_PROFESIONAL.py
```

### Probar Telegram

```bash
python test_telegram.py
```

## 📊 Estrategia ICT Híbrida

La estrategia utiliza análisis multi-temporal:

- **D1**: Tendencia macro, zonas de liquidez mayor
- **H4**: BOS/CHoCH institucionales, estructuras
- **H1**: Zonas institucionales activas
- **M15/M5**: BOS/CHoCH limpios, barridas de liquidez
- **M1/M3**: Confirmación de entrada tipo sniper

### Confirmaciones Requeridas

Para generar una señal, se requieren **mínimo 3 de 5 confirmaciones**:

1. ✅ Sweep de liquidez
2. ✅ Mitigación OB/FVG
3. ✅ BOS/CHoCH interno
4. ✅ Vela institucional
5. ✅ Divergencia RSI (opcional)

## ⚙️ Configuración

### Límites de Trading

- **Máximo de operaciones simultáneas**: 3 (configurable en `.env`)
- **Riesgo por operación**: 1% (configurable en `.env`)
- **Risk:Reward mínimo**: 1:1.5 (configurable en `.env`)

### Frecuencias

- **Análisis completo**: Cada 180 segundos (3 minutos)
- **Actualización de posiciones**: Cada 30 segundos
- **Reportes a Telegram**: Cada hora

## 📱 Alertas de Telegram

El bot envía notificaciones para:

- 🚀 Inicio y cierre del bot
- 📊 Señales generadas
- ✅ Trades ejecutados
- 📉 Trades cerrados
- ⚙️ Actualizaciones de posiciones (SL a BE, cierres parciales)
- 📈 Reportes horarios y diarios
- 📊 Métricas de performance

## 📁 Estructura del Proyecto

```
MoneyBot/
├── live/              # Módulos de trading en vivo
│   ├── mt5_trading.py      # Loop principal del bot
│   ├── telegram_alerts.py  # Sistema de alertas
│   ├── position_manager.py # Gestión de posiciones
│   └── trade_analyzer.py   # Análisis de trades
├── strategy/          # Estrategias de trading
│   └── ict_hybrid_strategy.py
├── utils/             # Utilidades
│   ├── logger.py      # Sistema de logging
│   ├── database.py    # Base de datos SQLite
│   └── indicators.py  # Indicadores técnicos
├── backtest/          # Motor de backtesting
├── data/              # Datos históricos
├── logs/              # Archivos de log
└── config.py          # Configuración centralizada
```

## 🔒 Seguridad

- ⚠️ **NUNCA** subas el archivo `.env` a Git
- ⚠️ Mantén tus credenciales seguras
- ⚠️ Usa cuentas demo para pruebas

## 📝 Licencia

Este proyecto es de uso personal. Úsalo bajo tu propia responsabilidad.

## ⚠️ Advertencia

El trading automatizado conlleva riesgo real de pérdida de capital. Siempre prueba primero en cuenta demo y nunca arriesgues más de lo que puedes permitirte perder.

## 🤝 Contribuciones

Este es un proyecto personal, pero las sugerencias son bienvenidas.

## 📧 Contacto

Para preguntas o soporte, abre un issue en GitHub.

---

**Desarrollado con ❤️ para trading automatizado profesional**
