#!/bin/bash

# ⚡ Quick Deploy: GitHub + Vercel em 3 passos
# Execute este script para setup interativo

PROJECT_DIR="/Users/kaiofernandes/Desktop/Análise de CRO"
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

clear

cat << "EOF"
╔════════════════════════════════════════════════════════╗
║    🚀 Deploy: GitHub → Vercel (3 passos, 10 min)     ║
╚════════════════════════════════════════════════════════╝

EOF

echo -e "${BLUE}Seu projeto completo precisa ser:${NC}"
echo "  1. Enviado para GitHub (versionamento)"
echo "  2. Importado no Vercel (deploy automático)"
echo ""
echo -e "${YELLOW}Tempo total: ~10 minutos${NC}"
echo ""

# Menu
echo "Escolha:"
echo "  1. 🚀 Setup automático (recomendado)"
echo "  2. 📖 Ver guia detalhado"
echo "  3. ⏭️  Skip (não quer fazer agora)"
echo ""
read -p "Opção (1-3): " choice

case $choice in
    1)
        # Execute setup script
        cd "$PROJECT_DIR"
        ./github-setup.sh
        ;;
    
    2)
        # Show guide
        cat << "EOF"

╔════════════════════════════════════════════════════════╗
║              📖 Guia Passo-a-Passo                    ║
╚════════════════════════════════════════════════════════╝

PASSO 1️⃣  Criar Repo no GitHub (2 min)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Acesse: https://github.com/new
2. Preencha:
   • Name: cro-analyzer
   • Description: CRO Analysis with Python + Node.js
   • Public ← importante
3. Clique: "Create repository"
4. Copie a URL (https://github.com/seu-user/cro-analyzer.git)


PASSO 2️⃣  Push Para GitHub (3 min)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

cd "/Users/kaiofernandes/Desktop/Análise de CRO"

git init
git add .
git commit -m "CRO Analyzer complete"

git remote add origin https://github.com/seu-user/cro-analyzer.git
git branch -M main
git push -u origin main


PASSO 3️⃣  Deploy em Vercel (5 min)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Acesse: https://vercel.com/import/git
2. Clique: "Continue with GitHub"
3. Selecione: cro-analyzer
4. Configure:
   Root Directory: ./web
   Environment Variables:
   - SUPABASE_URL=... (do seu projeto Supabase)
   - SUPABASE_ANON_KEY=...
5. Clique: "Deploy"
6. Aguarde 2 minutos
7. Seu app está LIVE! 🎉


PARA DEPOIS: Deploy automático

Toda vez que fizer:
  git push
Vercel faz deploy automaticamente!


Dúvidas? Veja:
  GITHUB_VERCEL_GUIDE.md (guia completo)

EOF

        read -p "Pressione ENTER para voltar ao menu..."
        ;;
    
    3)
        echo ""
        echo -e "${YELLOW}Sem problemas! Pode fazer depois.${NC}"
        echo ""
        echo "Se mudar de ideia, execute:"
        echo "  ./github-setup.sh"
        echo "ou"
        echo "  ./vercel-deploy.sh"
        echo ""
        ;;
    
    *)
        echo -e "${RED}Opção inválida${NC}"
        ;;
esac
