"""
utils/database.py - Base de Datos SQLite para Trading

Guarda todas las señales, operaciones y métricas del sistema.
Permite análisis histórico y mejora continua.
"""

import sqlite3
import os
from datetime import datetime, date
from typing import Dict, List, Optional
from pathlib import Path
import json


class TradingDatabase:
    """
    Base de datos SQLite para almacenar:
    - Señales generadas (aceptadas y rechazadas)
    - Operaciones ejecutadas
    - Posiciones abiertas
    - Métricas de performance
    """
    
    def __init__(self, db_path: str = "data/trading_bot.db"):
        """
        Inicializa la base de datos.
        
        Args:
            db_path: Ruta al archivo de base de datos
        """
        # Crear directorio si no existe
        db_dir = Path(db_path).parent
        db_dir.mkdir(parents=True, exist_ok=True)
        
        self.db_path = db_path
        self.conn = None
        self._init_database()
    
    def _init_database(self):
        """Crea las tablas si no existen"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row  # Permite acceso por nombre de columna
        
        cursor = self.conn.cursor()
        
        # Tabla de señales (todas las señales generadas)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS signals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME NOT NULL,
                symbol TEXT NOT NULL,
                direction TEXT NOT NULL,
                entry_price REAL NOT NULL,
                stop_loss REAL NOT NULL,
                take_profit_1 REAL NOT NULL,
                take_profit_2 REAL,
                take_profit_final REAL,
                risk_reward REAL NOT NULL,
                confirmations INTEGER NOT NULL,
                confirmations_list TEXT,
                justifications TEXT,
                status TEXT NOT NULL,
                rejection_reason TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabla de operaciones (trades ejecutados)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                signal_id INTEGER,
                ticket INTEGER UNIQUE NOT NULL,
                symbol TEXT NOT NULL,
                direction TEXT NOT NULL,
                entry_time DATETIME NOT NULL,
                entry_price REAL NOT NULL,
                exit_time DATETIME,
                exit_price REAL,
                lot_size REAL NOT NULL,
                stop_loss REAL NOT NULL,
                take_profit REAL NOT NULL,
                pnl REAL,
                pnl_pct REAL,
                swap REAL DEFAULT 0,
                exit_reason TEXT,
                risk_reward REAL,
                comment TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (signal_id) REFERENCES signals(id)
            )
        """)
        
        # Tabla de posiciones (posiciones abiertas actuales)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS positions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                trade_id INTEGER,
                ticket INTEGER UNIQUE NOT NULL,
                symbol TEXT NOT NULL,
                direction TEXT NOT NULL,
                entry_time DATETIME NOT NULL,
                entry_price REAL NOT NULL,
                lot_size REAL NOT NULL,
                stop_loss REAL NOT NULL,
                take_profit REAL NOT NULL,
                current_price REAL,
                unrealized_pnl REAL,
                swap REAL DEFAULT 0,
                sl_moved_to_be BOOLEAN DEFAULT 0,
                partial_close_1 BOOLEAN DEFAULT 0,
                partial_close_2 BOOLEAN DEFAULT 0,
                last_update DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (trade_id) REFERENCES trades(id)
            )
        """)
        
        # Tabla de métricas diarias
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS daily_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE UNIQUE NOT NULL,
                total_signals INTEGER DEFAULT 0,
                accepted_signals INTEGER DEFAULT 0,
                rejected_signals INTEGER DEFAULT 0,
                trades_opened INTEGER DEFAULT 0,
                trades_closed INTEGER DEFAULT 0,
                total_pnl REAL DEFAULT 0,
                win_rate REAL,
                profit_factor REAL,
                max_drawdown REAL,
                avg_risk_reward REAL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabla de estado del bot (para tracking de news gate y otros estados)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bot_state (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp_utc DATETIME NOT NULL,
                symbol TEXT NOT NULL,
                news_mode TEXT DEFAULT 'NORMAL',
                blocked INTEGER DEFAULT 0,
                reasons TEXT,
                cooldown_until_utc DATETIME,
                spread REAL,
                atr_ratio REAL,
                daily_dd_pct REAL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabla de pivots diarios (Fibonacci)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS daily_pivots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE NOT NULL,
                symbol TEXT NOT NULL,
                pivot REAL NOT NULL,
                r1 REAL NOT NULL,
                r2 REAL NOT NULL,
                r3 REAL NOT NULL,
                s1 REAL NOT NULL,
                s2 REAL NOT NULL,
                s3 REAL NOT NULL,
                high REAL NOT NULL,
                low REAL NOT NULL,
                close REAL NOT NULL,
                calculated_at DATETIME NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(date, symbol)
            )
        """)
        
        self.conn.commit()
    
    def save_signal(self, signal: Dict, status: str = "GENERATED", rejection_reason: str = None) -> int:
        """
        Guarda una señal en la base de datos.
        
        Args:
            signal: Diccionario con información de la señal
            status: "GENERATED", "ACCEPTED", "REJECTED"
            rejection_reason: Razón si fue rechazada
        
        Returns:
            ID de la señal guardada
        """
        cursor = self.conn.cursor()
        
        cursor.execute("""
            INSERT INTO signals (
                timestamp, symbol, direction, entry_price, stop_loss,
                take_profit_1, take_profit_2, take_profit_final,
                risk_reward, confirmations, confirmations_list,
                justifications, status, rejection_reason
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.now(),
            signal.get("symbol", "XAUUSD"),
            signal.get("signal", "HOLD"),
            signal.get("entry_price", 0.0),
            signal.get("stop_loss", 0.0),
            signal.get("take_profit_1", 0.0),
            signal.get("take_profit_2", 0.0),
            signal.get("take_profit_final", 0.0),
            signal.get("risk_reward", 0.0),
            len(signal.get("justifications", [])),
            json.dumps(signal.get("justifications", [])),
            ", ".join(signal.get("justifications", [])),
            status,
            rejection_reason
        ))
        
        self.conn.commit()
        return cursor.lastrowid
    
    def save_trade(self, ticket: int, signal: Dict, lot_size: float, 
                   entry_price: float, stop_loss: float, take_profit: float,
                   signal_id: Optional[int] = None) -> int:
        """
        Guarda una operación ejecutada.
        
        Args:
            ticket: Ticket de la orden en MT5
            signal: Diccionario con información de la señal
            lot_size: Tamaño de la posición
            entry_price: Precio de entrada
            stop_loss: Stop loss
            take_profit: Take profit
            signal_id: ID de la señal relacionada
        
        Returns:
            ID del trade guardado
        """
        cursor = self.conn.cursor()
        
        cursor.execute("""
            INSERT INTO trades (
                signal_id, ticket, symbol, direction, entry_time,
                entry_price, lot_size, stop_loss, take_profit,
                risk_reward, comment
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            signal_id,
            ticket,
            signal.get("symbol", "XAUUSD"),
            signal.get("signal", "BUY"),
            datetime.now(),
            entry_price,
            lot_size,
            stop_loss,
            take_profit,
            signal.get("risk_reward", 0.0),
            f"ICT Strategy - RR:{signal.get('risk_reward', 0.0):.2f}"
        ))
        
        self.conn.commit()
        trade_id = cursor.lastrowid
        
        # También guarda en positions
        self.save_position(trade_id, ticket, signal, lot_size, entry_price, stop_loss, take_profit)
        
        return trade_id
    
    def save_position(self, trade_id: int, ticket: int, signal: Dict,
                     lot_size: float, entry_price: float, stop_loss: float, take_profit: float):
        """Guarda o actualiza una posición abierta"""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO positions (
                trade_id, ticket, symbol, direction, entry_time,
                entry_price, lot_size, stop_loss, take_profit
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            trade_id,
            ticket,
            signal.get("symbol", "XAUUSD"),
            signal.get("signal", "BUY"),
            datetime.now(),
            entry_price,
            lot_size,
            stop_loss,
            take_profit
        ))
        
        self.conn.commit()
    
    def update_position(self, ticket: int, current_price: float, unrealized_pnl: float,
                       sl_moved_to_be: bool = False, partial_close_1: bool = False,
                       partial_close_2: bool = False):
        """Actualiza información de una posición abierta"""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            UPDATE positions SET
                current_price = ?,
                unrealized_pnl = ?,
                sl_moved_to_be = ?,
                partial_close_1 = ?,
                partial_close_2 = ?,
                last_update = ?
            WHERE ticket = ?
        """, (current_price, unrealized_pnl, sl_moved_to_be, partial_close_1, partial_close_2, datetime.now(), ticket))
        
        self.conn.commit()
    
    def close_trade(self, ticket: int, exit_price: float, exit_reason: str, pnl: float, pnl_pct: float):
        """Marca un trade como cerrado"""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            UPDATE trades SET
                exit_time = ?,
                exit_price = ?,
                exit_reason = ?,
                pnl = ?,
                pnl_pct = ?
            WHERE ticket = ?
        """, (datetime.now(), exit_price, exit_reason, pnl, pnl_pct, ticket))
        
        # Elimina de positions
        cursor.execute("DELETE FROM positions WHERE ticket = ?", (ticket,))
        
        self.conn.commit()
    
    def get_open_positions(self) -> List[Dict]:
        """Obtiene todas las posiciones abiertas"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM positions")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    def get_trade_history(self, limit: int = 100) -> List[Dict]:
        """Obtiene historial de trades"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM trades 
            ORDER BY entry_time DESC 
            LIMIT ?
        """, (limit,))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    def get_today_trades(self) -> List[Dict]:
        """Obtiene todos los trades del día actual"""
        cursor = self.conn.cursor()
        today = datetime.now().date()
        today_str = today.strftime('%Y-%m-%d')
        
        # SQLite puede almacenar fechas como strings, así que usamos LIKE para mayor compatibilidad
        cursor.execute("""
            SELECT * FROM trades 
            WHERE entry_time LIKE ? OR DATE(entry_time) = ?
            ORDER BY entry_time DESC
        """, (f'{today_str}%', today))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    def get_today_closed_trades(self) -> List[Dict]:
        """Obtiene todos los trades cerrados del día actual"""
        cursor = self.conn.cursor()
        today = datetime.now().date()
        cursor.execute("""
            SELECT * FROM trades 
            WHERE DATE(exit_time) = ? AND exit_time IS NOT NULL
            ORDER BY exit_time DESC
        """, (today,))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    def get_performance_metrics(self, today_only: bool = False) -> Dict:
        """Calcula métricas de performance"""
        cursor = self.conn.cursor()
        
        # Construye la consulta base
        base_query = """
            SELECT 
                COUNT(*) as total_trades,
                SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) as winning_trades,
                SUM(CASE WHEN pnl < 0 THEN 1 ELSE 0 END) as losing_trades,
                SUM(pnl) as total_pnl,
                AVG(pnl) as avg_pnl,
                AVG(risk_reward) as avg_rr
            FROM trades
            WHERE exit_time IS NOT NULL
        """
        
        if today_only:
            today = datetime.now().date()
            query = base_query + " AND DATE(exit_time) = ?"
            cursor.execute(query, (today,))
        else:
            cursor.execute(base_query)
        
        result = cursor.fetchone()
        
        if result and result['total_trades'] > 0:
            win_rate = (result['winning_trades'] / result['total_trades']) * 100
            
            # Profit factor
            pf_query = """
                SELECT 
                    SUM(CASE WHEN pnl > 0 THEN pnl ELSE 0 END) as total_profit,
                    ABS(SUM(CASE WHEN pnl < 0 THEN pnl ELSE 0 END)) as total_loss
                FROM trades
                WHERE exit_time IS NOT NULL
            """
            if today_only:
                today = datetime.now().date()
                pf_query += " AND DATE(exit_time) = ?"
                cursor.execute(pf_query, (today,))
            else:
                cursor.execute(pf_query)
            
            pf_result = cursor.fetchone()
            profit_factor = (pf_result['total_profit'] / pf_result['total_loss']) if pf_result['total_loss'] > 0 else 0
            
            return {
                "total_trades": result['total_trades'],
                "winning_trades": result['winning_trades'],
                "losing_trades": result['losing_trades'],
                "win_rate": win_rate,
                "total_pnl": result['total_pnl'] or 0,
                "avg_pnl": result['avg_pnl'] or 0,
                "profit_factor": profit_factor,
                "avg_risk_reward": result['avg_rr'] or 0
            }
        
        return {
            "total_trades": 0,
            "winning_trades": 0,
            "losing_trades": 0,
            "win_rate": 0,
            "total_pnl": 0,
            "avg_pnl": 0,
            "profit_factor": 0,
            "avg_risk_reward": 0
        }
    
    def save_bot_state(self, symbol: str, news_mode: str, blocked: bool, 
                      reasons: List[str], cooldown_until_utc: Optional[datetime] = None,
                      spread: float = None, atr_ratio: float = None, 
                      daily_dd_pct: float = None):
        """
        Guarda el estado actual del bot en la base de datos.
        
        Args:
            symbol: Símbolo operado
            news_mode: Modo de noticias (NORMAL, CONSERVATIVE, BLOCKED)
            blocked: Si está bloqueado para nuevas entradas
            reasons: Lista de razones del bloqueo
            cooldown_until_utc: Fecha UTC hasta cuando está en cooldown
            spread: Spread actual
            atr_ratio: Ratio ATR actual/promedio
            daily_dd_pct: Drawdown diario porcentual
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO bot_state (
                timestamp_utc, symbol, news_mode, blocked, reasons,
                cooldown_until_utc, spread, atr_ratio, daily_dd_pct
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.utcnow(),
            symbol,
            news_mode,
            1 if blocked else 0,
            json.dumps(reasons) if reasons else None,
            cooldown_until_utc,
            spread,
            atr_ratio,
            daily_dd_pct
        ))
        self.conn.commit()
    
    def get_daily_drawdown_pct(self, target_date: Optional[date] = None) -> float:
        """
        Calcula el drawdown diario porcentual basado en P&L del día.
        
        Args:
            date: Fecha para calcular (default: hoy)
        
        Returns:
            Drawdown porcentual (ej: -2.5 significa 2.5% de pérdida)
            Nota: Retorna negativo para pérdidas, positivo para ganancias
        """
        from datetime import date as date_type
        if target_date is None:
            target_date = datetime.now().date()
        
        cursor = self.conn.cursor()
        
        # Obtiene P&L total del día
        cursor.execute("""
            SELECT 
                COALESCE(SUM(pnl), 0) as total_pnl,
                COUNT(*) as total_trades
            FROM trades
            WHERE DATE(exit_time) = ? AND exit_time IS NOT NULL
        """, (date,))
        
        result = cursor.fetchone()
        
        if result and result['total_trades'] > 0:
            total_pnl = result['total_pnl'] or 0
            
            # Obtiene el balance inicial del día (del primer trade)
            cursor.execute("""
                SELECT entry_price, lot_size, direction
                FROM trades
                WHERE DATE(entry_time) = ?
                ORDER BY entry_time ASC
                LIMIT 1
            """, (target_date,))
            
            first_trade = cursor.fetchone()
            
            if first_trade:
                # Aproximación: calcula drawdown como % del P&L total
                # En producción, debería calcularse respecto al balance inicial del día
                # Por ahora, usamos una aproximación basada en el valor de la posición
                entry_price = first_trade['entry_price'] or 0
                lot_size = first_trade['lot_size'] or 0
                
                if entry_price > 0 and lot_size > 0:
                    # Valor aproximado de la posición inicial
                    position_value = entry_price * lot_size * 100  # Para XAUUSD, 1 lote = 100 onzas
                    
                    if position_value > 0:
                        # Drawdown como porcentaje del valor de posición
                        dd_pct = (total_pnl / position_value) * 100
                        return dd_pct
        
        return 0.0
    
    def close(self):
        """Cierra la conexión a la base de datos"""
        if self.conn:
            self.conn.close()

