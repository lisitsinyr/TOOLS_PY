@echo off
rem -------------------------------------------------------------------
rem 
rem -------------------------------------------------------------------
chcp 1251>NUL

setlocal enabledelayedexpansion

    rem -------------------------------------------------------------------
    rem PROJECTS_LYR_ROOT - Каталог ROOT
    rem -------------------------------------------------------------------
    rem set PROJECTS_LYR_ROOT=D:\WORK\WIN
    set PROJECTS_LYR_ROOT=D:
    rem echo PROJECTS_LYR_ROOT:!PROJECTS_LYR_ROOT!

    rem -------------------------------------------------------------------
    rem PROJECTS_LYR_DIR - Каталог проектов LYR
    rem -------------------------------------------------------------------
    set PROJECTS_LYR_DIR=!PROJECTS_LYR_ROOT!\PROJECTS_LYR
    rem echo PROJECTS_LYR_DIR:!PROJECTS_LYR_DIR!
    if not exist "!PROJECTS_LYR_DIR!"\ (
        rem echo INFO: Dir "!PROJECTS_LYR_DIR!" not exist ...
        rem echo INFO: Create "!PROJECTS_LYR_DIR!" ...
        rem mkdir "!PROJECTS_LYR_DIR!"
        exit /b 1
    )

    rem -------------------------------------------------------------------
    rem SCRIPTS_DIR - Каталог скриптов BAT
    rem -------------------------------------------------------------------
    if not defined SCRIPTS_DIR (
        rem set SCRIPTS_DIR=D:\TOOLS\TOOLS_BAT
        rem set SCRIPTS_DIR=D:\PROJECTS_LYR\CHECK_LIST\SCRIPT\BAT\PROJECTS_BAT\TOOLS_SRC_BAT\SRC
        set SCRIPTS_DIR=!PROJECTS_LYR_DIR!\CHECK_LIST\SCRIPT\BAT\PROJECTS_BAT\TOOLS_SRC_BAT\SRC
    )
    rem echo SCRIPTS_DIR:!SCRIPTS_DIR!

    rem -------------------------------------------------------------------
    rem LIB_BAT - каталог библиотеки скриптов BAT
    rem -------------------------------------------------------------------
    if not defined LIB_BAT (
        set LIB_BAT=!SCRIPTS_DIR!\LIB
    )
    rem echo LIB_BAT:!LIB_BAT!
    if not exist !LIB_BAT!\ (
        echo ERROR: Каталог библиотеки LYR !LIB_BAT! не существует...
        exit /b 1
    )

rem --------------------------------------------------------------------------------
rem 
rem --------------------------------------------------------------------------------
:begin
    set BATNAME=%~nx0
    echo Start !BATNAME! ...

    set DEBUG=
    set /a LOG_FILE_ADD=0

    rem -------------------------------------------------------------------
    rem SCRIPTS_DIR_PY - Каталог скриптов PY
    rem -------------------------------------------------------------------
    if not defined SCRIPTS_DIR_PY (
        set SCRIPTS_DIR_PY=D:\PROJECTS_LYR\CHECK_LIST\DESKTOP\Python\PROJECTS_PY\SCRIPTS_PY\SRC\01.DEPLOY
    )
    rem echo SCRIPTS_DIR_PY:!SCRIPTS_DIR_PY!

    set PY_ENVDIR=D:\PROJECTS_LYR\CHECK_LIST\DESKTOP\Python\VENV
    set PY_ENVNAME=%PY_ENVNAME%
    if not defined PY_ENVNAME (
        set PY_ENVNAME=P313
    )
    if not exist !PY_ENVDIR!\!PY_ENVNAME! (
        echo INFO: Dir !PY_ENVDIR!\!PY_ENVNAME! not exist ...
        exit /b 1
    )

    rem Количество аргументов
    call :Read_N %* || exit /b 1

    call :SET_LIB %0 || exit /b 1

    rem -------------------------------------
    rem OPTION
    rem -------------------------------------
    set OPTION=
    set O1_Name=O1
    set O1_Caption=O1_Caption
    set O1_Default=
    set O1=!O1_Default!
    set PN_CAPTION=!O1_Caption!
    call :Read_P O1 !O1! || exit /b 1
    rem echo O1:!O1!
    if defined O1 (
        set OPTION=!OPTION! -!O1_Name! "!O1!"
    ) else (
        echo INFO: O1 [O1_Name:!O1_Name! O1_Caption:!O1_Caption!] not defined ...
    )
    rem echo OPTION:!OPTION!

    rem -------------------------------------
    rem ARGS
    rem -------------------------------------
    rem Проверка на обязательные аргументы
    set A1=D:\PROJECTS_LYR\CHECK_LIST\OS\UNIX\PROJECTS_UNIX\COMMANDS_SH\SRC\TOOLS
    set PN_CAPTION=Directory
    call :Read_P A1 !A1! || exit /b 1
    echo A1:!A1!
    if defined A1 (
        set ARGS=!ARGS! !A1!
    ) else (
        echo ERROR: A1 not defined ...
        set OK=
    )
    echo ARGS:!ARGS!

    set SCRIPT_DIR=!SCRIPTS_DIR_PY!\LISTDIR
    set SCRIPT_NAME=LISTDIR.py

    call :PY_ENV_START || exit /b 1

    python "!SCRIPT_DIR!"\!SCRIPT_NAME! !OPTION! !ARGS!

    call :PY_ENV_STOP || exit /b 1

    rem call :PressAnyKey || exit /b 1

    exit /b 0
:end
rem --------------------------------------------------------------------------------

rem =================================================
rem ФУНКЦИИ LIB
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

rem =================================================
rem LYRConst.bat
rem =================================================
:SET_LIB
%LIB_BAT%\LYRConst.bat %*
exit /b 0
:SET_KIX
%LIB_BAT%\LYRConst.bat %*
exit /b 0
rem =================================================
rem LYRDateTime.bat
rem =================================================
rem =================================================
rem LYRFileUtils.bat
rem =================================================
rem =================================================
rem LYRLog.bat
rem =================================================
rem =================================================
rem LYRStrUtils.bat
rem =================================================
rem =================================================
rem LYRSupport.bat
rem =================================================
:PressAnyKey
%LIB_BAT%\LYRSupport.bat %*
exit /b 0
:Read_N
%LIB_BAT%\LYRSupport.bat %*
exit /b 0
:Read_P
%LIB_BAT%\LYRSupport.bat %*
exit /b 0
rem =================================================
