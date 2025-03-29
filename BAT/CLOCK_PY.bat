@echo off
rem -------------------------------------------------------------------
rem PATTERN1_PY.bat
rem -------------------------------------------------------------------
chcp 1251>NUL

setlocal enabledelayedexpansion

:begin
    set BATNAME=%~nx0
    echo Старт !BATNAME! ...

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
    rem TEST - 
    rem -------------------------------------------------------------------
    set TEST=
    rem -------------------------------------------------------------------
    rem SCRIPT_NAME - 
    rem -------------------------------------------------------------------
    set SCRIPT_NAME=CLOCK
    rem -------------------------------------------------------------------
    rem SCRIPT_DIR - 
    rem -------------------------------------------------------------------
    set SCRIPT_DIR=!SCRIPT_NAME!
    rem -------------------------------------------------------------------
    rem SCRIPTS_DIR_PY - Каталог скриптов PY
    rem -------------------------------------------------------------------
    if not defined SCRIPTS_DIR_PY (
        set SCRIPTS_DIR_PY=D:\PROJECTS_LYR\CHECK_LIST\DESKTOP\Python\PROJECTS_PY\SCRIPTS_PY\SRC\SCRIPTS_PY
    )
    set FULL_SCRIPT_NAME=!SCRIPTS_DIR_PY!\!SCRIPT_DIR!\!SCRIPT_NAME!.py
    if defined TEST (
        set FULL_SCRIPT_NAME=.\!SCRIPT_NAME!.py
    )

    call :PY_ENV_START || exit /b 1

    python "!FULL_SCRIPT_NAME!" !OPTION! !ARGS!

    call :PY_ENV_STOP || exit /b 1

    rem call :PressAnyKey || exit /b 1

    exit /b 0
:end
rem =================================================

rem =================================================
rem ФУНКЦИИ LIB
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
