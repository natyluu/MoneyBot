# ⚡ Inicio Rápido - Bot de Trading ICT

## 🚀 En 5 Minutos

### 1. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 2. Generar Datos de Ejemplo
```bash
python utils/generate_sample_data.py
```

### 3. Ejecutar Backtest
```bash
python backtest/backtest.py
```

¡Listo! Ya tienes resultados del backtest.

---

## 📊 Para Backtesting Avanzado

```bash
# Usa el script rápido
./ejecutar_backtest_ahora.sh

# O ejecuta directamente
python backtest/backtest.py
```

**Resultados:**
- Número de operaciones
- Winrate
- Profit Factor
- Drawdown
- Risk:Reward promedio

---

## 🤖 Para Trading en Vivo (MT5)

### Requisitos
- Windows (o Parallels en Mac)
- MetaTrader 5 instalado
- Cuenta Zeven (Demo o Real)

### Pasos

```bash
# 1. Configurar credenciales
python setup_mt5.py

# 2. Probar conexión (con MT5 abierto)
python test_mt5_connection.py

# 3. Ejecutar bot
python live/mt5_trading.py
```

---

## 📚 Documentación Completa

- **README.md** - Documentación principal
- **GUIA_PARALLELS_COMPLETA.md** - Para configurar Parallels
- **INICIO_RAPIDO_MT5.md** - Inicio rápido MT5
- **CHECKLIST_FINAL.md** - Estado del proyecto

---

## ⚠️ Importante

- **Backtesting**: Funciona en macOS y Windows
- **Trading en Vivo**: Solo Windows (o Parallels en Mac)
- **Siempre prueba en DEMO** antes de usar cuenta real

---

**¿Listo para empezar?** 🎯








