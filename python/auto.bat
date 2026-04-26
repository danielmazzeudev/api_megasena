@echo off
setlocal

set REPO_DIR=C:\Users\npx\Documents\GitHub\api_megasena
set PYTHON_PATH=C:\Users\npx\AppData\Local\Python\bin\python.exe
set SCRIPT_PATH=%REPO_DIR%\python\megasena.py
set LOG_PATH=%REPO_DIR%\python\auto.log

cd /d "%REPO_DIR%"

echo [%DATE% %TIME%] Iniciando script Python... >> "%LOG_PATH%"

"%PYTHON_PATH%" "%SCRIPT_PATH%" >> "%LOG_PATH%" 2>&1

if %ERRORLEVEL% neq 0 (
    echo [%DATE% %TIME%] Erro: O script Python falhou. Git Push cancelado. >> "%LOG_PATH%"
    exit /b 1
)

echo [%DATE% %TIME%] Python finalizado com sucesso. Iniciando Git Push... >> "%LOG_PATH%"

git add python\megasena.json >> "%LOG_PATH%" 2>&1

git diff --cached --quiet -- python\megasena.json
if %ERRORLEVEL% equ 0 (
    echo [%DATE% %TIME%] Nenhuma mudanca detectada. Pulando push. >> "%LOG_PATH%"
    exit /b 0
)

git commit -m "Auto-commit: atualizacao via script em %DATE% %TIME%" >> "%LOG_PATH%" 2>&1
git push origin main >> "%LOG_PATH%" 2>&1

if %ERRORLEVEL% neq 0 (
    echo [%DATE% %TIME%] Erro no git push. >> "%LOG_PATH%"
    exit /b 1
)

echo [%DATE% %TIME%] Git push concluido com sucesso! >> "%LOG_PATH%"
endlocal
