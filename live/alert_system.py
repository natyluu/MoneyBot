"""
live/alert_system.py - Sistema de Alertas

Sistema para enviar alertas cuando se generan señales de trading.
Soporta múltiples canales: consola, archivo, email, webhook, etc.
"""

import json
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import asdict
from strategy.ict_hybrid_strategy import TradingSignal


class AlertSystem:
    """
    Sistema de alertas para señales de trading.
    
    Permite enviar alertas a múltiples canales cuando se detectan señales.
    """
    
    def __init__(self, alert_file: Optional[str] = None, 
                 webhook_url: Optional[str] = None,
                 email_config: Optional[Dict] = None):
        """
        Inicializa el sistema de alertas.
        
        Args:
            alert_file: Ruta al archivo donde guardar alertas (opcional)
            webhook_url: URL de webhook para enviar alertas (opcional)
            email_config: Configuración de email {'smtp_server', 'port', 'user', 'password', 'to'} (opcional)
        """
        self.alert_file = alert_file
        self.webhook_url = webhook_url
        self.email_config = email_config
        self.alert_history: List[Dict] = []
    
    def send_alert(self, signal: TradingSignal, alert_type: str = "SIGNAL"):
        """
        Envía una alerta cuando se detecta una señal.
        
        Args:
            signal: TradingSignal a alertar
            alert_type: Tipo de alerta (default: "SIGNAL")
        """
        alert_data = {
            'timestamp': datetime.now().isoformat(),
            'type': alert_type,
            'symbol': 'XAUUSD',  # Por defecto, puede ajustarse
            'direction': signal.direction,
            'operation': signal.operation_type,
            'entry_price': signal.entry_price,
            'stop_loss': signal.stop_loss,
            'take_profit_1': signal.take_profit_1,
            'take_profit_2': signal.take_profit_2,
            'take_profit_final': signal.take_profit_final,
            'risk_reward': signal.risk_reward,
            'justifications': signal.justifications,
            'active_zones': len(signal.active_zones)
        }
        
        # Guarda en historial
        self.alert_history.append(alert_data)
        
        # Envía a diferentes canales
        self._send_to_console(alert_data)
        
        if self.alert_file:
            self._send_to_file(alert_data)
        
        if self.webhook_url:
            self._send_to_webhook(alert_data)
        
        if self.email_config:
            self._send_to_email(alert_data)
    
    def _send_to_console(self, alert_data: Dict):
        """Envía alerta a la consola"""
        print("\n" + "=" * 70)
        print("🚨 ALERTA DE TRADING")
        print("=" * 70)
        print(f"Timestamp: {alert_data['timestamp']}")
        print(f"Tipo: {alert_data['type']}")
        print(f"Símbolo: {alert_data['symbol']}")
        print(f"\n📊 Señal:")
        print(f"   Dirección: {alert_data['direction']}")
        print(f"   Operación: {alert_data['operation']}")
        print(f"   Entrada: ${alert_data['entry_price']:.2f}")
        print(f"   Stop Loss: ${alert_data['stop_loss']:.2f}")
        print(f"   TP1: ${alert_data['take_profit_1']:.2f}")
        print(f"   TP2: ${alert_data['take_profit_2']:.2f}")
        print(f"   TP Final: ${alert_data['take_profit_final']:.2f}")
        print(f"   Risk:Reward: 1:{alert_data['risk_reward']:.2f}")
        print(f"\n📋 Justificaciones:")
        for i, justification in enumerate(alert_data['justifications'], 1):
            print(f"   {i}. {justification}")
        print(f"\n🎯 Zonas Activas: {alert_data['active_zones']}")
        print("=" * 70 + "\n")
    
    def _send_to_file(self, alert_data: Dict):
        """Guarda alerta en archivo"""
        try:
            import os
            os.makedirs(os.path.dirname(self.alert_file) if os.path.dirname(self.alert_file) else '.', exist_ok=True)
            
            mode = 'a' if os.path.exists(self.alert_file) else 'w'
            with open(self.alert_file, mode) as f:
                f.write(json.dumps(alert_data, indent=2) + '\n\n')
        except Exception as e:
            print(f"⚠️ Error al guardar alerta en archivo: {e}")
    
    def _send_to_webhook(self, alert_data: Dict):
        """Envía alerta a webhook (Discord, Slack, Telegram, etc.)"""
        try:
            import requests
            
            # Formatea el mensaje para webhook
            message = {
                "content": f"🚨 Señal de Trading: {alert_data['operation']} {alert_data['symbol']}",
                "embeds": [{
                    "title": f"Señal {alert_data['operation']} - {alert_data['symbol']}",
                    "fields": [
                        {"name": "Entrada", "value": f"${alert_data['entry_price']:.2f}", "inline": True},
                        {"name": "Stop Loss", "value": f"${alert_data['stop_loss']:.2f}", "inline": True},
                        {"name": "TP Final", "value": f"${alert_data['take_profit_final']:.2f}", "inline": True},
                        {"name": "Risk:Reward", "value": f"1:{alert_data['risk_reward']:.2f}", "inline": True},
                        {"name": "Dirección", "value": alert_data['direction'], "inline": True},
                    ],
                    "timestamp": alert_data['timestamp']
                }]
            }
            
            response = requests.post(self.webhook_url, json=message, timeout=5)
            if response.status_code != 200:
                print(f"⚠️ Error al enviar webhook: {response.status_code}")
        except ImportError:
            print("⚠️ requests no está instalado. Instala con: pip install requests")
        except Exception as e:
            print(f"⚠️ Error al enviar webhook: {e}")
    
    def _send_to_email(self, alert_data: Dict):
        """Envía alerta por email"""
        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            
            msg = MIMEMultipart()
            msg['From'] = self.email_config.get('user')
            msg['To'] = self.email_config.get('to')
            msg['Subject'] = f"🚨 Señal de Trading: {alert_data['operation']} {alert_data['symbol']}"
            
            body = f"""
Señal de Trading Detectada

Símbolo: {alert_data['symbol']}
Operación: {alert_data['operation']}
Dirección: {alert_data['direction']}

Precios:
- Entrada: ${alert_data['entry_price']:.2f}
- Stop Loss: ${alert_data['stop_loss']:.2f}
- TP1: ${alert_data['take_profit_1']:.2f}
- TP2: ${alert_data['take_profit_2']:.2f}
- TP Final: ${alert_data['take_profit_final']:.2f}

Risk:Reward: 1:{alert_data['risk_reward']:.2f}

Justificaciones:
{chr(10).join(f"- {j}" for j in alert_data['justifications'])}

Timestamp: {alert_data['timestamp']}
"""
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(self.email_config.get('smtp_server'), 
                                self.email_config.get('port', 587))
            server.starttls()
            server.login(self.email_config.get('user'), self.email_config.get('password'))
            server.send_message(msg)
            server.quit()
            
        except Exception as e:
            print(f"⚠️ Error al enviar email: {e}")
    
    def get_alert_history(self, limit: int = 10) -> List[Dict]:
        """Obtiene el historial de alertas"""
        return self.alert_history[-limit:]













