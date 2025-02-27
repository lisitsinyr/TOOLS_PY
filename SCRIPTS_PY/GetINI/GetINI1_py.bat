@echo off
rem -------------------------------------------------------------------
rem GetINI1_py.bat
rem -------------------------------------------------------------------
chcp 1251>NUL

setlocal enabledelayedexpansion

:begin
    set BATNAME=%~nx0
    echo —Ú‡Ú !BATNAME! ...

    set LIB_BAT=D:\PROJECTS_LYR\CHECK_LIST\SCRIPT\BAT\PROJECTS_BAT\TOOLS_SRC_BAT\SRC\LIB
    set PY_ENVDIR=D:\PROJECTS_LYR\CHECK_LIST\DESKTOP\Python\VENV

    set PY_ENVNAME=%PY_ENVNAME%
    if not defined PY_ENVNAME (
        set PY_ENVNAME=P313
    )
    if not exist !PY_ENVDIR!\!PY_ENVNAME! (
        echo INFO: Dir !PY_ENVDIR!\!PY_ENVNAME! not exist ...
        exit /b 1
    )

    set FileINI=%1
    if not defined FileINI (
        echo INFO: FileINI empty ...
        exit /b 1
    )
    set Section=%2
    if not defined Section (
        echo INFO: Section empty ...
        exit /b 1
    )
    set Parameter=%3
    if not defined Parameter (
        echo INFO: Parameter empty ...
        exit /b 1
    )
    
    call :PY_ENV_START || exit /b 1

    rem echo %~dp0
    python %~dp0GetINI.py "!FileINI!" "!Section!" "!Parameter!"

    call :PY_ENV_STOP || exit /b 1

    exit /b 0
:end
rem ===================================================================

rem =================================================
rem ‘”Õ ÷»» LIB
rem =================================================

rem =================================================
rem LYRPY.bat
rem =================================================
:PY_ENV_START
%LIB_BAT%\LYRPY.bat %*
exit /b 0
:PY_ENV_STOP
%LIB_BAT%\LYRPY.bat %*
exit /b 0
rem =================================================
