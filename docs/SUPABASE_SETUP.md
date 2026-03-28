# Guia de Integração Supabase

## 🚀 Setup Supabase com Exemplos CRO

### 1. Criar Projeto Supabase

1. Acesse [supabase.com](https://supabase.com)
2. Clique em "New Project"
3. Preencha os detalhes:
   - **Name**: `cro-examples`
   - **Database Password**: Salve em local seguro
   - **Region**: Selecione mais próximo de você

### 2. Obter Credenciais

1. Vá para **Settings → API → Project Settings**
2. Copie:
   - `SUPABASE_URL` 
   - `SUPABASE_ANON_KEY`

### 3. Configurar Variáveis .env

```bash
# Abra seu arquivo .env
nano .env

# Adicione:
SUPABASE_URL=https://seu-project.supabase.co
SUPABASE_KEY=sua-anon-key
```

### 4. Rodar SQL Schema

1. Vá para **SQL Editor** no Supabase
2. Copie o SQL de `src/supabase_manager.py` (seção `SUPABASE_SCHEMA`)
3. Cole no editor e execute

### 5. Criar Bucket de Storage

1. Vá para **Storage → New Bucket**
2. Nome: `cro-examples`
3. Marque **Public bucket**
4. Clique **Create**

### 6. Instalar Dependência

```bash
pip install supabase
```

### 7. Usar no Código

```python
from src.supabase_manager import SupabaseExamplesManager
import os

# Inicializar
manager = SupabaseExamplesManager(
    supabase_url=os.getenv('SUPABASE_URL'),
    supabase_key=os.getenv('SUPABASE_KEY')
)

# Armazenar exemplo
manager.store_example(
    recommendation_id='high_cart_abandonment_add_to_cart',
    title='Exemplo: Banner Hero Otimizado',
    description='Banner com hierarquia clara, CTA destacado',
    example_type='good',
    image_url='https://exemplo.com/banner.jpg'
)

# Recuperar exemplos
examples = manager.get_examples_for_recommendation('high_cart_abandonment_add_to_cart')

# Armazenar análise de concorrente
manager.store_competitor_analysis(
    competitor_name='Concorrente X',
    website_url='https://concorrente.com',
    strengths=['Banner otimizado', 'Vídeos de produto'],
    weaknesses=['Sem prova social', 'Checkout longo'],
    insights='Bom exemplo de hero banner com urgência',
    cro_score=72
)

# Recuperar insights de concorrentes
competitors = manager.get_competitor_insights(limit=10)
```

## 📊 Estrutura de Dados

### Tabela: `cro_examples`
| Campo | Tipo | Descrição |
|-------|------|-----------|
| `recommendation_id` | TEXT | ID da recomendação |
| `title` | TEXT | Título do exemplo |
| `description` | TEXT | Descrição |
| `type` | TEXT | 'good', 'bad', 'competitor' |
| `image_url` | TEXT | URL da imagem |
| `video_url` | TEXT | URL do vídeo |
| `metadata` | JSONB | Dados adicionais |

### Tabela: `competitor_analysis`
| Campo | Tipo | Descrição |
|-------|------|-----------|
| `name` | TEXT | Nome do concorrente |
| `website_url` | TEXT | URL do site |
| `strengths` | JSONB | Pontos fortes |
| `weaknesses` | JSONB | Pontos fracos |
| `insights` | TEXT | Insights CRO |
| `screenshot_url` | TEXT | Screenshot |
| `cro_score` | NUMERIC | Score 0-100 |

## 🔄 Fluxo Completo

```
1. Análise CRO → 2. Gera Recomendações → 3. Armazena Exemplos no Supabase
   ↓                    ↓
   Dados               Insights
   
4. Relatório Busca Exemplos → 5. Gera HTML Otimizado com Imagens
   no Supabase
```

## 📦 Upload de Imagens

```python
# Upload de imagem
public_url = manager.upload_image(
    file_path='/caminho/para/exemplo.jpg',
    bucket_name='cro-examples'
)

# Usar em exemplo
manager.store_example(
    recommendation_id='...',
    title='...',
    image_url=public_url,  # URL pública
    ...
)
```

## 🔐 Segurança

- Use `SUPABASE_ANON_KEY` para leitura pública
- Use `SUPABASE_SERVICE_KEY` para admin (nunca exponha no client)
- Configure RLS policies para controlar acesso
- Use secrets no `.env`

## 🐛 Troubleshooting

### Erro: "Supabase client not installed"
```bash
pip install supabase python-dotenv
```

### Erro: "Connection refused"
- Verifique se `SUPABASE_URL` está correto
- Verifique conexão com internet
- Teste acesso ao projeto no dashboard

### Imagens não aparecem
- Verifique se bucket é público
- Verifique URL da imagem
- Teste acesso direto no browser

## 📚 Recursos

- [Supabase Docs](https://supabase.com/docs)
- [Python Client](https://github.com/supabase-community/supabase-py)
- [Storage Guide](https://supabase.com/docs/guides/storage)
