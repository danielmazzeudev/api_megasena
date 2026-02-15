@echo off

cd /d "C:\Users\danmz\Documents\GitHub\api_megasena\python"

python megasena.py
git add .
git commit -am "Update"
git push

exit