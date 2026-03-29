# 📊 Endpoints: PARA QUE SERVE CADA UM?

## 🗺️ Mapa Visual dos Endpoints

```
┌─────────────────────────────────────────────────────────────────┐
│  GOOGLE ANALYTICS 4 - Dados de Eventos & Conversões             │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  POST /ga4/import              → Importa TUDO do GA4            │
│  ├─ Eventos (page_view, purchase, etc)                          │
│  ├─ Métricas de sessão                                          │
│  └─ Dados de conversão                                          │
│                                                                   │
│  GET /ga4/funnel               → Rastreia sequência específica  │
│  └─ Exemplo: page_view → cart → checkout → purchase            │
│                                                                   │
│  GET /ga4/metrics              → 4 métricas principais          │
│  ├─ Total de sessões                                            │
│  ├─ Taxa de rejeição                                            │
│  ├─ Duração média de sessão                                     │
│  └─ Vistas de página                                            │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  MICROSOFT CLARITY - Comportamento & Heatmaps                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  POST /clarity/import          → Importa TUDO da Clarity        │
│  ├─ Heatmaps                                                    │
│  ├─ Métricas por página                                         │
│  └─ Comparação conversores vs abandonadores                     │
│                                                                   │
│  GET /clarity/heatmap          → ONDE usuários clicam?          │
│  └─ Coordenadas x,y com densidade de clicks                     │
│                                                                   │
│  GET /clarity/pages            → QUAIS páginas abandonam?       │
│  └─ Lista de páginas com bounce rate + tempo                    │
│                                                                   │
│  GET /clarity/recordings       → VER o que usuários fazem       │
│  └─ URLs de vídeos reais de sessões                             │
│                                                                   │
│  GET /clarity/feedback         → O que usuários FALAM?          │
│  └─ Comentários com sentimento (positivo/negativo)              │
│                                                                   │
│  GET /clarity/comparison       → Diferença conversores vs quit   │
│  └─ Padrões de comportamento que levam à conversão              │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📋 Tabela Rápida de Referência

| Endpoint | Tipo | Para Que Serve | Resposta | Prioridade |
|----------|------|----------------|----------|-----------|
| `/ga4/import` | POST | Trazer tudo de GA4 | Eventos + métricas | 🔴 High |
| `/ga4/funnel` | GET | Ver sequência de compra | Taxa conversão/step | 🔴 High |
| `/ga4/metrics` | GET | Métricas gerais | 4 números principais | 🟡 Med |
| `/clarity/import` | POST | Trazer tudo de Clarity | Heatmap + dados | 🔴 High |
| `/clarity/heatmap` | GET | Ver onde clicam | Pontos de coordenadas | 🟡 Med |
| `/clarity/pages` | GET | Quais páginas são ruins | Bounce rate por URL | 🔴 High |
| `/clarity/recordings` | GET | Ver vídeos de usuários | URLs das gravações | 🟢 Ready |
| `/clarity/feedback` | GET | Ler o que falam | Comentários + sentimento | 🟢 Ready |
| `/clarity/comparison` | GET | Encontrar padrões | Diferenças de comportamento | 🟡 Med |

---

## 🎯 Casos de Uso Reais

### Caso 1: "Minha taxa de conversão caiu 50%"
```
1. GET /ga4/funnel
   → Identifica qual step perdeu mais usuários
   
2. GET /clarity/pages
   → Encontra qual página ficou com bounce alto
   
3. GET /clarity/recordings
   → Assiste gravações dos usuários naquela página
   
4. GET /clarity/feedback
   → Lê comentários dos usuários para entender o problema
```

---

### Caso 2: "Quero otimizar meu checkout"
```
1. GET /clarity/heatmap
   → Vê onde clicam no checkout
   → Se botão de compra está em área fria, move!
   
2. GET /clarity/comparison
   → Descobre: conversores clicam 3x mais que abandonadores
   → Qual elemento está confuno?
   
3. GET /clarity/recordings
   → Assiste usuários tentando fazer checkout
   → Nota: "Clicam no campo errado", "Confundem com anúncio", etc
   
4. Implementa mudanças
```

---

### Caso 3: "Estou com pouco tempo, quero diagnosticar tudo agora"
```
1. POST /ga4/import
2. POST /clarity/import
   ↓
   Pego TODOS os dados de uma vez

3. Depois analisar os dois responses:
   - GA4: onde estão perdendo no funil?
   - Clarity: que páginas/elementos causam saída?
