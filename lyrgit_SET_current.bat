@echo off
rem -------------------------------------------------------------------
rem lyrgit_set_current.bat
rem ----------------------------------------------------------------------------"
rem ***SET_current
rem ----------------------------------------------------------------------------"
chcp 1251

:begin
echo ---------------------------------------------------------------
echo git config user.name "lisitsinyr"
echo git config user.email "lisitsinyr@gmail.com"
echo git config --list
echo ---------------------------------------------------------------
git config user.name "lisitsinyr"

git config user.email "lisitsinyr@gmail.com"

git config --list > ./GIT_CONFIG_set_list_current

:Exit
