# 📋 Pasos para Configurar Parallels - Resumen Ejecutivo

## ✅ PASO 1: Instalar Parallels Desktop

### Desde Mac App Store:
1. Abre **Mac App Store**
2. Busca "Parallels Desktop"
3. Descarga e instala (prueba 14 días gratis)

### O descarga directa:
- Ve a: https://www.parallels.com/products/desktop/
- Descarga e instala

## ✅ PASO 2: Crear Windows en Parallels

1. **Abre Parallels Desktop**
2. Clic en **"Instalar Windows"**
3. Parallels descarga Windows 11 automáticamente
4. Espera 30-60 minutos
5. Configura Windows (cuenta Microsoft, etc.)

## ✅ PASO 3: En Windows (dentro de Parallels)

### 3.1 Instalar Python

1. Abre **navegador** en Windows
2. Ve a: https://www.python.org/downloads/
3. Descarga **Python 3.11 o 3.12** (Windows 64-bit)
4. **IMPORTANTE:** Marca ✅ **"Add Python to PATH"**
5. Instala

**Verifica:**
```powershell
python --version
pip --version
```

### 3.2 Copiar Proyecto a Windows

**Método más fácil - Carpeta Compartida:**

1. En Parallels: **Configuración** → **Opciones** → **Compartir**
2. Marca ✅ **"Compartir Mac"**
3. En Windows: Abre **Explorador de archivos**
4. Ve a **Red** → **Mac** → Tu carpeta
5. Copia `trading-bot-windows-20251210` a `C:\trading-bot`

### 3.3 Instalar Dependencias

```powershell
cd C:\trading-bot
pip install MetaTrader5 python-dotenv pandas numpy
```

### 3.4 Instalar MetaTrader 5

1. Abre navegador en Windows
2. Ve a: https://www.metatrader5.com/es/download
3. Descarga e instala MT5
4. Abre MT5 y conéctate a Zeven

## ✅ PASO 4: Configurar Bot

```powershell
cd C:\trading-bot

# 1. Configurar credenciales
python setup_mt5.py

# 2. Probar conexión (con MT5 abierto)
python test_mt5_connection.py

# 3. Ejecutar bot
python live/mt5_trading.py
```

## 🎯 Comandos Rápidos (Copia y Pega)

```powershell
# En PowerShell de Windows (dentro de Parallels)

# 1. Navegar al proyecto
cd C:\trading-bot

# 2. Instalar todo
pip install MetaTrader5 python-dotenv pandas numpy

# 3. Configurar
python setup_mt5.py

# 4. Probar (abre MT5 primero)
python test_mt5_connection.py

# 5. Ejecutar bot
python live/mt5_trading.py
```

## 📦 Paquete Preparado

Ya creé un paquete listo para Windows en:
- **Carpeta:** `../trading-bot-windows-20251210`
- **ZIP:** `../trading-bot-windows-20251210.zip` (si se creó)

Este paquete contiene:
- ✅ Todo el código del bot
- ✅ Scripts de instalación
- ✅ Instrucciones para Windows
- ✅ Archivos de configuración

## ⚡ Siguiente Acción

1. **Instala Parallels Desktop** (si no lo tienes)
2. **Crea VM con Windows**
3. **Copia el proyecto** a Windows
4. **Sigue los pasos 3 y 4** arriba

¿Tienes Parallels instalado ya, o necesitas instalarlo primero?









