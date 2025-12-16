# ✅ Dependencias Instaladas - Siguiente Paso

## ✅ COMPLETADO

- [x] Python 3.12 instalado
- [x] python-dotenv instalado
- [x] pandas instalado
- [x] numpy instalado
- [x] MetaTrader5 instalado (versión 5.0.5430)

---

## Paso 1: Verificar MetaTrader5

Ejecuta este comando para verificar que MetaTrader5 funciona:

```powershell
py -3.12 -c "import MetaTrader5; print('✅ MetaTrader5 OK')"
```

**Deberías ver:** `✅ MetaTrader5 OK`

---

## Paso 2: Copiar Proyecto a Windows

Ahora necesitas copiar el proyecto desde Mac a Windows.

### Opción A: Carpeta Compartida (Recomendado)

1. En Parallels: **Configuración** (⚙️) → **Opciones** → **Compartir**
2. Marca ✅ **"Compartir Mac"**
3. En Windows: Abre **Explorador de archivos**
4. Ve a **Red** → **Mac** → Busca la carpeta del proyecto
5. Copia toda la carpeta a `C:\trading-bot`

### Opción B: Usar ZIP

1. En Mac, el ZIP está en: `trading-bot-windows-20251210.zip` (si existe)
2. Copia el ZIP a Windows (carpeta compartida, USB, etc.)
3. En Windows, descomprime en `C:\trading-bot`

---

## Paso 3: Verificar Estructura del Proyecto

En PowerShell:

```powershell
cd C:\trading-bot
dir
```

Deberías ver:
- `backtest/`
- `live/`
- `strategy/`
- `utils/`
- `config.py`
- `setup_mt5.py`
- `test_mt5_connection.py`
- etc.

---

## Paso 4: Instalar MetaTrader 5 (La Aplicación)

1. Abre navegador en Windows
2. Ve a: https://www.metatrader5.com/es/download
3. Descarga **MetaTrader 5 para Windows**
4. Instala MT5
5. Abre MT5 y conéctate a tu cuenta Zeven:
   - Archivo → Iniciar sesión en cuenta comercial
   - Servidor: `ZevenGlobal-Demo` (o `ZevenGlobal-Real`)
   - Login: Tu número de cuenta
   - Contraseña: Tu contraseña
   - Clic en "Iniciar sesión"

---

## Paso 5: Configurar Credenciales del Bot

En PowerShell (con el proyecto en `C:\trading-bot`):

```powershell
cd C:\trading-bot
py -3.12 setup_mt5.py
```

Ingresa:
- Número de cuenta MT5
- Contraseña
- Servidor (ej: `ZevenGlobal-Demo`)
- Símbolo (ej: `XAUUSD`)

---

## Paso 6: Probar Conexión

**IMPORTANTE:** MT5 debe estar abierto y conectado.

```powershell
py -3.12 test_mt5_connection.py
```

Deberías ver: `✅ PRUEBA COMPLETADA EXITOSAMENTE`

---

## Paso 7: Ejecutar Bot

**IMPORTANTE:** MT5 debe estar abierto y conectado.

```powershell
py -3.12 live/mt5_trading.py
```

Para detener: Presiona `Ctrl+C`

---

## 🎯 Progreso Actual

**Completado: ~50%**

✅ Python 3.12 instalado
✅ Dependencias instaladas
⏳ Proyecto en Windows (siguiente paso)
⏳ MT5 instalado
⏳ Configuración final

---

## 📝 Nota sobre pip

Hay un aviso sobre actualizar pip, pero no es crítico. Si quieres actualizarlo:

```powershell
py -3.12 -m pip install --upgrade pip
```

Pero no es necesario para continuar.

---

¡Siguiente paso: Copiar el proyecto a Windows! 🚀







