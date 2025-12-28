"""
Script de análisis completo de señales y trades para mejorar la estrategia
"""

from utils.database import TradingDatabase
from datetime import datetime
from collections import Counter, defaultdict
import json
import sys

def format_datetime(dt_str):
    """Formatea una fecha/hora para mostrar"""
    if not dt_str:
        return "N/A"
    try:
        if isinstance(dt_str, str):
            dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
        else:
            dt = dt_str
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except:
        return str(dt_str)

def get_all_signals(db):
    """Obtiene todas las señales de la base de datos"""
    cursor = db.conn.cursor()
    cursor.execute("""
        SELECT * FROM signals 
        ORDER BY timestamp DESC
    """)
    rows = cursor.fetchall()
    return [dict(row) for row in rows]

def get_all_trades(db):
    """Obtiene todos los trades de la base de datos"""
    return db.get_trade_history(limit=10000)

def analyze_signals(signals):
    """Analiza las señales generadas"""
    if not signals:
        return None
    
    analysis = {
        'total': len(signals),
        'accepted': 0,
        'rejected': 0,
        'generated': 0,
        'by_status': Counter(),
        'by_direction': Counter(),
        'by_confirmations': defaultdict(list),
        'rejection_reasons': Counter(),
        'avg_risk_reward': {'accepted': [], 'rejected': []},
        'confirmations_breakdown': Counter()
    }
    
    for signal in signals:
        status = signal.get('status', 'GENERATED')
        analysis['by_status'][status] += 1
        
        if status == 'ACCEPTED':
            analysis['accepted'] += 1
        elif status == 'REJECTED':
            analysis['rejected'] += 1
        else:
            analysis['generated'] += 1
        
        direction = signal.get('direction', 'UNKNOWN')
        analysis['by_direction'][direction] += 1
        
        confirmations = signal.get('confirmations', 0)
        analysis['by_confirmations'][confirmations].append(signal)
        
        rr = signal.get('risk_reward', 0)
        if rr:
            if status == 'ACCEPTED':
                analysis['avg_risk_reward']['accepted'].append(rr)
            elif status == 'REJECTED':
                analysis['avg_risk_reward']['rejected'].append(rr)
        
        # Analiza confirmaciones individuales
        justifications = signal.get('justifications', '')
        if justifications:
            just_list = justifications.split(', ')
            for j in just_list:
                if 'Sweep' in j or 'Barrida' in j:
                    analysis['confirmations_breakdown']['SWEEP'] += 1
                if 'Mitigación' in j:
                    analysis['confirmations_breakdown']['MITIGATION'] += 1
                if 'BOS' in j or 'CHoCH' in j:
                    analysis['confirmations_breakdown']['BOS_CHOCH'] += 1
                if 'institucional' in j.lower() or 'Vela' in j:
                    analysis['confirmations_breakdown']['INSTITUTIONAL_CANDLE'] += 1
                if 'RSI' in j or 'Divergencia' in j:
                    analysis['confirmations_breakdown']['RSI_DIVERGENCE'] += 1
        
        rejection_reason = signal.get('rejection_reason')
        if rejection_reason:
            analysis['rejection_reasons'][rejection_reason] += 1
    
    return analysis

