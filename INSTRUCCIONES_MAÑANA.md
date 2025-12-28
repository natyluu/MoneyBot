# 📋 Instrucciones para Mañana - Protección de Noticias

## ✅ Cambios Implementados

Se han implementado las siguientes mejoras para proteger el bot durante noticias:

### 1. **SafeNewsProvider** (Cache Seguro)
- ✅ Cache en memoria (evita leer archivo constantemente)
- ✅ File locking (evita conflictos de lectura/escritura)
- ✅ Fallback automático si hay errores
- ✅ **El bot NUNCA se rompe por errores de noticias**

### 2. **News Risk Gate Mejorado**
- ✅ Bloquea eventos **HIGH individuales** (antes solo clusters)
- ✅ Bloquea eventos **MED importantes** (Fed speeches, CPI, etc.)
- ✅ Considera divisas relevantes para XAUUSD (USD, GBP, EUR)
- ✅ Tiempos de bloqueo más largos para eventos HIGH (30 min antes, 60 min después)

### 3. **Nuevas Variables de Configuración**
Agregadas en `config.py` (con valores por defecto):
- `HIGH_NEWS_BLOCK_PRE_MINUTES=30` (minutos antes de evento HIGH)
- `HIGH_NEWS_BLOCK_POST_MINUTES=60` (minutos después de evento HIGH)
- `HIGH_NEWS_COOLDOWN_MINUTES=30` (cooldown después de evento HIGH)

## 🚀 Pasos para Mañana

### Paso 1: Actualizar Noticias (5 minutos)

1. **Abre el calendario económico:**
   - https://www.forexfactory.com/calendar
   - O cualquier otro calendario económico

2. **Identifica eventos importantes para mañana:**
   - Busca eventos **HIGH** (NFP, CPI, Inflation, etc.)
   - Busca eventos **MED importantes** (Fed speeches, GDP, etc.)
   - Especialmente de **USD, GBP, EUR** (afectan XAUUSD)

3. **Edita `ACTUALIZAR_EVENTOS_HOY.py`:**
   ```python
   events_today = [
       {
           "timestamp_utc": "2025-01-XXT13:30:00Z",  # Fecha y hora UTC
           "currency": "GBP",  # USD, GBP, EUR, etc.
           "impact": "HIGH",  # LOW, MED, HIGH
           "title": "Inflation Rate YoY (Nov)"
       },
       # ... más eventos
   ]
   ```

4. **Ejecuta el script:**
   ```bash
   python ACTUALIZAR_EVENTOS_HOY.py
   ```

### Paso 2: Verificar que Funciona (2 minutos)

1. **Verifica que el JSON se actualizó:**
   ```bash
   # En PowerShell o CMD
   type data\news_events.json
   ```

2. **Inicia el bot y verifica logs:**
   - Deberías ver: `News Risk Gate: Modo NORMAL` (si no hay bloqueo)
   - O: `News Risk Gate: Modo BLOCKED` (si hay evento cerca)

### Paso 3: Monitorear Esta Semana

- ✅ Revisa logs para ver si bloquea correctamente
- ✅ Verifica que no se rompe si hay errores
- ✅ Ajusta tiempos de bloqueo si es necesario

## 📝 Formato de Eventos

Cada evento debe tener este formato:

```json
{
    "timestamp_utc": "2025-01-XXT13:30:00Z",  // Fecha y hora en UTC
    "currency": "USD",  // Código de divisa: USD, GBP, EUR, etc.
    "impact": "HIGH",  // LOW, MED, o HIGH
    "title": "Non-Farm Payrolls"  // Nombre del evento
}
```

### Ejemplos de Eventos Importantes:

**HIGH Impact:**
- Non-Farm Payrolls (NFP)
- CPI (Consumer Price Index)
- Inflation Rate
- Interest Rate Decision
- GDP

**MED Importante:**
- Fed Speech / Fed Testimony
- Retail Sales
- Unemployment Rate
- Manufacturing PMI

## ⚙️ Configuración Opcional (.env)

Si quieres ajustar los tiempos de bloqueo, agrega a tu `.env`:

```env
# Eventos HIGH (NFP, CPI, etc.)
HIGH_NEWS_BLOCK_PRE_MINUTES=30
HIGH_NEWS_BLOCK_POST_MINUTES=60
HIGH_NEWS_COOLDOWN_MINUTES=30
```

## 🔍 Verificación Rápida

Para verificar que todo funciona:

```python
# Ejecuta en Python
from news.provider import get_news_provider
from datetime import datetime

provider = get_news_provider()
today = datetime.utcnow().date()
events = provider.get_events_for_day(today)

print(f"Eventos de hoy: {len(events)}")
for event in events:
    print(f"  - {event.get('title')} ({event.get('impact')}) a las {event.get('timestamp_utc')}")
```

## ⚠️ Recordatorios

1. **Siempre usa hora UTC** en los timestamps
2. **Actualiza las noticias cada mañana** antes de iniciar el bot
3. **Incluye eventos HIGH y MED importantes** de USD, GBP, EUR
4. **El bot seguirá funcionando** aunque olvides actualizar (usará cache anterior)

## 🎯 Resultado Esperado

Con estos cambios, el bot debería:
- ✅ Bloquear operaciones **30 minutos antes** de eventos HIGH
- ✅ Bloquear operaciones **60 minutos después** de eventos HIGH
- ✅ Bloquear eventos MED importantes (Fed speeches, etc.)
- ✅ **NUNCA romperse** por errores de noticias
- ✅ Continuar funcionando aunque el archivo esté bloqueado

---

**¡Listo para mañana!** 🚀





