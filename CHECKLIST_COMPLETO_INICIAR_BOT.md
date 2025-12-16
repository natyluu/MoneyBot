# ✅ CHECKLIST COMPLETO: ¿Qué falta para iniciar el bot?

## 🔍 VERIFICACIÓN PASO A PASO

### 1️⃣ ARCHIVOS NECESARIOS

Verifica que estos archivos existan en Windows:
```
C:\BOT\trading-bot-windows-20251210 on 'Mac'\
├── config.py                    ✅ REQUERIDO
├── .env                         ✅ REQUERIDO (con credenciales)
├── live\
│   └── mt5_trading.py          ✅ REQUERIDO
├── strategy\
│   └── ict_hybrid_strategy.py  ✅ REQUERIDO
└── requirements.txt            ✅ REQUERIDO
```

**Para verificar en Windows:**
```powershell
cd "C:\BOT\trading-bot-windows-20251210 on 'Mac'"
dir config.py
dir .env
dir live\mt5_trading.py
dir strategy\ict_hybrid_strategy.py
```

---

### 2️⃣ ARCHIVO .env CON CREDENCIALES

El archivo `.env` debe existir y contener:

```env
MT5_LOGIN=94342
MT5_PASSWORD=TuContraseña
MT5_SERVER=ZevenGlobal-Live
MT5_SYMBOL=XAUUSD.vip
RISK_PER_TRADE=0.01
MAX_CONCURRENT_TRADES=3
MIN_RR=2.0
```

**Para verificar:**
```powershell
type .env
```

**Si NO existe, créalo:**
1. Abre Notepad
2. Copia el contenido de arriba
3. Reemplaza `TuContraseña` con tu contraseña real
4. Guarda como `.env` (con el punto al inicio)
5. Ubicación: `C:\BOT\trading-bot-windows-20251210 on 'Mac'\.env`

---

### 3️⃣ PYTHON 3.12 INSTALADO

**Verificar:**
```powershell
python --version
```

**Debe mostrar:** `Python 3.12.x`

**Si NO está instalado:**
1. Descarga Python 3.12 desde: https://www.python.org/downloads/
2. Durante la instalación, marca ✅ **"Add Python to PATH"**
3. Reinicia PowerShell después de instalar

---

### 4️⃣ MÓDULOS PYTHON INSTALADOS

**Verificar cada módulo:**
```powershell
python -c "import MetaTrader5; print('OK')"
python -c "import pandas; print('OK')"
python -c "import numpy; print('OK')"
python -c "import dotenv; print('OK')"
```

**Si alguno falla, instálalo:**
```powershell
pip install MetaTrader5
pip install pandas
pip install numpy
pip install python-dotenv
```

**O instala todos de una vez:**
```powershell
pip install -r requirements.txt
```

---

### 5️⃣ METATRADER 5 ABIERTO Y CONECTADO

**Verificar que MT5 está abierto:**
```powershell
tasklist | findstr terminal64
```

**Si NO está abierto:**
1. Abre MetaTrader 5
2. Conéctate a tu cuenta:
   - Servidor: `ZevenGlobal-Live`
   - Login: `94342`
   - Contraseña: Tu contraseña
3. Verifica que **XAUUSD.vip** esté visible en Market Watch

---

### 6️⃣ ESTRUCTURA DEL PROYECTO

**Verificar estructura completa:**
```powershell
cd "C:\BOT\trading-bot-windows-20251210 on 'Mac'"
dir
dir live
dir strategy
```

**Debes ver:**
- Carpeta `live\` con `mt5_trading.py`
- Carpeta `strategy\` con `ict_hybrid_strategy.py`
- Archivo `config.py` en la raíz
- Archivo `.env` en la raíz

---

## 🚀 SCRIPT DE VERIFICACIÓN AUTOMÁTICA

Ejecuta este script para verificar todo automáticamente:

**En Windows, haz doble clic en:**
```
TEST_BOT.bat
```

Este script verificará:
- ✅ Archivos necesarios
- ✅ Python instalado
- ✅ Módulos instalados
- ✅ MT5 abierto
- ✅ Estructura del proyecto

---

## 📋 RESUMEN: QUÉ FALTA

Marca cada punto cuando esté completo:

- [ ] **Archivo .env existe** con credenciales correctas
- [ ] **Python 3.12 instalado** y en PATH
- [ ] **MetaTrader5 instalado** (`pip install MetaTrader5`)
- [ ] **pandas instalado** (`pip install pandas`)
- [ ] **numpy instalado** (`pip install numpy`)
- [ ] **python-dotenv instalado** (`pip install python-dotenv`)
- [ ] **MetaTrader 5 abierto** y conectado a cuenta 94342
- [ ] **XAUUSD.vip visible** en Market Watch
- [ ] **Archivos del proyecto** en `C:\BOT\trading-bot-windows-20251210 on 'Mac'`

---

## ✅ CUANDO TODO ESTÉ LISTO

1. Abre MetaTrader 5 y conéctate
2. Haz doble clic en: `INICIAR_BOT_FINAL.bat`
3. El bot debería iniciarse

---

## 🆘 SI ALGO FALLA

Ejecuta `TEST_BOT.bat` y comparte el resultado completo para identificar qué falta específicamente.




