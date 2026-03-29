# 🎯 Google Analytics + Clarity Endpoints - Resumo Técnico

## 📁 Estrutura de Arquivos Criada

```
web/server/
├── integrations/
│   ├── googleAnalytics.js          ← Classe que conecta com GA4
│   └── clarityConnector.js         ← Classe que conecta com Clarity
├── routes/
│   └── integrations.js             ← Todos os 9 endpoints da API
├── middleware/
│   └── auth.js                     ← Verificação de token
└── server.js                       ← (modificado: adicionado import)

web/
├── INTEGRATIONS_GUIDE.md           ← Guia detalhado de uso
├── ENDPOINTS_EXPLAINED.md          ← Explicação clara de cada endpoint
└── REACT_MIGRATION.md              ← Já existia
```

---

## 📊 Endpoints Criados (9 Total)

### Google Analytics 4 (3 endpoints)

| Endpoint | Método | Para Que Serve |
|----------|--------|----------------|
| `/ga4/import` | POST | Importar todos eventos de GA4 |
| `/ga4/funnel` | GET | Rastrear sequência específica de eventos |
| `/ga4/metrics` | GET | Pegar 4 métricas principais de sessão |

### Microsoft Clarity (6 endpoints)

| Endpoint | Método | Para Que Serve |
|----------|--------|----------------|
| `/clarity/import` | POST | Importar tudo de Clarity |
| `/clarity/heatmap` | GET | Ver ONDE usuários clicam |
| `/clarity/pages` | GET | Identificar quais páginas abandonam |
| `/clarity/recordings` | GET | Pegar vídeos de usuários reais |
| `/clarity/feedback` | GET | Coletar comentários dos usuários |
| `/clarity/comparison` | GET | Comparar conversores vs abandonadores |

### Status (1 endpoint)

| Endpoint | Método | Para Que Serve |
|----------|--------|----------------|
| `/health` | GET | Verificar se integração está ok |

---

## 🔑 Como Usar

### Passo 1: Autenticar
Todos os endpoints precisam de token:
```bash
Authorization: Bearer seu-token-aqui
```

### Passo 2: Importar Dados
```javascript
// Trazer tudo de GA4
POST /api/integrations/ga4/import
{
  "credentialsPath": "/path/to/google-creds.json",
  "propertyId": "123456789",
  "dateStart": "2024-03-01",
  "dateEnd": "2024-03-31"
}

// Trazer tudo de Clarity
POST /api/integrations/clarity/import
{
  "clarityToken": "seu-token",
  "projectId": "123456",
  "dateStart": "2024-03-01",
  "dateEnd": "2024-03-31"
}
```

### Passo 3: Analisar Dados Específicos
```javascript
// Ver funil
GET /ga4/funnel?propertyId=123&funnelSteps=page_view,purchase

// Ver heatmap
GET /clarity/heatmap?clarityToken=...&projectId=123

// Comparar comportamento
GET /clarity/comparison?clarityToken=...&projectId=123
```

---

## 🎨 Arquitetura

```
┌─────────────────────────────────────────┐
│         React Dashboard                 │
│   (web/app/dashboard/page.tsx)          │
└────────────┬────────────────────────────┘
             │
             ↓ fetch(/api/integrations/...)
             │
┌─────────────────────────────────────────┐
│       Express API Server                │
│    (web/server/server.js)               │
│                                         │
│  ├─ POST /api/integrations/ga4/import  │
│  ├─ GET  /api/integrations/ga4/funnel  │
│  ├─ POST /api/integrations/clarity/... │
│  └─ GET  /api/integrations/clarity/... │
└────┬──────────┬────────────────────────┘
     │          │
     ↓          ↓
┌─────────┐  ┌──────────┐
│  GA4    │  │ Clarity  │
│  API    │  │   API    │
└─────────┘  └──────────┘
```

---

## 📝 Exemplo Completo

