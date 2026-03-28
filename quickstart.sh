#!/bin/bash

# 🚀 Setup Quick Start para CRO Analyzer
# Execute este script para escolher qual versão usar

PROJECT_DIR="/Users/kaiofernandes/Desktop/Análise de CRO"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

clear

echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  🚀 CRO Analyzer - Quick Start Setup   ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo ""
echo -e "${CYAN}Bem-vindo! Escolha como quer rodar seu CRO Analyzer:${NC}"
echo ""
echo -e "  ${GREEN}1. 🖥️  Python Local${NC}"
echo -e "     Rodar no seu Mac, offline, grátis"
echo -e "     ✅ $0 custo  ❌ Manual 24/7"
echo ""
echo -e "  ${GREEN}2. ☁️  Node.js + Vercel (Recomendado)${NC}"
echo -e "     Cloud automático, compartilhado, multi-user"
echo -e "     ✅ 99.95% uptime  ✅ $0-20/mês"
echo ""
echo -e "  ${GREEN}3. 🔗 Ambos (Best of Both Worlds)${NC}"
echo -e "     Python local + Cloud dashboard"
echo -e "     ✅ Máxima flexibilidade"
echo ""
echo -e "  ${GREEN}4. 📖 Ver documentação${NC}"
echo -e "     Detalhes sobre cada opção"
echo ""
read -p "Escolha (1-4): " choice

