# 🔗 Integrations API Guide

## 📌 Overview

Endpoints para integrar **Google Analytics 4** e **Microsoft Clarity** com seu dashboard CRO.

**Base URL:**
- Development: `http://localhost:3001/api/integrations`
- Production: `https://seu-app.vercel.app/api/integrations`

**Autenticação:** Todos os endpoints precisam de `Authorization: Bearer {token}`

---

## 🟢 Google Analytics 4

### 1️⃣ POST `/ga4/import` - Importar Todos os Dados

**Para que serve:** Conecta com seu GA4 e traz TODOS os dados de eventos e sessões

**Exemplo de requisição:**
```bash
curl -X POST http://localhost:3001/api/integrations/ga4/import \
  -H "Authorization: Bearer seu-token" \
  -H "Content-Type: application/json" \
  -d '{
    "credentialsPath": "/path/to/google-service-account.json",
    "propertyId": "123456789",
    "dateStart": "2024-03-01",
    "dateEnd": "2024-03-31"
  }'
```

**Resposta:**
```json
{
  "success": true,
  "eventsImported": 15430,
  "metrics": {
    "sessions": 50000,
    "bounceRate": 45.2,
    "avgSessionDuration": 240,
    "pageViews": 150000
  },
  "data": [
    {
      "eventName": "purchase",
      "date": "2024-03-15",
      "userId": "user_001",
      "count": 45,
      "users": 30
    }
  ]
}
```

**O que fazer com isso:**
- Salvar no banco de dados
- Usar para calcular a taxa de conversão
- Alimentar o motor de recomendações

---

### 2️⃣ GET `/ga4/funnel` - Buscar Funil de Conversão

**Para que serve:** Rastreia a sequência específica de eventos (ex: página inicial → carrinho → checkout → compra)

**Exemplo de requisição:**
```bash
curl "http://localhost:3001/api/integrations/ga4/funnel?propertyId=123456789&funnelSteps=page_view,add_to_cart,checkout,purchase&dateStart=2024-03-01&dateEnd=2024-03-31&credentialsPath=/path/to/creds.json" \
  -H "Authorization: Bearer seu-token"
```

**Resposta:**
```json
{
  "success": true,
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
      "step": "checkout",
      "position": 3,
      "users": 150,
      "conversionRate": 1.5
    },
    {
      "step": "purchase",
      "position": 4,
      "users": 50,
      "conversionRate": 0.5
    }
  ]
}
```

**Como ler:**
- 📊 100% chegam na página inicial
- 📉 Cai para 5% no carrinho (perdem 9.500 usuários!)
- 📉 Cai para 1.5% no checkout
- 🎯 0.5% completam a compra

**Ação:** Otimize o carrinho que está perdendo 95% dos usuários!

---

### 3️⃣ GET `/ga4/metrics` - Métricas Gerais de Sessão

**Para que serve:** Pega as 4 métricas principais do GA4

**Exemplo de requisição:**
```bash
curl "http://localhost:3001/api/integrations/ga4/metrics?propertyId=123456789&dateStart=2024-03-01&dateEnd=2024-03-31&credentialsPath=/path/to/creds.json" \
  -H "Authorization: Bearer seu-token"
```

**Resposta:**
```json
{
  "sessions": 50000,
  "bounceRate": 45.2,
  "avgSessionDuration": 240,
  "pageViews": 150000
}
```

**O que significa:**
- 50.000 sessões no mês
- 45% abandonam sem fazer nada
- Tempo médio: 240 segundos (4 minutos)
- 150.000 páginas vistas (média 3 páginas/sessão)

---

## 🔵 Microsoft Clarity

### 1️⃣ POST `/clarity/import` - Importar Todos os Dados

**Para que serve:** Traz dados de heatmap, comportamento, comparação conversão/abandono

**Exemplo de requisição:**
```bash
curl -X POST http://localhost:3001/api/integrations/clarity/import \
  -H "Authorization: Bearer seu-token" \
  -H "Content-Type: application/json" \
  -d '{
    "clarityToken": "seu-token-do-clarity",
    "projectId": "123456",
    "dateStart": "2024-03-01",
    "dateEnd": "2024-03-31"
  }'
```

