# Sistema de Trading en Vivo

Sistema completo para operar la estrategia ICT en tiempo real con múltiples modos de operación.

## Modos de Operación

### 1. PAPER TRADING (Simulación)
Simula operaciones sin riesgo real. Perfecto para probar la estrategia antes de usar dinero real.

### 2. ALERT (Solo Alertas)
Solo envía alertas cuando se detectan señales. No ejecuta operaciones.

### 3. LIVE (Trading Real)
Ejecuta operaciones reales con el broker. **Requiere integración con API del broker.**

## Características

- ✅ Análisis multi-temporal en tiempo real
- ✅ Paper trading con simulación completa
- ✅ Sistema de alertas (consola, archivo, webhook, email)
- ✅ Gestión automática de posiciones (SL/TP)
- ✅ Estadísticas en tiempo real

## Uso Básico

### Modo Paper Trading

```python
from live.ict_live_trader import ICTLiveTrader

# Inicializa trader en modo paper
trader = ICTLiveTrader(
    symbol="XAUUSD",
    mode="PAPER"
)

# Inicia el trader
trader.start(
    analysis_interval=300,  # Análisis cada 5 minutos
    update_interval=60      # Actualización cada 1 minuto
)
```

### Modo Solo Alertas

```python
trader = ICTLiveTrader(
    symbol="XAUUSD",
    mode="ALERT",
    alert_file="alerts.json",
    webhook_url="https://discord.com/api/webhooks/..."  # Opcional
)

trader.start()
```

### Desde Línea de Comandos

```bash
# Modo paper trading
python live/ict_live_trader.py --symbol XAUUSD --mode PAPER

# Modo alertas con webhook
python live/ict_live_trader.py --symbol XAUUSD --mode ALERT --webhook https://...

# Modo alertas con archivo
python live/ict_live_trader.py --symbol XAUUSD --mode ALERT --alert-file alerts.json
```

## Sistema de Alertas

El sistema de alertas soporta múltiples canales:

### 1. Consola
Se muestra automáticamente en la consola cuando se detecta una señal.

### 2. Archivo JSON
Guarda todas las alertas en un archivo JSON.

```python
alert_system = AlertSystem(alert_file="alerts.json")
```

### 3. Webhook (Discord, Slack, Telegram)
Envía alertas a webhooks.

```python
alert_system = AlertSystem(
    webhook_url="https://discord.com/api/webhooks/YOUR_WEBHOOK_URL"
)
```

### 4. Email
Envía alertas por email.

```python
email_config = {
    'smtp_server': 'smtp.gmail.com',
    'port': 587,
    'user': 'tu_email@gmail.com',
    'password': 'tu_password',
    'to': 'destinatario@gmail.com'
}

alert_system = AlertSystem(email_config=email_config)
```

## Paper Trading

El sistema de paper trading simula operaciones completas:

- ✅ Apertura de posiciones
- ✅ Gestión de Stop Loss y Take Profits
- ✅ Cálculo de P&L en tiempo real
- ✅ Estadísticas completas

### Obtener Estadísticas

```python
# Obtiene estadísticas del paper trading
stats = paper_trader.get_statistics(current_prices)

print(f"Capital: ${stats['current_capital']:,.2f}")
print(f"Equity: ${stats['equity']:,.2f}")
print(f"Retorno: {stats['total_return_pct']:.2f}%")
print(f"Trades: {stats['total_trades']}")
print(f"Tasa de acierto: {stats['win_rate_pct']:.2f}%")
```

## Integración con API de Broker

Para usar el modo LIVE, necesitas implementar la conexión con tu broker:

```python
# En ict_live_trader.py, implementa:
def _get_multi_timeframe_data(self):
    # Conecta a API del broker y obtiene datos
    # Ejemplo con Binance:
    # from binance.client import Client
    # client = Client(api_key, api_secret)
    # klines = client.get_klines(symbol=self.symbol, interval='1h')
    # ... procesar y retornar DataFrame
    pass

def _get_current_prices(self):
    # Obtiene precios actuales desde API
    # return {self.symbol: current_price}
    pass
```

## Configuración Recomendada

### Para Desarrollo/Pruebas
- Modo: `PAPER`
- Análisis cada: 300 segundos (5 minutos)
- Actualización cada: 60 segundos (1 minuto)

### Para Producción (Alertas)
- Modo: `ALERT`
- Análisis cada: 300 segundos
- Webhook configurado para notificaciones

### Para Producción (Trading Real)
- Modo: `LIVE`
- Análisis cada: 300 segundos
- API del broker configurada
- ⚠️ **Usar con precaución - riesgo real de pérdida**

## Monitoreo

Puedes obtener el estado del trader en cualquier momento:

```python
status = trader.get_status()
print(status)
```

Retorna:
- Estado de ejecución
- Modo actual
- Último análisis realizado
- Última señal detectada
- Estadísticas de paper trading (si aplica)

## Detener el Trader

Presiona `Ctrl+C` para detener el trader de forma segura. El sistema:
- Cierra todas las posiciones abiertas (en paper trading)
- Muestra estadísticas finales
- Guarda estado si es necesario

## Próximos Pasos

1. **Obtener datos en tiempo real**: Implementar conexión con API del broker
2. **Optimizar intervalos**: Ajustar según el símbolo y condiciones de mercado
3. **Agregar más canales de alerta**: Telegram bot, SMS, etc.
4. **Dashboard**: Crear interfaz web para monitoreo
5. **Logging avanzado**: Sistema de logs más robusto