def analyze_trades(trades):
    """Analiza los trades ejecutados"""
    if not trades:
        return None
    
    closed_trades = [t for t in trades if t.get('exit_time')]
    open_trades = [t for t in trades if not t.get('exit_time')]
    
    analysis = {
        'total': len(trades),
        'closed': len(closed_trades),
        'open': len(open_trades),
        'winning': [],
        'losing': [],
        'by_direction': {'BUY': [], 'SELL': []},
        'by_exit_reason': Counter(),
        'risk_reward_analysis': {'winning': [], 'losing': []},
        'pnl_stats': {
            'total': 0,
            'avg_win': 0,
            'avg_loss': 0,
            'largest_win': 0,
            'largest_loss': 0
        }
    }
    
    for trade in closed_trades:
        pnl = trade.get('pnl', 0)
        direction = trade.get('direction', 'UNKNOWN')
        exit_reason = trade.get('exit_reason', 'UNKNOWN')
        rr = trade.get('risk_reward', 0)
        
        analysis['by_exit_reason'][exit_reason] += 1
        
        if direction in ['BUY', 'SELL']:
            analysis['by_direction'][direction].append(trade)
        
        if pnl > 0:
            analysis['winning'].append(trade)
            analysis['risk_reward_analysis']['winning'].append(rr)
        elif pnl < 0:
            analysis['losing'].append(trade)
            analysis['risk_reward_analysis']['losing'].append(rr)
        
        analysis['pnl_stats']['total'] += pnl
    
    if analysis['winning']:
        wins = [t.get('pnl', 0) for t in analysis['winning']]
        analysis['pnl_stats']['avg_win'] = sum(wins) / len(wins)
        analysis['pnl_stats']['largest_win'] = max(wins)
    
    if analysis['losing']:
        losses = [t.get('pnl', 0) for t in analysis['losing']]
        analysis['pnl_stats']['avg_loss'] = sum(losses) / len(losses)
        analysis['pnl_stats']['largest_loss'] = min(losses)
    
    return analysis

def correlate_signals_trades(signals, trades):
    """Correlaciona señales con trades para análisis de performance"""
    correlation = {
        'signals_with_trades': 0,
        'signals_without_trades': 0,
        'accepted_signals_performance': {'winning': 0, 'losing': 0},
        'by_confirmations_performance': defaultdict(lambda: {'winning': 0, 'losing': 0})
    }
    
    # Crea un mapa de signal_id a trade
    signal_to_trade = {}
    for trade in trades:
        signal_id = trade.get('signal_id')
        if signal_id:
            signal_to_trade[signal_id] = trade
    
    for signal in signals:
        signal_id = signal.get('id')
        if signal_id in signal_to_trade:
            correlation['signals_with_trades'] += 1
            trade = signal_to_trade[signal_id]
            
            if signal.get('status') == 'ACCEPTED':
                pnl = trade.get('pnl')
                if pnl:
                    if pnl > 0:
                        correlation['accepted_signals_performance']['winning'] += 1
                    else:
                        correlation['accepted_signals_performance']['losing'] += 1
                
                # Análisis por número de confirmaciones
                confirmations = signal.get('confirmations', 0)
                if pnl:
                    if pnl > 0:
                        correlation['by_confirmations_performance'][confirmations]['winning'] += 1
                    else:
                        correlation['by_confirmations_performance'][confirmations]['losing'] += 1
        else:
            if signal.get('status') == 'ACCEPTED':
                correlation['signals_without_trades'] += 1
    
    return correlation

