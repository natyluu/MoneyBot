# Sistema de Backtesting ICT

Sistema completo de backtesting para la estrategia ICT Híbrida con soporte multi-temporal.

## Características

- ✅ Análisis multi-temporal (D1, H4, H1, M15, M5, M3, M1)
- ✅ Simulación realista con slippage y comisiones
- ✅ Múltiples Take Profits (TP1, TP2, TP Final)
- ✅ Métricas avanzadas (Sharpe Ratio, Drawdown, Profit Factor)
- ✅ Re-muestreo automático de timeframes si faltan datos

## Uso Básico

```python
from backtest.run_ict_backtest import run_ict_backtest

# Ejecuta backtest con parámetros por defecto
results = run_ict_backtest(
    symbol="XAUUSD",
    start_date="2023-01-01",
    end_date="2024-01-01",
    use_resampling=True  # Permite re-muestreo si faltan datos
)
```

## Ejecutar desde Línea de Comandos

```bash
python backtest/run_ict_backtest.py
```

## Parámetros

- `symbol`: Par de trading (default: "XAUUSD")
- `start_date`: Fecha de inicio (formato: "YYYY-MM-DD")
- `end_date`: Fecha de fin (formato: "YYYY-MM-DD")
- `initial_capital`: Capital inicial (default: desde config.py)
- `commission`: Comisión por operación (default: desde config.py)
- `use_resampling`: Si True, re-muestrea desde timeframe base si faltan datos

## Requisitos de Datos

Para un backtest preciso, necesitas datos históricos de múltiples timeframes:

**Mínimo requerido:**
- D1 (diario)
- H4 (4 horas)
- H1 (1 hora)
- M15 (15 minutos)
- M5 (5 minutos)

**Opcional pero recomendado:**
- M3 (3 minutos)
- M1 (1 minuto)

Los archivos deben estar en la carpeta `data/` con formato:
```
{SYMBOL}_{TIMEFRAME}.csv
```

Ejemplo: `XAUUSD_1d.csv`, `XAUUSD_4h.csv`, etc.

## Métricas Calculadas

El backtest calcula:

- **Capital**: Inicial, final, retorno total
- **Operaciones**: Total, ganadoras, perdedoras, tasa de acierto
- **P&L**: Total, promedio por operación ganadora/perdedora
- **Profit Factor**: Ratio ganancias/pérdidas
- **Sharpe Ratio**: Ratio de riesgo/retorno ajustado
- **Max Drawdown**: Máxima caída desde un pico
- **Duración de Drawdown**: Tiempo en drawdown máximo

## Resultados

Los resultados incluyen:

- `BacktestResults`: Objeto con todas las métricas
- `trades`: Lista de todas las operaciones realizadas
- `equity_curve`: Evolución del capital a lo largo del tiempo
- `signals_generated`: Número de señales generadas
- `signals_executed`: Número de señales ejecutadas

## Ejemplo de Salida

```
======================================================================
BACKTEST: ESTRATEGIA ICT HÍBRIDA 2022
======================================================================
Símbolo: XAUUSD
Período: 2023-01-01 a 2024-01-01

📊 Cargando datos multi-temporales...
✓ Datos cargados para 5 timeframes
   D1: 365 velas
   H4: 2190 velas
   H1: 8760 velas
   M15: 35040 velas
   M5: 105120 velas

💰 Capital:
   Inicial: $10,000.00
   Final: $12,450.00
   Retorno: +24.50%
   P&L Total: $2,450.00

📊 Operaciones:
   Total: 45
   Ganadoras: 28
   Perdedoras: 17
   Tasa de acierto: 62.22%

📈 Métricas:
   Ganancia promedio: $125.50
   Pérdida promedio: -$85.30
   Profit Factor: 2.45
   Sharpe Ratio: 1.85
   Max Drawdown: 8.50%
```













