# 📱 Configurar Alertas de Telegram

Guía paso a paso para configurar las alertas de Telegram en tu bot de trading.

## 🎯 ¿Qué alertas recibirás?

- ✅ **Nueva señal detectada** - Cuando el bot encuentra una oportunidad
- ✅ **Trade ejecutado** - Cuando se abre una posición
- ✅ **Trade cerrado** - Cuando se cierra una posición (con P&L)
- ✅ **SL movido a break-even** - Cuando se protege la posición
- ✅ **Cierre parcial** - Cuando se realiza un cierre parcial
- ✅ **Métricas de performance** - Cada 5 minutos (si hay trades)
- ✅ **Reporte diario** - Al finalizar el día
- ⚠️ **Errores críticos** - Si algo falla

---

## 📋 Paso 1: Crear un Bot de Telegram

1. **Abre Telegram** y busca `@BotFather`
2. **Envía el comando:** `/newbot`
3. **Sigue las instrucciones:**
   - Elige un nombre para tu bot (ej: "Mi Trading Bot")
   - Elige un username (debe terminar en `bot`, ej: `mi_trading_bot`)
4. **Copia el TOKEN** que te da BotFather
   - Se ve así: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`
   - **Guárdalo bien**, lo necesitarás después

---

## 📋 Paso 2: Obtener tu Chat ID

Tienes dos opciones:

### Opción A: Chat personal (recomendado)

1. **Busca en Telegram:** `@userinfobot`
2. **Envía:** `/start`
3. **Copia tu Chat ID** (es un número, ej: `123456789`)

### Opción B: Grupo de Telegram

1. **Crea un grupo** en Telegram
2. **Agrega tu bot** al grupo (busca el username de tu bot)
3. **Envía un mensaje** en el grupo
4. **Visita esta URL** en tu navegador (reemplaza `TU_TOKEN`):
   ```
   https://api.telegram.org/botTU_TOKEN/getUpdates
   ```
5. **Busca `"chat":{"id"`** en la respuesta
6. **Copia el número** que aparece después de `"id":` (puede ser negativo para grupos)

---

## 📋 Paso 3: Configurar en el Bot

### En Windows VPS:

1. **Abre el archivo `.env`** en la carpeta del bot:
   ```cmd
   notepad .env
   ```

2. **Agrega estas líneas** al final del archivo:
   ```
   TELEGRAM_BOT_TOKEN=tu_token_aqui
   TELEGRAM_CHAT_ID=tu_chat_id_aqui
   ```

3. **Reemplaza los valores:**
   - `tu_token_aqui` → El token que te dio BotFather
   - `tu_chat_id_aqui` → Tu Chat ID

4. **Ejemplo:**
   ```
   TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
   TELEGRAM_CHAT_ID=123456789
   ```

5. **Guarda el archivo** (Ctrl+S)

---

## 📋 Paso 4: Instalar dependencias

Si aún no tienes `requests` instalado:

```cmd
pip install requests
```

O instala todas las dependencias:

```cmd
pip install -r requirements.txt
```

---

## 📋 Paso 5: Probar la conexión

Ejecuta el bot:

```cmd
python -u live\mt5_trading.py
```

Deberías ver:
```
✅ Telegram bot conectado: @tu_bot_username
```

Si ves esto, **¡está funcionando!** 🎉

---

## 🔧 Solución de problemas

### ❌ "Token de Telegram inválido"
- Verifica que copiaste el token completo
- Asegúrate de que no hay espacios extra
- El token debe tener formato: `123456789:ABCdef...`

### ❌ "No se pudo conectar con Telegram"
- Verifica tu conexión a internet
- El VPS debe tener acceso a internet
- Prueba abrir `https://api.telegram.org` en un navegador

### ❌ "Chat ID no funciona"
- Verifica que copiaste el Chat ID correcto
- Si es un grupo, asegúrate de que el bot está agregado
- Prueba enviar un mensaje al bot primero

### ❌ No recibo alertas
- Verifica que el bot está corriendo
- Revisa los logs en `logs/bot_YYYYMMDD.log`
- Asegúrate de que el bot tiene permisos para enviar mensajes

---

## 📱 Ejemplo de alertas

### Nueva Señal:
```
🟢 NUEVA SEÑAL DETECTADA

📊 Símbolo: XAUUSD
📈 Dirección: BUY
💰 Entrada: $2345.67
🛑 Stop Loss: $2340.00
🎯 TP1: $2355.00
📊 Risk:Reward: 1:2.5

✅ Confirmaciones: 3
📋 Razones:
   1. Sweep de liquidez
   2. Mitigación de FVG
   3. BOS interno

⏰ 2025-12-15 10:30:45
```

### Trade Ejecutado:
```
🟢 TRADE EJECUTADO

🎫 Ticket: 12345678
📊 Símbolo: XAUUSD
📈 Dirección: BUY
💰 Entrada: $2345.67
📦 Tamaño: 0.10 lotes
🛑 Stop Loss: $2340.00
🎯 TP1: $2355.00
📊 Risk:Reward: 1:2.5

⏰ 2025-12-15 10:31:00
```

### Trade Cerrado:
```
✅ TRADE CERRADO

🎫 Ticket: 12345678
💰 P&L: $45.50 (+1.94%)
📋 Razón: TP1

⏰ 2025-12-15 14:20:30
```

---

## ✅ Verificación final

1. ✅ Bot creado en Telegram
2. ✅ Token copiado
3. ✅ Chat ID obtenido
4. ✅ Variables agregadas a `.env`
5. ✅ Dependencias instaladas
6. ✅ Bot ejecutándose y conectado

**¡Listo!** Ahora recibirás todas las alertas en Telegram. 🚀

---

## 💡 Tips

- **Grupo privado:** Crea un grupo solo para ti y agrega el bot
- **Notificaciones:** Activa las notificaciones del grupo para no perderte nada
- **Historial:** Todas las alertas también se guardan en la base de datos
- **Privacidad:** El token y chat ID son privados, no los compartas

---

¿Necesitas ayuda? Revisa los logs en `logs/bot_YYYYMMDD.log` para ver errores detallados.

