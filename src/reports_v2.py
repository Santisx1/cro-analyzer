"""
Advanced Report Generator v2
Generates optimized AdScale-style reports with visual examples and competitor insights
"""

import json
from typing import Dict, List


class AdvancedReportGenerator:
    """Generate advanced visual reports with examples and competitor insights"""
    
    HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    
    <!-- FONTS: Otimizado para legibilidade -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
    
    <style>
        :root {
            --bg: #080809;
            --surface: #0f0f12;
            --surface-2: #16161a;
            --surface-3: #1c1c22;
            --border: rgba(255,255,255,0.08);
            --border-accent: rgba(76,192,115,0.3);
            
            /* Primary accent - Green (mais legível que lime) */
            --accent: #4cc073;
            --accent-dim: rgba(76,192,115,0.12);
            --accent-glow: rgba(76,192,115,0.25);
            
            /* Status colors */
            --critical: #ff4757;
            --warning: #ffa502;
            --success: #4cc073;
            --info: #3b82f6;
            
            --text-primary: #f0f0f0;
            --text-secondary: #b0b0b0;
            --text-tertiary: #808080;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        html, body {
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }
        
        body {
            background: var(--bg);
            color: var(--text-primary);
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            font-size: 14px;
            line-height: 1.6;
            min-height: 100vh;
        }
        
        code, pre, .mono {
            font-family: 'JetBrains Mono', 'Courier New', monospace;
            font-size: 13px;
        }
        
        .noise {
            position: fixed;
            inset: 0;
            background-image: 
                url("data:image/svg+xml,%3Csvg width='100' height='100' xmlns='http://www.w3.org/2000/svg'%3E%3CfilterE id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.03'/%3E%3C/svg%3E");
            pointer-events: none;
            z-index: -1;
            opacity: 0.4;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 40px;
            position: relative;
            z-index: 1;
        }
        
        /* HEADER */
        header {
            padding: 32px 0;
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            background: rgba(8,8,9,0.95);
            backdrop-filter: blur(20px);
            z-index: 100;
        }
        
        .logo {
            display: flex;
            align-items: center;
            gap: 12px;
            font-weight: 700;
            font-size: 18px;
        }
        
        .logo-icon {
            width: 36px;
            height: 36px;
            background: var(--accent);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--bg);
            font-weight: 800;
            font-size: 16px;
        }
        
        .logo span {
            color: var(--accent);
        }
        
        .header-meta {
            display: flex;
            gap: 24px;
            align-items: center;
            font-size: 12px;
            color: var(--text-secondary);
        }
        
        .header-date {
            font-family: 'JetBrains Mono', monospace;
        }
        
        /* SECTIONS */
        .section {
            margin: 60px 0;
        }
        
        .section-header {
            display: flex;
            align-items: baseline;
            gap: 16px;
            margin-bottom: 32px;
        }
        
        .section-number {
            font-size: 48px;
            font-weight: 700;
            color: var(--surface-3);
            line-height: 1;
        }
        
        .section-title {
            font-size: 24px;
            font-weight: 700;
            letter-spacing: -0.5px;
        }
        
        /* CARDS */
        .card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 24px;
            transition: all 0.2s;
        }
        
        .card:hover {
            border-color: var(--border-accent);
            background: var(--surface-2);
        }
        
        .card-title {
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 12px;
        }
        
        .card-desc {
            font-size: 13px;
            color: var(--text-secondary);
            line-height: 1.6;
        }
        
        /* GRID */
        .grid {
            display: grid;
            gap: 20px;
            margin-bottom: 32px;
        }
        
        .grid-2 { grid-template-columns: repeat(2, 1fr); }
        .grid-3 { grid-template-columns: repeat(3, 1fr); }
        .grid-4 { grid-template-columns: repeat(4, 1fr); }
        
        @media (max-width: 1200px) {
            .grid-3 { grid-template-columns: repeat(2, 1fr); }
            .grid-4 { grid-template-columns: repeat(2, 1fr); }
        }
        
        @media (max-width: 768px) {
            .grid-2, .grid-3, .grid-4 { grid-template-columns: 1fr; }
            .container { padding: 0 20px; }
        }
        
        /* KPI CARDS */
        .kpi-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 24px;
            position: relative;
            overflow: hidden;
        }
        
        .kpi-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: var(--accent);
        }
        
        .kpi-label {
            font-size: 12px;
            color: var(--text-tertiary);
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 12px;
            font-weight: 600;
        }
        
        .kpi-value {
            font-size: 32px;
            font-weight: 700;
            line-height: 1;
            margin-bottom: 8px;
        }
        
        .kpi-delta {
            font-size: 12px;
            color: var(--text-secondary);
        }
        
        .kpi-delta.up { color: var(--success); }
        .kpi-delta.down { color: var(--critical); }
        
        /* RECOMMENDATION CARD */
        .rec-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 24px;
            display: flex;
            flex-direction: column;
            gap: 16px;
        }
        
        .rec-header {
            display: flex;
            gap: 12px;
            align-items: flex-start;
        }
        
        .rec-priority {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            white-space: nowrap;
        }
        
        .rec-priority.p1 {
            background: rgba(255,71,87,0.2);
            color: #ff4757;
            border: 1px solid rgba(255,71,87,0.3);
        }
        
        .rec-priority.p2 {
            background: rgba(255,165,2,0.2);
            color: #ffa502;
            border: 1px solid rgba(255,165,2,0.3);
        }
        
        .rec-title {
            font-size: 16px;
            font-weight: 600;
            line-height: 1.4;
        }
        
        .rec-desc {
            font-size: 13px;
            color: var(--text-secondary);
            line-height: 1.6;
        }
        
        .rec-actions {
            background: var(--surface-2);
            border-left: 3px solid var(--accent);
            padding: 16px;
            border-radius: 8px;
            font-size: 13px;
        }
        
        .rec-actions h4 {
            font-size: 12px;
            color: var(--accent);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 10px;
            font-weight: 600;
        }
        
        .rec-actions ul {
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        
        .rec-actions li {
            padding-left: 20px;
            position: relative;
        }
        
        .rec-actions li::before {
            content: '→';
            position: absolute;
            left: 0;
            color: var(--accent);
            font-weight: 600;
        }
        
        .rec-impact {
            display: flex;
            gap: 16px;
            padding-top: 16px;
            border-top: 1px solid var(--border);
        }
        
        .rec-impact-item {
            flex: 1;
        }
        
        .rec-impact-label {
            font-size: 11px;
            color: var(--text-tertiary);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 6px;
        }
        
        .rec-impact-value {
            font-size: 16px;
            font-weight: 700;
            color: var(--accent);
        }
        
        /* EXAMPLE SECTION */
        .example-section {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
            overflow: hidden;
            margin-bottom: 24px;
        }
        
        .example-header {
            background: var(--surface-2);
            padding: 16px 24px;
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .example-title {
            font-weight: 600;
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--accent);
        }
        
        .example-badge {
            font-size: 11px;
            padding: 4px 10px;
            background: rgba(76,192,115,0.2);
            color: var(--accent);
            border-radius: 4px;
            border: 1px solid rgba(76,192,115,0.3);
        }
        
        .example-content {
            padding: 24px;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 24px;
            align-items: center;
        }
        
        .example-visual {
            background: var(--surface-3);
            border: 1px solid var(--border);
            border-radius: 8px;
            aspect-ratio: 16 / 10;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--text-tertiary);
            font-size: 13px;
            position: relative;
            overflow: hidden;
            min-height: 200px;
        }
        
        .example-visual img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        
        .example-visual video {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        
        .example-text h3 {
            font-size: 16px;
            font-weight: 700;
            margin-bottom: 12px;
        }
        
        .example-text p {
            font-size: 13px;
            color: var(--text-secondary);
            line-height: 1.7;
            margin-bottom: 12px;
        }
        
        .example-tips {
            background: var(--surface-2);
            border-left: 3px solid var(--info);
            padding: 12px 16px;
            border-radius: 6px;
            font-size: 12px;
            margin-top: 12px;
        }
        
        .example-tips b {
            color: var(--info);
        }
        
        /* COMPETITOR BENCHMARK */
        .competitor-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }
        
        .competitor-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
            overflow: hidden;
        }
        
        .competitor-image {
            width: 100%;
            aspect-ratio: 16 / 10;
            background: var(--surface-2);
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--text-tertiary);
            font-size: 12px;
        }
        
        .competitor-image img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        
        .competitor-info {
            padding: 16px;
        }
        
        .competitor-name {
            font-weight: 700;
            font-size: 14px;
            margin-bottom: 8px;
        }
        
        .competitor-insight {
            font-size: 12px;
            color: var(--text-secondary);
            line-height: 1.6;
        }
        
        /* FOOTER */
        footer {
            border-top: 1px solid var(--border);
            padding: 32px 0;
            margin-top: 80px;
        }
        
        .footer-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 12px;
            color: var(--text-secondary);
        }
        
        .footer-links {
            display: flex;
            gap: 24px;
        }
        
        .footer-links a {
            color: var(--accent);
            text-decoration: none;
            transition: color 0.2s;
        }
        
        .footer-links a:hover {
            color: var(--text-primary);
        }
        
        /* UTILITY */
        .divider {
            height: 1px;
            background: var(--border);
            margin: 60px 0;
        }
        
        .badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 16px;
        }
        
        .badge-success {
            background: rgba(76,192,115,0.2);
            color: var(--success);
            border: 1px solid rgba(76,192,115,0.3);
        }
        
        .badge-critical {
            background: rgba(255,71,87,0.2);
            color: var(--critical);
            border: 1px solid rgba(255,71,87,0.3);
        }
        
        .badge-warning {
            background: rgba(255,165,2,0.2);
            color: var(--warning);
            border: 1px solid rgba(255,165,2,0.3);
        }
    </style>
