# 🚀 Guía Completa: Configurar Parallels para Trading en Vivo

Esta guía te llevará paso a paso para configurar Parallels Desktop y ejecutar tu bot de trading en Windows.

## 📋 PASO 1: Instalar Parallels Desktop

### Opción A: Desde Mac App Store (Recomendado)

1. Abre **Mac App Store**
2. Busca "Parallels Desktop"
3. Descarga e instala
4. **Prueba gratuita:** 14 días

### Opción B: Descarga Directa

1. Ve a: https://www.parallels.com/products/desktop/
2. Descarga la versión para Mac
3. Instala el archivo `.dmg`
4. Sigue las instrucciones del instalador

### Verificar Instalación

```bash
# Verifica que Parallels esté instalado
ls -la "/Applications/Parallels Desktop.app"
```

## 📋 PASO 2: Crear Máquina Virtual con Windows

### 2.1 Abrir Parallels Desktop

1. Abre **Parallels Desktop** desde Aplicaciones
2. Si es la primera vez, te pedirá crear una VM

### 2.2 Instalar Windows

**Opción A: Windows 11 (Recomendado)**
- Parallels puede descargar Windows 11 automáticamente
- Clic en "Instalar Windows 11"
- Parallels descarga e instala todo automáticamente
- Tiempo estimado: 30-60 minutos

**Opción B: Windows 10**
- Si tienes una imagen ISO de Windows 10
- Parallels puede usarla para instalar

### 2.3 Configuración de la VM

**Recursos recomendados:**
- **RAM:** Mínimo 4GB (8GB recomendado)
- **Disco:** Mínimo 50GB (100GB recomendado)
- **CPU:** 2-4 cores

**Durante la instalación de Windows:**
- Crea una cuenta de Microsoft (o usa cuenta local)
- Configura Windows según tus preferencias
- Espera a que termine la instalación

## 📋 PASO 3: Configurar Windows para el Bot

### 3.1 Instalar Python en Windows

1. **Abre el navegador en Windows** (dentro de Parallels)
2. Ve a: https://www.python.org/downloads/
3. Descarga **Python 3.11 o 3.12** (Windows 64-bit)
4. **IMPORTANTE:** Durante la instalación, marca ✅ **"Add Python to PATH"**
5. Completa la instalación

**Verificar Python:**
```powershell
# Abre PowerShell en Windows
python --version
pip --version
```

### 3.2 Copiar el Proyecto a Windows

**Método A: Carpeta Compartida (Más Fácil)**

1. En Parallels, ve a **Configuración** → **Opciones** → **Compartir**
2. Marca ✅ **"Compartir Mac"**
3. En Windows, abre **Explorador de archivos**
4. Ve a **Red** → **Mac** → Tu carpeta del proyecto
5. Copia la carpeta completa a Windows (ej: `C:\trading-bot`)

**Método B: Git (Si tienes el proyecto en Git)**

```powershell
# En Windows PowerShell
cd C:\
git clone [tu-repositorio]
cd trading-bot
```

**Método C: USB/Disco Externo**

1. Copia la carpeta del proyecto a un USB
2. Conecta el USB (Parallels lo detecta automáticamente)
3. Copia desde el USB a Windows

### 3.3 Instalar Dependencias en Windows

```powershell
# Abre PowerShell en Windows
cd C:\trading-bot  # O la ruta donde copiaste el proyecto

# Instala dependencias
pip install MetaTrader5 python-dotenv pandas numpy

# Verifica instalación
python -c "import MetaTrader5; print('✅ MetaTrader5 instalado')"
```

## 📋 PASO 4: Instalar MetaTrader 5 en Windows

1. **Abre el navegador en Windows**
2. Ve a: https://www.metatrader5.com/es/download
3. Descarga **MetaTrader 5 para Windows**
4. Instala MT5
5. **Abre MT5** y conéctate a tu cuenta Zeven

## 📋 PASO 5: Configurar el Bot

### 5.1 Configurar Credenciales

```powershell
# En PowerShell, dentro de la carpeta del proyecto
python setup_mt5.py
```

