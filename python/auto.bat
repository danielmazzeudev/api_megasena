@echo off
echo Iniciando o script Python...
python ./megasena.py

echo.
echo Script finalizado. Iniciando atualizacao no Git...

git add .
git commit -am "Update"
git push

echo.
echo Processo concluido com sucesso!
pause