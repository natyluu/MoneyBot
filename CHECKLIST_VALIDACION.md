# ✅ Checklist de Validación - News Risk Gate

## 📋 Pasos de Validación

### 1. Variables .env en VPS
- [ ] Agregar variables al `.env` en el VPS:
  ```env
  SPREAD_MAX=50.0
  ATR_MAX_RATIO=2.0
  DAILY_DD_LIMIT=-5.0
  NEWS_USD_WINDOW_MINUTES=90
  NEWS_MIN_EVENTS_FOR_CLUSTER=2
  NEWS_BLOCK_PRE_MINUTES=15
  NEWS_BLOCK_POST_MINUTES=30
  NEWS_COOLDOWN_MINUTES=20
  EIA_BLOCK_PRE_MINUTES=30
  EIA_BLOCK_POST_MINUTES=30
  ```

### 2. Actualizar eventos JSON
- [ ] Ejecutar `python3 ACTUALIZAR_EVENTOS_HOY.py` para agregar eventos de hoy
- [ ] Verificar que `data/news_events.json` tenga eventos con fecha UTC de hoy
- [ ] Formato: `YYYY-MM-DDTHH:MM:SSZ` (ej: `2025-01-17T15:30:00Z`)

### 3. Ejecutar tests
- [ ] Ejecutar: `python3 VALIDAR_NEWS_GATE.py`
- [ ] Verificar que todos los checks pasen (✅)
- [ ] Ejecutar: `python3 -m pytest tests/test_news_gate.py -v`
- [ ] Verificar que todos los tests pasen

### 4. Verificar logs
- [ ] Iniciar el bot
- [ ] Verificar en logs que aparezca:
  - `News Risk Gate: Modo NORMAL` (cuando no hay bloqueo)
  - `News Risk Gate: Modo CONSERVATIVE` (cuando hay cluster)
  - `News Risk Gate: Modo BLOCKED` (cuando está bloqueado)
- [ ] Verificar razones de bloqueo cuando aplica

### 5. Verificar tabla bot_state
- [ ] Conectar a la base de datos: `sqlite3 data/trading_bot.db`
- [ ] Ejecutar: `SELECT * FROM bot_state ORDER BY timestamp_utc DESC LIMIT 10;`
- [ ] Verificar que haya registros recientes
- [ ] Verificar campos: `news_mode`, `blocked`, `reasons`, `spread`, `atr_ratio`, `daily_dd_pct`

### 6. Ajustar SPREAD_MAX según unidad real
- [ ] Verificar unidad de spread en MT5 (puntos vs pips)
- [ ] Para XAUUSD: 1 punto = 0.01 USD
- [ ] Ajustar `SPREAD_MAX` según spread típico del broker
- [ ] Ejemplo: Si spread típico es 20-30 puntos, usar `SPREAD_MAX=50.0`

### 7. Revisar condición de drawdown
- [ ] Verificar cálculo de `get_daily_drawdown_pct()` en `utils/database.py`
- [ ] Ajustar `DAILY_DD_LIMIT` según tolerancia al riesgo
- [ ] Probar con datos reales de trades

## 🔍 Comandos Útiles

```bash
# Validar todo el sistema
python3 VALIDAR_NEWS_GATE.py

# Actualizar eventos de hoy
python3 ACTUALIZAR_EVENTOS_HOY.py

# Ejecutar tests
python3 -m pytest tests/test_news_gate.py -v

# Ver registros de bot_state
sqlite3 data/trading_bot.db "SELECT * FROM bot_state ORDER BY timestamp_utc DESC LIMIT 10;"

# Ver eventos de hoy
python3 -c "from news.provider import get_news_provider; from datetime import datetime; provider = get_news_provider(); events = provider.get_events_for_day(datetime.utcnow().date()); print(f'Eventos de hoy: {len(events)}'); [print(f\"  - {e.get('title')} a las {e.get('timestamp_utc')}\") for e in events]"
```

## 📝 Notas

- Los eventos deben estar en formato UTC
- El bot verifica el gate cada ciclo de análisis (cada 3 minutos)
- El gate NO cierra trades abiertos, solo previene nuevas entradas
- La gestión de posiciones (SL a BE, cierres parciales) continúa funcionando

