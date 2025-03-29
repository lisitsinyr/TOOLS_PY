@echo off
rem -------------------------------------------------------------------
rem PATTERN1_PY.bat
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

    rem -------------------------------------------------------------------
    rem SCRIPT - 
    rem -------------------------------------------------------------------
    set SCRIPT_NAME=CLOCK_PY.py

    call :PY_ENV_START || exit /b 1

    set SCRIPT_DIR=.\
    set SCRIPT_DIR=%~dp0
    rem echo SCRIPT_DIR:!SCRIPT_DIR!
    python "!SCRIPT_DIR!!SCRIPT_NAME!"

    call :PY_ENV_STOP || exit /b 1

    rem call :PressAnyKey || exit /b 1

    exit /b 0
:end
rem =================================================

rem =================================================
rem ‘”Õ ÷»» LIB
rem =================================================

rem =================================================
rem LYRPY.bat
rem =================================================
:LYRPY
%LIB_BAT%\LYRPY.bat %*
exit /b 0
:PY_ENV_START
%LIB_BAT%\LYRPY.bat %*
exit /b 0
:PY_ENV_STOP
%LIB_BAT%\LYRPY.bat %*
exit /b 0
