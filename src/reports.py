"""
Report generation module
Creates HTML and PDF reports from analysis results
"""

import json
from typing import Dict, List
from datetime import datetime
from jinja2 import Template


class ReportGenerator:
    """Generate visual reports from CRO analysis"""
    
    HTML_TEMPLATE = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Relatório de Análise CRO</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: #f5f5f5;
                color: #333;
            }
            
            .container {
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                padding: 40px;
            }
            
            header {
                border-bottom: 3px solid #0066cc;
                margin-bottom: 40px;
                padding-bottom: 20px;
            }
            
            h1 {
                color: #0066cc;
                font-size: 2.5em;
                margin-bottom: 10px;
            }
            
            .timestamp {
                color: #999;
                font-size: 0.9em;
            }
            
            .summary {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 20px;
                margin: 40px 0;
            }
            
            .metric-card {
                background: #f9f9f9;
                padding: 20px;
                border-radius: 8px;
                border-left: 4px solid #0066cc;
            }
            
            .metric-label {
                font-size: 0.85em;
                color: #666;
                text-transform: uppercase;
                margin-bottom: 10px;
            }
            
            .metric-value {
                font-size: 1.8em;
                font-weight: bold;
                color: #0066cc;
            }
            
            .funnel-section {
                margin: 40px 0;
            }
            
            .funnel-step {
                display: flex;
                align-items: center;
                margin: 15px 0;
                padding: 15px;
                background: #f9f9f9;
                border-radius: 4px;
            }
            
            .step-name {
                flex: 1;
                font-weight: bold;
            }
            
            .step-bar {
                flex: 2;
                height: 30px;
                background: linear-gradient(to right, #0066cc, #00d9ff);
                border-radius: 4px;
                margin: 0 20px;
            }
            
            .step-stats {
                text-align: right;
                font-size: 0.9em;
                min-width: 150px;
            }
            
            .recommendations {
                margin: 40px 0;
            }
            
            .rec-card {
                background: #f0f7ff;
                border-left: 4px solid #0066cc;
                padding: 20px;
                margin: 20px 0;
                border-radius: 4px;
            }
            
            .rec-title {
                font-size: 1.2em;
                font-weight: bold;
                color: #0066cc;
                margin-bottom: 10px;
            }
            
            .badge {
                display: inline-block;
                padding: 4px 12px;
                border-radius: 20px;
                font-size: 0.8em;
                font-weight: bold;
                margin-right: 10px;
            }
            
            .priority-high {
                background: #ff6b6b;
                color: white;
            }
            
            .priority-medium {
                background: #ffd93d;
                color: #333;
            }
            
            .rec-actions {
                list-style: none;
                margin: 15px 0;
            }
            
            .rec-actions li {
                padding: 8px 0;
                padding-left: 25px;
                position: relative;
            }
            
            .rec-actions li:before {
                content: "✓";
                position: absolute;
                left: 0;
                color: #0066cc;
                font-weight: bold;
            }
            
            footer {
                margin-top: 60px;
                padding-top: 20px;
                border-top: 1px solid #eee;
                text-align: center;
                color: #999;
                font-size: 0.9em;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>📊 Relatório de Análise CRO</h1>
                <p class="timestamp">Gerado em: {{ timestamp }}</p>
            </header>
            
            <section class="summary">
                <div class="metric-card">
                    <div class="metric-label">Total de Conversões</div>
                    <div class="metric-value">{{ total_conversion_rate }}%</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Usuários Únicos</div>
                    <div class="metric-value">{{ unique_users }}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Total de Eventos</div>
                    <div class="metric-value">{{ total_events }}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Pontos de Abandono</div>
                    <div class="metric-value">{{ abandonment_count }}</div>
                </div>
            </section>
            
            <section class="funnel-section">
                <h2>🎯 Funil de Conversão</h2>
                {% for step in funnel_steps %}
                <div class="funnel-step">
                    <div class="step-name">{{ step['name'] }}</div>
                    <div class="step-bar" style="width: {{ step['percentage'] }}%"></div>
                    <div class="step-stats">
                        {{ step['percentage'] }}% | {{ step['users'] }} usuários
                    </div>
                </div>
                {% endfor %}
            </section>
            
            <section class="recommendations">
                <h2>💡 Recomendações de Otimização</h2>
                {% for rec in recommendations %}
                <div class="rec-card">
                    <div class="rec-title">{{ rec['title'] }}</div>
                    <div>
                        <span class="badge priority-{{ rec['priority'] }}">
                            {{ rec['priority'].upper() }}
                        </span>
                        <span class="badge">Impacto: {{ rec['expected_impact'] }}</span>
                    </div>
                    <p style="margin: 15px 0; color: #666;">{{ rec['description'] }}</p>
                    <h4 style="margin-top: 15px; margin-bottom: 10px;">Ações recomendadas:</h4>
                    <ul class="rec-actions">
                        {% for action in rec['actions'] %}
                        <li>{{ action }}</li>
                        {% endfor %}
                    </ul>
                </div>
                {% endfor %}
            </section>
            
            <footer>
                <p>© 2026 CRO Analysis Tool | Análise Automática de Taxa de Conversão</p>
            </footer>
        </div>
    </body>
    </html>
    """
    
    def __init__(self):
        """Initialize report generator"""
        self.template = Template(self.HTML_TEMPLATE)
    
    def generate_html_report(
        self,
        analysis_results: Dict,
        output_file: str
    ) -> str:
        """
        Generate HTML report from analysis results
        
        Args:
            analysis_results: Complete analysis results
            output_file: Output HTML filename
            
        Returns:
            HTML content
        """
        # Prepare data for template
        summary = analysis_results.get('summary', {})
        funnel_metrics = analysis_results.get('funnel_metrics', {})
        recommendations = analysis_results.get('recommendations', [])
        abandonment_points = analysis_results.get('abandonment_points', [])
        
        # Build funnel steps for visualization
        funnel_steps = []
        max_users = summary.get('unique_users', 1)
        
        for step in funnel_metrics.get('steps', []):
            users = funnel_metrics.get('step_users', {}).get(step, 0)
            percentage = (users / max_users * 100) if max_users > 0 else 0
            
            funnel_steps.append({
                'name': step,
                'users': users,
                'percentage': round(percentage, 1)
            })
        
        # Render HTML
        html_content = self.template.render(
            timestamp=datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
            total_conversion_rate=round(analysis_results.get('total_conversion_rate', 0), 2),
            unique_users=summary.get('unique_users', 0),
            total_events=summary.get('total_events', 0),
            abandonment_count=len(abandonment_points),
            funnel_steps=funnel_steps,
            recommendations=recommendations
        )
        
        # Write to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return html_content
