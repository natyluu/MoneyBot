# 🚀 Guía Rápida: Conectar a MT5 con Zeven

## Paso 1: Instalar Dependencias

Ejecuta estos comandos en la terminal:

```bash
# Actualiza pip
python3 -m pip install --upgrade pip

# Instala las dependencias
python3 -m pip install MetaTrader5 python-dotenv pandas numpy
```

**Nota:** Si `MetaTrader5` no se instala, intenta:
```bash
pip3 install MetaTrader5
```

O instala desde el archivo requirements.txt:
```bash
python3 -m pip install -r requirements.txt
```

## Paso 2: Configurar Credenciales

Ejecuta el script de configuración:

```bash
python3 setup_mt5.py
```

Este script te pedirá:
- Tu número de cuenta MT5 de Zeven
- Tu contraseña
- Tipo de cuenta (Demo/Real) - **Usa Demo primero**
- Símbolo (default: XAUUSD)

O crea manualmente el archivo `.env`:

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

## Paso 3: Verificar que MT5 esté Abierto

**IMPORTANTE:** Antes de ejecutar el bot:
1. Abre MetaTrader 5 en tu computadora
2. Conéctate a tu cuenta Zeven
3. Verifica que el símbolo XAUUSD esté visible en Market Watch

## Paso 4: Probar la Conexión

Ejecuta el script de prueba:

```bash
python3 test_mt5_connection.py
```

Este script verificará:
- ✅ Que MT5 esté funcionando
- ✅ Que tus credenciales sean correctas
- ✅ Que el símbolo XAUUSD esté disponible
- ✅ Que puedas obtener datos

## Paso 5: Ejecutar el Bot

Si la prueba fue exitosa, ejecuta el bot:

```bash
python3 live/mt5_trading.py
```

## ⚠️ Si hay Problemas

### Error: "MetaTrader5 no se instala"

**Solución:**
```bash
# En macOS, puede necesitar:
python3 -m pip install --upgrade pip setuptools wheel
python3 -m pip install MetaTrader5

# O instala desde source:
python3 -m pip install git+https://github.com/EA31337/MetaTrader5.git
```

### Error: "No se pudo inicializar MT5"

- Verifica que MetaTrader 5 esté **abierto y funcionando**
- Intenta ejecutar Python como administrador
- Reinstala MT5 si es necesario

### Error: "Símbolo no encontrado"

1. En MT5, abre Market Watch (Ctrl+M)
2. Haz clic derecho → "Símbolos"
3. Busca "XAUUSD" o "GOLD"
4. Anota el nombre exacto
5. Actualiza `MT5_SYMBOL` en `.env`

## 📞 ¿Necesitas Ayuda?

Revisa el archivo `INSTRUCCIONES_MT5.md` para más detalles.













