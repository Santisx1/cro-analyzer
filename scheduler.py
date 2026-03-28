"""
Automated CRO Analysis Scheduler
Runs analysis automatically on schedule - set it and forget it!
"""

import schedule
import time
import os
import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from analyzer import CROAnalyzer
from reports_v2 import AdvancedReportGenerator
import pandas as pd


class CROScheduler:
    """Automated CRO Analysis Scheduler"""
    
    def __init__(self, data_source: str = 'examples/sample_data.csv'):
        """
        Initialize scheduler
        
        Args:
            data_source: Path to data CSV file
        """
        self.data_source = data_source
        self.analyzer = CROAnalyzer()
        self.report_gen = AdvancedReportGenerator()
        self.reports_dir = 'reports_automated'
        
        # Create reports directory if needed
        os.makedirs(self.reports_dir, exist_ok=True)
    
    def run_analysis(self):
        """Run complete CRO analysis automatically"""
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        print("\n" + "="*70)
        print(f"🤖 Análise Automática CRO — {timestamp}")
        print("="*70)
        
        try:
            # Load data
            print("📍 1. Carregando dados...")
            data = pd.read_csv(self.data_source)
            print(f"   ✅ {len(data)} eventos carregados")
            
            # Run analysis
            print("📍 2. Executando análise...")
            results = self.analyzer.analyze(
                events_data=data,
                funnel_steps=['page_view', 'view_item', 'add_to_cart', 'begin_checkout', 'purchase']
            )
            print(f"   ✅ Análise concluída")
            
            # Generate reports
            print("📍 3. Gerando relatórios...")
            
            # Advanced report
            report_name = f'{self.reports_dir}/relatorio_{timestamp}.html'
            self.report_gen.generate_html_report(
                results,
                report_name,
                client_name="CRO Intelligence — Análise Automática"
            )
            print(f"   ✅ Relatório gerado: {report_name}")
            
            # Export JSON
            json_name = f'{self.reports_dir}/analise_{timestamp}.json'
            self.analyzer.export_results(json_name)
            print(f"   ✅ Dados JSON exportados: {json_name}")
            
            # Summary
            print("\n📊 RESUMO:")
            print(f"   • Taxa de conversão: {results.get('total_conversion_rate', 0):.2f}%")
            print(f"   • Usuários: {results['summary']['unique_users']}")
            print(f"   • Pontos críticos: {len([a for a in results['abandonment_points'] if a['severity'] == 'high'])}")
            print(f"   • Recomendações: {len(results['recommendations'])}")
            
            print("\n✅ Análise concluída com sucesso!")
            print("="*70 + "\n")
            
            return True
            
        except Exception as e:
            print(f"\n❌ ERRO durante análise: {e}")
            print("="*70 + "\n")
            return False
    
    def schedule_daily(self, hour: int = 2, minute: int = 0):
        """
        Schedule analysis to run daily at specific time
        
        Args:
            hour: Hour (0-23), default 2 AM
            minute: Minute (0-59), default 0
        """
        time_str = f"{hour:02d}:{minute:02d}"
        schedule.every().day.at(time_str).do(self.run_analysis)
        print(f"📅 Análise agendada: Diariamente às {time_str}")
    
    def schedule_hourly(self):
        """Schedule analysis to run every hour"""
        schedule.every().hour.do(self.run_analysis)
        print("📅 Análise agendada: A cada hora")
    
    def schedule_weekly(self, day: str = 'monday', time_str: str = '02:00'):
        """
        Schedule analysis weekly
        
        Args:
            day: Day of week (monday-sunday)
            time_str: Time in HH:MM format
        """
        getattr(schedule.every(), day).at(time_str).do(self.run_analysis)
        print(f"📅 Análise agendada: Toda {day} às {time_str}")
    
    def start_daemon(self, check_interval: int = 60):
        """
        Start scheduler daemon (runs forever)
        
        Args:
            check_interval: How often to check schedule (seconds)
        """
        print("\n🚀 INICIANDO SCHEDULER EM BACKGROUND")
        print(f"⏰ Verificando schedule a cada {check_interval}s")
        print("🌙 Você pode fechar o terminal/ssh — análises continuarão rodando\n")
        
        while True:
            schedule.run_pending()
            time.sleep(check_interval)


def main():
    """Main entry point"""
    
    scheduler = CROScheduler(data_source='examples/sample_data.csv')
    
    # Escolher schedule
    print("\n📅 ESCOLHA O AGENDAMENTO:")
    print("1. Diário às 2 AM (recomendado)")
    print("2. A cada hora")
    print("3. Semanalmente às segundas 2 AM")
    print("4. Rodar uma vez agora")
    
    choice = input("\nOpção (1-4): ").strip()
    
    if choice == '1':
        scheduler.schedule_daily(hour=2, minute=0)
        scheduler.start_daemon()
    elif choice == '2':
        scheduler.schedule_hourly()
        scheduler.start_daemon()
    elif choice == '3':
        scheduler.schedule_weekly(day='monday', time_str='02:00')
        scheduler.start_daemon()
    elif choice == '4':
        scheduler.run_analysis()
    else:
        print("❌ Opção inválida")


if __name__ == '__main__':
    # Evitar rodar em modo daemon se importado
    if len(sys.argv) > 1:
        scheduler = CROScheduler()
        
        if sys.argv[1] == '--run':
            scheduler.run_analysis()
        elif sys.argv[1] == '--daily':
            hour = int(sys.argv[2]) if len(sys.argv) > 2 else 2
            scheduler.schedule_daily(hour=hour)
            scheduler.start_daemon()
        elif sys.argv[1] == '--hourly':
            scheduler.schedule_hourly()
            scheduler.start_daemon()
        else:
            print("Usage: python3 scheduler.py [--run|--daily [hour]|--hourly]")
    else:
        main()
