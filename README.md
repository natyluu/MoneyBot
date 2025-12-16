# 🤖 Bot de Trading Algorítmico - Estrategia ICT Híbrida

Proyecto completo para backtesting y trading en vivo de estrategias algorítmicas, especializado en estrategias institucionales ICT (Inner Circle Trader) para XAUUSD.

## 🎯 Características Principales

- ✅ **Estrategia ICT Híbrida 2022**: Análisis multi-temporal completo (D1, H4, H1, M15/M5, M1/M3)
- ✅ **Backtesting Avanzado**: Motor especializado para estrategias multi-temporales con métricas completas
- ✅ **Trading en Vivo con MT5**: Integración completa con MetaTrader 5 para trading automático
- ✅ **Paper Trading**: Simulación de trading sin riesgo real
- ✅ **Sistema de Alertas**: Múltiples canales (consola, archivo, webhook, email)
- ✅ **Detección Institucional**: BOS/CHoCH, Order Blocks, Fair Value Gaps, Liquidity Sweeps

## 📁 Estructura del Proyecto

```
trading-bot/
├── data/                      # Datos históricos (CSV)
│   └── README.md             # Instrucciones para datos
├── strategy/                  # Estrategias de trading
│   ├── ict_hybrid_strategy.py # Estrategia ICT Híbrida 2022 (PRINCIPAL)
│   ├── ict_utils.py           # Utilidades ICT (BOS, CHoCH, FVG, OB, etc.)
│   ├── base_strategy.py       # Clase base para estrategias
│   └── README_ICT.md          # Documentación estrategia ICT
├── backtest/                  # Motor de backtesting
│   ├── backtest.py            # Backtest multi-temporal completo
│   ├── ict_backtest_engine.py # Motor especializado para ICT
│   ├── run_ict_backtest.py    # Script para ejecutar backtests ICT
│   └── README_BACKTEST.md     # Documentación backtesting
├── live/                      # Trading en vivo
│   ├── mt5_trading.py         # Trading automático con MT5 (PRINCIPAL)
│   ├── ict_live_trader.py     # Trader en vivo para estrategia ICT
│   ├── paper_trader.py        # Sistema de paper trading
│   ├── alert_system.py        # Sistema de alertas
│   └── README_LIVE.md         # Documentación trading en vivo
├── utils/                     # Utilidades
│   ├── data_loader.py         # Carga datos históricos
│   ├── multi_timeframe_loader.py # Carga datos multi-temporales
│   ├── generate_sample_data.py # Genera datos de ejemplo
│   └── indicators.py         # Indicadores técnicos
├── config.py                  # Configuración centralizada
├── setup_mt5.py               # Configuración interactiva de MT5
├── test_mt5_connection.py      # Prueba de conexión a MT5
└── requirements.txt           # Dependencias Python
```

## 🚀 Inicio Rápido

### 1. Instalación

```bash
# Clona o descarga el proyecto
cd trading-bot

# Instala dependencias
pip install -r requirements.txt
```

### 2. Generar Datos de Ejemplo (Para Backtesting)

```bash
python utils/generate_sample_data.py
```

Esto crea archivos CSV de ejemplo en `data/` para todos los timeframes necesarios.

### 3. Ejecutar Backtest

```bash
# Backtest completo de la estrategia ICT
python backtest/backtest.py
```

O usando el script de ejecución rápida:
```bash
./ejecutar_backtest_ahora.sh
```

### 4. Configurar Trading en Vivo (MT5)

**Para macOS:**
- Necesitas Parallels Desktop + Windows (ver `GUIA_PARALLELS_COMPLETA.md`)
- O usar solo backtesting (funciona en macOS)

**Para Windows:**
```bash
# 1. Configurar credenciales
python setup_mt5.py

# 2. Probar conexión (con MT5 abierto)
python test_mt5_connection.py

# 3. Ejecutar bot
python live/mt5_trading.py
```

## 📊 Uso Detallado

### Backtesting de Estrategia ICT

```bash
# Backtest completo con datos multi-temporales
python backtest/backtest.py
```

El backtest:
- Carga datos de todos los timeframes (D1, H4, H1, M15, M5, M3, M1)
- Sincroniza timeframes automáticamente
- Ejecuta la estrategia ICT en cada vela
- Calcula métricas completas (winrate, profit factor, drawdown, RR promedio)
- Muestra resumen final con todas las operaciones

**Resultados incluyen:**
- Número de operaciones
- Winrate (%)
- Profit Factor
- Drawdown máximo
- Risk:Reward promedio
- Equity curve

### Trading en Vivo con MT5

**Requisitos:**
- MetaTrader 5 instalado y abierto
- Cuenta Zeven (Demo o Real)
- Credenciales configuradas en `.env`

**Configuración:**
```bash
# 1. Configura credenciales
python setup_mt5.py
```

Esto crea un archivo `.env` con:
```
MT5_LOGIN=tu_numero_cuenta
MT5_PASSWORD=tu_password
MT5_SERVER=ZevenGlobal-Demo
MT5_SYMBOL=XAUUSD
RISK_PER_TRADE=0.01
MAX_CONCURRENT_TRADES=3
MIN_RR=2.0
```

