# CRO Analysis Tool (Análise de CRO Automática)

Ferramenta Python completa para análise automatizada de **Conversion Rate Optimization (CRO)** - Otimização da Taxa de Conversão.

## 🎯 Recursos Principais

### ✅ Análise Automática de Funil de Conversão
- Identificação automática de steps do funil
- Cálculo de taxas de conversão em cada etapa
- Detecção de pontos de abandono
- Análise de tempo entre eventos

### ✅ Integração com Dados
- **Google Analytics 4** - Conexão nativa com GA4
- **Heatmap Providers** - Microsoft Clarity, Hotjar, Smartlook
- **CSV/JSON** - Suporte para arquivos locais

### ✅ Recomendações Inteligentes
- Geração automática de 30+ tipos de recomendações
- Priorização por impacto esperado
- Ações específicas e acionáveis
- Métricas para rastrear resultados

### ✅ Relatórios Profissionais
- **HTML interativo** - Visualizações do funil em tempo real
- **PDF** - Relatórios para compartilhamento
- **JSON** - Integração com outras ferramentas

### ✅ Web Application (React + Next.js)
- **Dashboard em Tempo Real** - KPIs, gráficos e recomendações
- **Autenticação com Supabase** - Login seguro com email/senha
- **Histórico de Análises** - Rastreamento de resultados ao longo do tempo
- **Integração com API Node.js** - Backend escalável com Express.js
- **Deployment em Vercel** - Hospedagem rápida e confiável

## 📦 Instalação

### Requisitos
- Python 3.10+
- pip

### Setup

```bash
# Clonar ou descompactar o projeto
cd "Análise de CRO"

# Criar ambiente virtual (recomendado)
python -m venv venv

# Ativar ambiente virtual
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
```

## 🌐 Web Application (React + Next.js)

### Setup Rápido

```bash
# Instalar Node.js (https://nodejs.org/)
# macOS com Homebrew:
brew install node

# Navegar para o diretório web
cd web

# Instalar dependências
npm install

# Iniciar desenvolvimento
npm run dev:full
```

**URLs:**
- Frontend: http://localhost:3000
- API: http://localhost:3001

Para mais detalhes, veja [REACT_MIGRATION.md](web/REACT_MIGRATION.md)

## 🚀 Uso Rápido

### 1. Configurar Dados

Editar `examples/sample_config.json`:
```json
{
  "ga4_property_id": "seu-property-id",
  "funnel_steps": [
    "page_view",
    "view_item", 
    "add_to_cart",
    "begin_checkout",
    "purchase"
  ]
}
```

### 2. Cargando Dados

Opção A: CSV Local (exemplo)
```csv
event_name,timestamp,user_id,event_value,page_url
page_view,2024-03-20 10:00:00,user_001,0,https://example.com
```

Opção B: Google Analytics 4
```python
from src.integrations.google_analytics import GoogleAnalyticsConnector

ga = GoogleAnalyticsConnector('credentials.json')
ga.authenticate('property_id')
data = ga.fetch_events('2024-03-01', '2024-03-31')
```

### 3. Executar Análise

```bash
python main.py
```

Saída:
- `relatorio_cro_analysis.html` - Relatório visual interativo
- `cro_analysis_results.json` - Dados brutos da análise

## 📊 Estrutura do Projeto

```
Análise de CRO/
├── src/
│   ├── analyzer.py           # Motor de análise principal
│   ├── data_processor.py     # Processamento de dados
│   ├── recommendations.py    # Gerador de recomendações
│   ├── reports.py            # Geração de relatórios
│   └── integrations/
│       ├── google_analytics.py
│       └── heatmap_provider.py
├── tests/                     # Testes unitários
├── examples/
│   ├── sample_config.json
│   └── sample_data.csv
├── main.py                    # Entry point
├── requirements.txt           # Dependências
└── README.md                  # Este arquivo
```

## 💡 Exemplo de Uso Programático

```python
from src.analyzer import CROAnalyzer
from src.reports import ReportGenerator
import pandas as pd

# Carregar dados
data = pd.read_csv('data.csv')

# Executar análise
analyzer = CROAnalyzer()
results = analyzer.analyze(
    events_data=data,
    funnel_steps=['page_view', 'add_to_cart', 'purchase']
)

# Gerar relatório
report_gen = ReportGenerator()
report_gen.generate_html_report(results, 'relatorio.html')

# Acessar resultados
print(f"Taxa de conversão: {results['total_conversion_rate']}%")
print(f"Recomendações: {len(results['recommendations'])}")
```

## 📈 Tipos de Análise

### 1. **Funnel Analysis**
- Entrada: Sequência de eventos por usuário
- Saída: Taxa de conversão por step, drop-off rates
- Uso: Identificar gargalos no funil

