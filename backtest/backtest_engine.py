"""
backtest/backtest_engine.py - Motor de backtesting

Este módulo simula el trading con datos históricos para probar tu estrategia
sin arriesgar dinero real. Es como "viajar en el tiempo" y ver cómo habría
funcionado tu estrategia en el pasado.
"""

import pandas as pd
from config import INITIAL_CAPITAL, COMMISSION, STOP_LOSS_PCT, TAKE_PROFIT_PCT, MAX_POSITION_SIZE


class BacktestEngine:
    """
    Motor de backtesting que simula operaciones con datos históricos.
    """
    
    def __init__(self, initial_capital=None, commission=None):
        """
        Inicializa el motor de backtesting.
        
        Args:
            initial_capital: Capital inicial para el backtest
            commission: Comisión por operación (ej: 0.001 = 0.1%)
        """
        self.initial_capital = initial_capital or INITIAL_CAPITAL
        self.commission = commission or COMMISSION
        self.capital = self.initial_capital  # Capital disponible
        self.position = None  # Posición actual (None = sin posición)
        self.trades = []  # Lista de todas las operaciones realizadas
        self.equity_curve = []  # Evolución del capital a lo largo del tiempo
    
    def run(self, data, strategy):
        """
        Ejecuta el backtest de la estrategia con los datos proporcionados.
        
        Args:
            data: DataFrame con datos OHLCV y señales de la estrategia
            strategy: Instancia de la estrategia a probar
        
        Returns:
            Diccionario con resultados del backtest
        """
        print(f"Iniciando backtest con capital inicial: ${self.initial_capital:,.2f}")
        
        # Genera las señales de la estrategia
        data = strategy.generate_signals(data)
        
        # Itera sobre cada vela (momento en el tiempo)
        for i in range(len(data)):
            current_bar = data.iloc[i]
            
            # Si no hay posición abierta, busca señales de compra
            if self.position is None:
                if strategy.should_buy(data, i):
                    self._open_position(data, i, strategy)
            
            # Si hay posición abierta, busca señales de venta
            else:
                if strategy.should_sell(data, i, self.position):
                    self._close_position(data, i)
            
            # Registra el capital actual (equity curve)
            current_equity = self._calculate_equity(current_bar['close'])
            self.equity_curve.append({
                'timestamp': current_bar.name,
                'equity': current_equity
            })
        
        # Cierra cualquier posición abierta al final
        if self.position is not None:
            self._close_position(data, len(data) - 1)
        
        # Calcula métricas de rendimiento
        results = self._calculate_metrics()
        
        return results
    
    def _open_position(self, data, index, strategy):
        """
        Abre una nueva posición (compra).
        
        Args:
            data: DataFrame con datos
            index: Índice actual
            strategy: Estrategia utilizada
        """
        current_price = data.iloc[index]['close']
        
        # Calcula el tamaño de la posición según el capital disponible
        position_size = self.capital * MAX_POSITION_SIZE
        shares = position_size / current_price
        
        # Aplica comisión
        cost = shares * current_price * (1 + self.commission)
        
        if cost <= self.capital:
            self.position = {
                'entry_price': current_price,
                'shares': shares,
                'entry_time': data.index[index],
                'stop_loss': STOP_LOSS_PCT,
                'take_profit': TAKE_PROFIT_PCT
            }
            self.capital -= cost
            
            print(f"COMPRA en {data.index[index]}: {shares:.4f} acciones a ${current_price:.2f}")
    
    def _close_position(self, data, index):
        """
        Cierra la posición actual (venta).
        
        Args:
            data: DataFrame con datos
            index: Índice actual
        """
        if self.position is None:
            return
        
        current_price = data.iloc[index]['close']
        shares = self.position['shares']
        
        # Calcula el valor de la venta (descontando comisión)
        proceeds = shares * current_price * (1 - self.commission)
        self.capital += proceeds
        
        # Calcula la ganancia/pérdida
        entry_price = self.position['entry_price']
        pnl = proceeds - (shares * entry_price * (1 + self.commission))
        pnl_pct = (current_price - entry_price) / entry_price * 100
        
        # Registra la operación
        trade = {
            'entry_time': self.position['entry_time'],
            'exit_time': data.index[index],
            'entry_price': entry_price,
            'exit_price': current_price,
            'shares': shares,
            'pnl': pnl,
            'pnl_pct': pnl_pct
        }
        self.trades.append(trade)
        
        print(f"VENTA en {data.index[index]}: {shares:.4f} acciones a ${current_price:.2f} | P&L: ${pnl:.2f} ({pnl_pct:.2f}%)")
        
        self.position = None
    
    def _calculate_equity(self, current_price):
        """
        Calcula el capital total (efectivo + valor de posición abierta).
        
        Args:
            current_price: Precio actual del activo
        
        Returns:
            Capital total (equity)
        """
        if self.position is None:
            return self.capital
        
        # Capital = efectivo + valor actual de las acciones
        position_value = self.position['shares'] * current_price
        return self.capital + position_value
    
    def _calculate_metrics(self):
        """
        Calcula métricas de rendimiento del backtest.
        
        Returns:
            Diccionario con métricas calculadas
        """
        if not self.trades:
            return {"error": "No se realizaron operaciones"}
        
        # Convierte trades a DataFrame para facilitar cálculos
        trades_df = pd.DataFrame(self.trades)
        
        # Métricas básicas
        total_trades = len(self.trades)
        winning_trades = len(trades_df[trades_df['pnl'] > 0])
        losing_trades = len(trades_df[trades_df['pnl'] < 0])
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        
        # P&L total
        total_pnl = trades_df['pnl'].sum()
        total_return = (self.capital - self.initial_capital) / self.initial_capital * 100
        
        # P&L promedio
        avg_win = trades_df[trades_df['pnl'] > 0]['pnl'].mean() if winning_trades > 0 else 0
        avg_loss = trades_df[trades_df['pnl'] < 0]['pnl'].mean() if losing_trades > 0 else 0
        
        # Profit factor (ganancias totales / pérdidas totales)
        total_wins = trades_df[trades_df['pnl'] > 0]['pnl'].sum()
        total_losses = abs(trades_df[trades_df['pnl'] < 0]['pnl'].sum())
        profit_factor = total_wins / total_losses if total_losses > 0 else 0
        
        results = {
            'initial_capital': self.initial_capital,
            'final_capital': self.capital,
            'total_return_pct': total_return,
            'total_pnl': total_pnl,
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'win_rate_pct': win_rate,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'profit_factor': profit_factor,
            'trades': self.trades,
            'equity_curve': self.equity_curve
        }
        
        return results













