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
        
        # Verifica si hay trades del día (abiertos o cerrados) o posiciones abiertas
        has_trades = len(today_trades) > 0
        has_open_positions = len(open_positions) > 0
        has_closed_trades = metrics.get("total_trades", 0) > 0
        
        if not has_trades and not has_open_positions and not has_closed_trades:
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
        
        # Cuenta trades abiertos y cerrados
        open_trades_count = sum(1 for t in today_trades if not t.get("exit_time"))
        closed_trades_count = sum(1 for t in today_trades if t.get("exit_time"))
        total_trades_today = len(today_trades)
        
        message = f"""
📊 <b>REPORTE DIARIO DE OPERACIONES</b>

📅 <b>Fecha:</b> {datetime.now().strftime('%Y-%m-%d')}

━━━━━━━━━━━━━━━━━━━━
📈 <b>RESUMEN DEL DÍA</b>
━━━━━━━━━━━━━━━━━━━━

📊 <b>Total Trades Hoy:</b> {total_trades_today} (⏳ {open_trades_count} abiertos | ✅ {closed_trades_count} cerrados)
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
            # Separa trades abiertos y cerrados
            closed_trades_list = [t for t in today_trades if t.get("exit_time")]
            open_trades_list = [t for t in today_trades if not t.get("exit_time")]
            
            message += f"\n━━━━━━━━━━━━━━━━━━━━\n📋 <b>TRADES DEL DÍA ({len(today_trades)})</b>\n━━━━━━━━━━━━━━━━━━━━\n"
            
            # Muestra trades cerrados primero
            if closed_trades_list:
                message += f"\n✅ <b>TRADES CERRADOS ({len(closed_trades_list)})</b>\n"
                for i, trade in enumerate(closed_trades_list[:10], 1):  # Máximo 10 trades
                    direction_emoji = "🟢" if trade.get("direction") == "BUY" else "🔴"
                    pnl_trade = trade.get("pnl", 0) or 0
                    pnl_trade_emoji = "✅" if pnl_trade > 0 else "❌" if pnl_trade < 0 else "➖"
                    
                    message += f"\n{i}. {direction_emoji} <b>{trade.get('direction', 'N/A')}</b> | Ticket: {trade.get('ticket', 'N/A')}\n"
                    message += f"   {pnl_trade_emoji} P&L: ${pnl_trade:.2f} | RR: 1:{trade.get('risk_reward', 0):.2f}\n"
            
            # Muestra trades abiertos
            if open_trades_list:
                message += f"\n⏳ <b>TRADES ABIERTOS ({len(open_trades_list)})</b>\n"
                for i, trade in enumerate(open_trades_list[:10], 1):  # Máximo 10 trades
                    direction_emoji = "🟢" if trade.get("direction") == "BUY" else "🔴"
                    
                    message += f"\n{i}. {direction_emoji} <b>{trade.get('direction', 'N/A')}</b> | Ticket: {trade.get('ticket', 'N/A')}\n"
                    message += f"   📊 Entrada: ${trade.get('entry_price', 0):.2f} | SL: ${trade.get('stop_loss', 0):.2f} | TP: ${trade.get('take_profit', 0):.2f}\n"
                    message += f"   📈 RR: 1:{trade.get('risk_reward', 0):.2f}\n"
        
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
    
    def send_operations_report(self, db, include_open_positions: bool = True, current_positions: list = None) -> bool:
        """
        Envía reporte detallado de operaciones.
        
        Args:
            db: Instancia de TradingDatabase
            include_open_positions: Si incluir posiciones abiertas
            current_positions: Lista de posiciones actuales desde MT5 (opcional)
        """
        if not db:
            return False
        
        try:
            # Obtiene métricas del día (solo trades cerrados)
            today_metrics = db.get_performance_metrics(today_only=True)
            
            # Obtiene TODOS los trades del día (abiertos y cerrados)
            today_trades = db.get_today_trades()
            
            # Obtiene posiciones abiertas
            open_positions = []
            if include_open_positions:
                # Prioriza posiciones desde MT5 si se proporcionan
                if current_positions is not None and len(current_positions) > 0:
                    # Convierte formato MT5 a formato del reporte
                    open_positions = []
                    for pos in current_positions:
                        open_positions.append({
                            "ticket": pos.get("ticket"),
                            "symbol": pos.get("symbol"),
                            "direction": pos.get("type"),  # "BUY" o "SELL"
                            "entry_price": pos.get("entry_price"),
                            "current_price": pos.get("current_price"),
                            "stop_loss": pos.get("stop_loss"),
                            "take_profit": pos.get("take_profit"),
                            "unrealized_pnl": pos.get("profit", 0),
                            "volume": pos.get("volume")
                        })
                else:
                    # Intenta obtener desde MT5 directamente
                    try:
                        import MetaTrader5 as mt5
                        mt5_positions = mt5.positions_get()
                        if mt5_positions:
                            open_positions = []
                            for pos in mt5_positions:
                                open_positions.append({
                                    "ticket": pos.ticket,
                                    "symbol": pos.symbol,
                                    "direction": "BUY" if pos.type == mt5.ORDER_TYPE_BUY else "SELL",
                                    "entry_price": pos.price_open,
                                    "current_price": pos.price_current,
                                    "stop_loss": pos.sl,
                                    "take_profit": pos.tp,
                                    "unrealized_pnl": pos.profit,
                                    "volume": pos.volume
                                })
                    except Exception as e:
                        if logger:
                            logger.warning(f"No se pudieron obtener posiciones desde MT5: {e}")
                        # Fallback a base de datos
                        open_positions = db.get_open_positions()
            
            # Log para debugging
            if logger:
                logger.info(f"📊 Reporte: {len(today_trades)} trades del día, {len(open_positions)} posiciones abiertas")
            
            # Crea el reporte
            report = {
                "date": datetime.now().date(),
                "metrics": today_metrics,
                "today_trades": today_trades,  # Ahora incluye abiertos y cerrados
                "open_positions": open_positions
            }
            
            return self.send_daily_report(report)
        except Exception as e:
            if logger:
                logger.error(f"Error al generar reporte de operaciones: {e}", exc_info=True)
            return False
    
    def send_hourly_report(self, db, include_open_positions: bool = True, current_positions: list = None) -> bool:
        """
        Envía reporte horario con trades ejecutados (abiertos y cerrados).
        
        Args:
            db: Instancia de TradingDatabase
            include_open_positions: Si incluir posiciones abiertas
            current_positions: Lista de posiciones actuales desde MT5 (opcional)
        """
        if not db:
            return False
        
        try:
            # Obtiene métricas del día (solo trades cerrados)
            today_metrics = db.get_performance_metrics(today_only=True)
            
            # Obtiene TODOS los trades del día (abiertos y cerrados)
            today_trades = db.get_today_trades()
            
            # Obtiene posiciones abiertas
            open_positions = []
            if include_open_positions:
                # Prioriza posiciones desde MT5 si se proporcionan
                if current_positions is not None and len(current_positions) > 0:
                    open_positions = []
                    for pos in current_positions:
                        open_positions.append({
                            "ticket": pos.get("ticket"),
                            "symbol": pos.get("symbol"),
                            "direction": pos.get("type"),
                            "entry_price": pos.get("entry_price"),
                            "current_price": pos.get("current_price"),
                            "stop_loss": pos.get("stop_loss"),
                            "take_profit": pos.get("take_profit"),
                            "unrealized_pnl": pos.get("profit", 0),
                            "volume": pos.get("volume")
                        })
                else:
                    try:
                        import MetaTrader5 as mt5
                        mt5_positions = mt5.positions_get()
                        if mt5_positions:
                            open_positions = []
                            for pos in mt5_positions:
                                open_positions.append({
                                    "ticket": pos.ticket,
                                    "symbol": pos.symbol,
                                    "direction": "BUY" if pos.type == mt5.ORDER_TYPE_BUY else "SELL",
                                    "entry_price": pos.price_open,
                                    "current_price": pos.price_current,
                                    "stop_loss": pos.sl,
                                    "take_profit": pos.tp,
                                    "unrealized_pnl": pos.profit,
                                    "volume": pos.volume
                                })
                    except Exception as e:
                        if logger:
                            logger.warning(f"No se pudieron obtener posiciones desde MT5: {e}")
                        open_positions = db.get_open_positions()
            
            # Separa trades abiertos y cerrados
            closed_trades_list = [t for t in today_trades if t.get("exit_time")]
            open_trades_list = [t for t in today_trades if not t.get("exit_time")]
            
            # Construye mensaje
            message = f"""
