@echo off
rem -------------------------------------------------------------------
rem lyrgit_set_system.bat
rem ----------------------------------------------------------------------------
rem ***SET_system
rem ----------------------------------------------------------------------------
chcp 1251

:begin
echo ---------------------------------------------------------------
echo config --system user.name "lisitsinyr"
echo config --system user.email "lisitsinyr@gmail.com"
echo git config --list --system
echo ---------------------------------------------------------------
git config --system user.name "lisitsinyr"

git config --system user.email "lisitsinyr@gmail.com"

git config --list --system > ./GIT_CONFIG_set_list_system

:Exit
