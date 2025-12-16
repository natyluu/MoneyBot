# Instrucciones para Conectar a MT5 con Zeven

Esta guía te ayudará a conectar tu bot de trading con MetaTrader 5 y el broker Zeven.

## 📋 Paso 1: Instalar Dependencias

Primero, asegúrate de tener todas las dependencias instaladas:

```bash
pip3 install -r requirements.txt
```

O instala manualmente:

```bash
pip3 install MetaTrader5 python-dotenv pandas numpy
```

## 📋 Paso 2: Instalar MetaTrader 5

Si no tienes MT5 instalado:

1. **Descarga MetaTrader 5:**
   - Ve a: https://www.metatrader5.com/es/download
   - Descarga e instala la versión para tu sistema operativo

2. **Abre MetaTrader 5** y asegúrate de que esté funcionando

## 📋 Paso 3: Obtener Credenciales de Zeven

Necesitas tus credenciales de cuenta Zeven:

1. **Si tienes cuenta Demo:**
   - Abre MT5
   - Ve a "Herramientas" → "Opciones" → "Servidor"
   - O crea una cuenta demo desde el sitio de Zeven

2. **Si tienes cuenta Real:**
   - Usa las credenciales que te dio Zeven al abrir la cuenta
   - **⚠️ IMPORTANTE:** Empieza siempre con cuenta DEMO

3. **Anota:**
   - Número de cuenta (ej: 1234567)
   - Contraseña
   - Nombre del servidor (ej: "ZevenGlobal-Demo" o "ZevenGlobal-Real")

## 📋 Paso 4: Configurar el Bot

### Opción A: Configuración Automática (Recomendada)

Ejecuta el script de configuración guiada:

```bash
python3 setup_mt5.py
```

Este script te pedirá:
- Número de cuenta MT5
- Contraseña
- Tipo de cuenta (Demo/Real)
- Símbolo a operar (default: XAUUSD)
- Configuración de riesgo

### Opción B: Configuración Manual

1. Crea un archivo `.env` en la raíz del proyecto:

```bash
touch .env
```

2. Edita el archivo `.env` con tus credenciales:

```env
MT5_LOGIN=1234567
MT5_PASSWORD=tu_password_aqui
MT5_SERVER=ZevenGlobal-Demo
MT5_SYMBOL=XAUUSD

RISK_PER_TRADE=0.01
MAX_CONCURRENT_TRADES=3
MIN_RR=2.0
```

**⚠️ IMPORTANTE:**
- NO subas el archivo `.env` a Git (está en `.gitignore`)
- Usa cuenta DEMO primero
- Verifica el nombre exacto del servidor en MT5

## 📋 Paso 5: Verificar el Símbolo XAUUSD

En MetaTrader 5:

1. Abre la ventana "Market Watch" (Ctrl+M)
2. Busca "XAUUSD" o "GOLD"
3. Si no aparece, haz clic derecho → "Mostrar todos"
4. Verifica el nombre exacto (puede ser "XAUUSD" o "XAUUSD.m")
5. Actualiza el valor de `MT5_SYMBOL` en `.env` si es diferente

## 📋 Paso 6: Probar la Conexión

Ejecuta el script de prueba:

```bash
python3 test_mt5_connection.py
```

Este script verificará:
- ✅ Que MT5 esté instalado y funcionando
- ✅ Que las credenciales sean correctas
- ✅ Que el símbolo XAUUSD esté disponible
- ✅ Que puedas obtener datos del mercado

### Si hay errores:

**Error: "No se pudo inicializar MT5"**
- Verifica que MetaTrader 5 esté abierto
- Intenta ejecutar como administrador
- Reinstala MT5 si es necesario

**Error: "Error al conectar"**
- Verifica que las credenciales sean correctas
- Verifica que el servidor sea el correcto (Demo vs Real)
- Asegúrate de estar conectado a internet
- Verifica que la cuenta no esté bloqueada

**Error: "Símbolo no encontrado"**
- Verifica el nombre exacto del símbolo en MT5
- Puede ser "XAUUSD" o "XAUUSD.m"
- Activa el símbolo en MT5 (clic derecho → Mostrar)

## 📋 Paso 7: Ejecutar el Bot

Una vez que la prueba sea exitosa, puedes ejecutar el bot:

```bash
python3 live/mt5_trading.py
```

El bot:
- Se conectará automáticamente a MT5
- Obtendrá datos del mercado en tiempo real
- Generará señales usando tu estrategia ICT
- Ejecutará órdenes automáticamente

**Para detener el bot:** Presiona `Ctrl+C`

## 🔧 Solución de Problemas Comunes

### Problema: "ModuleNotFoundError: No module named 'MetaTrader5'"

**Solución:**
```bash
pip3 install MetaTrader5
```

### Problema: "MT5_LOGIN is 0" o credenciales vacías

**Solución:**
- Verifica que el archivo `.env` exista
- Verifica que tenga el formato correcto
- No uses espacios alrededor del `=`

### Problema: El símbolo no se encuentra

**Solución:**
1. En MT5, ve a Market Watch
2. Haz clic derecho → "Símbolos"
3. Busca "XAUUSD" o "GOLD"
4. Anota el nombre exacto
5. Actualiza `MT5_SYMBOL` en `.env`

### Problema: "Orden rechazada"

**Solución:**
- Verifica que tengas suficiente margen
- Verifica que el símbolo esté disponible para trading
- Verifica que los precios SL/TP sean válidos
- Revisa los logs de MT5 para más detalles

## 📞 Soporte

Si tienes problemas:

1. Revisa los mensajes de error en la consola
2. Verifica que MT5 esté abierto y conectado
3. Prueba conectarte manualmente desde MT5 primero
4. Consulta la documentación de MetaTrader 5

## ⚠️ Recordatorios Importantes

1. **Siempre usa cuenta DEMO primero**
2. **No arriesgues más del 1-2% por operación**
3. **Monitorea el bot regularmente**
4. **El trading automático conlleva riesgo real**
5. **Los resultados pasados no garantizan resultados futuros**

## ✅ Checklist de Verificación

Antes de ejecutar el bot en vivo, verifica:

- [ ] MetaTrader 5 está instalado y funcionando
- [ ] Tienes cuenta Zeven (preferiblemente Demo)
- [ ] Archivo `.env` creado con credenciales correctas
- [ ] Script de prueba (`test_mt5_connection.py`) ejecuta sin errores
- [ ] El símbolo XAUUSD está disponible en MT5
- [ ] Puedes obtener precios y velas desde MT5
- [ ] Entiendes los riesgos del trading automático

¡Listo! Ahora puedes empezar a operar con tu bot de trading ICT.













