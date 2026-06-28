#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
PYTHON_PATH="$(command -v python3)"
SCRIPT_PATH="$SCRIPT_DIR/megasena.py"
LOG_PATH="$SCRIPT_DIR/auto.log"

export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
export HOME="${HOME:-/home/daniel}"

cd "$REPO_DIR" || exit 1

echo "=== Iniciando em $(date '+%Y-%m-%d %H:%M:%S') ===" >> "$LOG_PATH"

if "$PYTHON_PATH" "$SCRIPT_PATH" >> "$LOG_PATH" 2>&1; then
    echo "Python finalizado com sucesso. Verificando alteracoes no Git..." >> "$LOG_PATH"

    git add python/megasena.json

    if git diff --cached --quiet -- python/megasena.json; then
        echo "Nenhuma mudanca detectada. Push ignorado." >> "$LOG_PATH"
    else
        git commit -m "Auto-commit: atualizacao via script em $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_PATH" 2>&1
        git push origin main >> "$LOG_PATH" 2>&1
        echo "Git push concluido com sucesso." >> "$LOG_PATH"
    fi
else
    echo "Erro: script Python falhou. Git push cancelado." >> "$LOG_PATH"
    exit 1
fi

echo "=== Finalizado em $(date '+%Y-%m-%d %H:%M:%S') ===" >> "$LOG_PATH"
