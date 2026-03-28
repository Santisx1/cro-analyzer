#!/bin/bash

# Setup script for CRO Analysis Tool
# This script automates the initial setup

set -e

echo "🚀 CRO Analysis Tool - Setup Script"
echo "===================================="
echo ""

# Check Python version
echo "📍 Verificando Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo "✅ Python $PYTHON_VERSION encontrado"
else
    echo "❌ Python 3 não encontrado. Por favor, instale Python 3.8 ou superior."
    exit 1
fi

# Create virtual environment
echo ""
echo "📍 Criando ambiente virtual..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Ambiente virtual criado"
else
    echo "⚠️  Ambiente virtual já existe"
fi

# Activate virtual environment
echo ""
echo "📍 Ativando ambiente virtual..."
source venv/bin/activate
echo "✅ Ambiente virtual ativado"

# Upgrade pip
echo ""
echo "📍 Atualizando pip..."
pip install --upgrade pip > /dev/null 2>&1
echo "✅ pip atualizado"

# Install dependencies
echo ""
echo "📍 Instalando dependências..."
pip install -r requirements.txt > /dev/null 2>&1
echo "✅ Dependências instaladas"

# Copy environment template
echo ""
echo "📍 Configurando variáveis de ambiente..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✅ Arquivo .env criado (edite com suas credenciais)"
else
    echo "⚠️  Arquivo .env já existe"
fi

# Run tests
echo ""
echo "📍 Executando testes..."
if python3 -m pytest tests/ -q 2>/dev/null; then
    echo "✅ Testes passaram"
else
    echo "⚠️  Alguns testes podem ter falhado (ignorando para prosseguir)"
fi

# Test import
echo ""
echo "📍 Testando importações..."
if python3 -c "from src.analyzer import CROAnalyzer; print('✅ Importações OK')" 2>/dev/null; then
    echo "✅ Módulos importados com sucesso"
else
    echo "❌ Erro ao importar módulos"
    exit 1
fi

echo ""
echo "===================================="
echo "✅ Setup concluído com sucesso!"
echo "===================================="
echo ""
echo "🚀 Próximos passos:"
echo "   1. Edite o arquivo .env com suas credenciais"
echo "   2. Configure seus dados em examples/sample_data.csv"
echo "   3. Execute: python3 main.py"
echo ""
echo "📚 Documentação: README.md"
echo ""
