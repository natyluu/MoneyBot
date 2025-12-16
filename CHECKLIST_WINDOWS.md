# ✅ Checklist: Configurar Windows para el Bot

Usa este checklist para asegurarte de que todo esté configurado correctamente.

## 📋 FASE 1: Instalación de Windows

- [ ] Parallels Desktop instalado y abierto
- [ ] Windows 11 (o Windows 10) instalado en Parallels
- [ ] Windows arranca correctamente
- [ ] Puedes ver el escritorio de Windows

**Tiempo estimado:** 30-60 minutos

---

## 📋 FASE 2: Configuración Básica de Windows

- [ ] Windows configurado (cuenta Microsoft o local)
- [ ] Navegador funcionando (Edge o Chrome)
- [ ] Explorador de archivos funcionando
- [ ] PowerShell funciona (clic derecho → "Abrir PowerShell aquí")

---

## 📋 FASE 3: Instalar Python

- [ ] Python descargado desde python.org
- [ ] Python instalado con **"Add Python to PATH"** marcado ✅
- [ ] Verificación: `python --version` funciona en PowerShell
- [ ] Verificación: `pip --version` funciona en PowerShell

**Comandos de verificación:**
```powershell
python --version
pip --version
```

---

## 📋 FASE 4: Copiar Proyecto a Windows

### Opción A: Carpeta Compartida (Recomendado)

- [ ] Parallels → Configuración → Opciones → Compartir → "Compartir Mac" ✅
- [ ] En Windows: Explorador → Red → Mac → Encontrar carpeta del proyecto
- [ ] Proyecto copiado a `C:\trading-bot`

### Opción B: Usar ZIP

- [ ] ZIP copiado a Windows (USB, carpeta compartida, etc.)
- [ ] ZIP descomprimido en `C:\trading-bot`
- [ ] Estructura del proyecto visible en `C:\trading-bot`

**Verificación:**
```powershell
cd C:\trading-bot
dir
```

Deberías ver: `backtest/`, `live/`, `strategy/`, `utils/`, `config.py`, etc.

---

## 📋 FASE 5: Instalar Dependencias

- [ ] Navegado a `C:\trading-bot` en PowerShell
- [ ] Dependencias instaladas: `pip install MetaTrader5 python-dotenv pandas numpy`
- [ ] Sin errores en la instalación
- [ ] Verificación: `python -c "import MetaTrader5; print('OK')"` funciona

**Comandos:**
```powershell
cd C:\trading-bot
pip install MetaTrader5 python-dotenv pandas numpy
python -c "import MetaTrader5; print('✅ MetaTrader5 OK')"
```

---

## 📋 FASE 6: Instalar MetaTrader 5

- [ ] MT5 descargado desde metatrader5.com
- [ ] MT5 instalado en Windows
- [ ] MT5 abierto y funcionando
- [ ] Conectado a cuenta Zeven (DEMO o REAL)
- [ ] Símbolo XAUUSD visible en el mercado

**URL:** https://www.metatrader5.com/es/download

---

## 📋 FASE 7: Configurar Credenciales del Bot

- [ ] Ejecutado: `python setup_mt5.py`
- [ ] Credenciales ingresadas:
  - [ ] Número de cuenta MT5
  - [ ] Contraseña
  - [ ] Servidor (ZevenGlobal-Demo o ZevenGlobal-Real)
  - [ ] Símbolo (XAUUSD)
- [ ] Archivo `.env` creado en `C:\trading-bot`

**Comando:**
```powershell
cd C:\trading-bot
python setup_mt5.py
```

---

## 📋 FASE 8: Probar Conexión

- [ ] MT5 abierto y conectado
- [ ] Ejecutado: `python test_mt5_connection.py`
- [ ] Mensaje: "✅ PRUEBA COMPLETADA EXITOSAMENTE"
- [ ] Sin errores de conexión

**Comando:**
```powershell
python test_mt5_connection.py
```

---

## 📋 FASE 9: Ejecutar Bot (Primera Vez)

- [ ] MT5 abierto y conectado
- [ ] Ejecutado: `python live/mt5_trading.py`
- [ ] Bot se conecta a MT5
- [ ] Bot obtiene datos multi-timeframe
- [ ] Bot muestra análisis (aunque no haya señales aún)
- [ ] Bot funciona sin errores

**Comando:**
```powershell
python live/mt5_trading.py
```

**Para detener:** Presiona `Ctrl+C`

---

## 📋 FASE 10: Verificación Final

- [ ] Bot ejecutándose sin errores
- [ ] Bot analiza mercado en tiempo real
- [ ] Bot muestra mensajes de análisis
- [ ] Entiendes cómo funciona el bot
- [ ] Sabes cómo detener el bot (`Ctrl+C`)
- [ ] Sabes cómo reiniciar el bot

---

## ⚠️ Problemas Comunes

### Python no se encuentra
- **Solución:** Reinstala Python y marca "Add Python to PATH"

### MetaTrader5 no se instala
- **Solución:** `python -m pip install --upgrade pip` y luego `pip install MetaTrader5`

### No puede conectar a MT5
- **Solución:** Verifica que MT5 esté abierto y conectado a tu cuenta

### No encuentra el proyecto
- **Solución:** Verifica la ruta `C:\trading-bot` y que el proyecto esté copiado

---

## 🎯 Estado Actual

Marca las fases que ya completaste:

- [ ] FASE 1: Instalación de Windows
- [ ] FASE 2: Configuración Básica
- [ ] FASE 3: Instalar Python
- [ ] FASE 4: Copiar Proyecto
- [ ] FASE 5: Instalar Dependencias
- [ ] FASE 6: Instalar MT5
- [ ] FASE 7: Configurar Credenciales
- [ ] FASE 8: Probar Conexión
- [ ] FASE 9: Ejecutar Bot
- [ ] FASE 10: Verificación Final

---

## 📞 Siguiente Paso

Una vez que completes cada fase, avísame y te guío para la siguiente.

¡Vamos paso a paso! 🚀







