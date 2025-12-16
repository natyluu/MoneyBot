# Estrategia ICT Híbrida 2022

Estrategia institucional basada en los conceptos de Inner Circle Trader (ICT) 2022, implementada con análisis multi-temporal completo.

## 📋 Características

### Análisis Multi-Temporal

La estrategia analiza múltiples timeframes para obtener una visión completa del mercado:

- **D1 (Diario)**: Tendencia macro, zonas de liquidez mayor, FVG grandes, Order Blocks macro
- **H4 (4 Horas)**: BOS/CHoCH institucionales, estructuras de acumulación/redistribución, FVG activos, Order Blocks
- **H1 (1 Hora)**: Aterriza zonas institucionales activas, valida mitigaciones
- **M15/M5 (15 y 5 Minutos)**: BOS/CHoCH limpios, barridas de liquidez, mitades de FVG no mitigados
- **M1/M3 (1 y 3 Minutos)**: Confirmación de entrada tipo sniper

### Patrones Detectados

#### Estructura de Mercado
- **BOS (Break of Structure)**: Ruptura de swings previos
- **CHoCH (Change of Character)**: Cambio en la secuencia de máximos/mínimos
- **Liquidity Sweeps**: Barridas de liquidez (stop hunts)

#### Bloques Institucionales (PD Arrays)
- **Order Block (OB)**: Última vela antes de una reversión
- **Fair Value Gap (FVG)**: Gaps en el precio sin negociación
- **Mitigation Block**: Bloque que ha sido "llenado" por el precio
- **Breaker Block**: Order Block roto que actúa como soporte/resistencia
- **Rejection Block**: Zona de rechazo fuerte del precio
- **Liquidity Void**: FVG grande y significativo

### Confirmaciones para Entrada

La estrategia requiere **mínimo 3 de 5 confirmaciones** para generar una señal:

1. ✅ **Sweep de liquidez**: Barrida de un swing high/low previo
2. ✅ **Mitigación válida**: OB o FVG que ha sido mitigado
3. ✅ **BOS/CHoCH interno**: Ruptura de estructura después de la barrida
4. ✅ **Vela institucional + volumen alto**: Vela con cuerpo grande y volumen significativo
5. ✅ **Divergencia RSI** (opcional): Divergencia entre precio y RSI

## 🚀 Uso

### Ejemplo Básico

```python
from strategy.ict_hybrid_strategy import ICTHybridStrategy
from utils.data_loader import load_historical_data

# Inicializa la estrategia
strategy = ICTHybridStrategy()

# Carga datos de múltiples timeframes
df_D1 = load_historical_data(symbol="XAUUSD", timeframe="1d")
df_H4 = load_historical_data(symbol="XAUUSD", timeframe="4h")
df_H1 = load_historical_data(symbol="XAUUSD", timeframe="1h")
df_M15 = load_historical_data(symbol="XAUUSD", timeframe="15m")
df_M5 = load_historical_data(symbol="XAUUSD", timeframe="5m")
df_M3 = load_historical_data(symbol="XAUUSD", timeframe="3m")
df_M1 = load_historical_data(symbol="XAUUSD", timeframe="1m")

# Ejecuta análisis multi-temporal
d1_results = strategy.analyze_D1(df_D1)
h4_results = strategy.analyze_H4(df_H4)
h1_results = strategy.analyze_H1(df_H1)
m15_m5_results = strategy.analyze_M15_M5(df_M15, df_M5)

# Busca entrada sniper
signal = strategy.find_sniper_entry(df_M1, df_M3, strategy.context)

if signal:
    print(f"Señal {signal.operation_type} generada")
    print(f"Entrada: ${signal.entry_price:.2f}")
    print(f"SL: ${signal.stop_loss:.2f}")
    print(f"TP1: ${signal.take_profit_1:.2f}")
    print(f"TP2: ${signal.take_profit_2:.2f}")
    print(f"TP Final: ${signal.take_profit_final:.2f}")
    print(f"Risk:Reward: 1:{signal.risk_reward:.2f}")
```

### Ejecutar Ejemplo Completo

```bash
python strategy/example_ict_usage.py
```

## 📊 Formato de Señal

Cada señal generada contiene:

```python
TradingSignal(
    direction="BULLISH" | "BEARISH",      # Dirección macro
    active_zones=[...],                    # Zonas institucionales activas
    operation_type="BUY" | "SELL",        # Tipo de operación
    entry_price=float,                     # Precio de entrada
    stop_loss=float,                       # Stop Loss
    take_profit_1=float,                   # TP1 (1:1.5 RR)
    take_profit_2=float,                   # TP2 (1:2.5 RR)
    take_profit_final=float,               # TP Final (1:4 RR o swing)
    risk_reward=float,                     # Ratio Risk:Reward
    justifications=[...],                  # Lista de justificaciones
    chart_data={...}                       # Datos para generar gráfico SVG
)
```

## 🔧 Configuración

La estrategia usa los parámetros por defecto, pero puedes ajustarlos en el código:

- **Lookback para swings**: Número de velas para confirmar un swing
- **Tolerancia para swings iguales**: Porcentaje para considerar swings al mismo nivel
- **Tamaño mínimo de FVG**: Porcentaje mínimo para considerar un FVG "grande"
- **Umbral de volumen**: Múltiplo del volumen promedio para considerar "alto volumen"

## 📝 Notas Importantes

1. **Datos Multi-Temporal**: Esta estrategia requiere datos de múltiples timeframes. Asegúrate de tener datos históricos suficientes para cada timeframe.

2. **Símbolo Recomendado**: XAUUSD (Oro) es el símbolo para el que está optimizada, pero puede usarse con otros pares.

3. **Backtesting**: Para backtesting completo, necesitarás adaptar el motor de backtesting para trabajar con señales multi-temporales.

4. **Trading en Vivo**: El módulo `live/` necesitará ser extendido para obtener datos en tiempo real de múltiples timeframes.

## 🎯 Próximos Pasos

- [ ] Integrar con el motor de backtesting
- [ ] Generar visualizaciones SVG de las señales
- [ ] Implementar conexión con API para datos en tiempo real
- [ ] Agregar más confirmaciones opcionales
- [ ] Optimizar parámetros por símbolo

## 📚 Referencias

- Inner Circle Trader (ICT) 2022 Concepts
- Market Structure Analysis
- Institutional Order Flow
- Price Delivery (PD) Arrays