📊 <b>REPORTE HORARIO</b>

⏰ <b>Hora:</b> {datetime.now().strftime('%H:%M:%S')}
📅 <b>Fecha:</b> {datetime.now().strftime('%Y-%m-%d')}

━━━━━━━━━━━━━━━━━━━━
📈 <b>RESUMEN</b>
━━━━━━━━━━━━━━━━━━━━

📊 <b>Total Trades Hoy:</b> {len(today_trades)} (⏳ {len(open_trades_list)} abiertos | ✅ {len(closed_trades_list)} cerrados)
✅ <b>Trades Cerrados:</b> {today_metrics.get('total_trades', 0)}
💰 <b>P&L Total:</b> ${today_metrics.get('total_pnl', 0):.2f}
📊 <b>Win Rate:</b> {today_metrics.get('win_rate', 0):.1f}%
"""
            
            # Muestra trades cerrados (ejecutados y cerrados)
            if closed_trades_list:
                message += f"\n━━━━━━━━━━━━━━━━━━━━\n✅ <b>TRADES CERRADOS ({len(closed_trades_list)})</b>\n━━━━━━━━━━━━━━━━━━━━\n"
                for i, trade in enumerate(closed_trades_list[:10], 1):  # Máximo 10 trades
                    direction_emoji = "🟢" if trade.get("direction") == "BUY" else "🔴"
                    pnl_trade = trade.get("pnl", 0) or 0
                    pnl_trade_emoji = "✅" if pnl_trade > 0 else "❌" if pnl_trade < 0 else "➖"
                    
                    # Formatea fecha de entrada y salida
                    entry_time = trade.get("entry_time", "")
                    exit_time = trade.get("exit_time", "")
                    if entry_time:
                        try:
                            if isinstance(entry_time, str):
                                entry_dt = datetime.fromisoformat(entry_time.replace('Z', '+00:00'))
                            else:
                                entry_dt = entry_time
                            entry_str = entry_dt.strftime('%H:%M')
                        except:
                            entry_str = str(entry_time)[:5] if len(str(entry_time)) > 5 else str(entry_time)
                    else:
                        entry_str = "N/A"
                    
                    if exit_time:
                        try:
                            if isinstance(exit_time, str):
                                exit_dt = datetime.fromisoformat(exit_time.replace('Z', '+00:00'))
                            else:
                                exit_dt = exit_time
                            exit_str = exit_dt.strftime('%H:%M')
                        except:
                            exit_str = str(exit_time)[:5] if len(str(exit_time)) > 5 else str(exit_time)
                    else:
                        exit_str = "N/A"
                    
                    message += f"\n{i}. {direction_emoji} <b>{trade.get('direction', 'N/A')}</b> | Ticket: {trade.get('ticket', 'N/A')}\n"
                    message += f"   ⏰ {entry_str} → {exit_str} | {pnl_trade_emoji} P&L: ${pnl_trade:.2f}\n"
                    message += f"   📊 Entrada: ${trade.get('entry_price', 0):.2f} | Salida: ${trade.get('exit_price', 0):.2f} | RR: 1:{trade.get('risk_reward', 0):.2f}\n"
            
            # Muestra trades abiertos (ejecutados pero aún abiertos)
            if open_trades_list:
                message += f"\n━━━━━━━━━━━━━━━━━━━━\n⏳ <b>TRADES ABIERTOS ({len(open_trades_list)})</b>\n━━━━━━━━━━━━━━━━━━━━\n"
                for i, trade in enumerate(open_trades_list[:10], 1):  # Máximo 10 trades
                    direction_emoji = "🟢" if trade.get("direction") == "BUY" else "🔴"
                    
                    entry_time = trade.get("entry_time", "")
                    if entry_time:
                        try:
                            if isinstance(entry_time, str):
                                entry_dt = datetime.fromisoformat(entry_time.replace('Z', '+00:00'))
                            else:
                                entry_dt = entry_time
                            entry_str = entry_dt.strftime('%H:%M')
                        except:
                            entry_str = str(entry_time)[:5] if len(str(entry_time)) > 5 else str(entry_time)
                    else:
                        entry_str = "N/A"
                    
                    message += f"\n{i}. {direction_emoji} <b>{trade.get('direction', 'N/A')}</b> | Ticket: {trade.get('ticket', 'N/A')}\n"
                    message += f"   ⏰ Entrada: {entry_str} | 📊 Entrada: ${trade.get('entry_price', 0):.2f} | SL: ${trade.get('stop_loss', 0):.2f} | TP: ${trade.get('take_profit', 0):.2f}\n"
                    message += f"   📈 RR: 1:{trade.get('risk_reward', 0):.2f}\n"
            
            # Si no hay trades, muestra mensaje
            if not closed_trades_list and not open_trades_list:
                message += "\nℹ️ No hay trades ejecutados hoy aún\n"
            
            # Agrega posiciones abiertas (si hay)
            if open_positions:
                message += f"\n━━━━━━━━━━━━━━━━━━━━\n📦 <b>POSICIONES ABIERTAS ({len(open_positions)})</b>\n━━━━━━━━━━━━━━━━━━━━\n"
                for i, pos in enumerate(open_positions[:5], 1):  # Máximo 5 posiciones
                    direction_emoji = "🟢" if pos.get("direction") == "BUY" else "🔴"
                    unrealized_pnl = pos.get("unrealized_pnl", 0)
                    pnl_emoji = "💰" if unrealized_pnl > 0 else "📉" if unrealized_pnl < 0 else "➖"
                    
                    message += f"\n{i}. {direction_emoji} <b>{pos.get('direction', 'N/A')}</b> | Ticket: {pos.get('ticket', 'N/A')}\n"
                    message += f"   {pnl_emoji} P&L No Realizado: ${unrealized_pnl:.2f}\n"
                    message += f"   📊 Entrada: ${pos.get('entry_price', 0):.2f} | Actual: ${pos.get('current_price', 0):.2f} | SL: ${pos.get('stop_loss', 0):.2f} | TP: ${pos.get('take_profit', 0):.2f}\n"
            
            return self.send_message(message)
        except Exception as e:
            if logger:
                logger.error(f"Error al generar reporte horario: {e}", exc_info=True)
            return False
    
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
    
    def send_news_gate_blocked(self, reasons: list, mode: str, cooldown_until: str = None) -> bool:
        """
        Envía alerta cuando se bloquea una entrada por News Risk Gate.
        
        Args:
            reasons: Lista de razones del bloqueo
            mode: Modo actual (CONSERVATIVE, BLOCKED)
            cooldown_until: Fecha/hora hasta cuando está en cooldown (opcional)
        """
        emoji = "🚫" if mode == "BLOCKED" else "⚠️"
        
        message = f"""
{emoji} <b>ENTRADA BLOQUEADA - NEWS RISK GATE</b>