def generate_improvement_suggestions(signal_analysis, trade_analysis, correlation):
    """Genera sugerencias de mejora basadas en el análisis"""
    suggestions = []
    
    # Análisis de confirmaciones
    if signal_analysis:
        total_signals = signal_analysis['total']
        accepted = signal_analysis['accepted']
        rejected = signal_analysis['rejected']
        
        acceptance_rate = (accepted / total_signals * 100) if total_signals > 0 else 0
        rejection_rate = (rejected / total_signals * 100) if total_signals > 0 else 0
        
        if rejection_rate > 70:
            suggestions.append({
                'tipo': 'ALTA TASA DE RECHAZO',
                'problema': f'El {rejection_rate:.1f}% de las señales son rechazadas',
                'sugerencia': 'Revisar los filtros de entrada. Puede que sean demasiado estrictos o que falten confirmaciones importantes.',
                'prioridad': 'ALTA'
            })
        
        # Análisis por número de confirmaciones
        confirmations_dist = signal_analysis['by_confirmations']
        if confirmations_dist:
            most_common = max(confirmations_dist.keys(), key=lambda k: len(confirmations_dist[k]))
            if most_common < 3:
                suggestions.append({
                    'tipo': 'CONFIRMACIONES INSUFICIENTES',
                    'problema': f'La mayoría de señales tienen solo {most_common} confirmaciones',
                    'sugerencia': 'Aumentar el número mínimo de confirmaciones requeridas o mejorar la detección de patrones.',
                    'prioridad': 'MEDIA'
                })
    
    # Análisis de performance de trades
    if trade_analysis and trade_analysis['closed'] > 0:
        winning = len(trade_analysis['winning'])
        losing = len(trade_analysis['losing'])
        win_rate = (winning / trade_analysis['closed'] * 100) if trade_analysis['closed'] > 0 else 0
        
        if win_rate < 40:
            suggestions.append({
                'tipo': 'WIN RATE BAJO',
                'problema': f'Win rate de solo {win_rate:.1f}%',
                'sugerencia': 'Mejorar filtros de entrada, ajustar stop loss/take profit, o revisar la lógica de confirmaciones.',
                'prioridad': 'ALTA'
            })
        
        # Análisis de Risk:Reward
        avg_rr_winning = 0
        avg_rr_losing = 0
        if trade_analysis['risk_reward_analysis']['winning']:
            avg_rr_winning = sum(trade_analysis['risk_reward_analysis']['winning']) / len(trade_analysis['risk_reward_analysis']['winning'])
        if trade_analysis['risk_reward_analysis']['losing']:
            avg_rr_losing = sum(trade_analysis['risk_reward_analysis']['losing']) / len(trade_analysis['risk_reward_analysis']['losing'])
        
        if avg_rr_winning < 1.5:
            suggestions.append({
                'tipo': 'RISK:REWARD BAJO',
                'problema': f'Risk:Reward promedio en ganadoras: {avg_rr_winning:.2f}',
                'sugerencia': 'Aumentar los take profit targets o mejorar la selección de puntos de entrada.',
                'prioridad': 'MEDIA'
            })
        
        # Análisis de pérdidas grandes
        largest_loss = abs(trade_analysis['pnl_stats']['largest_loss'])
        avg_loss = abs(trade_analysis['pnl_stats']['avg_loss'])
        if largest_loss > avg_loss * 2 and avg_loss > 0:
            suggestions.append({
                'tipo': 'PÉRDIDAS EXTREMAS',
                'problema': f'Pérdida más grande (${largest_loss:.2f}) es {largest_loss/avg_loss:.1f}x el promedio',
                'sugerencia': 'Revisar gestión de riesgo, considerar trailing stops o cierres parciales más agresivos.',
                'prioridad': 'ALTA'
            })
        
        # Análisis por dirección
        buy_trades = [t for t in trade_analysis['by_direction']['BUY'] if t.get('exit_time')]
        sell_trades = [t for t in trade_analysis['by_direction']['SELL'] if t.get('exit_time')]
        
        if buy_trades and sell_trades:
            buy_wins = len([t for t in buy_trades if t.get('pnl', 0) > 0])
            sell_wins = len([t for t in sell_trades if t.get('pnl', 0) > 0])
            buy_wr = (buy_wins / len(buy_trades) * 100) if buy_trades else 0
            sell_wr = (sell_wins / len(sell_trades) * 100) if sell_trades else 0
            
            if abs(buy_wr - sell_wr) > 20:
                better = 'COMPRAS' if buy_wr > sell_wr else 'VENTAS'
                suggestions.append({
                    'tipo': 'ASIMETRÍA DIRECCIONAL',
                    'problema': f'Win rate en compras: {buy_wr:.1f}%, en ventas: {sell_wr:.1f}%',
                    'sugerencia': f'Considerar enfocarse más en {better} o revisar la lógica de detección para la dirección con menor performance.',
                    'prioridad': 'MEDIA'
                })
    
    # Análisis de correlación
    if correlation:
        signals_with_trades = correlation['signals_with_trades']
        signals_without = correlation['signals_without_trades']
        if signals_without > signals_with_trades * 0.3:
            suggestions.append({
                'tipo': 'SEÑALES NO EJECUTADAS',
                'problema': f'{signals_without} señales aceptadas no se ejecutaron',
                'sugerencia': 'Revisar filtros de ejecución (news gate, límites de posición, etc.) o condiciones de mercado.',
                'prioridad': 'MEDIA'
            })
    
    return suggestions

