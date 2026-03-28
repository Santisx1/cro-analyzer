#!/bin/bash

# CRO Scheduler Background Runner
# Execute este script para rodar análises automaticamente em background

PROJECT_DIR="/Users/kaiofernandes/Desktop/Análise de CRO"
PYTHON="$PROJECT_DIR/venv/bin/python3"
SCHEDULER="$PROJECT_DIR/scheduler.py"
LOG_FILE="$PROJECT_DIR/scheduler.log"

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 CRO Scheduler — Background Automation${NC}"
echo ""

# Verificar se já está rodando
if pgrep -f "scheduler.py" > /dev/null; then
    echo -e "${YELLOW}⚠️  Scheduler já está em execução!${NC}"
    echo "PID: $(pgrep -f 'scheduler.py')"
    echo ""
    echo "Opções:"
    echo "1. Parar scheduler: ./run_scheduler.sh stop"
    echo "2. Ver logs: tail -f $LOG_FILE"
    exit 0
fi

# Se pediu stop
if [ "$1" = "stop" ]; then
    echo "⏹️  Parando scheduler..."
    pkill -f "scheduler.py"
    echo "✅ Scheduler parado"
    exit 0
fi

# Se pediu logs
if [ "$1" = "logs" ]; then
    echo "📋 Mostrando últimas 50 linhas do log:"
    tail -50 "$LOG_FILE"
    exit 0
fi

echo "📋 Opções de agendamento:"
echo ""
echo "1. Diário às 2 AM (recomendado)"
echo "2. A cada hora"
echo "3. Semanalmente (seg 2 AM)"
echo "4. Rodar uma vez agora"
echo ""
read -p "Escolha (1-4): " choice

echo ""
echo "Iniciando scheduler em background..."
echo "Log: $LOG_FILE"
echo ""

# Rodar em background com nohup
case $choice in
    1)
        nohup $PYTHON $SCHEDULER --daily 2 >> "$LOG_FILE" 2>&1 &
        echo -e "${GREEN}✅ Scheduler iniciado (diário às 2 AM)${NC}"
        ;;
    2)
        nohup $PYTHON $SCHEDULER --hourly >> "$LOG_FILE" 2>&1 &
        echo -e "${GREEN}✅ Scheduler iniciado (a cada hora)${NC}"
        ;;
    3)
        nohup $PYTHON $SCHEDULER --daily 2 >> "$LOG_FILE" 2>&1 &
        echo -e "${GREEN}✅ Scheduler iniciado (semanalmente)${NC}"
        ;;
    4)
        $PYTHON $SCHEDULER --run >> "$LOG_FILE" 2>&1
        echo -e "${GREEN}✅ Análise concluída${NC}"
        ;;
    *)
        echo -e "${RED}❌ Opção inválida${NC}"
        exit 1
        ;;
esac

echo ""
echo "PID: $(pgrep -f 'scheduler.py')"
echo ""
echo "Comandos úteis:"
echo "  ./run_scheduler.sh logs     # Ver logs"
echo "  ./run_scheduler.sh stop     # Parar scheduler"
echo "  tail -f $LOG_FILE           # Monitorar em tempo real"