### 1. Usuário clica "Importar Dados"
```javascript
// React component chama:
const response = await fetch('/api/integrations/ga4/import', {
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
});

const data = await response.json();
console.log('Eventos importados:', data.eventsImported);
```

### 2. Backend processa
```javascript
// Em web/server/routes/integrations.js:
// 1. Recebe request com credenciais
// 2. Cria instância de GoogleAnalyticsConnector
// 3. Autentica com Google
// 4. Busca eventos de GA4
// 5. Processa dados
// 6. Retorna resposta JSON
```

### 3. Frontend mostra resultado
```tsx
// Dashboard recebe dados e renderiza:
<KPICard 
  title="Taxa de Conversão"
  value={data.metrics.conversionRate}
  unit="%"
/>
```

---

## 🔐 Segurança

### Autenticação
- ✅ Todos os endpoints verificam `Authorization: Bearer`
- ✅ Arquivo `middleware/auth.js` valida token

### Credenciais Sensíveis
- ✅ Usar variáveis de ambiente (`.env`)
- ✅ NUNCA hardcodear credenciais
- ✅ Google Service Account = arquivo JSON protegido
- ✅ Clarity Token = armazenar como env var

---

## 🚀 Próximos Passos

### Fase 1: Integração Básica (Já Feito)
- ✅ Criar endpoints
- ✅ Documentazione completa
- ✅ Estrutura de código

### Fase 2: Integração com React (Próximo)
- [ ] Adicionar botão "Importar GA4" no dashboard
- [ ] Adicionar botão "Importar Clarity" no dashboard
- [ ] Salvar credenciais no Supabase
- [ ] Mostrar dados importados

### Fase 3: Visualizações (Depois)
- [ ] Gráficos de funil de GA4
- [ ] Mapa de calor visual do Clarity
- [ ] Tabela de páginas por bounce rate
- [ ] Timeline de comparação conversores/abandonadores

### Fase 4: Automação (Long-term)
- [ ] Agendar importação diária
- [ ] Alertas quando métricas caem
- [ ] Relatórios automáticos por email
- [ ] Histórico de mudanças

---

## 📚 Documentações Criadas

1. **INTEGRATIONS_GUIDE.md** (⭐ Recomendado começar aqui)
   - Exemplos de requisição/resposta para cada endpoint
   - Como obter credenciais
   - Troubleshooting

2. **ENDPOINTS_EXPLAINED.md**
   - Para que SERVE cada endpoint
   - Casos de uso reais
   - Como ler as respostas
   - Interpretação de dados

3. **googleAnalytics.js**
   - Classe JavaScript que fala com GA4
   - Métodos reutilizáveis

4. **clarityConnector.js**
   - Classe JavaScript que fala com Clarity
   - Métodos reutilizáveis

5. **integrations.js** (Routes)
   - 9 endpoints Express
   - Documentação em comentários
   - Tratamento de erros

---

## ✅ Checklist

- [x] Criar classe GoogleAnalyticsConnector
- [x] Criar classe ClarityConnector
- [x] Criar 9 endpoints da API
- [x] Adicionar middleware de autenticação
- [x] Documentação completa (2 arquivos)
- [x] Exemplos de requisição
- [x] Integrar routes no server.js
- [ ] Testar endpoints localmente (seu role)
- [ ] Integrar no React Dashboard
- [ ] Salvar dados no Supabase

---

## 🎓 Como Aprender

1. Leia: **ENDPOINTS_EXPLAINED.md**
   - Entender PARA QUE serve cada um

2. Leia: **INTEGRATIONS_GUIDE.md**
   - Ver exemplos reais de uso

3. Execute: Copiar exemplos bash e testar

4. Integre: Conexão no React Dashboard

---

## 🤝 Próxima Conversa

Quando você estiver pronto, podemos:
1. Testar endpoints localmente
2. Integrar no React Dashboard
3. Adicionar salvamento no Supabase
4. Criar visualizações dos dados

**Está pronto?** 🚀
