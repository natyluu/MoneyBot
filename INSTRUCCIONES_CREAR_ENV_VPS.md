# 📝 Instrucciones para Crear .env en el VPS

## 🎯 Problema

Cuando copias la carpeta del bot al VPS, el archivo `.env` no está incluido porque está en `.gitignore` (por seguridad, no se sube a GitHub).

## ✅ Solución Rápida

### Opción 1: Usar el Script Automático (RECOMENDADO)

En el VPS, ejecuta uno de estos scripts:

**Desde CMD:**
```cmd
cd "C:\Users\Administrator\Downloads\bot de trader"
CREAR_ENV_EN_VPS.bat
```

**Desde PowerShell:**
```powershell
cd "C:\Users\Administrator\Downloads\bot de trader"
.\CREAR_ENV_EN_VPS.ps1
```

Esto creará automáticamente el archivo `.env` con todas las credenciales.

---

### Opción 2: Crear Manualmente

1. Navega a la carpeta del bot en el VPS:
   ```cmd
   cd "C:\Users\Administrator\Downloads\bot de trader"
   ```

2. Crea el archivo `.env`:
   ```cmd
   notepad .env
   ```

3. Copia y pega este contenido completo:
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

4. Guarda el archivo (Ctrl+S) y cierra Notepad.

---

### Opción 3: Copiar desde el Archivo de Referencia

Si tienes el archivo `ENV_VPS_COPIA.txt` en el VPS:

```cmd
cd "C:\Users\Administrator\Downloads\bot de trader"
copy ENV_VPS_COPIA.txt .env
```

---

## ✅ Verificar que se Creó Correctamente

Después de crear el `.env`, verifica que existe:

```cmd
type .env
```

Deberías ver las 9 líneas con todas las credenciales.

---

## 🚀 Después de Crear el .env

Una vez que el archivo `.env` esté creado, puedes iniciar el bot:

```cmd
python -u live\mt5_trading.py
```

---

## 📋 Checklist

- [ ] Archivo `.env` creado en la carpeta del bot
- [ ] Contiene las 9 líneas de configuración
- [ ] Credenciales de MT5 correctas
- [ ] Token y Chat ID de Telegram correctos
- [ ] Archivo guardado correctamente

---

## ⚠️ Importante

- El archivo `.env` NO se sube a GitHub por seguridad
- Debes crearlo manualmente en cada VPS o máquina donde uses el bot
- Mantén las credenciales seguras y no las compartas

---

## 🔄 Si Cambias las Credenciales

Si necesitas actualizar las credenciales en el VPS:

1. Edita el archivo `.env`:
   ```cmd
   notepad .env
   ```

2. Actualiza los valores necesarios

3. Guarda y reinicia el bot

