# ✅ Probar Conexión con MT5 - Paso Final

## 🎯 Estado Actual

- ✅ Archivo `.env` creado y en la carpeta correcta
- ✅ Estás en la carpeta del proyecto
- ⏳ **SIGUIENTE:** Probar la conexión con MT5

---

## ⚠️ IMPORTANTE - Antes de Probar

**MetaTrader 5 DEBE estar abierto y conectado:**

1. Abre MetaTrader 5 (si no está abierto)
2. Verifica que esté conectado (ícono verde en la parte inferior)
3. Verifica que el símbolo `XAUUSD.vip` esté visible en Market Watch

---

## ✅ Paso 1: Probar la Conexión

Ejecuta este comando:

```powershell
python test_mt5_connection.py
```

---

## ✅ Qué Deberías Ver

### Si funciona correctamente:
- "✅ Conexión a MT5 exitosa"
- "✅ Símbolo XAUUSD.vip encontrado"
- "✅ Datos obtenidos correctamente"
- "✅ PRUEBA COMPLETADA EXITOSAMENTE"

### Si hay errores:
- **Error de conexión:** Verifica que MT5 esté abierto y conectado
- **Error de símbolo:** Verifica que el símbolo sea `XAUUSD.vip` (con `.vip`)
- **Error de credenciales:** Verifica que el número de cuenta y contraseña sean correctos

---

## ✅ Paso 2: Si la Prueba es Exitosa

¡Ya puedes ejecutar el bot!

```powershell
python live/mt5_trading.py
```

El bot comenzará a:
- Conectarse a MT5
- Obtener datos multi-timeframe
- Analizar el mercado
- Generar señales (cuando haya oportunidades)

**Para detener el bot:** Presiona `Ctrl+C`

---

## 🎯 Resumen

1. ✅ Asegúrate de que MT5 esté abierto y conectado
2. ✅ Ejecuta: `python test_mt5_connection.py`
3. ✅ Si funciona: `python live/mt5_trading.py`

---

## 🚀 ¡Casi Terminamos!

Solo falta probar la conexión y ejecutar el bot. ¡Vamos! 🎉