### 2. **Abandonment Detection**
- Identifica steps com >20% de abandono
- Classifica severidade (alta/média)
- Prioriza ações corretivas

### 3. **Recommendation Engine**
- Problemas automáticos detectados:
  - Abandono alto de carrinho
  - Taxa de rejeição alta
  - Friç friction em formulários
  - Baixo engajamento
  - Problemas mobile

### 4. **Performance Metrics**
- Taxa de conversão geral
- Eventos por usuário
- Período de análise
- Distribuição de eventos

## 🔧 Configuração Avançada

### Variáveis de Ambiente

Criar `.env`:
```env
GA4_PROPERTY_ID=seu-id
GA4_CREDENTIALS_PATH=/caminho/para/credentials.json
CLARITY_API_KEY=sua-chave
HOTJAR_API_KEY=sua-chave
```

### Personalizar Recomendações

Editar `src/recommendations.py`:
```python
RECOMMENDATIONS_DB = {
    'seu_tipo': {
        'title': 'Seu título',
        'actions': ['ação 1', 'ação 2'],
        'priority': 'high',
        'expected_impact': '20-30%'
    }
}
```

## 📝 API Reference

### CROAnalyzer

```python
analyzer = CROAnalyzer()

# Análise completa
results = analyzer.analyze(
    events_data: pd.DataFrame,
    funnel_steps: List[str],
    heatmap_data: Optional[pd.DataFrame],
    time_window_hours: int = 24
) -> Dict

# Obter resultados
results = analyzer.get_analysis_results() -> Dict

# Exportar
analyzer.export_results(filename: str)
```

### DataProcessor

```python
processor = DataProcessor()

# Carregar dados
processor.load_ga4_events(data: pd.DataFrame)
processor.load_heatmap_data(data: pd.DataFrame)

# Processar
funnel = processor.build_conversion_funnel(
    funnel_steps: List[str],
    time_window_hours: int = 24
) -> Dict

# Analisar
abandonment = processor.identify_abandonment_points() -> List[Dict]
stats = processor.get_summary_statistics() -> Dict
```

### RecommendationEngine

```python
engine = RecommendationEngine()

recommendations = engine.generate_recommendations(
    funnel_metrics: Dict,
    abandonment_points: List[Dict]
) -> List[Dict]
```

### ReportGenerator

```python
generator = ReportGenerator()

html = generator.generate_html_report(
    analysis_results: Dict,
    output_file: str
) -> str
```

## 🧪 Testes

```bash
# Executar todos os testes
pytest

# Com cobertura
pytest --cov=src tests/

# Teste específico
pytest tests/test_analyzer.py -v
```

## 🔐 Google Analytics Setup

### 1. Criar Service Account
1. Acesse Google Cloud Console
2. Projeto → Criar novo projeto
3. APIs e Serviços → Credenciais
4. Criar Service Account
5. Gerar chave JSON

### 2. Adicionar ao GA4
1. GA4 Admin → Contas e propriedades
2. Property Settings → User Management
3. Adicionar email do service account
4. Conceder permissão de "Editor"

### 3. Usar no projeto
```python
from src.integrations.google_analytics import GoogleAnalyticsConnector

ga = GoogleAnalyticsConnector('caminho/para/credentials.json')
ga.authenticate('seu-property-id')
```

## 📊 Formato de Dados Esperado

### CSV Input
```
event_name,timestamp,user_id,event_value,page_url
page_view,2024-03-20 10:00:00,user_001,0,https://example.com
add_to_cart,2024-03-20 10:05:00,user_001,29.99,https://example.com/cart
```

### JSON Output
```json
{
  "timestamp": "2024-03-27T10:00:00",
  "summary": {
    "total_events": 1024,
    "unique_users": 256,
    "events_per_user": 4.0
  },
  "funnel_metrics": {
    "steps": ["page_view", "add_to_cart", "purchase"],
    "conversion_rates": {},
    "drop_off_rates": {}
  },
  "recommendations": []
}
```

## 🐛 Troubleshooting

### Erro: "No module named 'src'"
```bash
# Ensure running from project root
cd "Análise de CRO"
python main.py
```

### Erro: "No events data loaded"
```python
# Certifique-se de carregar dados antes
processor.load_ga4_events(data)
```

### Erro: "Not authenticated"
```python
# Autentique antes de usar
ga.authenticate(property_id)
```

## 📚 Recursos Adicionais

- [Documentation](./docs/README.md)
- [Examples](./examples/)
- [API Reference](./src/)
- [Tests](./tests/)

## 🤝 Contribuindo

Melhorias e correções são bem-vindas!

## 📄 Licença

MIT License - Veja LICENSE.txt para detalhes

## 👥 Suporte

Para dúvidas ou problemas, crie uma issue no GitHub.

---

**Desenvolvido com ❤️ para otimizar suas taxas de conversão**
