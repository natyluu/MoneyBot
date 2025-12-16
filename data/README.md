# Carpeta de Datos Históricos

Coloca aquí tus archivos CSV con datos históricos de precios.

## Formato del CSV

El archivo CSV debe tener las siguientes columnas:

- `timestamp`: Fecha y hora (formato: YYYY-MM-DD HH:MM:SS)
- `open`: Precio de apertura
- `high`: Precio máximo
- `low`: Precio mínimo
- `close`: Precio de cierre
- `volume`: Volumen negociado

## Nombre del archivo

El nombre debe seguir el formato: `{SYMBOL}_{TIMEFRAME}.csv`

Ejemplo: `BTCUSDT_1h.csv`

## Ejemplo de contenido

```csv
timestamp,open,high,low,close,volume
2023-01-01 00:00:00,16500.0,16550.0,16480.0,16520.0,1234.56
2023-01-01 01:00:00,16520.0,16580.0,16510.0,16560.0,1456.78
```

## Obtener datos históricos

Puedes obtener datos históricos de:
- Binance (gratis, requiere cuenta)
- Alpha Vantage (gratis con límites)
- Yahoo Finance (gratis)
- Tu broker directamente