📋 <b>Modo:</b> {mode}
📊 <b>Razones:</b>
"""
        for i, reason in enumerate(reasons[:5], 1):  # Máximo 5 razones
            message += f"   {i}. {reason}\n"
        
        if cooldown_until:
            message += f"\n⏰ <b>Cooldown hasta:</b> {cooldown_until}"
        
        message += f"\n\n⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        return self.send_message(message)
    
    def send_market_conditions_alert(self, spread: float, spread_max: float, 
                                     atr_ratio: float, atr_max: float) -> bool:
        """
        Envía alerta cuando hay condiciones de mercado extremas.
        
        Args:
            spread: Spread actual
            spread_max: Spread máximo permitido
            atr_ratio: Ratio ATR actual
            atr_max: Ratio ATR máximo permitido
        """
        warnings = []
        if spread > spread_max * 0.8:  # 80% del máximo
            warnings.append(f"Spread alto: {spread:.2f} (máx: {spread_max:.2f})")
        if atr_ratio > atr_max * 0.8:  # 80% del máximo
            warnings.append(f"Volatilidad alta: ATR {atr_ratio:.2f} (máx: {atr_max:.2f})")
        
        if not warnings:
            return False
        
        message = f"""
⚠️ <b>CONDICIONES DE MERCADO EXTREMAS</b>

