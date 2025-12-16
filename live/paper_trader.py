"""
live/paper_trader.py - Sistema de Paper Trading

Sistema de simulación de trading en tiempo real sin usar dinero real.
Útil para probar estrategias antes de operar con capital real.
"""

import pandas as pd
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from config import INITIAL_CAPITAL, COMMISSION, MAX_POSITION_SIZE


@dataclass
class PaperPosition:
    """Posición en paper trading"""
    symbol: str
    direction: str  # 'BUY' o 'SELL'
    entry_price: float
    entry_time: datetime
    size: float
    stop_loss: float
    take_profit_1: float
    take_profit_2: float
    take_profit_final: float
    current_price: float = 0.0
    unrealized_pnl: float = 0.0
    unrealized_pnl_pct: float = 0.0


@dataclass
class PaperTrade:
    """Operación completada en paper trading"""
    symbol: str
    direction: str
    entry_time: datetime
    exit_time: datetime
    entry_price: float
    exit_price: float
    size: float
    pnl: float
    pnl_pct: float
    exit_reason: str


class PaperTrader:
    """
    Sistema de Paper Trading para simular operaciones sin riesgo real.
    
    Características:
    - Simula órdenes de mercado y límite
    - Gestiona múltiples posiciones
    - Calcula P&L en tiempo real
    - Registra todas las operaciones
    """
    
    def __init__(self, initial_capital: float = None, commission: float = None):
        """
        Inicializa el sistema de paper trading.
        
        Args:
            initial_capital: Capital inicial simulado
            commission: Comisión por operación
        """
        from config import INITIAL_CAPITAL, COMMISSION
        
        self.initial_capital = initial_capital or INITIAL_CAPITAL
        self.commission = commission or COMMISSION
        self.capital = self.initial_capital
        self.positions: Dict[str, PaperPosition] = {}  # symbol -> position
        self.trades: List[PaperTrade] = []
        self.order_history: List[Dict] = []
    
    def get_balance(self) -> float:
        """Obtiene el balance actual (capital disponible)"""
        return self.capital
    
    def get_equity(self, current_prices: Dict[str, float]) -> float:
        """
        Calcula el equity total (capital + valor de posiciones abiertas).
        
        Args:
            current_prices: Diccionario con precios actuales {symbol: price}
        
        Returns:
            Equity total
        """
        equity = self.capital
        
        for symbol, position in self.positions.items():
            if symbol in current_prices:
                position_value = position.size * current_prices[symbol]
                equity += position_value
        
        return equity
    
    def open_position(self, symbol: str, direction: str, entry_price: float,
                     size: float, stop_loss: float, take_profit_1: float,
                     take_profit_2: float, take_profit_final: float) -> bool:
        """
        Abre una nueva posición en paper trading.
        
        Args:
            symbol: Símbolo del activo
            direction: 'BUY' o 'SELL'
            entry_price: Precio de entrada
            size: Tamaño de la posición
            stop_loss: Precio de stop loss
            take_profit_1: Primer take profit
            take_profit_2: Segundo take profit
            take_profit_final: Take profit final
        
        Returns:
            True si la posición se abrió exitosamente, False en caso contrario
        """
        # Verifica si ya hay una posición abierta
        if symbol in self.positions:
            print(f"⚠️ Ya existe una posición abierta para {symbol}")
            return False
        
        # Calcula el costo (incluyendo comisión)
        cost = size * entry_price * (1 + self.commission)
        
        # Verifica que haya suficiente capital
        if cost > self.capital:
            print(f"❌ Capital insuficiente. Necesitas ${cost:,.2f}, tienes ${self.capital:,.2f}")
            return False
        
        # Crea la posición
        position = PaperPosition(
            symbol=symbol,
            direction=direction,
            entry_price=entry_price,
            entry_time=datetime.now(),
            size=size,
            stop_loss=stop_loss,
            take_profit_1=take_profit_1,
            take_profit_2=take_profit_2,
            take_profit_final=take_profit_final,
            current_price=entry_price
        )
        
        # Actualiza capital
        self.capital -= cost
        
        # Guarda la posición
        self.positions[symbol] = position
        
        # Registra la orden
        self.order_history.append({
            'time': datetime.now(),
            'type': 'OPEN',
            'symbol': symbol,
            'direction': direction,
            'price': entry_price,
            'size': size,
            'cost': cost
        })
        
        print(f"✅ Posición {direction} abierta para {symbol}")
        print(f"   Entrada: ${entry_price:.2f}")
        print(f"   Tamaño: {size:.4f}")
        print(f"   Capital restante: ${self.capital:,.2f}")
        
        return True
    
    def update_positions(self, current_prices: Dict[str, float]) -> List[PaperTrade]:
        """
        Actualiza posiciones abiertas con precios actuales y cierra si se alcanzan SL/TP.
        
        Args:
            current_prices: Diccionario con precios actuales {symbol: price}
        
        Returns:
            Lista de trades cerrados en esta actualización
        """
        closed_trades = []
        
        for symbol, position in list(self.positions.items()):
            if symbol not in current_prices:
                continue
            
            current_price = current_prices[symbol]
            position.current_price = current_price
            
            # Calcula P&L no realizado
            if position.direction == 'BUY':
                position.unrealized_pnl = (current_price - position.entry_price) * position.size
                position.unrealized_pnl_pct = ((current_price - position.entry_price) / position.entry_price) * 100
            else:  # SELL
                position.unrealized_pnl = (position.entry_price - current_price) * position.size
                position.unrealized_pnl_pct = ((position.entry_price - current_price) / position.entry_price) * 100
            
            # Verifica si se debe cerrar la posición
            exit_price = None
            exit_reason = None
            
            if position.direction == 'BUY':
                # Stop Loss
                if current_price <= position.stop_loss:
                    exit_price = position.stop_loss
                    exit_reason = 'STOP_LOSS'
                # Take Profits
                elif current_price >= position.take_profit_final:
                    exit_price = position.take_profit_final
                    exit_reason = 'TAKE_PROFIT_FINAL'
                elif current_price >= position.take_profit_2:
                    exit_price = position.take_profit_2
                    exit_reason = 'TAKE_PROFIT_2'
                elif current_price >= position.take_profit_1:
                    exit_price = position.take_profit_1
                    exit_reason = 'TAKE_PROFIT_1'
            
            else:  # SELL
                # Stop Loss
                if current_price >= position.stop_loss:
                    exit_price = position.stop_loss
                    exit_reason = 'STOP_LOSS'
                # Take Profits
                elif current_price <= position.take_profit_final:
                    exit_price = position.take_profit_final
                    exit_reason = 'TAKE_PROFIT_FINAL'
                elif current_price <= position.take_profit_2:
                    exit_price = position.take_profit_2
                    exit_reason = 'TAKE_PROFIT_2'
                elif current_price <= position.take_profit_1:
                    exit_price = position.take_profit_1
                    exit_reason = 'TAKE_PROFIT_1'
            
            if exit_price:
                trade = self.close_position(symbol, exit_price, exit_reason)
                if trade:
                    closed_trades.append(trade)
        
        return closed_trades
    
    def close_position(self, symbol: str, exit_price: float, exit_reason: str = 'MANUAL') -> Optional[PaperTrade]:
        """
        Cierra una posición abierta.
        
        Args:
            symbol: Símbolo del activo
            exit_price: Precio de salida
            exit_reason: Razón del cierre
        
        Returns:
            PaperTrade con los detalles de la operación cerrada
        """
        if symbol not in self.positions:
            print(f"⚠️ No hay posición abierta para {symbol}")
            return None
        
        position = self.positions[symbol]
        
        # Calcula P&L
        proceeds = position.size * exit_price * (1 - self.commission)
        cost = position.size * position.entry_price * (1 + self.commission)
        pnl = proceeds - cost
        
        if position.direction == 'SELL':
            pnl = -pnl
        
        pnl_pct = ((exit_price - position.entry_price) / position.entry_price) * 100
        if position.direction == 'SELL':
            pnl_pct = -pnl_pct
        
        # Crea el trade
        trade = PaperTrade(
            symbol=symbol,
            direction=position.direction,
            entry_time=position.entry_time,
            exit_time=datetime.now(),
            entry_price=position.entry_price,
            exit_price=exit_price,
            size=position.size,
            pnl=pnl,
            pnl_pct=pnl_pct,
            exit_reason=exit_reason
        )
        
        # Actualiza capital
        self.capital += proceeds
        
        # Guarda el trade
        self.trades.append(trade)
        
        # Elimina la posición
        del self.positions[symbol]
        
        # Registra la orden
        self.order_history.append({
            'time': datetime.now(),
            'type': 'CLOSE',
            'symbol': symbol,
            'direction': position.direction,
            'price': exit_price,
            'size': position.size,
            'pnl': pnl,
            'exit_reason': exit_reason
        })
        
        print(f"📉 Posición {position.direction} cerrada para {symbol}")
        print(f"   Salida: ${exit_price:.2f}")
        print(f"   P&L: ${pnl:+.2f} ({pnl_pct:+.2f}%)")
        print(f"   Capital: ${self.capital:,.2f}")
        
        return trade
    
    def get_positions(self) -> Dict[str, PaperPosition]:
        """Obtiene todas las posiciones abiertas"""
        return self.positions.copy()
    
    def get_trades(self) -> List[PaperTrade]:
        """Obtiene el historial de trades"""
        return self.trades.copy()
    
    def get_statistics(self, current_prices: Dict[str, float]) -> Dict:
        """
        Obtiene estadísticas del paper trading.
        
        Args:
            current_prices: Precios actuales para calcular equity
        
        Returns:
            Diccionario con estadísticas
        """
        equity = self.get_equity(current_prices)
        total_return = ((equity - self.initial_capital) / self.initial_capital) * 100
        
        winning_trades = [t for t in self.trades if t.pnl > 0]
        losing_trades = [t for t in self.trades if t.pnl < 0]
        
        win_rate = (len(winning_trades) / len(self.trades) * 100) if self.trades else 0
        total_pnl = sum(t.pnl for t in self.trades)
        avg_win = sum(t.pnl for t in winning_trades) / len(winning_trades) if winning_trades else 0
        avg_loss = sum(t.pnl for t in losing_trades) / len(losing_trades) if losing_trades else 0
        
        return {
            'initial_capital': self.initial_capital,
            'current_capital': self.capital,
            'equity': equity,
            'total_return_pct': total_return,
            'total_trades': len(self.trades),
            'winning_trades': len(winning_trades),
            'losing_trades': len(losing_trades),
            'win_rate_pct': win_rate,
            'total_pnl': total_pnl,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'open_positions': len(self.positions)
        }













