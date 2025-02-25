@echo off
rem -------------------------------------------------------------------
rem ftFormatTXT.bat
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

    set O1_Name=fp
    set O1_Caption=FilePath
    set O1_Default=%1
    set O1=!O1_Default!
    set PN_CAPTION=!O1_Caption!
    call :Read_P O1 !O1! || exit /b 1
    rem echo O1:!O1!
    if defined O1 (
        set OPTION=!OPTION! -!O1_Name! "!O1!"
    ) else (
        echo INFO: O1 [O1_Name:!O1_Name! O1_Caption:!O1_Caption!] not defined ...
    )
    
    set O2_Name=fm
    set O2_Caption=FileMask
    set O2_Default=%2
    set O2=!O2_Default!
    set PN_CAPTION=!O2_Caption!
    call :Read_P O2 !O2! || exit /b 1
    rem echo O2:!O2!
    if defined O2 (
        set OPTION=!OPTION! -!O2_Name! "!O2!"
    ) else (
        echo INFO: O2 [O2_Name:!O2_Name! O2_Caption:!O2_Caption!] not defined ...
    )

    set O3_Name=w
    set O3_Caption=width
    set O3_Default=%3
    set O3=!O3_Default!
    set PN_CAPTION=!O3_Caption!
    call :Read_P O3 !O3! || exit /b 1
    rem echo O3:!O3!
    if defined O3 (
        set OPTION=!OPTION! -!O3_Name! !O3!
    ) else (
        echo INFO: O3 [O3_Name:!O3_Name! O3_Caption:!O3_Caption!] not defined ...
    )
    rem echo OPTION:!OPTION!

    rem -------------------------------------
    rem ARGS
    rem -------------------------------------
    set ARGS=

    set A1_Name=
    set A1_Caption=
    set A1_Default=
    set A1=!A1_Default!
    set PN_CAPTION=!A1_Caption!
    rem call :Read_P A1 !A1! || exit /b 1
    rem echo A1:!A1!
    rem if defined A1 (
    rem     set ARGS=!ARGS! "!A1!"
    rem ) else (
    rem     echo ERROR: A1 [A1_Name:!A1_Name! A1_Caption:!A1_Caption!] not defined ... 
    rem     set OK=
    rem     exit /b 1
    rem )
    rem echo ARGS:!ARGS!

    rem echo %~dp0
    rem echo !SCRIPTS_DIR_PY!
    rem python !%~dp0!COPYFILE.py %1 "%2"

    rem set RUN=!SCRIPTS_DIR_PY!\COPYFILE\COPYFILE.py
    rem echo RUN:!RUN! 
    rem !RUN!

    call :PY_ENV_START || exit /b 1

    python "!SCRIPTS_DIR_PY!"\SRC\ftFormatTXT\ftFormatTXT.py !OPTION! !ARGS!

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