case $choice in
    1)
        echo ""
        echo -e "${CYAN}═══════════════════════════════════════${NC}"
        echo -e "${CYAN}  🖥️  Setup Python Local${NC}"
        echo -e "${CYAN}═══════════════════════════════════════${NC}"
        echo ""
        
        echo "📋 Checklist:"
        echo "  ✓ Python 3.9 instalado"
        echo "  ✓ Virtual environment ativado"
        echo "  ✓ Dependencies instaladas"
        echo ""
        
        echo "🔧 Próximos passos:"
        echo ""
        echo "  1. Automação Local (24h rodando seu Mac):"
        echo ""
        echo -e "    ${GREEN}cd \"$PROJECT_DIR\"${NC}"
        echo -e "    ${GREEN}./run_scheduler.sh${NC}"
        echo "    └─ Escolha: Diário às 2 AM"
        echo ""
        
        echo "  2. OU LaunchD (macOS native, mais elegante):"
        echo ""
        echo -e "    ${GREEN}./setup_launchd.sh${NC}"
        echo "    └─ Escolha: Opção 1 para instalar"
        echo ""
        
        echo "  3. Monitor logs:"
        echo ""
        echo -e "    ${GREEN}tail -f scheduler.log${NC}"
        echo ""
        
        echo -e "${GREEN}✅ Pronto! Seu Mac rodará análises todos os dias 🌙${NC}"
        echo ""
        ;;
        
    2)
        echo ""
        echo -e "${CYAN}═══════════════════════════════════════${NC}"
        echo -e "${CYAN}  ☁️  Setup Node.js + Vercel${NC}"
        echo -e "${CYAN}═══════════════════════════════════════${NC}"
        echo ""
        
        echo "📋 Pré-requisitos:"
        echo "  ✓ Conta GitHub"
        echo "  ✓ Conta Vercel (grátis)"
        echo "  ✓ Conta Supabase (grátis)"
        echo ""
        
        echo -e "${YELLOW}⏱️  Tempo total: ~5 minutos${NC}"
        echo ""
        
        echo "Step 1️⃣  Supabase Setup (2 min)"
        echo "  a) Visite: https://supabase.com"
        echo "  b) Crie novo projeto FREE TIER"
        echo "  c) Copie URL e API Key"
        echo "  d) Cole em: web/.env"
        echo ""
        
        echo "Step 2️⃣  Deploy (1 min)"
        echo "  a) npm install -g vercel"
        echo "  b) vercel login"
        echo "  c) cd web && vercel --prod"
        echo ""
        
        echo "Step 3️⃣  Configure variáveis no Vercel"
        echo "  a) Vá em Vercel > Project Settings"
        echo "  b) Environment Variables"
        echo "  c) Cole SUPABASE_URL e SUPABASE_ANON_KEY"
        echo ""
        
        echo "Step 4️⃣  Pronto! Seu app está LIVE 🎉"
        echo "  a) Link: https://seu-projeto.vercel.app"
        echo "  b) Compartilhe com time"
        echo "  c) Multi-user login automático"
        echo ""
        
        echo -e "${GREEN}Commands rápidos:${NC}"
        echo ""
        echo "  cd web"
        echo "  npm install"
        echo "  npm run dev              # Test localmente"
        echo "  vercel --prod            # Deploy"
        echo ""
        
        echo -e "📖 Veja: ${CYAN}./web/DEPLOY.md${NC} para guia detalhado"
        echo ""
        ;;
        
    3)
        echo ""
        echo -e "${CYAN}═══════════════════════════════════════${NC}"
        echo -e "${CYAN}  🔗 Setup Ambos (Recomendado!)${NC}"
        echo -e "${CYAN}═══════════════════════════════════════${NC}"
        echo ""
        
        echo "Melhor de ambos os mundos:"
        echo "  ✅ Python roda no Mac (análises locais)"
        echo "  ✅ Node.js em Vercel (dashboard web)"
        echo "  ✅ Supabase conecta os dois"
        echo "  ✅ Team vê resultados em tempo real"
        echo ""
        
        echo "Arquitetura:"
        echo ""
        echo "  Mac (Python) --publish--> Supabase"
        echo "      análise             database"
        echo "                             ↓"
        echo "                      Vercel (Node.js)"
        echo "                      dashboard + auth"
        echo ""
        
        echo "Setup:"
        echo ""
        echo "  1. Primeiro: Setup Supabase (como opção 2)"
        echo "  2. Depois: Deploy Node.js (como opção 2)"
        echo "  3. Python publica para Supabase automaticamente"
        echo "  4. Node.js lê de Supabase"
        echo "  5. Done! 🎉"
        echo ""
        
        echo -e "${GREEN}Commands:${NC}"
        echo ""
        echo "  # Setup Supabase + Deploy Vercel"
        echo "  cd web && npm install"
        echo "  vercel --prod"
        echo ""
        echo "  # Python publica para Supabase"
        echo "  cd .. && ./run_scheduler.sh"
        echo "  (escolha: Diário)"
        echo ""
        
        echo -e "📖 Veja: ${CYAN}./VERSOES.md${NC} para arquitetura completa"
        echo ""
        ;;
        
    4)
        echo ""
        echo -e "${CYAN}═══════════════════════════════════════${NC}"
        echo -e "${CYAN}  📖 Documentação Completa${NC}"
        echo -e "${CYAN}═══════════════════════════════════════${NC}"
        echo ""
        
        echo "📚 Arquivos de Documentação:"
        echo ""
        echo "  Principal:"
        echo "    • VERSOES.md ........... Comparação Python vs Node.js"
        echo "    • README.md ........... Documentação geral"
        echo ""
        echo "  Python:"
        echo "    • docs/AUTOMACAO.md ... Setup automação"
        echo "    • docs/SUPABASE_SETUP.md ... Integração cloud"
        echo ""
        echo "  Node.js:"
        echo "    • web/README.md ....... Setup Node.js"
        echo "    • web/DEPLOY.md ....... Deploy Vercel"
        echo "    • web/.env.example .... Variables template"
        echo ""
        echo "  Ferramentas:"
        echo "    • debug_scheduler.py .. Monitor scheduler"
        echo "    • run_scheduler.sh .... Rodar automação"
        echo "    • setup_launchd.sh .... macOS automação"
        echo ""
        
        echo -e "${GREEN}Abrir documentação:${NC}"
        echo ""
        echo "  Open all:"
        echo "    open VERSOES.md"
        echo "    open web/DEPLOY.md"
        echo "    open docs/AUTOMACAO.md"
        echo ""
        ;;
        
    *)
        echo -e "${RED}❌ Opção inválida${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${CYAN}═══════════════════════════════════════${NC}"
echo -e "${CYAN}  Precisa de ajuda?${NC}"
echo -e "${CYAN}═══════════════════════════════════════${NC}"
echo ""
echo "  Verificar ambiente:"
echo "    python3 debug_scheduler.py --check"
echo ""
echo "  Ver logs:"
echo "    python3 debug_scheduler.py --logs"
echo ""
echo "  Rodar análise manual:"
echo "    python3 debug_scheduler.py --run"
echo ""
echo "  Ou execute este script novamente:"
echo "    ./quickstart.sh"
echo ""

echo -e "${GREEN}✨ Bom trabalho! Você consegue!${NC}"
echo ""