**Resposta:**
```json
{
  "success": true,
  "heatmapData": [
    { "x": 450, "y": 200, "density": 450, "clicks": 450 },
    { "x": 500, "y": 250, "density": 380, "clicks": 380 }
  ],
  "pageMetrics": [
    { "url": "/checkout", "sessions": 1000, "bounceRate": 65, "timeOnPage": 120 }
  ],
  "sessionComparison": {
    "converted": { "avgClicks": 8.5, "avgScrollDepth": 75 },
    "abandoned": { "avgClicks": 3.2, "avgScrollDepth": 30 }
  }
}
```

---

### 2️⃣ GET `/clarity/heatmap` - Mapa de Calor

**Para que serve:** Mostra EXATAMENTE ONDE usuários clicam mais na página

**Exemplo:**
```bash
curl "http://localhost:3001/api/integrations/clarity/heatmap?clarityToken=...&projectId=123&dateStart=2024-03-01&dateEnd=2024-03-31" \
  -H "Authorization: Bearer seu-token"
```

**Resposta:**
```json
{
  "success": true,
  "heatmap": [
    { "x": 450, "y": 200, "density": 450 },
    { "x": 450, "y": 210, "density": 420 },
    { "x": 450, "y": 220, "density": 380 },
    { "x": 500, "y": 250, "density": 380 }
  ],
  "insight": "Mostra onde usuários clicam mais - útil para otimizar CTAs"
}
```

**Como usar:**
- Desenhe um mapa de calor da sua página
- Onde tem cor VERMELHA = muitos cliques
- Onde tem cor FRIA = poucos cliques
- Se botão de CTA está em área fria, move para área quente!

---

### 3️⃣ GET `/clarity/pages` - Páginas com Maior Rejeição

**Para que serve:** Identifica quais páginas estão perdendo usuários

**Exemplo:**
```bash
curl "http://localhost:3001/api/integrations/clarity/pages?clarityToken=...&projectId=123&dateStart=2024-03-01&dateEnd=2024-03-31" \
  -H "Authorization: Bearer seu-token"
```

**Resposta:**
```json
{
  "success": true,
  "pages": [
    {
      "url": "/checkout",
      "bounceRate": 65,
      "sessions": 1000,
      "timeOnPage": 120,
      "clicks": 450
    },
    {
      "url": "/cart",
      "bounceRate": 55,
      "sessions": 800,
      "timeOnPage": 180,
      "clicks": 350
    },
    {
      "url": "/product",
      "bounceRate": 30,
      "sessions": 5000,
      "timeOnPage": 240,
      "clicks": 2100
    }
  ],
  "topProblems": [
    { "url": "/checkout", "bounceRate": 65 },
    { "url": "/cart", "bounceRate": 55 }
  ]
}
```

**Insight:** Checkout está MUITO ruim (65% saem). É a prioridade #1!

---

### 4️⃣ GET `/clarity/recordings` - Gravações de Sessão

**Para que serve:** VER EXATAMENTE o que usuários fazem antes de abandonar

**Exemplo:**
```bash
curl "http://localhost:3001/api/integrations/clarity/recordings?clarityToken=...&projectId=123&filter=abandoned&limit=5" \
  -H "Authorization: Bearer seu-token"
```

**Resposta:**
```json
{
  "success": true,
  "recordings": [
    {
      "recordingId": "rec_123",
      "url": "https://clarity.microsoft.com/recordings/...",
      "duration": 240,
      "where": "/checkout"
    }
  ],
  "count": 5,
  "tip": "Assista essas gravações para entender o que usuários experimentam"
}
```

**Como usar:** Clique em cada URL para assistir o vídeo de verdade de um usuário tentando comprar!

---

### 5️⃣ GET `/clarity/feedback` - Feedback dos Usuários

**Para que serve:** Coleta o que usuários realmente pensam (em suas próprias palavras!)

**Exemplo:**
```bash
curl "http://localhost:3001/api/integrations/clarity/feedback?clarityToken=...&projectId=123&dateStart=2024-03-01&dateEnd=2024-03-31" \
  -H "Authorization: Bearer seu-token"
```

**Resposta:**
```json
{
  "success": true,
  "feedback": [
    {
      "comment": "Checkout muito complicado, pedindo muitas informações",
      "sentiment": "negative",
      "page": "/checkout",
      "timestamp": "2024-03-15T10:30:00Z"
    },
    {
      "comment": "Adorei a experiência de compra!",
      "sentiment": "positive",
      "page": "/",
      "timestamp": "2024-03-15T11:00:00Z"
    }
  ],
  "stats": {
    "total": 25,
    "positive": 8,
    "negative": 12,
    "neutral": 5
  }
}
```

