"""
Script wrapper para ejecutar el bot con output forzado inmediato
Este script fuerza que todos los mensajes aparezcan inmediatamente
"""

import sys
import os
import subprocess

# Configurar variables de entorno para unbuffered
os.environ['PYTHONUNBUFFERED'] = '1'
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Cambiar al directorio del script
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Configurar stdout y stderr para unbuffered
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace', line_buffering=True)
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace', line_buffering=True)

# Forzar flush inmediato
sys.stdout.flush()
sys.stderr.flush()

print("🔧 Iniciando bot con output forzado...", flush=True)
sys.stdout.flush()

# Importar y ejecutar el bot
try:
    # Cambiar al directorio live
    live_dir = os.path.join(script_dir, 'live')
    if os.path.exists(live_dir):
        sys.path.insert(0, script_dir)
        
        # Importar el módulo
        from live.mt5_trading import run_auto_trading_loop
        
        # Ejecutar el bot
        run_auto_trading_loop(analysis_interval=180, update_interval=30)
    else:
        print("❌ No se encontró el directorio 'live'", flush=True)
        sys.exit(1)
        
except KeyboardInterrupt:
    print("\n\n⏹️ Bot detenido por el usuario", flush=True)
    sys.stdout.flush()
except Exception as e:
    print(f"\n❌ Error: {e}", flush=True)
    import traceback
    traceback.print_exc()
    sys.stdout.flush()
    sys.stderr.flush()




