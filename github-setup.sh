#!/bin/bash

# 🚀 Setup Git + GitHub + Vercel
# Deploy seu CRO Analyzer em minutos

PROJECT_DIR="/Users/kaiofernandes/Desktop/Análise de CRO"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

clear

echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  🚀 GitHub + Vercel Deploy Setup      ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo ""

# Step 1: Initialize Git locally
echo -e "${CYAN}Step 1️⃣  Inicializando Git localmente...${NC}"
echo ""

cd "$PROJECT_DIR"

# Initialize git
git init

# Add all files
git add .

# Initial commit
git commit -m "🚀 CRO Analyzer - Python + Node.js + Vercel

- Full CRO analysis system with Python backend
- Node.js + Express API with Supabase integration
- Modern dashboard with authentication
- Ready for Vercel deployment
- Automated scheduler for daily analysis"

# Create main branch
git branch -M main

echo -e "${GREEN}✅ Git inicializado localmente!${NC}"
echo ""
echo "Repository files:"
git log --oneline -1
echo ""

# Step 2: GitHub instructions
echo -e "${CYAN}Step 2️⃣  Criar repositório no GitHub...${NC}"
echo ""
echo -e "${YELLOW}⚠️  Faça isso MANUALMENTE (leva 1 minuto):${NC}"
echo ""
echo "  1. Visite: https://github.com/new"
echo "  2. Preencha:"
echo "     • Repository name: cro-analyzer"
echo "     • Description: CRO Analysis with Python + Node.js + Vercel"
echo "     • Visibility: Public (para deploy fácil)"
echo "     • NÃO inicie com README"
echo ""
echo "  3. Clique: Create repository"
echo ""

read -p "Pressione ENTER quando terminar de criar a repo no GitHub..."

# Step 3: Add remote and push
echo ""
echo -e "${CYAN}Step 3️⃣  Conectar ao GitHub e fazer Push...${NC}"
echo ""

read -p "Cole sua URL GitHub (https://github.com/seu-usuario/cro-analyzer.git): " github_url

if [ -z "$github_url" ]; then
    echo -e "${RED}❌ URL vazia!${NC}"
    exit 1
fi

# Add remote
git remote add origin "$github_url"

# Push to GitHub
echo ""
echo "📤 Fazendo push para GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Push concluído!${NC}"
    echo ""
    echo "Repository online em:"
    echo -e "${BLUE}$github_url${NC}"
else
    echo -e "${RED}❌ Erro no push. Verifique a URL e tente novamente.${NC}"
    exit 1
fi

# Step 4: Vercel deployment
echo ""
echo -e "${CYAN}Step 4️⃣  Deploy no Vercel (2 minutos)...${NC}"
echo ""

echo -e "${YELLOW}⚠️  Faça isso MANUALMENTE:${NC}"
echo ""
echo "  1. Visite: https://vercel.com/import/git"
echo "  2. Clique: 'Connect Git Repository'"
echo "  3. Selecione: cro-analyzer"
echo "  4. Clique: Import"
echo ""
echo "  5. Configure Environment Variables:"
echo "     • SUPABASE_URL: [valor do seu Supabase]"
echo "     • SUPABASE_ANON_KEY: [valor do seu Supabase]"
echo "     • SUPABASE_SERVICE_KEY: [valor do seu Supabase]"
echo ""
echo "     📌 Se não tem Supabase ainda, veja: web/DEPLOY.md"
echo ""
echo "  6. Clique: Deploy"
echo "  7. Aguarde ~2 minutos"
echo "  8. Acesse o link gerado!"
echo ""

echo -e "${GREEN}✨ Pronto! Seu app estará live em alguns minutos!${NC}"
echo ""

echo -e "${CYAN}═══════════════════════════════════════${NC}"
echo -e "${CYAN}  📋 Próximas Vezes (Deploy automático)${NC}"
echo -e "${CYAN}═══════════════════════════════════════${NC}"
echo ""
echo "Depois de hoje, deploy é AUTOMÁTICO:"
echo ""
echo "  1. Faça mudanças localmente"
echo "  2. Commit:"
echo ""
echo -e "     ${BLUE}git add .${NC}"
echo -e "     ${BLUE}git commit -m 'Descrição da mudança'${NC}"
echo -e "     ${BLUE}git push${NC}"
echo ""
echo "  3. Vercel detecta automaticamente e faz deploy"
echo "  4. Seu app updatea em <1 minuto 🚀"
echo ""

echo -e "${CYAN}═══════════════════════════════════════${NC}"
echo -e "${CYAN}  🔗 Links Úteis${NC}"
echo -e "${CYAN}═══════════════════════════════════════${NC}"
echo ""
echo "  GitHub: $github_url"
echo "  Vercel: https://vercel.com/dashboard"
echo "  Supabase: https://app.supabase.com"
echo ""
echo "  Deploy Docs: web/DEPLOY.md"
echo "  Tech Docs: web/README.md"
echo ""

# Save info
cat > ".github-vercel-info.txt" << EOF
GitHub Repository: $github_url
Created: $(date)

Deploy Steps Completed:
✅ 1. Git initialized locally
✅ 2. Initial commit
✅ 3. Pushed to GitHub

Next:
⏳ 1. Create Supabase project (if needed)
⏳ 2. Import into Vercel via GitHub
⏳ 3. Add environment variables
⏳ 4. Deploy!
EOF

echo -e "${GREEN}✅ Setup completado!${NC}"
echo ""