**Insight:** 12 comentários negativos sobre checkout vs 8 positivos gerais. Foco = CHECKOUT!

---

### 6️⃣ GET `/clarity/comparison` - Comportamento Conversores vs Abandonadores

**Para que serve:** Compara o que conversores fazem diferente dos que saem

**Exemplo:**
```bash
curl "http://localhost:3001/api/integrations/clarity/comparison?clarityToken=...&projectId=123&dateStart=2024-03-01&dateEnd=2024-03-31" \
  -H "Authorization: Bearer seu-token"
```

**Resposta:**
```json
{
  "success": true,
  "converted": {
    "totalSessions": 500,
    "avgClicks": 8.5,
    "avgScrollDepth": 75,
    "avgTimeSpent": 420,
    "avgPageViews": 4.2
  },
  "abandoned": {
    "totalSessions": 9500,
    "avgClicks": 3.2,
    "avgScrollDepth": 30,
    "avgTimeSpent": 120,
    "avgPageViews": 1.8
  },
  "comparison": {
    "clickDiff": "165.6%",
    "scrollDiff": "150.0%",
    "timeDiff": "250.0%",
    "insight": "Usuários que conversam tendem a..."
  },
  "recommendation": "Replique o comportamento de conversores nos abandonadores"
}
```

**Padrão 🎯:**
| Métrica | Conversores | Abandonadores | Diferença |
|---------|-------------|---------------|-----------|
| Clicks | 8.5 | 3.2 | **166%** ↑ |
| Scroll | 75% | 30% | **150%** ↑ |
| Tempo | 420s | 120s | **250%** ↑ |

**Ação:** Conversores clicam mais, scrollam mais, ficam mais tempo. Que elemento está faltando para abandonadores?

---

## 🔑 Como Obter as Credenciais

### Google Analytics 4

1. Acesse [Google Cloud Console](https://console.cloud.google.com/)
2. Crie um projeto novo
3. Ative a API: `Google Analytics Data API`
4. Crie uma Service Account
5. Baixe o arquivo JSON
6. **`credentialsPath`** = caminho local do arquivo JSON

### Microsoft Clarity

1. Acesse [Clarity](https://clarity.microsoft.com/)
2. Login com sua conta Microsoft
3. Vá em Project Settings
4. Copie o **Project ID**
5. Na seção API, gere um **Auth Token**
6. **`clarityToken`** = seu token
7. **`projectId`** = ID do seu projeto

---

## 💡 Fluxo Recomendado

```
1. POST /ga4/import        → Importa todos os eventos
      ↓
2. GET /ga4/funnel        → Identifica onde estão perdendo
      ↓
3. POST /clarity/import   → Traz dados de comportamento
      ↓
4. GET /clarity/comparison → Compara conversores vs abandonadores
      ↓
5. GET /clarity/recordings → Assiste gravações dos problemas
      ↓
6. Implementa recomendações → Testa mudanças
      ↓
7. Repite processo próximo mês
```

---

## 🐛 Troubleshooting

### ❌ "Missing required fields"
- Verifique se todos os parâmetros foram enviados
- `credentialsPath` ou `clarityToken` são obrigatórios

### ❌ "Failed to authenticate"
- Verifique suas credenciais (arquivo JSON ou token)
- Confirme que credenciais têm as permissões corretas

### ❌ "Empty records"
- Pode não ter dados no período
- Tente expandir o dateStart/dateEnd

---

## 📊 Integração com Dashboard React

**Exemplo de uso no React:**

```tsx
// Buscar dados do GA4
const response = await fetch(
  '/api/integrations/ga4/import',
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      credentialsPath: credentialsPath,
      propertyId: propertyId,
      dateStart: '2024-03-01',
      dateEnd: '2024-03-31'
    })
  }
);

const data = await response.json();
console.log('Eventos importados:', data.eventsImported);
```

---

## ✅ Próximas Etapas

- [ ] Obter credenciais do GA4
- [ ] Obter token do Clarity
- [ ] Testar endpoints localmente
- [ ] Integrar no dashboard React
- [ ] Salvar dados no Supabase
- [ ] Criar visualizações dos dados
