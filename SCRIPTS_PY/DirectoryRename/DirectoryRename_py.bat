@echo off
rem -------------------------------------------------------------------
rem DirectoryRename.bat
rem -------------------------------------------------------------------
chcp 1251>NUL

setlocal enabledelayedexpansion

:begin
    set BATNAME=%~nx0
    echo Старт !BATNAME! ...


    rem -------------------------------------------------------------------
    rem SCRIPTS_DIR_PY - Каталог скриптов PY
    rem -------------------------------------------------------------------
    if not defined SCRIPTS_DIR_PY (
        set SCRIPTS_DIR_PY=D:\PROJECTS_LYR\CHECK_LIST\DESKTOP\Python\PROJECTS_PY\SCRIPTS_PY\SRC\SCRIPTS_PY
    )
    rem echo SCRIPTS_DIR_PY:!SCRIPTS_DIR_PY!
    rem -------------------------------------------------------------------
    rem SCRIPT_NAME - 
    rem -------------------------------------------------------------------
    set SCRIPT_NAME=DirectoryRename.py
    rem -------------------------------------------------------------------
    rem SCRIPT_DIR - 
    rem -------------------------------------------------------------------
    set SCRIPT_DIR=DirectoryRename

    call D:\PROJECTS_LYR\CHECK_LIST\DESKTOP\Python\VENV\P312\Scripts\activate.bat
    rem echo VIRTUAL_ENV_PROMPT:!VIRTUAL_ENV_PROMPT!
    rem echo PROMPT:!PROMPT!
    rem echo PYTHONHOME:!PYTHONHOME!
    rem echo PATH:!PATH!

    rem python "%~dp0FindDirectory.py" "%1" "%2" "%3"
    python "!SCRIPTS_DIR_PY!\!SCRIPT_DIR!\!SCRIPT_NAME!" "%1" "%2" "%3"

    call D:\PROJECTS_LYR\CHECK_LIST\DESKTOP\Python\VENV\P312\Scripts\deactivate.bat
    rem echo VIRTUAL_ENV_PROMPT:!VIRTUAL_ENV_PROMPT!
    rem echo PROMPT:!PROMPT!
    rem echo PYTHONHOME:!PYTHONHOME!
    rem echo PATH:!PATH!

    exit /b 0
:end
rem ===================================================================