def print_analysis_report(signal_analysis, trade_analysis, correlation, suggestions):
    """Imprime el reporte completo de análisis"""
    print("\n" + "="*80)
    print("📊 ANÁLISIS COMPLETO DE ENTRADAS Y ESTRATEGIA")
    print("="*80)
    
    # 1. RESUMEN DE SEÑALES
    print("\n" + "="*80)
    print("1️⃣  ANÁLISIS DE SEÑALES GENERADAS")
    print("="*80)
    
    if signal_analysis:
        print(f"\n📈 Total de señales: {signal_analysis['total']}")
        print(f"   ✅ Aceptadas: {signal_analysis['accepted']} ({signal_analysis['accepted']/signal_analysis['total']*100:.1f}%)")
        print(f"   ❌ Rechazadas: {signal_analysis['rejected']} ({signal_analysis['rejected']/signal_analysis['total']*100:.1f}%)")
        print(f"   ⏳ Generadas: {signal_analysis['generated']} ({signal_analysis['generated']/signal_analysis['total']*100:.1f}%)")
        
        print(f"\n📊 Por dirección:")
        for direction, count in signal_analysis['by_direction'].items():
            print(f"   {direction}: {count}")
        
        print(f"\n📊 Por número de confirmaciones:")
        for conf_count in sorted(signal_analysis['by_confirmations'].keys()):
            signals_count = len(signal_analysis['by_confirmations'][conf_count])
            print(f"   {conf_count} confirmaciones: {signals_count} señales")
        
        if signal_analysis['rejection_reasons']:
            print(f"\n❌ Razones de rechazo más comunes:")
            for reason, count in signal_analysis['rejection_reasons'].most_common(5):
                print(f"   • {reason}: {count} veces")
        
        if signal_analysis['confirmations_breakdown']:
            print(f"\n✅ Confirmaciones detectadas:")
            for conf_type, count in signal_analysis['confirmations_breakdown'].most_common():
                print(f"   • {conf_type}: {count} veces")
        
        if signal_analysis['avg_risk_reward']['accepted']:
            avg_rr_accepted = sum(signal_analysis['avg_risk_reward']['accepted']) / len(signal_analysis['avg_risk_reward']['accepted'])
            print(f"\n💰 Risk:Reward promedio (señales aceptadas): {avg_rr_accepted:.2f}")
    else:
        print("\n⚠️  No se encontraron señales en la base de datos")
    
    # 2. RESUMEN DE TRADES
    print("\n" + "="*80)
    print("2️⃣  ANÁLISIS DE TRADES EJECUTADOS")
    print("="*80)
    
    if trade_analysis:
        print(f"\n📈 Total de trades: {trade_analysis['total']}")
        print(f"   ✅ Cerrados: {trade_analysis['closed']}")
        print(f"   ⏳ Abiertos: {trade_analysis['open']}")
        
        if trade_analysis['closed'] > 0:
            winning = len(trade_analysis['winning'])
            losing = len(trade_analysis['losing'])
            win_rate = (winning / trade_analysis['closed'] * 100)
            
            print(f"\n📊 Performance:")
            print(f"   🟢 Ganadores: {winning} ({win_rate:.1f}%)")
            print(f"   🔴 Perdedores: {losing} ({100-win_rate:.1f}%)")
            
            stats = trade_analysis['pnl_stats']
            print(f"\n💰 P&L:")
            print(f"   Total: ${stats['total']:.2f}")
            if stats['avg_win']:
                print(f"   Ganancia promedio: ${stats['avg_win']:.2f}")
            if stats['avg_loss']:
                print(f"   Pérdida promedio: ${stats['avg_loss']:.2f}")
            if stats['largest_win']:
                print(f"   Mayor ganancia: ${stats['largest_win']:.2f}")
            if stats['largest_loss']:
                print(f"   Mayor pérdida: ${stats['largest_loss']:.2f}")
            
            if trade_analysis['by_exit_reason']:
                print(f"\n📊 Razones de cierre:")
                for reason, count in trade_analysis['by_exit_reason'].most_common():
                    print(f"   • {reason}: {count} veces")
            
            # Análisis por dirección
            buy_closed = [t for t in trade_analysis['by_direction']['BUY'] if t.get('exit_time')]
            sell_closed = [t for t in trade_analysis['by_direction']['SELL'] if t.get('exit_time')]
            
            if buy_closed:
                buy_wins = len([t for t in buy_closed if t.get('pnl', 0) > 0])
                buy_wr = (buy_wins / len(buy_closed) * 100)
                print(f"\n📊 Por dirección:")
                print(f"   BUY: {len(buy_closed)} trades, Win Rate: {buy_wr:.1f}%")
            
            if sell_closed:
                sell_wins = len([t for t in sell_closed if t.get('pnl', 0) > 0])
                sell_wr = (sell_wins / len(sell_closed) * 100)
                print(f"   SELL: {len(sell_closed)} trades, Win Rate: {sell_wr:.1f}%")
    else:
        print("\n⚠️  No se encontraron trades en la base de datos")
    
    # 3. CORRELACIÓN
    if correlation:
        print("\n" + "="*80)
        print("3️⃣  CORRELACIÓN SEÑALES-TRADES")
        print("="*80)
        print(f"\n   Señales con trades ejecutados: {correlation['signals_with_trades']}")
        print(f"   Señales aceptadas sin ejecutar: {correlation['signals_without_trades']}")
        
        if correlation['accepted_signals_performance']['winning'] + correlation['accepted_signals_performance']['losing'] > 0:
            total = correlation['accepted_signals_performance']['winning'] + correlation['accepted_signals_performance']['losing']
            wr = (correlation['accepted_signals_performance']['winning'] / total * 100)
            print(f"\n   Win Rate de señales aceptadas: {wr:.1f}%")
    
    # 4. SUGERENCIAS DE MEJORA
    print("\n" + "="*80)
    print("4️⃣  SUGERENCIAS DE MEJORA")
    print("="*80)
    
    if suggestions:
        for i, suggestion in enumerate(suggestions, 1):
            priority_icon = "🔴" if suggestion['prioridad'] == 'ALTA' else "🟡" if suggestion['prioridad'] == 'MEDIA' else "🟢"
            print(f"\n{priority_icon} {i}. {suggestion['tipo']} ({suggestion['prioridad']})")
            print(f"   Problema: {suggestion['problema']}")
            print(f"   Sugerencia: {suggestion['sugerencia']}")
    else:
        print("\n✅ No se identificaron problemas críticos. La estrategia parece estar funcionando bien.")
    
    print("\n" + "="*80)
    print("FIN DEL ANÁLISIS")
    print("="*80 + "\n")

def main():
    """Función principal"""
    print("\n🔍 Iniciando análisis completo...")
    
    try:
        db = TradingDatabase()
    except Exception as e:
        print(f"❌ Error al conectar con la base de datos: {e}")
        sys.exit(1)
    
    try:
        # Obtiene todos los datos
        print("📥 Obteniendo señales...")
        signals = get_all_signals(db)
        
        print("📥 Obteniendo trades...")
        trades = get_all_trades(db)
        
        if not signals and not trades:
            print("\n⚠️  La base de datos está vacía. El bot aún no ha generado señales ni ejecutado trades.")
            db.close()
            return
        
        # Analiza los datos
        print("🔬 Analizando datos...")
        signal_analysis = analyze_signals(signals) if signals else None
        trade_analysis = analyze_trades(trades) if trades else None
        correlation = correlate_signals_trades(signals, trades) if signals and trades else None
        
        # Genera sugerencias
        print("💡 Generando sugerencias...")
        suggestions = generate_improvement_suggestions(signal_analysis, trade_analysis, correlation)
        
        # Imprime el reporte
        print_analysis_report(signal_analysis, trade_analysis, correlation, suggestions)
        
    except Exception as e:
        print(f"❌ Error durante el análisis: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    main()

