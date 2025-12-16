# 📋 COPIAR ARCHIVOS DESDE MAC A WINDOWS

## Si la sincronización de Parallels no funciona

---

## MÉTODO 1: Usar el Explorador de Windows

### Paso 1: En Windows
1. Abre el **Explorador de Windows**
2. En la barra de direcciones, escribe:
   ```
   \\Mac\Home\bot de trader
   ```
3. Presiona Enter

### Paso 2: Si no funciona, busca la carpeta compartida
1. Abre el **Explorador de Windows**
2. En el panel izquierdo, busca **"Mac"** o **"Parallels Shared Folders"**
3. Navega hasta: `bot de trader`

### Paso 3: Copiar archivos
1. Selecciona estos archivos/carpetas:
   - `live` (carpeta completa)
   - `strategy` (carpeta completa)
   - `config.py`
   - `.env`
   - `requirements.txt`
   - `*.bat` (todos los scripts .bat)
   - `*.ps1` (todos los scripts .ps1)

2. Copia (Ctrl+C)

3. Ve a: `C:\BOT\trading-bot-windows-20251210 on 'Mac'`

4. Pega (Ctrl+V)

---

## MÉTODO 2: Usar CMD para copiar

### En Windows (CMD):

```cmd
REM Crear directorio si no existe
mkdir "C:\BOT\trading-bot-windows-20251210 on 'Mac'" 2>nul

REM Copiar desde la carpeta compartida
xcopy "\\Mac\Home\bot de trader\live" "C:\BOT\trading-bot-windows-20251210 on 'Mac'\live\" /E /I /Y
xcopy "\\Mac\Home\bot de trader\strategy" "C:\BOT\trading-bot-windows-20251210 on 'Mac'\strategy\" /E /I /Y
copy "\\Mac\Home\bot de trader\config.py" "C:\BOT\trading-bot-windows-20251210 on 'Mac'\"
copy "\\Mac\Home\bot de trader\.env" "C:\BOT\trading-bot-windows-20251210 on 'Mac'\"
copy "\\Mac\Home\bot de trader\requirements.txt" "C:\BOT\trading-bot-windows-20251210 on 'Mac'\"
copy "\\Mac\Home\bot de trader\*.bat" "C:\BOT\trading-bot-windows-20251210 on 'Mac'\"
copy "\\Mac\Home\bot de trader\*.ps1" "C:\BOT\trading-bot-windows-20251210 on 'Mac'\"
```

---

## MÉTODO 3: Crear ZIP en Mac y copiar

### En macOS (Terminal):

```bash
cd "/Users/nataliaturizo/bot de trader"
zip -r proyecto_windows.zip live/ strategy/ config.py .env requirements.txt *.bat *.ps1 -x "*.pyc" "__pycache__/*"
```

### En Windows:
1. Abre el Explorador
2. Ve a: `\\Mac\Home\bot de trader`
3. Copia `proyecto_windows.zip`
4. Extráelo en: `C:\BOT\trading-bot-windows-20251210 on 'Mac'`

---

## VERIFICAR DESPUÉS DE COPIAR

Ejecuta en Windows:

```cmd
cd "C:\BOT\trading-bot-windows-20251210 on 'Mac'"
VERIFICAR_ARCHIVOS_WINDOWS.bat
```

O manualmente:

```cmd
dir live\mt5_trading.py
dir config.py
dir strategy\ict_hybrid_strategy.py
dir .env
```

---

## ARCHIVOS CRÍTICOS QUE DEBEN COPIARSE

1. ✅ `live/mt5_trading.py` - Script principal del bot
2. ✅ `config.py` - Configuración
3. ✅ `strategy/ict_hybrid_strategy.py` - Estrategia de trading
4. ✅ `.env` - Credenciales (importante: no compartir públicamente)
5. ✅ `requirements.txt` - Dependencias de Python

---

## DESPUÉS DE COPIAR

1. Verifica que todos los archivos estén presentes
2. Ejecuta: `python -u live\mt5_trading.py`
3. Si hay errores de módulos, ejecuta: `pip install -r requirements.txt`




