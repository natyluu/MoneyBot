# 🛡️ News Risk Gate - Sistema de Protección por Noticias

## 📋 Descripción

Sistema de protección que bloquea nuevas entradas durante eventos de noticias económicas, alta volatilidad, spreads altos o drawdown excesivo. **NO cierra trades abiertos**, solo previene nuevas entradas.

## 🎯 Características

- ✅ **Detección de clusters de noticias USD** (múltiples noticias LOW/MED en ventana de tiempo)
- ✅ **Bloqueo de eventos EIA** (especialmente para XAUUSD)
- ✅ **Filtro de spread** (bloquea si spread > máximo)
- ✅ **Filtro de volatilidad** (bloquea si ATR ratio > máximo)
- ✅ **Kill switch diario** (bloquea si drawdown diario excede límite)
- ✅ **Cooldown post-noticia** (espera después de eventos)
- ✅ **Logging completo** en base de datos y logs
- ✅ **Gestión de posiciones** continúa normalmente (SL a BE, cierres parciales)

## 📁 Estructura

```
news/
├── __init__.py
└── provider.py          # Proveedor de eventos de noticias (mock por ahora)

risk/
├── __init__.py
└── news_gate.py         # Lógica del News Risk Gate

data/
└── news_events.json     # Eventos de noticias (mock)

utils/
├── indicators.py        # Funciones ATR agregadas
└── database.py          # Tabla bot_state agregada
```

## ⚙️ Configuración

Agrega estas variables a tu archivo `.env`:

```env
# News Risk Gate - Filtros de Mercado
SPREAD_MAX=50.0
ATR_MAX_RATIO=2.0
DAILY_DD_LIMIT=-5.0

# News Risk Gate - Configuración de Noticias USD
NEWS_USD_WINDOW_MINUTES=90
NEWS_MIN_EVENTS_FOR_CLUSTER=2
NEWS_BLOCK_PRE_MINUTES=15
NEWS_BLOCK_POST_MINUTES=30
NEWS_COOLDOWN_MINUTES=20

# News Risk Gate - Configuración de Eventos EIA
EIA_BLOCK_PRE_MINUTES=30
EIA_BLOCK_POST_MINUTES=30
```

### Parámetros Explicados

#### Filtros de Mercado

- **SPREAD_MAX**: Spread máximo permitido en puntos (default: 50.0)
  - Si el spread actual > SPREAD_MAX, bloquea nuevas entradas
- **ATR_MAX_RATIO**: Ratio máximo ATR actual / ATR promedio (default: 2.0)
  - Si ATR ratio > ATR_MAX_RATIO, bloquea (alta volatilidad)
- **DAILY_DD_LIMIT**: Drawdown diario límite en % (default: -5.0)
  - Si drawdown diario <= DAILY_DD_LIMIT, bloquea (kill switch)

#### Noticias USD

- **NEWS_USD_WINDOW_MINUTES**: Ventana de tiempo para detectar cluster (default: 90)
- **NEWS_MIN_EVENTS_FOR_CLUSTER**: Mínimo de eventos para considerar cluster (default: 2)
- **NEWS_BLOCK_PRE_MINUTES**: Minutos antes de noticia para bloquear (default: 15)
- **NEWS_BLOCK_POST_MINUTES**: Minutos después de noticia para bloquear (default: 30)
- **NEWS_COOLDOWN_MINUTES**: Cooldown después de noticia (default: 20)

#### Eventos EIA

- **EIA_BLOCK_PRE_MINUTES**: Minutos antes de EIA para bloquear (default: 30)
- **EIA_BLOCK_POST_MINUTES**: Minutos después de EIA para bloquear (default: 30)

## 🔄 Cómo Funciona

### 1. Antes de Generar Señales

En cada ciclo de análisis (cada 3 minutos), el bot:

1. **Carga eventos del día** desde `data/news_events.json`
2. **Calcula métricas de mercado**:
   - Spread actual
   - ATR ratio (volatilidad)
   - Drawdown diario
   - Posiciones abiertas