"""
        for warning in warnings:
            message += f"📊 {warning}\n"
        
        message += f"\n⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        return self.send_message(message)
    
    def send_drawdown_alert(self, drawdown_pct: float, limit: float) -> bool:
        """
        Envía alerta cuando el drawdown diario es significativo.
        
        Args:
            drawdown_pct: Drawdown porcentual actual (negativo)
            limit: Límite de drawdown permitido
        """
        if drawdown_pct >= limit * 0.7:  # Solo alertar si está cerca del límite (70%)
            return False
        
        severity = "🔴" if drawdown_pct <= limit else "🟡"
        
        message = f"""
{severity} <b>ALERTA DE DRAWDOWN</b>

📉 <b>Drawdown Diario:</b> {drawdown_pct:.2f}%
🛑 <b>Límite:</b> {limit:.2f}%

"""
        if drawdown_pct <= limit:
            message += "🚫 <b>TRADING BLOQUEADO</b> - Drawdown excedido\n"
        else:
            message += "⚠️ <b>Atención:</b> Drawdown cercano al límite\n"
        
        message += f"\n⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        return self.send_message(message)
    
    def send_losing_streak_alert(self, losing_streak: int, max_streak: int = 3) -> bool:
        """
        Envía alerta cuando hay una racha de pérdidas.
        
        Args:
            losing_streak: Número de pérdidas consecutivas
            max_streak: Número máximo antes de alertar
        """
        if losing_streak < max_streak:
            return False
        
        emoji = "🔴" if losing_streak >= max_streak + 2 else "🟡"
        
        message = f"""
{emoji} <b>RACHA DE PÉRDIDAS</b>

