@echo off
rem -------------------------------------------------------------------
rem lyrgit_create_exists_TOOS_GIT.bat
rem -------------------------------------------------------------------
chcp 1251

:begin
git add --all

git commit -m "Git Bash commit update"

rem git remote add origin https://github.com/lisitsinyr/TOOLS_PY.git
git remote add origin git@github.com:lisitsinyr/TOOLS_PY.git

git branch -M main

git push -u origin main

:Exit
