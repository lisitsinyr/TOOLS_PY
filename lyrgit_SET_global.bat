@echo off
rem -------------------------------------------------------------------
rem lyrgit_set_global.bat
rem ----------------------------------------------------------------------------
rem ***SET_global
rem ----------------------------------------------------------------------------
chcp 1251

:begin
echo ---------------------------------------------------------------
echo git config --global init.defaultBranch main
echo git config --global user.name "lisitsinyr"
echo git config --global user.email "lisitsinyr@gmail.com"
echo git config --list
echo ---------------------------------------------------------------
git config --global init.defaultBranch main

git config --global user.name "lisitsinyr"

git config --global user.email "lisitsinyr@gmail.com"

git config --list --global > ./GIT_CONFIG_set_list_global

:Exit
