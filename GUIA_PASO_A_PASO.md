# 🚀 Guía Paso a Paso: Conectar a MT5 con Zeven

Sigue estos pasos en orden para conectar tu bot a MetaTrader 5.

## ✅ PASO 1: Verificar Python

Ya tienes Python 3.9.6 instalado. ✅

## 📦 PASO 2: Instalar Dependencias

Ejecuta estos comandos en tu terminal:

```bash
cd "/Users/nataliaturizo/bot de trader"

# Actualiza pip
python3 -m pip install --upgrade pip

# Instala dependencias básicas
python3 -m pip install python-dotenv pandas numpy

# Instala MetaTrader5
python3 -m pip install MetaTrader5
```

**Si MetaTrader5 no se instala**, intenta:
```bash
pip3 install MetaTrader5
```

O visita: https://pypi.org/project/MetaTrader5/

## 🔍 PASO 3: Verificar Instalación

Ejecuta para verificar que todo esté instalado:

```bash
python3 -c "import MetaTrader5; import pandas; import dotenv; print('✅ Todo OK')"
```

## 📥 PASO 4: Instalar MetaTrader 5 (Aplicación)

Si no tienes MT5 instalado:

1. Ve a: https://www.metatrader5.com/es/download
2. Descarga e instala MetaTrader 5
3. Ábrelo y conéctate a tu cuenta Zeven

## ⚙️ PASO 5: Configurar Credenciales

Tienes dos opciones:

### Opción A: Script Interactivo (Recomendado)

```bash
python3 setup_mt5.py
```

Este script te pedirá:
- Número de cuenta MT5
- Contraseña
- Tipo de cuenta (Demo/Real)
- Símbolo (default: XAUUSD)

### Opción B: Manual

Crea un archivo `.env` en la raíz del proyecto:

```bash
nano .env
```

Y agrega:

```env
MT5_LOGIN=tu_numero_cuenta
MT5_PASSWORD=tu_password
MT5_SERVER=ZevenGlobal-Demo
MT5_SYMBOL=XAUUSD
RISK_PER_TRADE=0.01
MAX_CONCURRENT_TRADES=3
MIN_RR=2.0
```

**⚠️ IMPORTANTE:**
- NO subas el archivo `.env` a Git
- Usa cuenta **DEMO** primero
- Verifica el nombre exacto del servidor en MT5

## 🔌 PASO 6: Abrir MetaTrader 5

**ANTES de probar la conexión:**

1. Abre MetaTrader 5 en tu computadora
2. Conéctate a tu cuenta Zeven
3. Verifica que el símbolo XAUUSD esté visible en Market Watch
   - Si no aparece: Clic derecho → "Mostrar todos"
   - Anota el nombre exacto (puede ser "XAUUSD" o "XAUUSD.m")

## 🧪 PASO 7: Probar la Conexión

Con MT5 abierto y conectado, ejecuta:

```bash
python3 test_mt5_connection.py
```

Este script verificará:
- ✅ Que MT5 esté funcionando
- ✅ Que tus credenciales sean correctas
- ✅ Que el símbolo XAUUSD esté disponible
- ✅ Que puedas obtener datos

### Si hay errores:

**"No se pudo inicializar MT5"**
- Verifica que MT5 esté **abierto**
- Intenta ejecutar como administrador

**"Error al conectar"**
- Verifica credenciales en `.env`
- Verifica que el servidor sea correcto
- Asegúrate de estar conectado a internet

**"Símbolo no encontrado"**
- Verifica el nombre exacto en MT5
- Actualiza `MT5_SYMBOL` en `.env`

## 🚀 PASO 8: Ejecutar el Bot

Si la prueba fue exitosa, ejecuta el bot:

```bash
python3 live/mt5_trading.py
```

El bot:
- Se conectará automáticamente
- Obtendrá datos en tiempo real
- Generará señales ICT
- Ejecutará órdenes automáticamente

**Para detener:** Presiona `Ctrl+C`

## 📋 Resumen de Comandos

```bash
# 1. Instalar dependencias
python3 -m pip install python-dotenv pandas numpy MetaTrader5

# 2. Configurar credenciales
python3 setup_mt5.py

# 3. Probar conexión (con MT5 abierto)
python3 test_mt5_connection.py

# 4. Ejecutar bot
python3 live/mt5_trading.py
```

## ⚠️ Recordatorios

1. **Siempre usa cuenta DEMO primero**
2. **Abre MT5 antes de ejecutar el bot**
3. **Monitorea el bot regularmente**
4. **No arriesgues más del 1-2% por operación**

## 🆘 ¿Necesitas Ayuda?

- Revisa `INSTRUCCIONES_MT5.md` para más detalles
- Verifica los mensajes de error en la consola
- Asegúrate de que MT5 esté abierto y conectado

¡Listo para empezar! 🎉












