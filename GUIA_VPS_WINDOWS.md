# 🚀 Guía Completa: Configurar Bot en VPS Windows

## 📋 Estado Actual

✅ **Cambio aplicado:** El bot ahora requiere **3 confirmaciones** (más selectivo y profesional)

---

## 🎯 PASO 1: Preparar Archivos para VPS

### Opción A: Subir Todo el Proyecto

1. **Comprime el proyecto completo:**
   - Carpeta completa: `bot de trader`
   - Formato: ZIP o RAR
   - Incluye: todo el código, `.env`, `requirements.txt`

2. **Sube al VPS:**
   - Usa RDP (Remote Desktop) para conectarte al VPS
   - Copia el archivo ZIP al VPS
   - Descomprime en: `C:\BOT\trading-bot\`

### Opción B: Usar Git (Recomendado)

```powershell
# En el VPS, ejecuta:
cd C:\BOT
git clone [tu-repositorio] trading-bot
cd trading-bot
```

---

## 🎯 PASO 2: Instalar Dependencias en VPS

### 1. Verificar Python

```powershell
python --version
# Debe ser Python 3.10 o superior
```

Si no está instalado:
```powershell
# Descarga Python desde python.org
# O usa winget:
winget install Python.Python.3.12
```

### 2. Instalar Módulos

```powershell
cd C:\BOT\trading-bot
pip install -r requirements.txt
```

O manualmente:
```powershell
pip install MetaTrader5 pandas numpy python-dotenv
```

### 3. Instalar MetaTrader 5

1. Descarga MT5 desde: https://www.metatrader5.com/es/download
2. Instala en el VPS
3. Conéctate a tu cuenta Zeven (94342)
4. Verifica que XAUUSD.vip esté visible

---

## 🎯 PASO 3: Configurar .env

Crea el archivo `.env` en la raíz del proyecto:

```env
MT5_LOGIN=94342
MT5_PASSWORD=TuContraseñaReal
MT5_SERVER=ZevenGlobal-Live
MT5_SYMBOL=XAUUSD.vip
RISK_PER_TRADE=0.01
MAX_CONCURRENT_TRADES=3
MIN_RR=1.5
```

**Ubicación:** `C:\BOT\trading-bot\.env`

---

## 🎯 PASO 4: Probar Conexión

```powershell
cd C:\BOT\trading-bot
python test_mt5_connection.py
```

**Debe mostrar:**
- ✅ MT5 inicializado
- ✅ Conectado a cuenta
- ✅ Símbolo disponible

---

## 🎯 PASO 5: Ejecutar el Bot

### Opción A: Ejecución Manual

```powershell
cd C:\BOT\trading-bot
python -u live\mt5_trading.py
```

### Opción B: Script de Inicio (Recomendado)

Crea `INICIAR_BOT_VPS.bat`:

```batch
@echo off
chcp 65001 >nul 2>&1
cd /d "C:\BOT\trading-bot"
set PYTHONUNBUFFERED=1
python -u live\mt5_trading.py
pause
```

Ejecuta haciendo doble clic o desde consola.

---

## 🎯 PASO 6: Ejecutar como Servicio (24/7)

### Opción A: Usar NSSM (Non-Sucking Service Manager)

1. **Descarga NSSM:**
   - https://nssm.cc/download
   - Extrae en `C:\nssm\`

2. **Instala como servicio:**
   ```powershell
   cd C:\nssm\win64
   .\nssm.exe install TradingBot "C:\Python312\python.exe" "-u C:\BOT\trading-bot\live\mt5_trading.py"
   ```

3. **Configura el servicio:**
   ```powershell
   .\nssm.exe set TradingBot AppDirectory "C:\BOT\trading-bot"
   .\nssm.exe set TradingBot AppStdout "C:\BOT\trading-bot\logs\bot.log"
   .\nssm.exe set TradingBot AppStderr "C:\BOT\trading-bot\logs\bot_error.log"
   ```

4. **Inicia el servicio:**
   ```powershell
   .\nssm.exe start TradingBot
   ```

### Opción B: Usar Task Scheduler (Windows)

1. Abre **Task Scheduler** (Programador de tareas)
2. Crea tarea básica:
   - **Nombre:** Trading Bot
   - **Trigger:** Al iniciar sesión
   - **Acción:** Iniciar programa
   - **Programa:** `C:\Python312\python.exe`
   - **Argumentos:** `-u C:\BOT\trading-bot\live\mt5_trading.py`
   - **Directorio:** `C:\BOT\trading-bot`
   - **Opciones:** Ejecutar aunque el usuario no haya iniciado sesión

---

## 🎯 PASO 7: Monitorear el Bot

### Ver Logs en Tiempo Real

```powershell
# Si usas NSSM:
Get-Content C:\BOT\trading-bot\logs\bot.log -Wait -Tail 50