❌ <b>Pérdidas consecutivas:</b> {losing_streak}
⚠️ <b>Recomendación:</b> Revisar estrategia

⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        return self.send_message(message)
    
    def send_milestone_alert(self, milestone_type: str, value: float, target: float = None) -> bool:
        """
        Envía alerta cuando se alcanza un hito importante.
        
        Args:
            milestone_type: Tipo de hito (win_rate, profit_factor, total_trades, total_profit)
            value: Valor actual
            target: Valor objetivo (opcional)
        """
        emoji_map = {
            "win_rate": "🎯",
            "profit_factor": "💰",
            "total_trades": "📊",
            "total_profit": "💎"
        }
        
        title_map = {
            "win_rate": "Win Rate Objetivo",
            "profit_factor": "Profit Factor Objetivo",
            "total_trades": "Hito de Trades",
            "total_profit": "Hito de Profit"
        }
        
        emoji = emoji_map.get(milestone_type, "🎉")
        title = title_map.get(milestone_type, "Hito Alcanzado")
        
        message = f"""
{emoji} <b>{title}</b>

📊 <b>Valor actual:</b> {value:.2f}
"""
        if target:
            message += f"🎯 <b>Objetivo:</b> {target:.2f}\n"
        
        message += f"\n⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        return self.send_message(message)
    
    def send_upcoming_news_alert(self, event: Dict, minutes_until: int) -> bool:
        """
        Envía alerta de noticia importante próxima.
        
        Args:
            event: Diccionario con información del evento
            minutes_until: Minutos hasta el evento
        """
        impact = event.get('impact', 'MED')
        impact_emoji = "🔴" if impact == "HIGH" else "🟡" if impact == "MED" else "🟢"
        
        message = f"""
{impact_emoji} <b>NOTICIA IMPORTANTE PRÓXIMA</b>

📰 <b>Evento:</b> {event.get('title', 'N/A')}
📅 <b>Moneda:</b> {event.get('currency', 'N/A')}
⚠️ <b>Impacto:</b> {impact}
⏰ <b>En:</b> {minutes_until} minutos

🚫 <b>El bot bloqueará nuevas entradas</b>

⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        return self.send_message(message)
    
    def send_weekly_report(self, report: Dict) -> bool:
        """
        Envía reporte semanal de operaciones.
        
        Args:
            report: Diccionario con el reporte semanal
        """
        metrics = report.get("metrics", {})
        week_trades = report.get("week_trades", [])
        
        win_rate = metrics.get("win_rate", 0)
        win_rate_emoji = "🟢" if win_rate >= 50 else "🟡" if win_rate >= 40 else "🔴"
        
        profit_factor = metrics.get("profit_factor", 0)
        pf_emoji = "🟢" if profit_factor >= 1.5 else "🟡" if profit_factor >= 1.0 else "🔴"
        
        pnl = metrics.get("total_pnl", 0)
        pnl_emoji = "💰" if pnl > 0 else "📉" if pnl < 0 else "➖"
        
        message = f"""
