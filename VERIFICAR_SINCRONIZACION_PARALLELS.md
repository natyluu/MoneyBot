# 🔄 VERIFICAR SINCRONIZACIÓN PARALLELS

## PROBLEMA
Los cambios en macOS no aparecen en Windows (disco C)

## SOLUCIÓN: Verificar y corregir la sincronización

---

## PASO 1: Verificar la carpeta compartida en Parallels

### En macOS:
1. Abre **Parallels Desktop**
2. Ve a **Configuración** (Settings) de tu VM Windows
3. Busca **Opciones** → **Compartir**
4. Verifica que:
   - ✅ **Compartir Mac** esté activado
   - ✅ La carpeta del proyecto esté en la lista de carpetas compartidas

### Ubicación del proyecto en macOS:
```
/Users/nataliaturizo/bot de trader
```

### Ubicación en Windows (debería ser):
```
C:\BOT\trading-bot-windows-20251210 on 'Mac'
```

O podría estar en:
```
\\Mac\Home\bot de trader
```

---

## PASO 2: Verificar archivos en Windows

### En Windows (CMD o PowerShell):

```cmd
cd "C:\BOT\trading-bot-windows-20251210 on 'Mac'"
dir live\mt5_trading.py
```

Si NO aparece el archivo, la sincronización NO está funcionando.

---

## PASO 3: Verificar fecha de modificación

### En macOS (Terminal):
```bash
ls -la "live/mt5_trading.py"
```

### En Windows (CMD):
```cmd
dir live\mt5_trading.py
```

**Compara las fechas**. Si la fecha en Windows es más antigua, los archivos NO se están sincronizando.

---

## PASO 4: Soluciones

### OPCIÓN A: Forzar actualización en Parallels

1. En Parallels Desktop → **Configuración** → **Opciones** → **Compartir**
2. **Desactiva** "Compartir Mac"
3. **Aplica** cambios
4. **Activa** "Compartir Mac" de nuevo
5. **Aplica** cambios
6. Espera 30 segundos
7. Verifica de nuevo en Windows

### OPCIÓN B: Copiar manualmente (más confiable)

#### En macOS (Terminal):
```bash
cd "/Users/nataliaturizo/bot de trader"
# Verifica que los archivos existen
ls -la live/mt5_trading.py
ls -la config.py
ls -la strategy/ict_hybrid_strategy.py
```

#### En Windows:
1. Abre el **Explorador de Windows**
2. Ve a: `\\Mac\Home\bot de trader` (o la ruta que aparezca en Parallels)
3. Copia los archivos manualmente a: `C:\BOT\trading-bot-windows-20251210 on 'Mac'`

### OPCIÓN C: Usar red compartida

En Windows, accede directamente a la carpeta compartida:

```cmd
cd "\\Mac\Home\bot de trader"
python -u live\mt5_trading.py
```

---

## PASO 5: Verificar archivos críticos

### Archivos que DEBEN existir en Windows:

```
C:\BOT\trading-bot-windows-20251210 on 'Mac'\
├── live\
│   └── mt5_trading.py          ← CRÍTICO
├── config.py                   ← CRÍTICO
├── strategy\
│   └── ict_hybrid_strategy.py  ← CRÍTICO
├── .env                        ← CRÍTICO
└── requirements.txt
```

### Comando para verificar en Windows:

```cmd
cd "C:\BOT\trading-bot-windows-20251210 on 'Mac'"
dir live\mt5_trading.py
dir config.py
dir strategy\ict_hybrid_strategy.py
dir .env
```

---

## PASO 6: Si nada funciona - Copiar desde macOS

### En macOS (Terminal):
```bash
cd "/Users/nataliaturizo/bot de trader"
# Crear un ZIP con todos los archivos
zip -r proyecto_completo.zip live/ strategy/ config.py .env requirements.txt *.bat *.ps1
```

Luego en Windows:
1. Abre el Explorador
2. Ve a `\\Mac\Home\bot de trader`
3. Copia `proyecto_completo.zip`
4. Extráelo en `C:\BOT\trading-bot-windows-20251210 on 'Mac'`

---

## VERIFICACIÓN RÁPIDA

### En Windows, ejecuta:

```cmd
cd "C:\BOT\trading-bot-windows-20251210 on 'Mac'"
echo Verificando archivos...
if exist "live\mt5_trading.py" (echo OK: mt5_trading.py existe) else (echo ERROR: mt5_trading.py NO existe)
if exist "config.py" (echo OK: config.py existe) else (echo ERROR: config.py NO existe)
if exist "strategy\ict_hybrid_strategy.py" (echo OK: ict_hybrid_strategy.py existe) else (echo ERROR: ict_hybrid_strategy.py NO existe)
if exist ".env" (echo OK: .env existe) else (echo ERROR: .env NO existe)
```

---

## PRÓXIMOS PASOS

1. Ejecuta la verificación rápida en Windows
2. Comparte los resultados
3. Si faltan archivos, usamos la OPCIÓN B (copiar manualmente)