# Si ejecutas manualmente:
# Los mensajes aparecen en la consola
```

### Verificar que Está Corriendo

```powershell
# Ver procesos Python:
tasklist | findstr python

# Ver si MT5 está abierto:
tasklist | findstr terminal64
```

---

## 🔧 Scripts Útiles para VPS

### INICIAR_BOT_VPS.bat

```batch
@echo off
chcp 65001 >nul 2>&1
echo ========================================
echo   INICIANDO BOT DE TRADING EN VPS
echo ========================================
cd /d "C:\BOT\trading-bot"
set PYTHONUNBUFFERED=1
python -u live\mt5_trading.py
pause
```

### DETENER_BOT_VPS.bat

```batch
@echo off
echo Deteniendo bot de trading...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *mt5_trading*"
echo Bot detenido.
pause
```

### VERIFICAR_BOT_VPS.bat

```batch
@echo off
echo ========================================
echo   VERIFICANDO ESTADO DEL BOT
echo ========================================
echo.
echo Procesos Python activos:
tasklist | findstr python
echo.
echo Procesos MT5 activos:
tasklist | findstr terminal64
echo.
echo ========================================
pause
```

---

## 📊 Configuración Recomendada para VPS

### Recursos Mínimos:
- **CPU:** 2 cores
- **RAM:** 4 GB
- **Disco:** 20 GB
- **Sistema:** Windows Server 2019/2022 o Windows 10/11

### Configuración de MT5:
- ✅ AutoTrading habilitado
- ✅ Trading algorítmico activado
- ✅ Símbolo XAUUSD.vip visible
- ✅ Cuenta conectada

---

## 🚨 Solución de Problemas

### El bot no inicia:
1. Verifica que MT5 esté abierto y conectado
2. Verifica que `.env` existe y tiene credenciales correctas
3. Verifica que Python y módulos estén instalados

### El bot se detiene:
1. Verifica logs de errores
2. Verifica conexión a internet
3. Verifica que MT5 siga conectado

### No aparecen señales:
- **Normal:** El bot ahora requiere 3 confirmaciones (más selectivo)
- Espera a que se cumplan las condiciones
- Revisa los mensajes de análisis cada 3 minutos

---

## ✅ Checklist Final

Antes de dejar el bot corriendo 24/7:

- [ ] Python 3.10+ instalado
- [ ] Módulos instalados (MetaTrader5, pandas, numpy, dotenv)
- [ ] MetaTrader 5 instalado y conectado
- [ ] Archivo `.env` configurado correctamente
- [ ] Bot probado manualmente (funciona)
- [ ] Bot configurado como servicio o tarea programada
- [ ] Logs configurados para monitoreo
- [ ] AutoTrading habilitado en MT5

---

## 🎯 Próximos Pasos

1. **Sube el proyecto al VPS**
2. **Instala dependencias**
3. **Configura `.env`**
4. **Prueba manualmente**
5. **Configura como servicio**
6. **Monitorea los primeros días**

¡El bot está listo para operar 24/7 con 3 confirmaciones! 🚀

