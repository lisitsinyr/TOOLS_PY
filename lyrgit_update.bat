@echo off
rem -------------------------------------------------------------------
rem lyrgit_update.bat
rem -------------------------------------------------------------------
chcp 1251

:begin
git add --all
git commit -m "Git Bash commit update"

git push -u origin main

:Exit
