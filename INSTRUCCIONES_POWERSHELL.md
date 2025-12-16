# ✅ CÓMO INICIAR EL BOT EN POWERSHELL CON MENSAJES INMEDIATOS

## 🎯 SOLUCIÓN PARA POWERSHELL

PowerShell tiene buffering, pero hay formas de ver los mensajes inmediatamente.

---

## ✅ MÉTODO 1: Script PowerShell Mejorado (RECOMENDADO)

### Paso 1: Abrir PowerShell
1. Presiona `Win + X`
2. Selecciona "Windows PowerShell"

### Paso 2: Ejecutar el Script
En PowerShell, ejecuta:

```powershell
cd "C:\BOT\trading-bot-windows-20251210 on 'Mac'"
.\INICIAR_BOT_POWERSHELL_DIRECTO.ps1
```

**Si PowerShell bloquea scripts, primero ejecuta:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Luego ejecuta el script de nuevo.

---

## ✅ MÉTODO 2: Comandos Directos en PowerShell

### Ejecuta estos comandos uno por uno:

```powershell
cd "C:\BOT\trading-bot-windows-20251210 on 'Mac'"
```

```powershell
$env:PYTHONUNBUFFERED = "1"
python -u live\mt5_trading.py | ForEach-Object { Write-Host $_; [Console]::Out.Flush() }
```

Esto fuerza el flush después de cada línea.

---

## ✅ MÉTODO 3: Ver en Archivo en Tiempo Real

### Ventana 1: Ejecutar el bot
```powershell
cd "C:\BOT\trading-bot-windows-20251210 on 'Mac'"
python -u live\mt5_trading.py > bot_output.txt 2>&1
```

### Ventana 2: Ver en tiempo real
Abre otra ventana de PowerShell y ejecuta:
```powershell
Get-Content bot_output.txt -Wait
```

Esto mostrará los mensajes en tiempo real.

---

## ✅ MÉTODO 4: Usar Tee-Object

```powershell
cd "C:\BOT\trading-bot-windows-20251210 on 'Mac'"
$env:PYTHONUNBUFFERED = "1"
python -u live\mt5_trading.py 2>&1 | Tee-Object -FilePath "bot_output.txt"
```

Esto muestra los mensajes en pantalla Y los guarda en archivo.

---

## 🔧 CONFIGURACIÓN ADICIONAL PARA POWERSHELL

Si quieres que PowerShell siempre muestre output inmediato, agrega esto a tu perfil:

```powershell
# Abre tu perfil
notepad $PROFILE

# Agrega estas líneas:
$env:PYTHONUNBUFFERED = "1"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```

---

## 📋 RESUMEN RÁPIDO

**Opción más fácil:**
1. Abre PowerShell
2. Ejecuta: `cd "C:\BOT\trading-bot-windows-20251210 on 'Mac'"`
3. Ejecuta: `.\INICIAR_BOT_POWERSHELL_DIRECTO.ps1`

**Si no funciona, usa:**
```powershell
$env:PYTHONUNBUFFERED = "1"
python -u live\mt5_trading.py | ForEach-Object { Write-Host $_; [Console]::Out.Flush() }
```

---

## ⚠️ NOTA IMPORTANTE

PowerShell tiene buffering más agresivo que CMD. Si los mensajes aún no aparecen inmediatamente:

1. **Usa CMD** (funciona mejor para esto)
2. **O usa el método de archivo** (ventana 1 ejecuta, ventana 2 muestra)

---

## ✅ VERIFICACIÓN

Cuando inicies el bot, deberías ver **inmediatamente**:

```
🔧 Bot iniciando...
======================================================================
🚀 INICIANDO BOT DE TRADING AUTOMÁTICO
======================================================================
```

Si ves estos mensajes inmediatamente, ¡funciona!




