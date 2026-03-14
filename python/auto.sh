#!/bin/bash

# 1. Configurações de caminhos (Use caminhos absolutos)
REPO_DIR="/home/lumni/Documents/GitHub/api_megasena"
PYTHON_PATH="/usr/bin/python3"
SCRIPT_PATH="$REPO_DIR/python/megasena.py"

# Entra na pasta do repositório (CRUCIAL para o Git funcionar)
cd "$REPO_DIR" || exit

echo "Iniciando script Python em $(date)..."

# 2. Executa o Python
# O && garante que o Git só rode se o Python retornar código 0 (sem erros)
$PYTHON_PATH $SCRIPT_PATH && {
    echo "Python finalizado com sucesso. Iniciando Git Push..."
    
    # 3. Comandos do Git
    # Removido o 'git init' pois o repo já existe
    git add .
    
    # O commit só acontece se houver mudanças reais (evita erro de 'nothing to commit')
    if git diff-index --quiet HEAD --; then
        echo "Nenhuma mudança detectada nos arquivos. Pulando push."
    else
        git commit -m "Auto-commit: atualização via script em $(date)"
        git push origin main
        echo "Git push concluído com sucesso!"
    fi
} || {
    echo "Erro: O script Python falhou ou foi interrompido. Git Push cancelado."
    exit 1
}