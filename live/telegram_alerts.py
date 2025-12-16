"""
live/telegram_alerts.py - Sistema de Alertas de Telegram

Envía notificaciones al bot de Telegram cuando ocurren eventos importantes.
"""

import requests
from typing import Dict, Optional
from datetime import datetime

# Importar logger si está disponible
try:
    from utils.logger import logger
except ImportError:
    logger = None


class TelegramAlerts:
    """
    Sistema de alertas para Telegram.
    
    Envía notificaciones cuando:
    - Se genera una señal
    - Se ejecuta un trade
    - Se cierra un trade
    - Se mueve SL a break-even
    - Se realiza un cierre parcial
    - Hay métricas importantes
    - Hay errores críticos
    """
    
    def __init__(self, bot_token: str, chat_id: str):
        """
        Inicializa el sistema de alertas de Telegram.
        
        Args:
            bot_token: Token del bot de Telegram (obtenido de @BotFather)
            chat_id: ID del chat donde enviar mensajes (tu ID o ID del grupo)
        """
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{bot_token}"
        self.enabled = bool(bot_token and chat_id)
        
        if self.enabled:
            try:
                # Verifica que el bot funciona
                response = requests.get(f"{self.base_url}/getMe", timeout=5)
                if response.status_code == 200:
                    bot_info = response.json()
                    if bot_info.get("ok"):
                        bot_username = bot_info['result'].get('username', 'Unknown')
                        if logger:
                            logger.info(f"✅ Telegram bot conectado: @{bot_username}")
                        print(f"✅ Telegram bot conectado: @{bot_username}")
                    else:
                        if logger:
                            logger.warning("⚠️ Token de Telegram inválido")
                        print("⚠️ Token de Telegram inválido")
                        self.enabled = False
                else:
                    if logger:
                        logger.warning("⚠️ No se pudo conectar con Telegram")
                    print("⚠️ No se pudo conectar con Telegram")
                    self.enabled = False
            except Exception as e:
                if logger:
                    logger.warning(f"⚠️ Error al verificar Telegram: {e}")
                print(f"⚠️ Error al verificar Telegram: {e}")
                self.enabled = False
    
    def send_message(self, message: str, parse_mode: str = "HTML") -> bool:
        """
        Envía un mensaje a Telegram.
        
        Args:
            message: Mensaje a enviar
            parse_mode: Modo de parseo (HTML o Markdown)
        
        Returns:
            True si se envió exitosamente, False en caso contrario
        """
        if not self.enabled:
            return False
        
        try:
            url = f"{self.base_url}/sendMessage"
            data = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": parse_mode
            }
            
            response = requests.post(url, json=data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("ok"):
                    return True
                else:
                    error_desc = result.get('description', 'Unknown error')
                    if logger:
                        logger.warning(f"⚠️ Error Telegram: {error_desc}")
                    return False
            else:
                if logger:
                    logger.warning(f"⚠️ Error HTTP Telegram: {response.status_code}")
                return False
                
        except Exception as e:
            if logger:
                logger.error(f"❌ Error al enviar mensaje a Telegram: {e}")
            return False
    
    def send_signal_alert(self, signal: Dict) -> bool:
        """
        Envía alerta cuando se genera una señal.
        
        Args:
            signal: Diccionario con información de la señal
        """
        direction_emoji = "🟢" if signal.get("signal") == "BUY" else "🔴"
        
        message = f"""
{direction_emoji} <b>NUEVA SEÑAL DETECTADA</b>

📊 <b>Símbolo:</b> {signal.get('symbol', 'XAUUSD')}
📈 <b>Dirección:</b> {signal.get('signal', 'N/A')}
💰 <b>Entrada:</b> ${signal.get('entry_price', 0):.2f}
🛑 <b>Stop Loss:</b> ${signal.get('stop_loss', 0):.2f}
🎯 <b>TP1:</b> ${signal.get('take_profit_1', 0):.2f}
📊 <b>Risk:Reward:</b> 1:{signal.get('risk_reward', 0):.2f}

✅ <b>Confirmaciones:</b> {len(signal.get('justifications', []))}
"""
        
        if signal.get('justifications'):
            message += "\n📋 <b>Razones:</b>\n"
            for i, reason in enumerate(signal.get('justifications', [])[:3], 1):
                message += f"   {i}. {reason}\n"
        
        message += f"\n⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        return self.send_message(message)
    
    def send_trade_opened(self, ticket: int, signal: Dict, lot_size: float) -> bool:
        """
        Envía alerta cuando se abre un trade.
        
        Args:
            ticket: Ticket de la orden
            signal: Información de la señal
            lot_size: Tamaño de la posición
        """
        direction_emoji = "🟢" if signal.get("signal") == "BUY" else "🔴"
        
        message = f"""
{direction_emoji} <b>TRADE EJECUTADO</b>

🎫 <b>Ticket:</b> {ticket}
📊 <b>Símbolo:</b> {signal.get('symbol', 'XAUUSD')}
📈 <b>Dirección:</b> {signal.get('signal', 'N/A')}
💰 <b>Entrada:</b> ${signal.get('entry_price', 0):.2f}
📦 <b>Tamaño:</b> {lot_size:.2f} lotes
🛑 <b>Stop Loss:</b> ${signal.get('stop_loss', 0):.2f}
🎯 <b>TP1:</b> ${signal.get('take_profit_1', 0):.2f}
📊 <b>Risk:Reward:</b> 1:{signal.get('risk_reward', 0):.2f}

⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        return self.send_message(message)
    
    def send_trade_closed(self, ticket: int, pnl: float, pnl_pct: float, 
                         exit_reason: str) -> bool:
        """
        Envía alerta cuando se cierra un trade.
        
        Args:
            ticket: Ticket de la orden
            pnl: P&L del trade
            pnl_pct: P&L porcentual
            exit_reason: Razón de salida
        """
        emoji = "✅" if pnl > 0 else "❌"
        pnl_emoji = "💰" if pnl > 0 else "📉"
        
        message = f"""
{emoji} <b>TRADE CERRADO</b>

🎫 <b>Ticket:</b> {ticket}
{pnl_emoji} <b>P&L:</b> ${pnl:.2f} ({pnl_pct:+.2f}%)
📋 <b>Razón:</b> {exit_reason}

⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        return self.send_message(message)
    
    def send_position_update(self, action: str, ticket: int, details: str = "") -> bool:
        """
        Envía alerta cuando se actualiza una posición.
        
        Args:
            action: Acción realizada (SL_MOVED_TO_BE, PARTIAL_CLOSE, etc.)
            ticket: Ticket de la posición
            details: Detalles adicionales
        """
        emoji_map = {
            "SL_MOVED_TO_BE": "🛡️",
            "PARTIAL_CLOSE_TP1": "📊",
            "PARTIAL_CLOSE_TP2": "📊",
        }
        
        action_map = {
            "SL_MOVED_TO_BE": "SL Movido a Break-Even",
            "PARTIAL_CLOSE_TP1": "Cierre Parcial (50% en TP1)",
            "PARTIAL_CLOSE_TP2": "Cierre Parcial (25% en TP2)",
        }
        
        emoji = emoji_map.get(action, "⚙️")
        action_text = action_map.get(action, action)
        
        message = f"""
{emoji} <b>POSICIÓN ACTUALIZADA</b>

🎫 <b>Ticket:</b> {ticket}
📋 <b>Acción:</b> {action_text}
"""
        
        if details:
            message += f"\n{details}"
        
        message += f"\n⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        return self.send_message(message)
    
    def send_metrics(self, metrics: Dict) -> bool:
        """
        Envía métricas de performance.
        
        Args:
            metrics: Diccionario con métricas
        """
        if metrics.get("total_trades", 0) == 0:
            return False
        
        win_rate = metrics.get("win_rate", 0)
        win_rate_emoji = "🟢" if win_rate >= 50 else "🟡" if win_rate >= 40 else "🔴"
        
        profit_factor = metrics.get("profit_factor", 0)
        pf_emoji = "🟢" if profit_factor >= 1.5 else "🟡" if profit_factor >= 1.0 else "🔴"
        
        message = f"""
📊 <b>MÉTRICAS DE PERFORMANCE</b>

📈 <b>Trades:</b> {metrics.get('total_trades', 0)}
{win_rate_emoji} <b>Win Rate:</b> {win_rate:.1f}%
💰 <b>P&L Total:</b> ${metrics.get('total_pnl', 0):.2f}
{pf_emoji} <b>Profit Factor:</b> {metrics.get('profit_factor', 0):.2f}
📊 <b>Avg Risk:Reward:</b> 1:{metrics.get('avg_risk_reward', 0):.2f}

✅ <b>Ganadores:</b> {metrics.get('winning_trades', 0)}
❌ <b>Perdedores:</b> {metrics.get('losing_trades', 0)}

⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        return self.send_message(message)
    
    def send_error(self, error_message: str) -> bool:
        """
        Envía alerta de error crítico.
        
        Args:
            error_message: Mensaje de error
        """
        message = f"""
⚠️ <b>ERROR CRÍTICO</b>

{error_message}

⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        return self.send_message(message)
    
    def send_daily_report(self, report: Dict) -> bool:
        """
        Envía reporte diario detallado.
        
        Args:
            report: Diccionario con el reporte
        """
        metrics = report.get("metrics", {})
        today_trades = report.get("today_trades", [])
        open_positions = report.get("open_positions", [])
        
        if metrics.get("total_trades", 0) == 0 and len(today_trades) == 0:
            message = f"""
📊 <b>REPORTE DIARIO</b>

📅 <b>Fecha:</b> {datetime.now().strftime('%Y-%m-%d')}

ℹ️ Sin operaciones hoy

⏰ {datetime.now().strftime('%H:%M:%S')}
"""
            return self.send_message(message)
        
        win_rate = metrics.get("win_rate", 0)
        win_rate_emoji = "🟢" if win_rate >= 50 else "🟡" if win_rate >= 40 else "🔴"
        
        profit_factor = metrics.get("profit_factor", 0)
        pf_emoji = "🟢" if profit_factor >= 1.5 else "🟡" if profit_factor >= 1.0 else "🔴"
        
        pnl = metrics.get("total_pnl", 0)
        pnl_emoji = "💰" if pnl > 0 else "📉" if pnl < 0 else "➖"
        
        message = f"""
📊 <b>REPORTE DIARIO DE OPERACIONES</b>

📅 <b>Fecha:</b> {datetime.now().strftime('%Y-%m-%d')}

━━━━━━━━━━━━━━━━━━━━
📈 <b>RESUMEN DEL DÍA</b>
━━━━━━━━━━━━━━━━━━━━

📊 <b>Trades Cerrados:</b> {metrics.get('total_trades', 0)}
{win_rate_emoji} <b>Win Rate:</b> {win_rate:.1f}%
{pnl_emoji} <b>P&L Total:</b> ${pnl:.2f}
{pf_emoji} <b>Profit Factor:</b> {metrics.get('profit_factor', 0):.2f}
📊 <b>Avg Risk:Reward:</b> 1:{metrics.get('avg_risk_reward', 0):.2f}

✅ <b>Ganadores:</b> {metrics.get('winning_trades', 0)}
❌ <b>Perdedores:</b> {metrics.get('losing_trades', 0)}
"""
        
        # Agrega trades del día si hay
        if today_trades:
            message += f"\n━━━━━━━━━━━━━━━━━━━━\n📋 <b>TRADES DEL DÍA ({len(today_trades)})</b>\n━━━━━━━━━━━━━━━━━━━━\n"
            for i, trade in enumerate(today_trades[:10], 1):  # Máximo 10 trades
                direction_emoji = "🟢" if trade.get("direction") == "BUY" else "🔴"
                pnl_trade = trade.get("pnl", 0)
                pnl_trade_emoji = "✅" if pnl_trade > 0 else "❌"
                
                if trade.get("exit_time"):
                    # Trade cerrado
                    message += f"\n{i}. {direction_emoji} <b>{trade.get('direction', 'N/A')}</b> | Ticket: {trade.get('ticket', 'N/A')}\n"
                    message += f"   {pnl_trade_emoji} P&L: ${pnl_trade:.2f} | RR: 1:{trade.get('risk_reward', 0):.2f}\n"
                else:
                    # Trade abierto
                    message += f"\n{i}. {direction_emoji} <b>{trade.get('direction', 'N/A')}</b> | Ticket: {trade.get('ticket', 'N/A')}\n"
                    message += f"   ⏳ <b>ABIERTO</b> | Entrada: ${trade.get('entry_price', 0):.2f}\n"
        
        # Agrega posiciones abiertas
        if open_positions:
            message += f"\n━━━━━━━━━━━━━━━━━━━━\n📦 <b>POSICIONES ABIERTAS ({len(open_positions)})</b>\n━━━━━━━━━━━━━━━━━━━━\n"
            for i, pos in enumerate(open_positions[:5], 1):  # Máximo 5 posiciones
                direction_emoji = "🟢" if pos.get("direction") == "BUY" else "🔴"
                unrealized_pnl = pos.get("unrealized_pnl", 0)
                pnl_emoji = "💰" if unrealized_pnl > 0 else "📉" if unrealized_pnl < 0 else "➖"
                
                message += f"\n{i}. {direction_emoji} <b>{pos.get('direction', 'N/A')}</b> | Ticket: {pos.get('ticket', 'N/A')}\n"
                message += f"   {pnl_emoji} P&L No Realizado: ${unrealized_pnl:.2f}\n"
                message += f"   📊 Entrada: ${pos.get('entry_price', 0):.2f} | SL: ${pos.get('stop_loss', 0):.2f} | TP: ${pos.get('take_profit', 0):.2f}\n"
        
        message += f"\n⏰ {datetime.now().strftime('%H:%M:%S')}"
        
        return self.send_message(message)
    
    def send_operations_report(self, db, include_open_positions: bool = True) -> bool:
        """
        Envía reporte detallado de operaciones.
        
        Args:
            db: Instancia de TradingDatabase
            include_open_positions: Si incluir posiciones abiertas
        """
        if not db:
            return False
        
        # Obtiene métricas del día
        today_metrics = db.get_performance_metrics(today_only=True)
        
        # Obtiene trades del día
        today_trades = db.get_today_closed_trades()
        
        # Obtiene posiciones abiertas
        open_positions = []
        if include_open_positions:
            open_positions = db.get_open_positions()
        
        # Crea el reporte
        report = {
            "date": datetime.now().date(),
            "metrics": today_metrics,
            "today_trades": today_trades,
            "open_positions": open_positions
        }
        
        return self.send_daily_report(report)
    
    def send_bot_started(self, account_info: Dict = None) -> bool:
        """
        Envía notificación cuando el bot se inicia.
        
        Args:
            account_info: Información de la cuenta MT5 (opcional)
        """
        message = f"""
🚀 <b>BOT INICIADO</b>

✅ El bot de trading ha sido iniciado correctamente

⏰ <b>Hora:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        if account_info:
            message += f"""
📊 <b>Información de la cuenta:</b>
💰 Balance: ${account_info.get('balance', 0):.2f}
💵 Equity: ${account_info.get('equity', 0):.2f}
📈 Leverage: {account_info.get('leverage', 0)}
"""
        
        message += f"\n🤖 El bot está operando y monitoreando el mercado..."
        
        return self.send_message(message)
    
    def send_bot_stopped(self, reason: str = "Usuario", uptime: str = None) -> bool:
        """
        Envía notificación cuando el bot se detiene.
        
        Args:
            reason: Razón de la detención (Usuario, Error, etc.)
            uptime: Tiempo que estuvo activo (opcional)
        """
        reason_emoji = {
            "Usuario": "👤",
            "Error": "❌",
            "KeyboardInterrupt": "👤",
            "Exception": "⚠️"
        }.get(reason, "⏹️")
        
        message = f"""
{reason_emoji} <b>BOT DETENIDO</b>

⏹️ El bot de trading ha sido detenido

📋 <b>Razón:</b> {reason}
⏰ <b>Hora:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        if uptime:
            message += f"\n⏱️ <b>Tiempo activo:</b> {uptime}"
        
        message += f"\n\n✅ El bot se ha cerrado correctamente"
        
        return self.send_message(message)

