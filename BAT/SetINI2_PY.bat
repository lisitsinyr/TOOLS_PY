@echo off
rem -------------------------------------------------------------------
rem SetINI2_PY.bat
rem -------------------------------------------------------------------
chcp 1251>NUL

setlocal enabledelayedexpansion

rem -------------------------------------------------------------------
rem SCRIPTS_DIR - Каталог скриптов
rem -------------------------------------------------------------------
if not defined SCRIPTS_DIR (
    set SCRIPTS_DIR=D:\PROJECTS_LYR\CHECK_LIST\SCRIPT\BAT\PROJECTS_BAT\TOOLS_SRC_BAT
)
rem -------------------------------------------------------------------
rem LIB_BAT - каталог библиотеки скриптов
rem -------------------------------------------------------------------
set LIB_BAT=!SCRIPTS_DIR!\SRC\LIB
rem -------------------------------------------------------------------
rem SCRIPTS_DIR_PY - Каталог скриптов PY
rem -------------------------------------------------------------------
if not defined SCRIPTS_DIR_PY (
    rem set SCRIPTS_DIR_PY=D:\PROJECTS_LYR\CHECK_LIST\DESKTOP\Python\PROJECTS_PY\TOOLS_SRC_PY
    set SCRIPTS_DIR_PY=D:\PROJECTS_LYR\CHECK_LIST\DESKTOP\Python\PROJECTS_PY\SCRIPTS_PY
)
rem echo SCRIPTS_DIR_PY:!SCRIPTS_DIR_PY!

rem --------------------------------------------------------------------------------
rem 
rem --------------------------------------------------------------------------------
:begin
    set BATNAME=%~nx0
    echo Start !BATNAME! ...

    set DEBUG=
    set /a LOG_FILE_ADD=0

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

    rem Количество аргументов
    call :Read_N %* || exit /b 1

    call :SET_LIB %0 || exit /b 1

    call :CurrentDir
    rem echo CurrentDir:!CurrentDir!

    rem -------------------------------------
    rem OPTION
    rem -------------------------------------
    set OPTION=

    set O1_Name=O1
    set O1_Caption=O1_Caption
    set O1_Default=O1_Default
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
    set ARGS=

    set A1_Name=FileINI
    set A1_Caption=FileINI
    set A1_Default=%1
    set A1=!A1_Default!
    set PN_CAPTION=!A1_Caption!
    call :Read_P A1 !A1! || exit /b 1
    rem echo A1:!A1!
    if defined A1 (
        set ARGS=!ARGS! "!A1!"
    ) else (
        echo ERROR: A1 [A1_Name:!A1_Name! A1_Caption:!A1_Caption!] not defined ... 
        set OK=
        rem exit /b 1
    )

    set A2_Name=Section
    set A2_Caption=Section
    set A2_Default=%2
    set A2=!A1_Default!
    set PN_CAPTION=!A2_Caption!
    call :Read_P A2 !A2! || exit /b 1
    rem echo A2:!A2!
    if defined A2 (
        set ARGS=!ARGS! "!A2!"
    ) else (
        echo ERROR: A2 [A2_Name:!A2_Name! A2_Caption:!A2_Caption!] not defined ... 
        set OK=
        rem exit /b 1
    )

    set A3_Name=Parameter
    set A3_Caption=Parameter
    set A3_Default=%3
    set A3=!A3_Default!
    set PN_CAPTION=!A3_Caption!
    call :Read_P A3 !A3! || exit /b 1
    rem echo A3:!A3!
    if defined A3 (
        set ARGS=!ARGS! "!A3!"
    ) else (
        echo ERROR: A3 [A3_Name:!A3_Name! A3_Caption:!A3_Caption!] not defined ... 
        set OK=
        rem exit /b 1
    )

    set A4_Name=Value
    set A4_Caption=Value
    set A4_Default=%4
    set A4=!A4_Default!
    set PN_CAPTION=!A4_Caption!
    call :Read_P A4 "!A4!" || exit /b 1
    rem echo A4:!A4!
    if defined A4 (
        set ARGS=!ARGS! "!A4!"
    ) else (
        echo ERROR: A4 [A4_Name:!A4_Name! A4_Caption:!A4_Caption!] not defined ... 
        set OK=
        rem exit /b 1
    )

    rem echo ARGS:!ARGS!

    call :PY_ENV_START || exit /b 1

    python "!SCRIPTS_DIR_PY!"\SRC\SetINI\SetINI.py !OPTION! !ARGS!

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
:CurrentDir
%LIB_BAT%\LYRFileUtils.bat %*
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
