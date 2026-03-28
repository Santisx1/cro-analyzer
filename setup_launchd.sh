#!/bin/bash

# macOS LaunchD Setup Script
# Configura automação nativa do Mac com launchd

PROJECT_DIR="/Users/kaiofernandes/Desktop/Análise de CRO"
PLIST_FILE="$PROJECT_DIR/com.cro.analyzer.scheduler.plist"
LAUNCH_AGENTS="$HOME/Library/LaunchAgents"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🚀 macOS LaunchD CRO Scheduler Setup${NC}"
echo ""

# Menu
echo "Opções:"
echo "1. Instalar scheduler automático (diário às 2 AM)"
echo "2. Desinstalar scheduler"
echo "3. Ver status"
echo "4. Ver logs"
echo ""
read -p "Escolha (1-4): " choice

case $choice in
    1)
        echo ""
        echo -e "${YELLOW}Instalando LaunchD Agent...${NC}"
        
        # Criar diretório se não existir
        mkdir -p "$LAUNCH_AGENTS"
        
        # Copiar plist
        cp "$PLIST_FILE" "$LAUNCH_AGENTS/"
        
        # Fazer chmod correto
        chmod 644 "$LAUNCH_AGENTS/com.cro.analyzer.scheduler.plist"
        
        # Carregar o agent
        launchctl load "$LAUNCH_AGENTS/com.cro.analyzer.scheduler.plist"
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✅ LaunchD Agent instalado com sucesso!${NC}"
            echo ""
            echo "Detalhes:"
            echo "  • Executará diariamente às 2:00 AM"
            echo "  • Log: $PROJECT_DIR/launchd.log"
            echo "  • Erros: $PROJECT_DIR/launchd_error.log"
            echo ""
            echo "Próximas execuções:"
            echo "  $(date -v+1d '+%Y-%m-%d 02:00:00')"
            echo ""
            echo "Comandos úteis:"
            echo "  launchctl list | grep cro                    # Ver status"
            echo "  launchctl start com.cro.analyzer.scheduler    # Forçar execução agora"
            echo "  tail -f $PROJECT_DIR/launchd.log             # Ver logs"
        else
            echo -e "${RED}❌ Erro ao instalar agent${NC}"
            exit 1
        fi
        ;;
    
    2)
        echo ""
        echo -e "${YELLOW}Desinstalando LaunchD Agent...${NC}"
        
        launchctl unload "$LAUNCH_AGENTS/com.cro.analyzer.scheduler.plist"
        rm "$LAUNCH_AGENTS/com.cro.analyzer.scheduler.plist"
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✅ LaunchD Agent removido com sucesso!${NC}"
        else
            echo -e "${RED}❌ Erro ao desinstalar${NC}"
            exit 1
        fi
        ;;
    
    3)
        echo ""
        echo -e "${BLUE}Status do LaunchD Agent:${NC}"
        echo ""
        if launchctl list | grep -q "com.cro.analyzer.scheduler"; then
            echo -e "${GREEN}✅ Agent instalado e ativo${NC}"
            echo ""
            echo "Informações completas:"
            launchctl list | grep "com.cro.analyzer.scheduler"
        else
            echo -e "${YELLOW}⚠️  Agent não instalado${NC}"
        fi
        ;;
    
    4)
        echo ""
        echo -e "${BLUE}Últimas 30 linhas do log:${NC}"
        echo ""
        if [ -f "$PROJECT_DIR/launchd.log" ]; then
            tail -30 "$PROJECT_DIR/launchd.log"
        else
            echo "Nenhum log encontrado ainda"
        fi
        
        echo ""
        echo -e "${BLUE}Erros (se houver):${NC}"
        echo ""
        if [ -f "$PROJECT_DIR/launchd_error.log" ]; then
            tail -30 "$PROJECT_DIR/launchd_error.log"
        else
            echo "Nenhum erro registrado"
        fi
        ;;
    
    *)
        echo -e "${RED}❌ Opção inválida${NC}"
        exit 1
        ;;
esac

echo ""
