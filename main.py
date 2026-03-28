"""
Main entry point for CRO Analysis Tool
Run automated CRO analysis on your data
"""

import sys
import json
import pandas as pd
from pathlib import Path

# Add src to path
src_path = str(Path(__file__).parent / 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from src.analyzer import CROAnalyzer
from src.reports import ReportGenerator
from src.reports_v2 import AdvancedReportGenerator
from src.supabase_manager import SupabaseExamplesManager


def load_config(config_file: str) -> dict:
    """Load configuration from JSON file"""
    with open(config_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_data(data_file: str) -> pd.DataFrame:
    """Load event data from CSV"""
    return pd.read_csv(data_file)


def main():
    """Main execution function"""
    
    print("🚀 CRO Analysis Tool - Iniciando análise...\n")
    
    # Load configuration
    config_file = 'examples/sample_config.json'
    try:
        config = load_config(config_file)
        print(f"✅ Configuração carregada de {config_file}")
    except FileNotFoundError:
        print(f"❌ Arquivo de configuração não encontrado: {config_file}")
        return
    
    # Load data
    data_file = 'examples/sample_data.csv'
    try:
        data = load_data(data_file)
        print(f"✅ Dados carregados: {len(data)} eventos de {data['user_id'].nunique()} usuários\n")
    except FileNotFoundError:
        print(f"❌ Arquivo de dados não encontrado: {data_file}")
        return
    
    # Run analysis
    print("📊 Executando análise de funil de conversão...\n")
    
    analyzer = CROAnalyzer()
    funnel_steps = config.get('funnel_steps', [])
    
    try:
        results = analyzer.analyze(
            events_data=data,
            funnel_steps=funnel_steps
        )
        print("✅ Análise concluída!\n")
    except Exception as e:
        print(f"❌ Erro durante análise: {e}")
        return
    
    # Display results
    print("=" * 60)
    print("📈 RESULTADOS DA ANÁLISE")
    print("=" * 60)
    
    summary = results.get('summary', {})
    print(f"\n📊 Resumo dos dados:")
    print(f"   • Total de eventos: {summary.get('total_events', 0)}")
    print(f"   • Usuários únicos: {summary.get('unique_users', 0)}")
    print(f"   • Taxa de conversão geral: {results.get('total_conversion_rate', 0):.2f}%")
    
    # Display funnel
    print(f"\n🎯 Funil de conversão:")
    funnel_metrics = results.get('funnel_metrics', {})
    
    for step in funnel_steps:
        users = funnel_metrics.get('step_users', {}).get(step, 0)
        conversion = funnel_metrics.get('conversion_rates', {}).get(step, 0)
        print(f"   • {step}: {users} usuários ({conversion:.1f}%)")
    
    # Display abandonment points
    abandonment = results.get('abandonment_points', [])
    if abandonment:
        print(f"\n⚠️  Principais pontos de abandono ({len(abandonment)}):")
        for point in abandonment[:3]:
            print(f"   • {point['step']}: {point['drop_off_rate']:.1f}% [{point['severity'].upper()}]")
    
    # Display recommendations
    recommendations = results.get('recommendations', [])
    if recommendations:
        print(f"\n💡 Principais recomendações ({len(recommendations)}):")
        for rec in recommendations[:3]:
            print(f"   • {rec['title']} ({rec['priority'].upper()})")
            print(f"     Impacto esperado: {rec['expected_impact']}")
    
    # Generate reports
    print("\n" + "=" * 60)
    print("📄 Gerando relatórios...")
    
    # Standard report
    report_generator = ReportGenerator()
    output_file = 'relatorio_cro_analysis.html'
    
    try:
        report_generator.generate_html_report(results, output_file)
        print(f"✅ Relatório simples gerado: {output_file}")
    except Exception as e:
        print(f"⚠️  Erro ao gerar relatório: {e}")
    
    # Advanced report with examples
    advanced_generator = AdvancedReportGenerator()
    advanced_output = 'relatorio_cro_advanced.html'
    
    try:
        advanced_generator.generate_html_report(
            results,
            advanced_output,
            client_name="Seu E-commerce",
            competitor_examples=None
        )
        print(f"✅ Relatório avançado gerado: {advanced_output}")
    except Exception as e:
        print(f"⚠️  Erro ao gerar relatório avançado: {e}")
    
    # Export results
    print("📁 Exportando resultados em JSON...")
    output_json = 'cro_analysis_results.json'
    
    try:
        analyzer.export_results(output_json)
        print(f"✅ Resultados exportados: {output_json}")
    except Exception as e:
        print(f"⚠️  Erro ao exportar resultados: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Análise concluída com sucesso!")
    print("=" * 60)


if __name__ == '__main__':
    main()