```

---

## 🔍 Entender as Respostas

### GET `/ga4/funnel` - O que significa cada número?

```json
{
  "funnel": [
    {
      "step": "page_view",
      "position": 1,
      "users": 10000,
      "conversionRate": 100
    },
    {
      "step": "add_to_cart",
      "position": 2,
      "users": 500,
      "conversionRate": 5
    },
    {
      "step": "purchase",
      "position": 3,
      "users": 50,
      "conversionRate": 0.5
    }
  ]
}
```

**Interpretação:**
- 📌 `step` = Nome do evento no GA4
- 📍 `position` = Ordem no funil (1º, 2º, 3º...)
- 👥 `users` = Quantos chegaram neste step
- 📊 `conversionRate` = Percentual em relação ao initial

**Leitura:**
- 10.000 visitas na página = 100% (baseline)
- 500 adicionam ao carrinho = 5% (perdeu 9.500!)
- 50 completam compra = 0.5% (perdeu 450!)

**Ação:** O maior drop é page_view → add_to_cart (95% saem). Otimize isso!

---

### GET `/clarity/comparison` - O que significa?

```json
{
  "converted": {
    "avgClicks": 8.5,
    "avgScrollDepth": 75,
    "avgTimeSpent": 420
  },
  "abandoned": {
    "avgClicks": 3.2,
    "avgScrollDepth": 30,
    "avgTimeSpent": 120
  },
  "comparison": {
    "clickDiff": "165.6%",
    "scrollDiff": "150.0%",
    "timeDiff": "250.0%"
  }
}
```

**O que significa:**

| Métrica | Conversores | Abandonadores | Significado |
|---------|-------------|---------------|-------------|
| Clicks | 8.5 | 3.2 | Conversores interagem 166% mais |
| Scroll | 75% | 30% | Conversores veem mais conteúdo |
| Tempo | 420s | 120s | Conversores ficam 3x5 mais |

**Insight:** Conversores exploram mais a página. Talvez abandonadores não encontram o que procuram?

**Ação:** 
- Melhor navegação
- CTA mais visível
- Conteúdo mais claro

---

### GET `/clarity/heatmap` - Como ler a densidade?

```json
{
  "heatmap": [
    { "x": 450, "y": 200, "density": 450 },  ← Muitos cliques aqui!
    { "x": 500, "y": 250, "density": 380 },
    { "x": 100, "y": 100, "density": 5 }     ← Quase ninguém clica
  ]
}
```

**Visualizar:**
```
╔════════════════════════╗
║  Página do Navegador   ║
║                        ║
║   5    [Header]   5    ║     ← Poucos clicam aqui
║                        ║
║   🔴🔴🔴🔴 [CTA] 450   ║  ← MUITO interesse!
║   🔴🔴🔴  clicks                │
║                        ║
║   [Footer]        20   ║     ← Alguns clicam
║                        ║
╚════════════════════════╝
```

**Ação:** São essa região RED (alta densidade) é onde está o CTA? Perfeito! Se não, move o CTA para ali!

---

## 🚀 Estratégia de Uso

### Semana 1: Diagnóstico
```
✅ POST /ga4/import      → Entender funil completo
✅ POST /clarity/import  → Ver comportamento/abandono
✅ GET /clarity/pages    → Identificar página problema #1
```

### Semana 2: Análise Profunda
```
✅ GET /clarity/comparison   → Comparar conversores vs quit
✅ GET /clarity/recordings   → Assistir 10 vídeos de abandonadores
✅ GET /clarity/feedback     → Ler comentários negativos
```

### Semana 3: Identificar Solução
```
✅ GET /clarity/heatmap      → Onde estão clicando?
✅ GET /ga4/funnel          → Qual exato step está quebrando?
❌ Pensar em 3 mudanças
✅ Implementar #1
```

### Semana 4: Medir Resultado
```
✅ GET /ga4/metrics         → Comparar com semana 1
✅ GET /clarity/comparison  → Dados melhorando?
✅ Repetir para próxima página problema
```

---

## ⚠️ Notas Importantes

### 1. Autenticação
Todos os endpoints precisam de `Authorization: Bearer {token}`
```bash
curl http://localhost:3001/api/integrations/ga4/metrics \
  -H "Authorization: Bearer seu-token-aqui"
```

### 2. Credenciais Seguras
**NUNCA** coloque credenciais no código.
Use arquivo `.env`:
```
GOOGLE_CREDENTIALS_PATH=/path/to/creds.json
CLARITY_TOKEN=sua-token-aqui
```

### 3. Limites de Taxa (Rate Limiting)
- GA4: ~100 requisições por minuto
- Clarity: ~60 requisições por minuto

### 4. Atraso de Dados
- GA4: 24-48 horas de latência
- Clarity: ~2-4 horas de latência

---

## 📈 ROI dos Endpoints

| Endpoint | Esforço | Impacto | ROI |
|----------|---------|--------|-----|
| /ga4/funnel | 15 min | Alto (identifica bottleneck) | ⭐⭐⭐⭐⭐ |
| /clarity/pages | 10 min | Alto (encontra página problema) | ⭐⭐⭐⭐⭐ |
| /clarity/comparison | 20 min | Alto (explica por que saem) | ⭐⭐⭐⭐⭐ |
| /clarity/recordings | 60 min | Alto (vê tudo de verdade) | ⭐⭐⭐⭐ |
| /clarity/feedback | 10 min | Médio (contexto adicional) | ⭐⭐⭐ |
| /clarity/heatmap | 30 min | Médio (melhora UX) | ⭐⭐⭐ |
| /ga4/metrics | 5 min | Baixo (dados básicos) | ⭐⭐ |

---

## ✅ Checklist de Implementação

- [ ] Obter credenciais Google Analytics 4
- [ ] Obter token Microsoft Clarity
- [ ] Testar POST /ga4/import localmente
- [ ] Testar POST /clarity/import localmente
- [ ] Integrar no React Dashboard
- [ ] Criar visualizações dos dados
- [ ] Salvar histórico no Supabase
- [ ] Criar relatório mensal automático
- [ ] Documentar insights para o time

---

## 🎓 Próximas Lições

1. Como integrar estes endpoints no React
2. Como salvar dados no Supabase
3. Como criar gráficos dos dados
4. Como gerar relatórios automáticos
5. Como integrar com Slack/Email
