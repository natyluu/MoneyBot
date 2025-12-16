# 📱 Actualizar Chat ID de Telegram

## Nuevo Chat ID del Grupo

El nuevo Chat ID de Telegram para el grupo es: **-1003607928345**

---

## Pasos para actualizar en el VPS

### 1. Navega a la carpeta del bot:

```cmd
cd "C:\Users\Administrator\Downloads\bot de trader"
```

### 2. Abre el archivo `.env`:

```cmd
notepad .env
```

### 3. Busca la línea `TELEGRAM_CHAT_ID` y cámbiala a:

```
TELEGRAM_CHAT_ID=-1003607928345
```

### 4. Guarda el archivo (Ctrl+S)

### 5. Verifica que se actualizó:

```cmd
type .env | findstr TELEGRAM_CHAT_ID
```

Deberías ver:
```
TELEGRAM_CHAT_ID=-1003607928345
```

---

## Contenido completo del archivo `.env`

Si necesitas recrear el archivo completo, usa este contenido:

```
MT5_LOGIN=94342
MT5_PASSWORD=Santos2025!
MT5_SERVER=ZevenGlobal-Live
MT5_SYMBOL=XAUUSD.vip
RISK_PER_TRADE=0.01
MAX_CONCURRENT_TRADES=3
MIN_RR=1.5
TELEGRAM_BOT_TOKEN=8447919749:AAEM0_pIrfA6h8c7PoQST4_Pd1FJ_cp8cNA
TELEGRAM_CHAT_ID=-1003607928345
```

---

## Después de actualizar

Reinicia el bot para que tome los nuevos valores:

```cmd
python -u live\mt5_trading.py
```

Ahora el bot enviará todos los reportes y alertas al grupo de Telegram con el nuevo ID.

---

## Reportes que recibirás

Con los cambios implementados, ahora recibirás:

1. **Cada hora**: Reporte detallado con:
   - Resumen del día (trades cerrados, win rate, P&L, profit factor)
   - Lista de trades del día (hasta 10 trades)
   - Posiciones abiertas (hasta 5 posiciones)

2. **Cada 5 minutos**: Métricas simples (si hay trades)

3. **Al finalizar el bot**: Reporte final completo del día

4. **En tiempo real**: Alertas de:
   - Señales generadas
   - Trades ejecutados
   - Trades cerrados
   - Actualizaciones de posiciones (SL a break-even, cierres parciales)

