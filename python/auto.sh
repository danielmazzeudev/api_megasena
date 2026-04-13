#!/usr/bin/env bash

set -euo pipefail

REPO_DIR="/home/danielmazzeu/Documents/Github/api_megasena"
PYTHON_PATH="/usr/bin/python3"
SCRIPT_PATH="$REPO_DIR/python/megasena.py"
LOG_PATH="$REPO_DIR/python/auto.log"

cd "$REPO_DIR" || exit

echo "Iniciando script Python em $(date)..." >> "$LOG_PATH"

"$PYTHON_PATH" "$SCRIPT_PATH" >> "$LOG_PATH" 2>&1 && {
    echo "Python finalizado com sucesso. Iniciando Git Push..." >> "$LOG_PATH"

    git add python/megasena.json
    
    if git diff --cached --quiet -- python/megasena.json; then
        echo "Nenhuma mudança detectada nos arquivos. Pulando push." >> "$LOG_PATH"
    else
        git commit -m "Auto-commit: atualização via script em $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_PATH" 2>&1
        git push origin main >> "$LOG_PATH" 2>&1
        echo "Git push concluído com sucesso!" >> "$LOG_PATH"
    fi
} || {
    echo "Erro: O script Python falhou ou foi interrompido. Git Push cancelado." >> "$LOG_PATH"
    exit 1
}