📊 <b>REPORTE SEMANAL</b>

📅 <b>Semana:</b> {report.get('week_start', 'N/A')} - {report.get('week_end', 'N/A')}

━━━━━━━━━━━━━━━━━━━━
📈 <b>RESUMEN DE LA SEMANA</b>
━━━━━━━━━━━━━━━━━━━━

📊 <b>Total Trades:</b> {metrics.get('total_trades', 0)}
{win_rate_emoji} <b>Win Rate:</b> {win_rate:.1f}%
{pnl_emoji} <b>P&L Total:</b> ${pnl:.2f}
{pf_emoji} <b>Profit Factor:</b> {metrics.get('profit_factor', 0):.2f}
📊 <b>Avg Risk:Reward:</b> 1:{metrics.get('avg_risk_reward', 0):.2f}

✅ <b>Ganadores:</b> {metrics.get('winning_trades', 0)}
❌ <b>Perdedores:</b> {metrics.get('losing_trades', 0)}

⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        return self.send_message(message)
    
    def send_connection_lost_alert(self, component: str, error: str = None) -> bool:
        """
        Envía alerta cuando se pierde conexión con un componente crítico.
        
        Args:
            component: Componente que perdió conexión (MT5, Database, etc.)
            error: Mensaje de error (opcional)
        """
        message = f"""
🔴 <b>CONEXIÓN PERDIDA</b>

⚠️ <b>Componente:</b> {component}
"""
        if error:
            message += f"📋 <b>Error:</b> {error}\n"
        
        message += f"\n🔄 <b>El bot intentará reconectar...</b>"
        message += f"\n\n⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        return self.send_message(message)
    
    def send_high_risk_alert(self, open_positions: int, max_positions: int, 
                            total_exposure: float = None) -> bool:
        """
        Envía alerta cuando hay riesgo alto (muchas posiciones abiertas).
        
        Args:
            open_positions: Número de posiciones abiertas
            max_positions: Máximo de posiciones permitidas
            total_exposure: Exposición total (opcional)
        """
        if open_positions < max_positions * 0.8:  # Solo alertar si está cerca del máximo (80%)
            return False
        
        emoji = "🔴" if open_positions >= max_positions else "🟡"
        
        message = f"""
{emoji} <b>ALERTA DE RIESGO ALTO</b>

📊 <b>Posiciones abiertas:</b> {open_positions} / {max_positions}
"""
        if total_exposure:
            message += f"💰 <b>Exposición total:</b> ${total_exposure:.2f}\n"
        
        if open_positions >= max_positions:
            message += "\n🚫 <b>Máximo alcanzado - No se abrirán más posiciones</b>\n"
        else:
            message += "\n⚠️ <b>Atención:</b> Cerca del límite de posiciones\n"
        
        message += f"\n⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        return self.send_message(message)

