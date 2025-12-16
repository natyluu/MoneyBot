# ✅ Probar Conexión con MT5

## Paso 1: Verificar que el archivo .env existe

```powershell
dir .env
```

Deberías ver el archivo `.env` listado.

---

## Paso 2: Verificar contenido (opcional)

```powershell
type .env
```

Deberías ver tus credenciales (sin mostrar la contraseña completa por seguridad).

---

## Paso 3: IMPORTANTE - Asegúrate de que MT5 esté abierto

⚠️ **MetaTrader 5 DEBE estar abierto y conectado** antes de ejecutar el test.

1. Abre MetaTrader 5
2. Verifica que esté conectado (ícono verde en la parte inferior)
3. Verifica que el símbolo `XAUUSD.vip` esté visible en Market Watch

---

## Paso 4: Probar la conexión

```powershell
python test_mt5_connection.py
```

### ✅ Si funciona correctamente:
Verás mensajes como:
- "✅ Conexión a MT5 exitosa"
- "✅ Símbolo XAUUSD.vip encontrado"
- "✅ PRUEBA COMPLETADA EXITOSAMENTE"

### ❌ Si hay errores:
- **Error de conexión:** Verifica que MT5 esté abierto y conectado
- **Error de símbolo:** Verifica que el símbolo sea `XAUUSD.vip` (con .vip)
- **Error de credenciales:** Verifica que el número de cuenta y contraseña sean correctos

---

## Paso 5: Si la prueba es exitosa

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

1. ✅ Verificar `.env`: `dir .env`
2. ✅ Abrir MT5 y conectar
3. ✅ Probar conexión: `python test_mt5_connection.py`
4. ✅ Si funciona: `python live/mt5_trading.py`





