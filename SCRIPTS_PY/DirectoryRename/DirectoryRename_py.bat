@echo off
rem -------------------------------------------------------------------
rem DirectoryRename.bat
rem -------------------------------------------------------------------
chcp 1251>NUL

setlocal enabledelayedexpansion

:begin
    set BATNAME=%~nx0
    echo Старт !BATNAME! ...

    call D:\PROJECTS_LYR\CHECK_LIST\DESKTOP\Python\VENV\P312\Scripts\activate.bat
    rem echo VIRTUAL_ENV_PROMPT:!VIRTUAL_ENV_PROMPT!
    rem echo PROMPT:!PROMPT!
    rem echo PYTHONHOME:!PYTHONHOME!
    rem echo PATH:!PATH!

    rem echo %~dp0
    python "%~dp0FindDirectory.py" "%1" "%2" "%3"

    call D:\PROJECTS_LYR\CHECK_LIST\DESKTOP\Python\VENV\P312\Scripts\deactivate.bat
    rem echo VIRTUAL_ENV_PROMPT:!VIRTUAL_ENV_PROMPT!
    rem echo PROMPT:!PROMPT!
    rem echo PYTHONHOME:!PYTHONHOME!
    rem echo PATH:!PATH!

    exit /b 0
:end
rem ===================================================================