</head>
<body>
    <div class="noise"></div>
    
    <header>
        <div class="container" style="display:flex;width:100%;justify-content:space-between;align-items:center;">
            <div class="logo">
                <div class="logo-icon">📊</div>
                <div>CRO Intelligence<br><small style="font-size:12px;font-weight:400;color:var(--text-tertiary);">{{ client_name }}</small></div>
            </div>
            <div class="header-meta">
                <div>Período: <strong>{{ date_range }}</strong></div>
                <div class="header-date">{{ generation_date }}</div>
            </div>
        </div>
    </header>
    
    <div class="container">
        <!-- EXECUTIVE SUMMARY -->
        <section class="section">
            <div class="section-header">
                <div class="section-number">01</div>
                <div class="section-title">Sumário Executivo</div>
            </div>
            
            <div class="grid grid-4">
                {{ kpi_cards }}
            </div>
        </section>
        
        <div class="divider"></div>
        
        <!-- FUNNEL ANALYSIS -->
        <section class="section">
            <div class="section-header">
                <div class="section-number">02</div>
                <div class="section-title">Funil de Conversão</div>
            </div>
            
            <div class="card" style="padding:32px;">
                <div id="funnelChart"></div>
            </div>
        </section>
        
        <div class="divider"></div>
        
        <!-- RECOMMENDATIONS WITH EXAMPLES -->
        <section class="section">
            <div class="section-header">
                <div class="section-number">03</div>
                <div class="section-title">Recomendações Priorizadas</div>
            </div>
            
            <div id="recommendationsSection"></div>
        </section>
        
        <div class="divider"></div>
        
        <!-- COMPETITOR BENCHMARKS -->
        <section class="section">
            <div class="section-header">
                <div class="section-number">04</div>
                <div class="section-title">Análise de Concorrentes</div>
            </div>
            
            <div class="card" style="padding:24px;">
                <p style="color:var(--text-secondary);margin-bottom:24px;">Exemplos de ações de concorrentes que você pode implementar:</p>
                <div class="competitor-grid" id="competitorGrid"></div>
            </div>
        </section>
        
        <footer>
            <div class="footer-content">
                <div>© 2026 CRO Intelligence • Análise Automática de Conversão</div>
                <div class="footer-links">
                    <a href="#recommendations">Recomendações</a>
                    <a href="#examples">Exemplos</a>
                    <a href="#competitors">Concorrentes</a>
                </div>
            </div>
        </footer>
    </div>
    
    <script>
        // Render funnel chart
        function renderFunnelChart() {
            const data = {{ funnel_data }};
            const html = data.map((step, i) => `
                <div style="margin-bottom:20px;">
                    <div style="display:flex;justify-content:space-between;margin-bottom:8px;">
                        <span style="font-weight:600;color:var(--text-primary);">${step.name}</span>
                        <span style="color:var(--text-secondary);">${step.pct.toFixed(1)}% (${step.users} usuários)</span>
                    </div>
                    <div style="height:24px;background:var(--surface-2);border-radius:6px;overflow:hidden;">
                        <div style="height:100%;width:${step.pct}%;background:linear-gradient(90deg, var(--accent), var(--info));border-radius:6px;transition:width 1s ease;"></div>
                    </div>
                    ${step.dropoff > 0 ? `<div style="font-size:12px;color:var(--critical);margin-top:6px;">↓ ${step.dropoff.toFixed(1)}% abandono</div>` : ''}
                </div>
            `).join('');
            document.getElementById('funnelChart').innerHTML = html;
        }
        
        // Render recommendations
        function renderRecommendations() {
            const recs = {{ recommendations }};
            const html = recs.map(r => `
                <div class="rec-card">
                    <div class="rec-header">
                        <div class="rec-priority ${r.priority}">P${r.priority_num}</div>
                        <div style="flex:1;">
                            <div class="rec-title">${r.title}</div>
                            <div class="rec-desc">${r.description}</div>
                        </div>
                    </div>
                    <div class="rec-actions">
                        <h4>Ações Recomendadas</h4>
                        <ul>
                            ${r.actions.map(a => `<li>${a}</li>`).join('')}
                        </ul>
                    </div>
                    <div class="rec-impact">
                        <div class="rec-impact-item">
                            <div class="rec-impact-label">Impacto Esperado</div>
                            <div class="rec-impact-value">${r.expected_impact}</div>
                        </div>
                        <div class="rec-impact-item">
                            <div class="rec-impact-label">Esforço</div>
                            <div class="rec-impact-value">${r.effort}</div>
                        </div>
                    </div>
                </div>
            `).join('');
            document.getElementById('recommendationsSection').innerHTML = html;
        }
        
        // Render competitors
        function renderCompetitors() {
            const competitors = {{ competitors }};
            const html = competitors.map(c => `
                <div class="competitor-card">
                    <div class="competitor-image">
                        ${c.image_url ? `<img src="${c.image_url}" alt="${c.name}">` : '<span>Imagem não disponível</span>'}
                    </div>
                    <div class="competitor-info">
                        <div class="competitor-name">${c.name}</div>
                        <div class="competitor-insight">${c.insight}</div>
                    </div>
                </div>
            `).join('');
            document.getElementById('competitorGrid').innerHTML = html;
        }
        
        renderFunnelChart();
        renderRecommendations();
        renderCompetitors();
    </script>
