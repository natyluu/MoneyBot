# 🚀 Inicio Rápido: Conectar a MT5

## Situación Actual

- ✅ Tienes el código del bot listo
- ✅ Backtesting funciona en macOS
- ❌ MetaTrader5 requiere Windows

## 🎯 Opción Más Rápida: Parallels Desktop

### Paso 1: Instalar Parallels

1. **Descarga Parallels Desktop:**
   - Ve a: https://www.parallels.com/products/desktop/
   - O desde Mac App Store
   - Versión de prueba gratuita: 14 días

2. **Instala Parallels** en tu Mac

### Paso 2: Crear Windows en Parallels

1. Abre Parallels Desktop
2. Clic en "Instalar Windows"
3. Parallels te guía automáticamente
4. Espera a que se instale (30-60 minutos)

### Paso 3: En Windows (dentro de Parallels)

1. **Abre PowerShell en Windows**

2. **Instala Python:**
   ```powershell
   # Descarga Python desde python.org
   # O usa winget:
   winget install Python.Python.3.11
   ```

3. **Verifica Python:**
   ```powershell
   python --version
   pip --version
   ```

4. **Instala dependencias:**
   ```powershell
   pip install MetaTrader5 python-dotenv pandas numpy
   ```

5. **Copia tu proyecto:**
   - Opción A: Compartir carpeta Mac ↔ Windows
   - Opción B: Usar Git para clonar
   - Opción C: Copiar archivos manualmente

6. **Configura credenciales:**
   ```powershell
   cd "ruta/a/tu/proyecto"
   python setup_mt5.py
   ```

7. **Prueba conexión:**
   ```powershell
   python test_mt5_connection.py
   ```

8. **Ejecuta el bot:**
   ```powershell
   python live/mt5_trading.py
   ```

## 📝 Comandos Rápidos (En Windows)

```powershell
# 1. Instalar dependencias
pip install MetaTrader5 python-dotenv pandas numpy

# 2. Configurar
python setup_mt5.py

# 3. Probar
python test_mt5_connection.py

# 4. Ejecutar bot
python live/mt5_trading.py
```

## ⚡ Alternativa: VPS Windows (Sin Instalar Nada en Mac)

Si prefieres no instalar Parallels:

1. **Contrata VPS Windows** (ej: AWS, Azure)
2. **Conéctate por RDP** desde Mac
3. **Sigue los mismos pasos** pero en el VPS

## 🎯 ¿Qué Hacer Ahora?

1. **Decide:** ¿Parallels o VPS?
2. **Si Parallels:** Sigue los pasos arriba
3. **Si VPS:** Te ayudo a configurarlo
4. **Si prefieres otra opción:** Dime cuál

## 💰 Costos Aproximados

- **Parallels Desktop:** $100/año (o prueba 14 días gratis)
- **Windows 11:** $140 (una vez, o usar versión de prueba)
- **VPS Windows:** $20-50/mes

## ✅ Una Vez que Tengas Windows

Todo el código ya está listo. Solo necesitas:
1. Instalar Python en Windows
2. Instalar `pip install MetaTrader5`
3. Ejecutar `python setup_mt5.py`
4. ¡Listo!

¿Tienes acceso a Windows o prefieres que te ayude a configurar Parallels/VPS?










