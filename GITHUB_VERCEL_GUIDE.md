# 🚀 GitHub + Vercel - Guia Completo

Transforme seu projeto local em uma app LIVE na nuvem em 3 passos.

## 📋 Pré-requisitos

- ✅ Conta GitHub (grátis em github.com)
- ✅ Conta Vercel (grátis em vercel.com)
- ✅ Conta Supabase (grátis em supabase.com) - opcional inicialmente

---

## 🎯 Passo 1: Criar Repositório no GitHub

### 1.1 Acesse GitHub
```
Ir para: https://github.com/new
```

### 1.2 Preencha os campos
```
Repository name:        cro-analyzer
Description:            CRO Analysis with Python + Node.js + Vercel
Visibility:             Public ← IMPORTANTE para Vercel
Initialize:             ❌ NÃO marque (vamos fazer localmente)
```

### 1.3 Clique: "Create Repository"

**Resultado:** Você recebe uma URL como:
```
https://github.com/seu-usuario/cro-analyzer.git
```

---

## 🔄 Passo 2: Push Código para GitHub

### 2.1 Clone/Initialize localmente (já feito)
```bash
cd "/Users/kaiofernandes/Desktop/Análise de CRO"

# Já tem git? Se não:
git init
git add .
git commit -m "Initial commit: CRO Analyzer"
```

### 2.2 Conecte ao GitHub
```bash
git remote add origin https://github.com/seu-usuario/cro-analyzer.git
git branch -M main
git push -u origin main
```

### 2.3 Resultado
Seu código agora está no GitHub! Acesse:
```
https://github.com/seu-usuario/cro-analyzer
```

**Você verá:**
- Pasta `web/` com Node.js
- Pasta `src/` com Python
- Pasta `docs/` com documentação
- Todos os arquivos versionados

---

## ☁️ Passo 3: Deploy no Vercel (1-click)

### 3.1 Acesse Vercel
```
Ir para: https://vercel.com/import/git
```

### 3.2 Conecte GitHub
```
Clique: "Continue with GitHub"
├─ GitHub pede autorização
└─ Aprove
```

### 3.3 Selecione seu repositório
```
Procure: "cro-analyzer"
Clique: para selecionar
```

### 3.4 Configure (IMPORTANTE)
```
Root Directory:    ./web    ← Aponte para pasta Node.js!
```

### 3.5 Variáveis de Ambiente
**Copie seu Supabase_URL e ANON_KEY:**

```
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=eyJhbGc...
SUPABASE_SERVICE_KEY=eyJhbGc... (opcional, apenas se usar scheduler)
NODE_ENV=production
```

Se não tem Supabase:
- Criar em: https://supabase.com (grátis)
- Copiar URL e keys
- Voltar aqui e adicionar

### 3.6 Deploy!
```
Clique: "Deploy"
```

**Aguarde 2-3 minutos...**

### 3.7 Resultado
Vercel gera link como:
```
https://cro-analyzer-abc123.vercel.app
```

✅ **Seu app está LIVE na internet!**

---

## 🔄 Depois: Deploy Automático

Toda vez que você fizer push para GitHub, Vercel detecta automaticamente:

```
Local:  git push
   ↓
GitHub: Recebe código
   ↓
Vercel: Detecta mudança
   ↓
Build:  npm install + npm build
   ↓
Deploy: ~1 minuto
   ↓
Live: Seu app atualizado!
```

**Sem fazer nada manualmente!** 🚀

---

## 📝 Fluxo Típico de Desenvolvimento

### Dia a dia:
```bash
# 1. Fazer mudanças nos arquivos localmente
# 2. Testar localmente:
npm run dev

# 3. Commit:
git add .
git commit -m "Adicionar X feature"

# 4. Push:
git push

# 5. Vercel detecta e faz deploy automaticamente
# Resultado: Seu app atualiza em produção em <1 min
```

### Usar no GitHub:
```
Arquivo modificado no VS Code
    ↓
git add . && git commit -m "msg"
    ↓
git push origin main
    ↓
Vercel vê mudança
    ↓
Build + Deploy automático
    ↓
App live com nova versão
```

---

## 🐛 Troubleshooting

### "Erro: Repository not found"
```bash
# Verifique URL:
git remote -v

# Se errada, corrija:
git remote set-url origin https://github.com/seu-usuario/cro-analyzer.git
```

### "Erro: Permission denied"
```bash
# Generate SSH key:
ssh-keygen -t ed25519 -C "seu-email@gmail.com"

# Add to GitHub > Settings > SSH Keys
```

### "Vercel deploy falhando"
```
Verificar:
1. Root Directory está ./web ?
2. package.json existe em web/?
3. Variáveis de ambiente estão corretas?
4. Node version é 18.x?
```

### "Supabase não conecta"
```
1. Verificar .env tem valores corretos
2. Supabase projeto está criado?
3. API key é ANON_KEY (não SERVICE)?
4. Database tabelas foram criadas?
```

---

## 📊 Verificar Status

### GitHub
```
Clicar em: Insights > Commits
Ver histórico de commits
```

### Vercel
```
Ir para: https://vercel.com/dashboard/cro-analyzer
Ver: Deployments
Cada linha é um deploy automático
```

---

## 🎯 Checklist Setup Completo

- [ ] Conta GitHub criada
- [ ] Repositório criado (cro-analyzer)
- [ ] Código feito push (`git push`)
- [ ] Conta Vercel criada
- [ ] Projeto importado no Vercel
- [ ] Variáveis de ambiente configuradas
- [ ] Deploy completado
- [ ] App está LIVE (vercel.app link funciona)
- [ ] Você acessa em http://seu-app.vercel.app
- [ ] Login funciona (Supabase Auth)

---

## 🚀 Seu App Está Live!

Agora você tem:

✅ **Repositório GitHub** - Versionamento de código  
✅ **Vercel Deployment** - App sempre online  
✅ **CI/CD Automático** - Push = Auto deploy  
✅ **Multi-user** - Login + Supabase  
✅ **Domínio Vercel** - URL pública  

**Compartilhável com:**
- Time inteiro
- Clientes
- Stakeholders
- Qualquer um com o link

---

## 🔗 Links

| O Quê | Link |
|-------|------|
| GitHub | https://github.com/seu-usuario/cro-analyzer |
| Vercel | https://vercel.com/dashboard |
| Live App | https://seu-app.vercel.app |
| Supabase | https://app.supabase.com |

---

## 🎓 Próximas Aprimorações

- [ ] Domínio customizado (seu-dominio.com)
- [ ] SSL/TLS automático
- [ ] Analytics no Vercel
- [ ] Edge Functions
- [ ] Database backups automáticos
- [ ] Email notifications
- [ ] Slack webhook

---

## 📞 Suporte

**Problemas?**
- Vercel Docs: https://vercel.com/docs
- GitHub Docs: https://docs.github.com
- Supabase Docs: https://supabase.com/docs

---

**Tudo pronto! Seu CRO Analyzer está LIVE na internet!** 🎉
