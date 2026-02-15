@echo off

cd /d "C:\Users\danmz\Documents\GitHub\api_megasena\python"

echo Iniciando o script Python em: %cd%
python megasena.py

echo.
echo Script finalizado. Iniciando atualizacao no Git...

git add .
git commit -am "Update"
git push

echo.
echo Processo concluido!
pause