</body>
</html>
    """
    
    def __init__(self):
        """Initialize advanced report generator"""
        pass
    
    def generate_html_report(
        self,
        analysis_results: Dict,
        output_file: str,
        client_name: str = "Seu E-commerce",
        competitor_examples: List[Dict] = None
    ) -> str:
        """
        Generate advanced HTML report
        
        Args:
            analysis_results: Complete analysis results
            output_file: Output HTML filename
            client_name: Client name for header
            competitor_examples: List of competitor examples
            
        Returns:
            HTML content
        """
        from datetime import datetime
        
        # Extract data
        summary = analysis_results.get('summary', {})
        funnel_metrics = analysis_results.get('funnel_metrics', {})
        recommendations = analysis_results.get('recommendations', [])
        abandonment = analysis_results.get('abandonment_points', [])
        
        # Build KPI cards
        kpi_cards = self._build_kpi_cards(analysis_results)
        
        # Build funnel data
        funnel_data = self._build_funnel_data(funnel_metrics, abandonment)
        
        # Build recommendations with examples
        recs_json = self._build_recommendations_json(recommendations)
        
        # Build competitor examples
        competitors_json = competitor_examples or self._get_default_competitors()
        
        # Render template
        html = self.HTML_TEMPLATE
        html = html.replace('{{ title }}', 'CRO intelligence Dashboard')
        html = html.replace('{{ client_name }}', client_name)
        html = html.replace('{{ date_range }}', f"{summary.get('date_range', {}).get('start', '')} até {summary.get('date_range', {}).get('end', '')}")
        html = html.replace('{{ generation_date }}', datetime.now().strftime('%d %b %Y • %H:%M'))
        html = html.replace('{{ kpi_cards }}', kpi_cards)
        html = html.replace('{{ funnel_data }}', funnel_data)
        html = html.replace('{{ recommendations }}', recs_json)
        html = html.replace('{{ competitors }}', competitors_json)
        
        # Write file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return html
    
    def _build_kpi_cards(self, results: Dict) -> str:
        """Build KPI cards HTML"""
        summary = results.get('summary', {})
        funnel = results.get('funnel_metrics', {})
        
        cards = []
        
        # Taxa de conversão
        conv_rate = results.get('total_conversion_rate', 0)
        cards.append(f"""
            <div class="kpi-card">
                <div class="kpi-label">Taxa de Conversão</div>
                <div class="kpi-value">{conv_rate:.2f}%</div>
                <div class="kpi-delta">Benchmark: 2-5%</div>
            </div>
        """)
        
        # Usuários
        users = summary.get('unique_users', 0)
        cards.append(f"""
            <div class="kpi-card">
                <div class="kpi-label">Usuários Únicos</div>
                <div class="kpi-value">{users}</div>
                <div class="kpi-delta">Período analisado</div>
            </div>
        """)
        
        # Eventos
        events = summary.get('total_events', 0)
        cards.append(f"""
            <div class="kpi-card">
                <div class="kpi-label">Total de Eventos</div>
                <div class="kpi-value">{events}</div>
                <div class="kpi-delta">{events / users if users > 0 else 0:.1f} por usuário</div>
            </div>
        """)
        
        # Pontos críticos
        critical = len([a for a in results.get('abandonment_points', []) if a.get('severity') == 'high'])
        cards.append(f"""
            <div class="kpi-card">
                <div class="kpi-label">Pontos Críticos</div>
                <div class="kpi-value">{critical}</div>
                <div class="kpi-delta">Identificados</div>
            </div>
        """)
        
        return '\n'.join(cards)
    
    def _build_funnel_data(self, funnel: Dict, abandonment: List) -> str:
        """Build funnel data as JSON string"""
        data = []
        steps = funnel.get('steps', [])
        users_map = funnel.get('step_users', {})
        
        total_users = users_map.get(steps[0], 1) if steps else 1
        
        for step in steps:
            users = users_map.get(step, 0)
            pct = (users / total_users * 100) if total_users > 0 else 0
            
            # Find dropoff
            dropoff = 0
            for a in abandonment:
                if a.get('step') == step:
                    dropoff = a.get('drop_off_rate', 0)
                    break
            
            data.append({
                'name': step,
                'users': users,
                'pct': pct,
                'dropoff': dropoff
            })
        
        return json.dumps(data)
    
    def _build_recommendations_json(self, recs: List) -> str:
        """Build recommendations as JSON"""
        formatted = []
        for i, r in enumerate(recs[:6]):  # Top 6
            priority = 'p1' if r.get('priority') == 'high' else 'p2'
            priority_num = '1' if r.get('priority') == 'high' else '2'
            
            formatted.append({
                'title': r.get('title', ''),
                'description': r.get('description', ''),
                'priority': priority,
                'priority_num': priority_num,
                'actions': r.get('actions', [])[:4],
                'expected_impact': r.get('expected_impact', '—'),
                'effort': '2-3 dias' if priority == 'p1' else '1-2 semanas'
            })
        
        return json.dumps(formatted)
    
    def _get_default_competitors(self) -> str:
        """Get default competitor examples"""
        competitors = [
            {
                'name': 'Strategy 1: Hero Banner',
                'insight': 'Banner principal com hierarquia clara: Headline grande, CTA destacado, urgência visível',
                'image_url': None
            },
            {
                'name': 'Strategy 2: Vídeo de Produto',
                'insight': 'Vídeos curtos mostrando produto em uso. Aumenta conversão em até 80%',
                'image_url': None
            },
            {
                'name': 'Strategy 3: Social Proof',
                'insight': 'Reviews, ratings e testimonials prominentes na PDP. Confiança visual',
                'image_url': None
            },
        ]
        return json.dumps(competitors)
