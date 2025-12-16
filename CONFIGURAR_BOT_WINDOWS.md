# 🤖 Configurar el Bot en Windows - Guía Completa

Sigue estos pasos en orden. Cada paso es importante.

---

## ✅ PASO 1: Verificar Python

Abre PowerShell en Windows y ejecuta:

```powershell
python --version
pip --version
```

**Si no funciona:** Instala Python desde https://www.python.org/downloads/
⚠️ Marca "Add Python to PATH" durante la instalación

---

## ✅ PASO 2: Navegar al Proyecto

```powershell
cd C:\trading-bot
```

**Si no existe:** Copia el proyecto primero (ver `COPIAR_PROYECTO_WINDOWS.md`)

---

## ✅ PASO 3: Instalar Dependencias

```powershell
pip install MetaTrader5 python-dotenv pandas numpy
```

Espera a que termine (2-5 minutos).

**Verificar:**
```powershell
python -c "import MetaTrader5; print('✅ MetaTrader5 OK')"
```

Deberías ver: `✅ MetaTrader5 OK`

---

## ✅ PASO 4: Instalar MetaTrader 5

1. Abre navegador en Windows
2. Ve a: https://www.metatrader5.com/es/download
3. Descarga **MetaTrader 5 para Windows**
4. Instala MT5 (siguiente, siguiente, instalar)
5. Abre MT5
6. Conéctate a tu cuenta Zeven:
   - Archivo → Iniciar sesión en cuenta comercial
   - Servidor: `ZevenGlobal-Demo` (o `ZevenGlobal-Real`)
   - Login: Tu número de cuenta
   - Contraseña: Tu contraseña
   - Clic en "Iniciar sesión"

**Verifica que MT5 esté conectado:**
- Deberías ver el precio de XAUUSD en la ventana de mercado
- El símbolo debe estar visible

---

## ✅ PASO 5: Configurar Credenciales del Bot

En PowerShell (con el proyecto en `C:\trading-bot`):

```powershell
python setup_mt5.py
```

Ingresa:
- **Número de cuenta MT5:** (el mismo que usaste en MT5)
- **Contraseña:** (la misma que usaste en MT5)
- **Servidor:** `ZevenGlobal-Demo` (o `ZevenGlobal-Real`)
- **Símbolo:** `XAUUSD` (o `XAUUSD.m` si aparece así en MT5)

Esto creará el archivo `.env` con tus credenciales.

---

## ✅ PASO 6: Probar Conexión

**IMPORTANTE:** MT5 debe estar abierto y conectado.

En PowerShell:

```powershell
python test_mt5_connection.py
```

**Deberías ver:**
```
✅ Conexión a MT5 exitosa
✅ Símbolo XAUUSD disponible
✅ PRUEBA COMPLETADA EXITOSAMENTE
```

**Si hay errores:**
- Verifica que MT5 esté abierto
- Verifica que estés conectado a tu cuenta
- Verifica las credenciales en `.env`

---

## ✅ PASO 7: Ejecutar el Bot

**IMPORTANTE:** MT5 debe estar abierto y conectado.

En PowerShell:

```powershell
python live/mt5_trading.py
```

**El bot:**
- Se conectará a MT5
- Obtendrá datos en tiempo real
- Analizará el mercado con la estrategia ICT
- Mostrará análisis en la consola
- Ejecutará órdenes automáticamente si detecta señales válidas

**Para detener el bot:** Presiona `Ctrl+C`

---

## 📊 Qué Esperar

### Salida Normal del Bot

```
🚀 INICIANDO LOOP DE TRADING AUTOMÁTICO EN MT5
✅ Conexión a MT5 exitosa

[2024-12-11 10:30:00] Realizando análisis...
   Analizando en 2024-12-11 10:30:00...
   No se generó señal de trading válida.

[2024-12-11 10:31:00] Realizando análisis...
   ✅ Señal detectada: BUY
      RR estimado: 1:2.50, Mínimo requerido: 1:2.00
   Calculando lotaje: 0.01
   ✅ Orden enviada: BUY XAUUSD
```

### Si Hay Señales

El bot mostrará:
- Tipo de operación (BUY/SELL)
- Precio de entrada
- Stop Loss
- Take Profit
- Risk:Reward
- Justificaciones

---

## ⚠️ Configuración de Riesgo

El bot está configurado con:
- **Riesgo por operación:** 1% del balance
- **Máximo de operaciones simultáneas:** 3
- **Risk:Reward mínimo:** 1:2.0

Puedes cambiar estos valores en `config.py` o `.env`.

---

## 🔧 Solución de Problemas

### Error: "No se puede conectar a MT5"

**Solución:**
1. Abre MT5
2. Verifica que estés conectado a tu cuenta
3. Verifica credenciales en `.env`

### Error: "Símbolo no encontrado"

**Solución:**
1. En MT5, busca XAUUSD en el mercado
2. Si aparece como `XAUUSD.m`, actualiza `.env` con ese símbolo
3. Ejecuta `python setup_mt5.py` de nuevo

### Error: "ModuleNotFoundError: MetaTrader5"

**Solución:**
```powershell
pip install MetaTrader5
```

### El bot no genera señales

**Esto es normal.** El bot solo genera señales cuando:
- Hay confluencias ICT válidas
- Se cumplen al menos 3 confirmaciones
- El Risk:Reward es ≥ 2.0

El bot analiza constantemente, pero las señales son selectivas.

---

## 📝 Notas Importantes

1. **Siempre prueba en DEMO primero**
2. **Monitorea el bot regularmente**
3. **El bot es automático, pero revisa las operaciones**
4. **Puedes detener el bot en cualquier momento con Ctrl+C**

---

## 🎯 Checklist Final

Antes de ejecutar el bot, verifica:

- [ ] Python instalado y funcionando
- [ ] Proyecto copiado a `C:\trading-bot`
- [ ] Dependencias instaladas
- [ ] MetaTrader 5 instalado y conectado
- [ ] Credenciales configuradas (`.env` creado)
- [ ] Prueba de conexión exitosa
- [ ] Entiendes cómo funciona el bot
- [ ] Estás usando cuenta DEMO

---

## 🚀 ¡Listo!

Una vez que completes todos los pasos, el bot estará funcionando.

**Comandos rápidos para recordar:**

```powershell
cd C:\trading-bot
python test_mt5_connection.py  # Probar conexión
python live/mt5_trading.py      # Ejecutar bot
```

¡Buena suerte con el trading! 📈







