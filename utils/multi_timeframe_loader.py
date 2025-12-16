"""
utils/multi_timeframe_loader.py - Cargador de datos multi-temporales

Este módulo se encarga de cargar datos históricos de múltiples timeframes
necesarios para estrategias multi-temporales como la ICT Híbrida.
"""

import pandas as pd
import os
from typing import Dict, Optional
from config import DATA_DIR


def load_multi_timeframe_data(symbol: str, start_date: Optional[str] = None,
                              end_date: Optional[str] = None) -> Dict[str, pd.DataFrame]:
    """
    Carga datos históricos de múltiples timeframes para análisis multi-temporal.
    
    Args:
        symbol: Par de trading (ej: "XAUUSD")
        start_date: Fecha de inicio (formato: "YYYY-MM-DD")
        end_date: Fecha de fin (formato: "YYYY-MM-DD")
    
    Returns:
        Diccionario con DataFrames de cada timeframe:
        {
            'D1': DataFrame,
            'H4': DataFrame,
            'H1': DataFrame,
            'M15': DataFrame,
            'M5': DataFrame,
            'M3': DataFrame,
            'M1': DataFrame
        }
    """
    timeframes = ['1d', '4h', '1h', '15m', '5m', '3m', '1m']
    timeframe_keys = ['D1', 'H4', 'H1', 'M15', 'M5', 'M3', 'M1']
    
    data = {}
    
    for tf, key in zip(timeframes, timeframe_keys):
        csv_path = os.path.join(DATA_DIR, f"{symbol}_{tf}.csv")
        
        if os.path.exists(csv_path):
            print(f"✓ Cargando {key} ({tf}) desde {csv_path}")
            df = pd.read_csv(csv_path)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df.set_index('timestamp', inplace=True)
            
            # Filtra por fechas si se especifican
            if start_date:
                df = df[df.index >= pd.to_datetime(start_date)]
            if end_date:
                df = df[df.index <= pd.to_datetime(end_date)]
            
            # Asegura que las columnas necesarias estén presentes
            required_columns = ['open', 'high', 'low', 'close', 'volume']
            if all(col in df.columns for col in required_columns):
                data[key] = df
            else:
                print(f"⚠️ {key}: Faltan columnas requeridas. Columnas encontradas: {df.columns.tolist()}")
        else:
            print(f"⚠️ {key} ({tf}): Archivo no encontrado: {csv_path}")
    
    return data


def resample_to_timeframes(base_data: pd.DataFrame, 
                          base_timeframe: str = '1h') -> Dict[str, pd.DataFrame]:
    """
    Re-muestrea datos de un timeframe base a múltiples timeframes.
    
    Útil cuando solo tienes datos de un timeframe pero necesitas otros.
    NOTA: Esto es una aproximación. Para backtesting preciso, usa datos reales de cada timeframe.
    
    Args:
        base_data: DataFrame con datos OHLCV del timeframe base
        base_timeframe: Timeframe base (ej: '1h', '15m')
    
    Returns:
        Diccionario con DataFrames re-muestreados
    """
    print(f"⚠️ Re-muestreando datos desde {base_timeframe} (aproximación)")
    print("   Para resultados precisos, usa datos reales de cada timeframe")
    
    data = {}
    
    # Mapeo de timeframes objetivo
    resample_map = {
        'D1': 'D',
        'H4': '4H',
        'H1': '1H',
        'M15': '15T',
        'M5': '5T',
        'M3': '3T',
        'M1': '1T'
    }
    
    for key, rule in resample_map.items():
        try:
            resampled = base_data.resample(rule).agg({
                'open': 'first',
                'high': 'max',
                'low': 'min',
                'close': 'last',
                'volume': 'sum'
            }).dropna()
            
            if len(resampled) > 0:
                data[key] = resampled
                print(f"   ✓ {key}: {len(resampled)} velas")
        except Exception as e:
            print(f"   ✗ {key}: Error al re-muestrear - {e}")
    
    return data


def align_timeframes(data_dict: Dict[str, pd.DataFrame], 
                    reference_timeframe: str = 'M1') -> Dict[str, pd.DataFrame]:
    """
    Alinea múltiples timeframes para que tengan el mismo rango de fechas.
    
    Útil para asegurar que todos los timeframes cubran el mismo período.
    
    Args:
        data_dict: Diccionario con DataFrames de cada timeframe
        reference_timeframe: Timeframe de referencia (el más granular)
    
    Returns:
        Diccionario con DataFrames alineados
    """
    if reference_timeframe not in data_dict:
        print(f"⚠️ Timeframe de referencia {reference_timeframe} no encontrado")
        return data_dict
    
    ref_data = data_dict[reference_timeframe]
    start_date = ref_data.index[0]
    end_date = ref_data.index[-1]
    
    print(f"Alineando timeframes al rango: {start_date} a {end_date}")
    
    aligned = {}
    for key, df in data_dict.items():
        # Filtra al rango de fechas de referencia
        aligned_df = df[(df.index >= start_date) & (df.index <= end_date)]
        if len(aligned_df) > 0:
            aligned[key] = aligned_df
            print(f"   ✓ {key}: {len(aligned_df)} velas")
        else:
            print(f"   ✗ {key}: Sin datos en el rango")
    
    return aligned


def validate_multi_timeframe_data(data_dict: Dict[str, pd.DataFrame]) -> bool:
    """
    Valida que los datos multi-temporales sean consistentes.
    
    Args:
        data_dict: Diccionario con DataFrames de cada timeframe
    
    Returns:
        True si los datos son válidos, False en caso contrario
    """
    if not data_dict:
        print("❌ No hay datos para validar")
        return False
    
    required_timeframes = ['D1', 'H4', 'H1', 'M15', 'M5']
    missing = [tf for tf in required_timeframes if tf not in data_dict]
    
    if missing:
        print(f"⚠️ Timeframes faltantes: {', '.join(missing)}")
        print("   Se recomienda tener al menos: D1, H4, H1, M15, M5")
    
    # Valida que cada DataFrame tenga las columnas necesarias
    required_columns = ['open', 'high', 'low', 'close', 'volume']
    for key, df in data_dict.items():
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            print(f"❌ {key}: Faltan columnas: {', '.join(missing_cols)}")
            return False
    
    print("✓ Validación de datos multi-temporales: OK")
    return True













