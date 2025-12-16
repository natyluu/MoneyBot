"""
live/trade_analyzer.py - Análisis Post-Trade

Analiza trades cerrados para identificar patrones y mejorar el sistema.
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
from utils.logger import logger
from utils.database import TradingDatabase


class TradeAnalyzer:
    """
    Analiza trades cerrados para:
    - Identificar qué funciona y qué no
    - Calcular métricas de performance
    - Generar insights para mejorar
    """
    
    def __init__(self, db: TradingDatabase):
        """
        Inicializa el analizador.
        
        Args:
            db: Instancia de TradingDatabase
        """
        self.db = db
    
    def analyze_closed_trade(self, ticket: int) -> Dict:
        """
        Analiza un trade cerrado específico.
        
        Args:
            ticket: Ticket del trade
        
        Returns:
            Diccionario con análisis del trade
        """
        # Obtiene el trade de la base de datos
        trades = self.db.get_trade_history(limit=1000)
        trade = next((t for t in trades if t["ticket"] == ticket), None)
        
        if not trade or not trade.get("exit_time"):
            return {"error": "Trade no encontrado o aún abierto"}
        
        analysis = {
            "ticket": ticket,
            "symbol": trade["symbol"],
            "direction": trade["direction"],
            "entry_time": trade["entry_time"],
            "exit_time": trade["exit_time"],
            "duration": self._calculate_duration(trade["entry_time"], trade["exit_time"]),
            "entry_price": trade["entry_price"],
            "exit_price": trade["exit_price"],
            "pnl": trade["pnl"],
            "pnl_pct": trade["pnl_pct"],
            "exit_reason": trade["exit_reason"],
            "risk_reward": trade["risk_reward"],
            "result": "WIN" if trade["pnl"] > 0 else "LOSS",
            "insights": []
        }
        
        # Genera insights
        if trade["pnl"] > 0:
            analysis["insights"].append("✅ Trade ganador")
            if trade["risk_reward"] >= 2.0:
                analysis["insights"].append("✅ Excelente Risk:Reward")
        else:
            analysis["insights"].append("❌ Trade perdedor")
            if trade["exit_reason"] == "STOP_LOSS":
                analysis["insights"].append("⚠️ Se activó el Stop Loss")
        
        # Analiza duración
        if analysis["duration"] < timedelta(hours=1):
            analysis["insights"].append("⚡ Trade de corta duración")
        elif analysis["duration"] > timedelta(days=1):
            analysis["insights"].append("⏳ Trade de larga duración")
        
        logger.info(f"📊 Análisis de trade {ticket}: {analysis['result']} | P&L: ${analysis['pnl']:.2f}")
        
        return analysis
    
    def generate_daily_report(self) -> Dict:
        """
        Genera reporte diario de performance.
        
        Returns:
            Diccionario con métricas del día
        """
        metrics = self.db.get_performance_metrics()
        
        report = {
            "date": datetime.now().date(),
            "metrics": metrics,
            "summary": self._generate_summary(metrics)
        }
        
        logger.info(f"📈 Reporte diario: {report['summary']}")
        
        return report
    
    def _calculate_duration(self, entry_time: str, exit_time: str) -> timedelta:
        """Calcula duración de un trade"""
        try:
            entry = datetime.fromisoformat(entry_time.replace("Z", "+00:00"))
            exit = datetime.fromisoformat(exit_time.replace("Z", "+00:00"))
            return exit - entry
        except:
            # Fallback para diferentes formatos
            return timedelta(0)
    
    def _generate_summary(self, metrics: Dict) -> str:
        """Genera resumen de métricas"""
        if metrics["total_trades"] == 0:
            return "Sin trades cerrados aún"
        
        return (
            f"Trades: {metrics['total_trades']} | "
            f"Win Rate: {metrics['win_rate']:.1f}% | "
            f"P&L Total: ${metrics['total_pnl']:.2f} | "
            f"Profit Factor: {metrics['profit_factor']:.2f}"
        )