3. **Ejecuta News Risk Gate**:
   - Verifica clusters de noticias USD
   - Verifica eventos EIA
   - Verifica spread, volatilidad y drawdown
4. **Si está bloqueado**:
   - ❌ NO genera señales
   - ✅ Continúa gestionando posiciones abiertas
   - 📊 Registra estado en base de datos
   - 📝 Loggea razones

### 2. Modos de Operación

- **NORMAL**: Sin restricciones, genera señales normalmente
- **CONSERVATIVE**: Cluster de noticias detectado, bloquea cerca de eventos
- **BLOCKED**: Bloqueado por spread alto, volatilidad o drawdown

### 3. Gestión de Posiciones

**IMPORTANTE**: El News Risk Gate NO afecta la gestión de posiciones abiertas:
- ✅ SL a break-even continúa funcionando
- ✅ Cierres parciales continúan funcionando
- ✅ Actualización de posiciones continúa cada 30 segundos

## 📊 Base de Datos

Se crea automáticamente la tabla `bot_state` con:

- `timestamp_utc`: Fecha/hora UTC
- `symbol`: Símbolo operado
- `news_mode`: Modo actual (NORMAL/CONSERVATIVE/BLOCKED)
- `blocked`: Si está bloqueado (0/1)
- `reasons`: Razones del bloqueo (JSON)
- `cooldown_until_utc`: Fecha UTC hasta cuando está en cooldown
- `spread`: Spread actual
- `atr_ratio`: Ratio ATR
- `daily_dd_pct`: Drawdown diario %

## 📝 Logging

El bot registra:

- **INFO**: Cambios de modo (NORMAL → CONSERVATIVE)
- **WARNING**: Bloqueos y razones
- **Base de datos**: Estado completo en cada ciclo

Ejemplo de log:

```
🚫 News Risk Gate: Modo CONSERVATIVE - Bloqueado
   ⚠️ Cluster de noticias USD cerca de Retail Sales
   ⚠️ Cooldown activo hasta 14:20:00 UTC
```

## 🧪 Tests

Ejecuta los tests:

```bash
python -m pytest tests/test_news_gate.py -v
```

O manualmente:

```bash
python tests/test_news_gate.py
```

## 📅 Agregar Eventos de Noticias

Edita `data/news_events.json` para agregar eventos:

```json
[
  {
    "timestamp_utc": "2025-01-15T13:30:00Z",
    "currency": "USD",
    "impact": "MED",
    "title": "Retail Sales"
  },
  {
    "timestamp_utc": "2025-01-15T15:30:00Z",
    "currency": "USD",
    "impact": "HIGH",
    "title": "EIA Crude Oil Stocks"
  }
]
```

**Formato de timestamp**: `YYYY-MM-DDTHH:MM:SSZ` (UTC)

**Impactos válidos**: `LOW`, `MED`, `HIGH`

## 🔮 Futuras Mejoras

- [ ] Integración con API real de noticias (ForexFactory, Investing.com)
- [ ] IA para interpretar "hawkish/dovish" de noticias
- [ ] Calendario económico automático
- [ ] Alertas de Telegram cuando se activa el gate

## ⚠️ Notas Importantes

1. **No cierra trades**: El gate solo previene nuevas entradas
2. **Gestión continúa**: SL a BE y cierres parciales funcionan normalmente
3. **Mock por ahora**: Los eventos vienen de JSON, no de API real
4. **Configuración flexible**: Todos los parámetros son ajustables vía `.env`

## 🐛 Solución de Problemas

### El bot no bloquea durante noticias

1. Verifica que `data/news_events.json` tenga eventos del día actual
2. Verifica que los timestamps estén en UTC
3. Revisa los logs para ver si hay errores

### El bot bloquea demasiado

1. Ajusta `SPREAD_MAX` más alto
2. Aumenta `ATR_MAX_RATIO`
3. Ajusta `DAILY_DD_LIMIT` más negativo

### El bot no bloquea cuando debería

1. Verifica que los eventos estén en el JSON
2. Verifica la configuración en `.env`
3. Revisa los logs para ver el estado del gate

---

**Última actualización**: 2025-01-15