Ingresa:
- Número de cuenta MT5
- Contraseña
- Servidor (ZevenGlobal-Demo o ZevenGlobal-Real)
- Símbolo (XAUUSD)

### 5.2 Probar Conexión

1. **Abre MetaTrader 5** en Windows
2. **Conéctate** a tu cuenta Zeven
3. **Ejecuta:**

```powershell
python test_mt5_connection.py
```

Deberías ver:
```
✅ PRUEBA COMPLETADA EXITOSAMENTE
```

## 📋 PASO 6: Ejecutar el Bot

```powershell
python live/mt5_trading.py
```

El bot:
- Se conectará automáticamente a MT5
- Obtendrá datos en tiempo real
- Generará señales ICT
- Ejecutará órdenes automáticamente

**Para detener:** Presiona `Ctrl+C`

## 🔧 Optimización de Parallels

### Mejorar Rendimiento

1. **Asignar más recursos:**
   - Configuración → Hardware → CPU y Memoria
   - Aumenta RAM a 8GB si es posible
   - Aumenta CPUs a 4 cores

2. **Modo Coherencia:**
   - Permite usar apps de Windows como si fueran de Mac
   - Útil para tener MT5 visible mientras trabajas

3. **Compartir archivos:**
   - Configuración → Opciones → Compartir
   - Facilita copiar archivos entre Mac y Windows

## ⚠️ Solución de Problemas

### Problema: Windows no arranca

**Solución:**
- Verifica que tengas suficiente RAM libre en Mac
- Cierra otras aplicaciones
- Reinicia Parallels

### Problema: Python no se encuentra

**Solución:**
```powershell
# Verifica que Python esté en PATH
python --version

# Si no funciona, reinstala Python y marca "Add to PATH"
```

### Problema: MetaTrader5 no se instala

**Solución:**
```powershell
# Actualiza pip
python -m pip install --upgrade pip

# Intenta de nuevo
pip install MetaTrader5
```

### Problema: No puede conectar a MT5

**Solución:**
- Verifica que MT5 esté **abierto** en Windows
- Verifica que estés **conectado** a tu cuenta
- Verifica credenciales en `.env`

## 📝 Checklist Final

Antes de ejecutar el bot en vivo:

- [ ] Parallels Desktop instalado
- [ ] Windows instalado en Parallels
- [ ] Python instalado en Windows (con PATH configurado)
- [ ] Proyecto copiado a Windows
- [ ] Dependencias instaladas (`pip install MetaTrader5...`)
- [ ] MetaTrader 5 instalado en Windows
- [ ] MT5 abierto y conectado a cuenta Zeven
- [ ] Credenciales configuradas (`python setup_mt5.py`)
- [ ] Prueba de conexión exitosa (`python test_mt5_connection.py`)
- [ ] Entiendes los riesgos del trading automático
- [ ] Usas cuenta DEMO primero

## 🎯 Comandos Rápidos (En Windows)

```powershell
# 1. Navegar al proyecto
cd C:\trading-bot

# 2. Instalar dependencias
pip install MetaTrader5 python-dotenv pandas numpy

# 3. Configurar
python setup_mt5.py

# 4. Probar (con MT5 abierto)
python test_mt5_connection.py

# 5. Ejecutar bot
python live/mt5_trading.py
```

## 💡 Consejos

1. **Empieza con cuenta DEMO** - Prueba todo antes de usar dinero real
2. **Monitorea el bot** - Revisa regularmente que funcione correctamente
3. **Usa modo Coherencia** - Para tener MT5 visible mientras trabajas
4. **Guarda backups** - Del proyecto y configuración
5. **Prueba primero** - Ejecuta `test_mt5_connection.py` antes del bot completo

## 🆘 ¿Necesitas Ayuda?

Si encuentras problemas:
1. Revisa los mensajes de error
2. Verifica cada paso del checklist
3. Asegúrate de que MT5 esté abierto y conectado
4. Revisa el archivo `.env` con las credenciales

¡Listo para empezar! 🚀