**Ejecutar:**
```bash
# 2. Prueba conexión (con MT5 abierto y conectado)
python test_mt5_connection.py

# 3. Ejecuta el bot
python live/mt5_trading.py
```

El bot:
- Se conecta automáticamente a MT5
- Obtiene datos en tiempo real de todos los timeframes
- Genera señales ICT
- Ejecuta órdenes BUY/SELL automáticamente
- Gestiona riesgo (SL, TP1, TP2, TP Final)
- Monitorea posiciones abiertas

## ⚙️ Configuración

Edita `config.py` para ajustar:
- Parámetros de la estrategia
- Gestión de riesgo (stop loss, take profit, tamaño de posición)
- Capital inicial y comisiones
- Configuración de datos

**Variables importantes en `.env`:**
- `RISK_PER_TRADE`: Porcentaje de riesgo por operación (ej: 0.01 = 1%)
- `MAX_CONCURRENT_TRADES`: Máximo de operaciones simultáneas
- `MIN_RR`: Risk:Reward mínimo requerido (ej: 2.0)

## 🎯 Estrategia ICT Híbrida

La estrategia implementa análisis multi-temporal completo basado en ICT 2022:

### Timeframes y Análisis

- **D1**: Tendencia macro, zonas de liquidez mayor, FVG grandes, OB macro
- **H4**: BOS/CHoCH institucionales, acumulación/redistribución, FVG activos
- **H1**: Zonas institucionales activas, validación de mitigaciones
- **M15/M5**: BOS/CHoCH limpios, barridas de liquidez, FVG no mitigados
- **M1/M3**: Confirmación entrada sniper

### Patrones Detectados

- **BOS/CHoCH**: Break of Structure / Change of Character
- **Order Blocks (OB)**: Bloques de órdenes institucionales
- **Fair Value Gaps (FVG)**: Gaps de valor justo
- **Liquidity Sweeps**: Barridas de liquidez
- **PD Arrays**: Mitigation Blocks, Breaker Blocks, Rejection Blocks, Liquidity Voids

### Confirmaciones Mínimas para Entrada

La estrategia requiere ≥3 de estas confirmaciones:
1. Sweep de liquidez
2. Mitigación válida de OB o FVG
3. BOS/CHoCH interno luego de la barrida
4. Vela institucional + volumen alto
5. Divergencia RSI (opcional)

## 📚 Documentación

- **Estrategia ICT**: `strategy/README_ICT.md`
- **Backtesting**: `backtest/README_BACKTEST.md`
- **Trading en Vivo**: `live/README_LIVE.md`
- **Configurar MT5 en Mac**: `GUIA_PARALLELS_COMPLETA.md`
- **Inicio Rápido MT5**: `INICIO_RAPIDO_MT5.md`
- **Pasos Parallels**: `PASOS_PARALLELS.md`

## 🖥️ Compatibilidad

### macOS
- ✅ **Backtesting**: Funciona perfectamente
- ❌ **MT5 Trading**: Requiere Parallels Desktop + Windows
- 💡 **Alternativa**: Usar solo backtesting o VPS Windows

### Windows
- ✅ **Backtesting**: Funciona perfectamente
- ✅ **MT5 Trading**: Funciona nativamente

## ⚠️ Advertencias Importantes

- **Paper Trading**: Perfecto para probar estrategias sin riesgo
- **Trading Real**: Conlleva riesgo real de pérdida de capital
- **Pruebas**: Siempre prueba exhaustivamente en DEMO antes de usar dinero real
- **Datos**: Para backtesting preciso, se recomiendan datos reales de múltiples timeframes
- **Riesgo**: El bot ejecuta órdenes automáticamente - monitorea regularmente

## 🔧 Solución de Problemas

### Error: "No module named 'MetaTrader5'"
- **En macOS**: El paquete solo funciona en Windows. Usa Parallels o VPS.
- **En Windows**: Ejecuta `pip install MetaTrader5`

### Error: "No se pueden cargar datos"
- Verifica que los archivos CSV estén en `data/`
- Ejecuta `python utils/generate_sample_data.py` para crear datos de ejemplo

### Error: "MT5 no se puede inicializar"
- Asegúrate de que MT5 esté **abierto** y **conectado** a tu cuenta
- Verifica credenciales en `.env`
- Ejecuta `python test_mt5_connection.py` para diagnosticar

## 📝 Notas

- El proyecto está optimizado para **XAUUSD** (Oro), pero puede adaptarse a otros símbolos
- La estrategia ICT requiere datos de múltiples timeframes para funcionar correctamente
- El sistema de trading en vivo está completamente funcional con MT5
- Para trading en macOS, se recomienda Parallels Desktop con Windows

## 🎓 Próximos Pasos

1. ✅ Ejecutar backtests para validar la estrategia
2. ✅ Probar en cuenta DEMO de MT5
3. ✅ Optimizar parámetros según resultados
4. ✅ Configurar alertas (webhook, email, etc.)
5. ✅ Monitorear rendimiento en DEMO antes de usar cuenta real

## 📞 Soporte

Para problemas o preguntas:
- Revisa la documentación en cada módulo (`README_*.md`)
- Verifica los archivos de configuración
- Ejecuta scripts de prueba (`test_mt5_connection.py`)

---

**¡Listo para operar!** 🚀
