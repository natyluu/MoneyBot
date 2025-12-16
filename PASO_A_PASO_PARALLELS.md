# 🚀 Configurar Parallels - Paso a Paso

## 📋 PASO 1: Instalar Parallels Desktop

### Opción A: Mac App Store (Recomendado)

1. **Abre Mac App Store**
2. **Busca** "Parallels Desktop"
3. **Descarga e instala**
4. **Prueba gratuita:** 14 días

**O ejecuta:**
```bash
open "macappstore://apps.apple.com/app/parallels-desktop/id1085114709"
```

### Opción B: Descarga Directa

1. Ve a: https://www.parallels.com/products/desktop/
2. Descarga la versión para Mac
3. Instala el archivo `.dmg`
4. Sigue las instrucciones del instalador

---

## 📋 PASO 2: Abrir Parallels Desktop

1. Abre **Parallels Desktop** desde Aplicaciones
2. Si es la primera vez, te pedirá crear una VM
3. Acepta los términos y condiciones

---

## 📋 PASO 3: Instalar Windows

### 3.1 Crear Nueva VM

1. En Parallels, verás la opción **"Instalar Windows"**
2. Clic en **"Instalar Windows 11"** (o Windows 10 si prefieres)
3. Parallels descargará Windows automáticamente
4. **Tiempo estimado:** 30-60 minutos

### 3.2 Durante la Instalación

- Parallels descarga Windows automáticamente
- No necesitas una clave de producto (puedes usar Windows sin activar)
- La instalación es automática

### 3.3 Configurar Windows

Cuando Windows termine de instalarse:

1. **Crea una cuenta de Microsoft** (o usa cuenta local)
2. **Configura Windows** según tus preferencias
3. **Espera** a que termine la configuración inicial

---

## 📋 PASO 4: Configurar Recursos de la VM

### 4.1 Asignar Recursos

1. En Parallels, ve a **Configuración** (⚙️)
2. **Hardware** → **CPU y Memoria**
3. **Recomendaciones:**
   - **RAM:** Mínimo 4GB (8GB recomendado si tienes 16GB+ en Mac)
   - **CPU:** 2-4 cores
   - **Disco:** Mínimo 50GB (100GB recomendado)

### 4.2 Configurar Compartir

1. **Configuración** → **Opciones** → **Compartir**
2. Marca ✅ **"Compartir Mac"**
3. Esto permite acceder a archivos de Mac desde Windows

---

## 📋 PASO 5: Instalar Python en Windows

### 5.1 Descargar Python

1. **Abre el navegador** en Windows (dentro de Parallels)
2. Ve a: https://www.python.org/downloads/
3. Descarga **Python 3.11 o 3.12** (Windows 64-bit)
4. Ejecuta el instalador

### 5.2 Instalar Python

**⚠️ IMPORTANTE:** Durante la instalación:

1. Marca ✅ **"Add Python to PATH"** (MUY IMPORTANTE)
2. Clic en **"Install Now"**
3. Espera a que termine

### 5.3 Verificar Instalación

Abre **PowerShell** en Windows y ejecuta:

```powershell
python --version
pip --version
```

Deberías ver las versiones instaladas.

---

## 📋 PASO 6: Copiar el Proyecto a Windows

### Método A: Carpeta Compartida (Más Fácil)

1. En Parallels: **Configuración** → **Opciones** → **Compartir**
2. Marca ✅ **"Compartir Mac"**
3. En Windows: Abre **Explorador de archivos**
4. Ve a **Red** → **Mac** → Tu carpeta del proyecto
5. Copia `trading-bot-windows-20251210` a `C:\trading-bot`

### Método B: Usar el ZIP

1. En Mac, el ZIP está en: `../trading-bot-windows-20251210.zip`
2. Copia el ZIP a Windows (USB, carpeta compartida, etc.)
3. En Windows, descomprime en `C:\trading-bot`

---

## 📋 PASO 7: Instalar Dependencias en Windows

Abre **PowerShell** en Windows y ejecuta:

```powershell
# Navegar al proyecto
cd C:\trading-bot

# Instalar dependencias
pip install MetaTrader5 python-dotenv pandas numpy

# Verificar instalación
python -c "import MetaTrader5; print('✅ MetaTrader5 instalado')"
```

---

## 📋 PASO 8: Instalar MetaTrader 5 en Windows

1. **Abre el navegador** en Windows
2. Ve a: https://www.metatrader5.com/es/download
3. Descarga **MetaTrader 5 para Windows**
4. Instala MT5
5. **Abre MT5** y conéctate a tu cuenta Zeven

---

## 📋 PASO 9: Configurar el Bot

### 9.1 Configurar Credenciales

En PowerShell de Windows:

```powershell
cd C:\trading-bot
python setup_mt5.py
```

Ingresa:
- Número de cuenta MT5
- Contraseña
- Servidor (ZevenGlobal-Demo o ZevenGlobal-Real)
- Símbolo (XAUUSD)

### 9.2 Probar Conexión

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

---

## 📋 PASO 10: Ejecutar el Bot

```powershell
python live/mt5_trading.py
```

El bot:
- Se conectará automáticamente a MT5
- Obtendrá datos en tiempo real
- Generará señales ICT
- Ejecutará órdenes automáticamente

**Para detener:** Presiona `Ctrl+C`

---

## 🔧 Optimizaciones Opcionales

### Modo Coherencia

Permite usar apps de Windows como si fueran de Mac:

1. **Configuración** → **Opciones** → **Aplicaciones**
2. Marca ✅ **"Modo Coherencia"**
3. Ahora puedes tener MT5 visible mientras trabajas en Mac

### Mejorar Rendimiento

1. **Asignar más recursos** (si tu Mac lo permite)
2. **Cerrar otras aplicaciones** en Mac
3. **Usar modo Fusion** para mejor integración

---

## ⚠️ Solución de Problemas

### Windows no arranca

- Verifica que tengas suficiente RAM libre en Mac
- Cierra otras aplicaciones
- Reinicia Parallels

### Python no se encuentra

```powershell
# Verifica PATH
python --version

# Si no funciona, reinstala Python y marca "Add to PATH"
```

### MetaTrader5 no se instala

```powershell
# Actualiza pip
python -m pip install --upgrade pip

# Intenta de nuevo
pip install MetaTrader5
```

### No puede conectar a MT5

- Verifica que MT5 esté **abierto** en Windows
- Verifica que estés **conectado** a tu cuenta
- Verifica credenciales en `.env`

---

## ✅ Checklist Final

Antes de ejecutar el bot:

- [ ] Parallels Desktop instalado
- [ ] Windows instalado en Parallels
- [ ] Python instalado en Windows (con PATH configurado)
- [ ] Proyecto copiado a Windows
- [ ] Dependencias instaladas
- [ ] MetaTrader 5 instalado en Windows
- [ ] MT5 abierto y conectado a cuenta Zeven
- [ ] Credenciales configuradas
- [ ] Prueba de conexión exitosa
- [ ] Entiendes los riesgos del trading automático
- [ ] Usas cuenta DEMO primero

---

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

---

## 📞 ¿Necesitas Ayuda?

- Revisa `GUIA_PARALLELS_COMPLETA.md` para más detalles
- Verifica cada paso del checklist
- Asegúrate de que MT5 esté abierto y conectado

¡Listo para empezar! 🚀








