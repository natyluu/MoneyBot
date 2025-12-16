"""
live/position_manager.py - Gestión Avanzada de Posiciones

Gestiona posiciones abiertas con:
- Mover SL a break-even automáticamente
- Cierres parciales (TP1, TP2, TP Final)
- Trailing stop
- Gestión de múltiples posiciones
"""

import MetaTrader5 as mt5
from typing import Dict, List, Optional
from datetime import datetime
from utils.logger import logger


class PositionManager:
    """
    Gestiona posiciones abiertas de forma profesional:
    - Mueve SL a break-even cuando se alcanza TP1
    - Realiza cierres parciales
    - Aplica trailing stop
    """
    
    def __init__(self, db=None):
        """
        Inicializa el gestor de posiciones.
        
        Args:
            db: Instancia de TradingDatabase (opcional)
        """
        self.db = db
        self.managed_positions = {}  # ticket -> información de gestión
    
    def check_and_manage_positions(self, symbol: str = None) -> List[Dict]:
        """
        Verifica y gestiona todas las posiciones abiertas.
        
        Args:
            symbol: Símbolo a verificar (None = todos)
        
        Returns:
            Lista de acciones realizadas
        """
        actions = []
        
        # Obtiene posiciones abiertas
        positions = mt5.positions_get(symbol=symbol)
        if positions is None:
            return actions
        
        for pos in positions:
            ticket = pos.ticket
            current_price = pos.price_current
            entry_price = pos.price_open
            stop_loss = pos.sl
            take_profit = pos.tp
            profit = pos.profit
            volume = pos.volume
            
            # Obtiene información de gestión de esta posición
            if ticket not in self.managed_positions:
                self.managed_positions[ticket] = {
                    "entry_price": entry_price,
                    "initial_sl": stop_loss,
                    "initial_tp": take_profit,
                    "tp1": take_profit,  # Por ahora, TP1 es el único TP
                    "sl_moved_to_be": False,
                    "partial_close_1": False,
                    "partial_close_2": False
                }
            
            mgmt_info = self.managed_positions[ticket]
            direction = "BUY" if pos.type == mt5.ORDER_TYPE_BUY else "SELL"
            
            # Calcula distancia a TP1
            if direction == "BUY":
                distance_to_tp1 = (current_price - entry_price) / (mgmt_info["tp1"] - entry_price) if (mgmt_info["tp1"] - entry_price) > 0 else 0
            else:
                distance_to_tp1 = (entry_price - current_price) / (entry_price - mgmt_info["tp1"]) if (entry_price - mgmt_info["tp1"]) > 0 else 0
            
            # 1. Mover SL a break-even cuando se alcanza TP1
            if not mgmt_info["sl_moved_to_be"] and distance_to_tp1 >= 0.8:  # 80% del camino a TP1
                if self._move_sl_to_break_even(ticket, entry_price, symbol or pos.symbol):
                    mgmt_info["sl_moved_to_be"] = True
                    actions.append({
                        "action": "SL_MOVED_TO_BE",
                        "ticket": ticket,
                        "new_sl": entry_price
                    })
                    logger.info(f"✅ SL movido a break-even para ticket {ticket}")
            
            # 2. Cierre parcial en TP1 (50% de la posición)
            if not mgmt_info["partial_close_1"] and distance_to_tp1 >= 1.0:
                if self._partial_close(ticket, volume * 0.5, symbol or pos.symbol):
                    mgmt_info["partial_close_1"] = True
                    actions.append({
                        "action": "PARTIAL_CLOSE_TP1",
                        "ticket": ticket,
                        "volume_closed": volume * 0.5
                    })
                    logger.info(f"✅ Cierre parcial (50%) en TP1 para ticket {ticket}")
            
            # Actualiza en base de datos si existe
            if self.db:
                self.db.update_position(
                    ticket=ticket,
                    current_price=current_price,
                    unrealized_pnl=profit,
                    sl_moved_to_be=mgmt_info["sl_moved_to_be"],
                    partial_close_1=mgmt_info["partial_close_1"],
                    partial_close_2=mgmt_info["partial_close_2"]
                )
        
        return actions
    
    def _move_sl_to_break_even(self, ticket: int, break_even_price: float, symbol: str) -> bool:
        """
        Mueve el Stop Loss a break-even (precio de entrada).
        
        Args:
            ticket: Ticket de la posición
            break_even_price: Precio de entrada (break-even)
            symbol: Símbolo de la posición
        
        Returns:
            True si se movió exitosamente
        """
        # Obtiene la posición actual
        position = mt5.positions_get(ticket=ticket)
        if position is None or len(position) == 0:
            return False
        
        pos = position[0]
        current_tp = pos.tp
        
        # Prepara solicitud para modificar SL
        request = {
            "action": mt5.TRADE_ACTION_SLTP,
            "symbol": symbol,
            "position": ticket,
            "sl": break_even_price,
            "tp": current_tp
        }
        
        # Envía la modificación
        result = mt5.order_send(request)
        
        if result is None:
            logger.error(f"❌ Error al mover SL a BE para ticket {ticket}: {mt5.last_error()}")
            return False
        
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            logger.warning(f"⚠️ No se pudo mover SL a BE: {result.retcode} - {result.comment}")
            return False
        
        return True
    
    def _partial_close(self, ticket: int, volume_to_close: float, symbol: str) -> bool:
        """
        Cierra parcialmente una posición.
        
        Args:
            ticket: Ticket de la posición
            volume_to_close: Volumen a cerrar
            symbol: Símbolo de la posición
        
        Returns:
            True si se cerró exitosamente
        """
        # Obtiene la posición actual
        position = mt5.positions_get(ticket=ticket)
        if position is None or len(position) == 0:
            return False
        
        pos = position[0]
        
        # Verifica que el volumen a cerrar sea menor que el volumen total
        if volume_to_close >= pos.volume:
            logger.warning(f"⚠️ Volumen a cerrar ({volume_to_close}) >= volumen total ({pos.volume})")
            return False
        
        # Obtiene precio actual
        tick = mt5.symbol_info_tick(symbol)
        if tick is None:
            return False
        
        # Determina precio según dirección
        if pos.type == mt5.ORDER_TYPE_BUY:
            price = tick.bid  # Para cerrar compra, vendes al precio bid
            order_type = mt5.ORDER_TYPE_SELL
        else:
            price = tick.ask  # Para cerrar venta, compras al precio ask
            order_type = mt5.ORDER_TYPE_BUY
        
        # Prepara solicitud de cierre parcial
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume_to_close,
            "type": order_type,
            "position": ticket,  # Cierra parcialmente esta posición
            "price": price,
            "deviation": 20,
            "magic": 234000,
            "comment": "Partial Close TP1",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC
        }
        
        # Envía la orden
        result = mt5.order_send(request)
        
        if result is None:
            logger.error(f"❌ Error en cierre parcial: {mt5.last_error()}")
            return False
        
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            logger.warning(f"⚠️ Cierre parcial rechazado: {result.retcode} - {result.comment}")
            return False
        
        return True
    
    def check_closed_positions(self, db, open_tickets: List[int]) -> List[Dict]:
        """
        Detecta posiciones que se cerraron y actualiza la base de datos.
        
        Args:
            db: Instancia de TradingDatabase
            open_tickets: Lista de tickets que deberían estar abiertos
        
        Returns:
            Lista de diccionarios con información de trades cerrados
        """
        closed_trades = []
        if not db:
            return closed_trades
        
        # Obtiene posiciones que estaban en la base de datos pero ya no están abiertas
        db_positions = db.get_open_positions()
        
        for db_pos in db_positions:
            ticket = db_pos["ticket"]
            if ticket not in open_tickets:
                # La posición se cerró
                # Obtiene información del trade cerrado desde MT5
                deals = mt5.history_deals_get(ticket=ticket)
                if deals and len(deals) > 0:
                    # Calcula P&L del trade
                    total_profit = sum(d.profit for d in deals)
                    total_swap = sum(d.swap for d in deals)
                    pnl = total_profit + total_swap
                    
                    # Obtiene precio de salida
                    exit_deal = deals[-1]
                    exit_price = exit_deal.price
                    
                    # Determina razón de salida
                    exit_reason = "MANUAL"
                    if db_pos.get("sl_moved_to_be"):
                        exit_reason = "SL_BREAK_EVEN"
                    
                    # Calcula P&L porcentual
                    entry_price = db_pos["entry_price"]
                    pnl_pct = ((exit_price - entry_price) / entry_price) * 100
                    if db_pos["direction"] == "SELL":
                        pnl_pct = -pnl_pct
                    
                    # Actualiza en base de datos
                    db.close_trade(ticket, exit_price, exit_reason, pnl, pnl_pct)
                    
                    # Elimina de managed_positions
                    if ticket in self.managed_positions:
                        del self.managed_positions[ticket]
                    
                    logger.info(f"📊 Trade cerrado: Ticket {ticket} | P&L: ${pnl:.2f} ({pnl_pct:.2f}%)")
                    
                    # Guarda información para notificar
                    closed_trades.append({
                        'ticket': ticket,
                        'pnl': pnl,
                        'pnl_pct': pnl_pct,
                        'exit_reason': exit_reason
                    })
        
        return closed_trades

