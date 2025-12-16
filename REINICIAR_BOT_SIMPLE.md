# 🔄 Reiniciar el Bot - Pasos Rápidos

## PASO 1: Detener el Bot Actual

En la ventana de PowerShell donde está corriendo el bot:
- Presiona `Ctrl + C`
- Espera a que se detenga completamente

## PASO 2: Reiniciar el Bot

Ejecuta estos comandos uno por uno:

```powershell
cd "C:\BOT\trading-bot-windows-20251210 on 'Mac'"
python -c "import sys; sys.path.insert(0, '.'); exec(open('live/mt5_trading.py', encoding='utf-8').read())"
```

## ✅ Listo!

El bot debería iniciar con los cambios aplicados. Ahora las señales deberían tener un Risk:Reward correcto (≥ 2.0) y no ser rechazadas.




