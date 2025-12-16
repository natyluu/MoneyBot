"""
test_mt5_connection.py - Script de prueba para conectar a MT5 con Zeven

Este script te ayuda a verificar que la conexión con MetaTrader 5 funcione correctamente
antes de ejecutar el bot de trading completo.
"""

import sys
import os

# Verifica que MetaTrader5 esté instalado
try:
    import MetaTrader5 as mt5
    print("✅ MetaTrader5 está instalado")
except ImportError:
    print("❌ MetaTrader5 no está instalado")
    print("   Instala con: pip install MetaTrader5")
    sys.exit(1)

# Carga configuración (config.py ya maneja la carga del .env)
from config import MT5_LOGIN, MT5_PASSWORD, MT5_SERVER, MT5_SYMBOL

def test_mt5_connection():
    """Prueba la conexión con MetaTrader 5"""
    
    print("=" * 70)
    print("PRUEBA DE CONEXIÓN A METATRADER 5")
    print("=" * 70)
    
    # Verifica que las credenciales estén configuradas
    print("\n📋 Verificando configuración...")
    if MT5_LOGIN == 0 or not MT5_PASSWORD:
        print("❌ Credenciales no configuradas")
        print("\nPor favor:")
        print("1. Crea un archivo .env en la raíz del proyecto")
        print("2. Agrega tus credenciales:")
        print("   MT5_LOGIN=tu_numero_cuenta")
        print("   MT5_PASSWORD=tu_password")
        print("   MT5_SERVER=ZevenGlobal-Demo")
        print("   MT5_SYMBOL=XAUUSD")
        return False
    
    print(f"   Login: {MT5_LOGIN}")
    print(f"   Server: {MT5_SERVER}")
    print(f"   Symbol: {MT5_SYMBOL}")
    
    # 1. Inicializa MT5
    print("\n🔌 Inicializando MT5...")
    if not mt5.initialize():
        error = mt5.last_error()
        print(f"❌ Error al inicializar MT5: {error}")
        print("\nPosibles soluciones:")
        print("1. Verifica que MetaTrader 5 esté instalado")
        print("2. Abre MetaTrader 5 manualmente")
        print("3. Verifica que tengas permisos de administrador si es necesario")
        return False
    
    print("✅ MT5 inicializado")
    
    # 2. Intenta conectar
    print(f"\n🔐 Conectando a cuenta {MT5_LOGIN} en servidor {MT5_SERVER}...")
    if not mt5.login(MT5_LOGIN, password=MT5_PASSWORD, server=MT5_SERVER):
        error = mt5.last_error()
        print(f"❌ Error al conectar: {error}")
        print("\nPosibles causas:")
        print("1. Credenciales incorrectas")
        print("2. Servidor incorrecto (verifica si es Demo o Real)")
        print("3. Cuenta no existe o está deshabilitada")
        print("4. Necesitas estar conectado a internet")
        mt5.shutdown()
        return False
    
    print("✅ Conexión exitosa")
    
    # 3. Muestra información de la cuenta
    print("\n📊 Información de la cuenta:")
    account_info = mt5.account_info()
    if account_info:
        print(f"   Nombre: {account_info.name}")
        print(f"   Balance: ${account_info.balance:,.2f}")
        print(f"   Equity: ${account_info.equity:,.2f}")
        print(f"   Margen libre: ${account_info.margin_free:,.2f}")
        print(f"   Leverage: 1:{account_info.leverage}")
        print(f"   Servidor: {account_info.server}")
        print(f"   Moneda: {account_info.currency}")
    else:
        print("   ⚠️ No se pudo obtener información de la cuenta")
    
    # 4. Verifica símbolo
    print(f"\n📈 Verificando símbolo {MT5_SYMBOL}...")
    symbol_info = mt5.symbol_info(MT5_SYMBOL)
    
    if symbol_info is None:
        print(f"❌ Símbolo {MT5_SYMBOL} no encontrado")
        print("\nPosibles soluciones:")
        print("1. Verifica el nombre exacto del símbolo en MT5")
        print("2. Puede ser 'XAUUSD' o 'XAUUSD.m'")
        print("3. En MT5, haz clic derecho en el símbolo → 'Mostrar'")
        print("4. Verifica que el símbolo esté disponible en tu broker")
        
        # Intenta buscar símbolos similares
        print("\n🔍 Buscando símbolos similares...")
        symbols = mt5.symbols_get()
        if symbols:
            gold_symbols = [s.name for s in symbols if 'GOLD' in s.name.upper() or 'XAU' in s.name.upper()]
            if gold_symbols:
                print("   Símbolos encontrados relacionados con oro:")
                for sym in gold_symbols[:10]:  # Muestra los primeros 10
                    print(f"   - {sym}")
        
        mt5.shutdown()
        return False
    
    # Activa el símbolo si no está visible
    if not symbol_info.visible:
        print(f"   Activando símbolo {MT5_SYMBOL}...")
        if not mt5.symbol_select(MT5_SYMBOL, True):
            print(f"❌ No se pudo activar el símbolo")
            mt5.shutdown()
            return False
    
    print(f"✅ Símbolo {MT5_SYMBOL} disponible")
    print(f"   Descripción: {symbol_info.description}")
    print(f"   Spread: {symbol_info.spread} puntos")
    print(f"   Digits: {symbol_info.digits}")
    print(f"   Contract size: {symbol_info.trade_contract_size}")
    
    # 5. Obtiene precio actual
    print(f"\n💰 Precio actual de {MT5_SYMBOL}:")
    import pandas as pd
    tick = mt5.symbol_info_tick(MT5_SYMBOL)
    if tick:
        print(f"   Bid (venta): ${tick.bid:.2f}")
        print(f"   Ask (compra): ${tick.ask:.2f}")
        print(f"   Spread: ${(tick.ask - tick.bid):.2f}")
        print(f"   Última actualización: {pd.Timestamp.fromtimestamp(tick.time)}")
    else:
        print("   ⚠️ No se pudo obtener el precio actual")
    
    # 6. Prueba obtener velas
    print(f"\n📊 Probando obtención de velas...")
    rates = mt5.copy_rates_from_pos(MT5_SYMBOL, mt5.TIMEFRAME_M1, 0, 10)
    if rates is not None and len(rates) > 0:
        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        print(f"✅ Se obtuvieron {len(df)} velas de M1")
        print(f"   Última vela: {df.iloc[-1]['time']}")
        print(f"   Close: ${df.iloc[-1]['close']:.2f}")
    else:
        print("⚠️ No se pudieron obtener velas")
    
    # 7. Verifica posiciones abiertas
    print(f"\n📋 Posiciones abiertas:")
    positions = mt5.positions_get(symbol=MT5_SYMBOL)
    if positions is None:
        if mt5.last_error()[0] == mt5.RES_S_OK:
            print("   No hay posiciones abiertas")
        else:
            print(f"   ⚠️ Error al obtener posiciones: {mt5.last_error()}")
    elif len(positions) == 0:
        print("   No hay posiciones abiertas")
    else:
        print(f"   Tienes {len(positions)} posición(es) abierta(s):")
        for pos in positions:
            print(f"   - Ticket {pos.ticket}: {pos.type} {pos.volume} lotes")
            print(f"     Entrada: ${pos.price_open:.2f} | P&L: ${pos.profit:+.2f}")
    
    # Cierra conexión
    print("\n🔌 Cerrando conexión...")
    mt5.shutdown()
    print("✅ Conexión cerrada")
    
    print("\n" + "=" * 70)
    print("✅ PRUEBA COMPLETADA EXITOSAMENTE")
    print("=" * 70)
    print("\nTu conexión con MT5 está funcionando correctamente.")
    print("Ahora puedes ejecutar el bot de trading con:")
    print("  python live/mt5_trading.py")
    
    return True


if __name__ == "__main__":
    try:
        success = test_mt5_connection()
        if not success:
            print("\n❌ La conexión falló. Revisa los errores arriba.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⏹️ Prueba cancelada por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

