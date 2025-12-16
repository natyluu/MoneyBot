"""
test_telegram.py - Script para probar la conexión con Telegram
"""

import sys
import os

# Agregar el directorio raíz al path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

try:
    from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
    from live.telegram_alerts import TelegramAlerts
    
    print("=" * 70)
    print("🧪 PRUEBA DE CONEXIÓN CON TELEGRAM")
    print("=" * 70)
    print()
    
    # Verifica que las variables estén configuradas
    if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == "":
        print("❌ ERROR: TELEGRAM_BOT_TOKEN no está configurado en .env")
        print("   Agrega: TELEGRAM_BOT_TOKEN=tu_token_aqui")
        sys.exit(1)
    
    if not TELEGRAM_CHAT_ID or TELEGRAM_CHAT_ID == "":
        print("❌ ERROR: TELEGRAM_CHAT_ID no está configurado en .env")
        print("   Agrega: TELEGRAM_CHAT_ID=tu_chat_id_aqui")
        sys.exit(1)
    
    print(f"✅ Token encontrado: {TELEGRAM_BOT_TOKEN[:10]}...")
    print(f"✅ Chat ID encontrado: {TELEGRAM_CHAT_ID}")
    print()
    
    # Inicializa Telegram
    print("Inicializando Telegram...")
    telegram = TelegramAlerts(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)
    
    if not telegram.enabled:
        print("❌ Telegram no está habilitado")
        sys.exit(1)
    
    print("✅ Telegram inicializado correctamente")
    print()
    
    # Envía mensaje de prueba
    print("Enviando mensaje de prueba...")
    success = telegram.send_message("🧪 <b>PRUEBA DE CONEXIÓN</b>\n\nSi ves este mensaje, Telegram está funcionando correctamente! ✅")
    
    if success:
        print("✅ MENSAJE ENVIADO EXITOSAMENTE")
        print()
        print("Revisa tu Telegram - deberías haber recibido el mensaje de prueba")
    else:
        print("❌ NO SE PUDO ENVIAR EL MENSAJE")
        print()
        print("Posibles causas:")
        print("  1. Token incorrecto")
        print("  2. Chat ID incorrecto")
        print("  3. Problema de conexión a internet")
        print("  4. El bot no tiene permisos para enviar mensajes")
    
    print()
    print("=" * 70)
    
except ImportError as e:
    print(f"❌ Error al importar módulos: {e}")
    print("   Asegúrate de estar en la carpeta correcta del proyecto")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

