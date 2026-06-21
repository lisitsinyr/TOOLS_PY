@echo off
rem -------------------------------------------------------------------
rem ftFormatTXT.bat
rem -------------------------------------------------------------------
chcp 1251>NUL

setlocal enabledelayedexpansion

    rem -------------------------------------------------------------------
    rem PROJECTS_LYR_ROOT - Каталог ROOT
    rem -------------------------------------------------------------------
    rem set PROJECTS_LYR_ROOT=D:\WORK\WIN
    set PROJECTS_LYR_ROOT=D:
    rem echo ..P1.. PROJECTS_LYR_ROOT:!PROJECTS_LYR_ROOT!

    rem -------------------------------------------------------------------
    rem PROJECTS_LYR_DIR - Каталог проектов LYR
    rem -------------------------------------------------------------------
    set PROJECTS_LYR_DIR=!PROJECTS_LYR_ROOT!\PROJECTS_LYR
    rem echo ..P1.. PROJECTS_LYR_DIR:!PROJECTS_LYR_DIR!
    if not exist "!PROJECTS_LYR_DIR!"\ (
        rem echo ..P1.. INFO: Dir "!PROJECTS_LYR_DIR!" not exist ...
        rem echo ..P1.. INFO: Create "!PROJECTS_LYR_DIR!" ...
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
    rem echo ..P1.. SCRIPTS_DIR:!SCRIPTS_DIR!

    rem -------------------------------------------------------------------
    rem LIB_BAT - каталог библиотеки скриптов BAT
    rem -------------------------------------------------------------------
    if not defined LIB_BAT (
        set LIB_BAT=!SCRIPTS_DIR!\LIB
    )
    rem echo ..P1.. LIB_BAT:!LIB_BAT!
    if not exist !LIB_BAT!\ (
        echo ERROR: Каталог библиотеки LYR !LIB_BAT! не существует...
        exit /b 1
    )

    rem -------------------------------------------------------------------
    rem Количество аргументов
    rem -------------------------------------------------------------------
    call :Read_N %* || exit /b 1

    rem -------------------------------------------------------------------
    rem Настройка среды
    rem -------------------------------------------------------------------
    call :SET_LIB %~f0 || exit /b 1

rem --------------------------------------------------------------------------------
rem 
rem --------------------------------------------------------------------------------
:begin
    set BATNAME=%~nx0
    echo Start !BATNAME! ...

    set DEBUG=

    set /a LOG_FILE_ADD=0

    rem -------------------------------------
    rem OPTION
    rem -------------------------------------
    set OPTION=

    call :CurrentDir || exit /b 1
    rem echo ..P1.. CurrentDir:!CurrentDir!

    rem -------------------------------------------------------------------
    rem O1
    rem -------------------------------------------------------------------
    set VarName=fp
    call :Read_P !VarName! "!CurrentDir!" "FilePath" "" || exit /b 1
    if defined !VarName! (
        set OPTION=!OPTION! -!VarName! "!%VarName%!"
    )

    rem -------------------------------------------------------------------
    rem O2
    rem -------------------------------------------------------------------
    set VarName=fm
    call :Read_P !VarName! "^.*..*$" "FileMask" "" || exit /b 1
    if defined !VarName! (
        set OPTION=!OPTION! -!VarName! "!%VarName%!"
    )

    rem -------------------------------------------------------------------
    rem O3
    rem -------------------------------------------------------------------
    set VarName=w
    call :Read_P !VarName! "60" "width" "" || exit /b 1
    if defined !VarName! (
        set OPTION=!OPTION! -!VarName! "!%VarName%!"
    )

    echo OPTION:!OPTION!

    rem -------------------------------------
    rem ARGS
    rem -------------------------------------
    set ARGS=

    rem echo ..P1.. ARGS:!ARGS!

    rem -------------------------------------------------------------------
    rem SCRIPTS_DIR_PY - Каталог скриптов PY
    rem -------------------------------------------------------------------
    if not defined SCRIPTS_DIR_PY (
        set SCRIPTS_DIR_PY=D:\PROJECTS_LYR\CHECK_LIST\DESKTOP\Python\PROJECTS_PY\SCRIPTS_PY\SRC\SCRIPTS_PY
    )
    rem echo ..P1.. SCRIPTS_DIR_PY:!SCRIPTS_DIR_PY!
    
    call :CurrentDir || exit /b 1
    echo CurrentDir:!CurrentDir!

    set project_dir=D:\PROJECTS_LYR\CHECK_LIST\DESKTOP\Python\PROJECTS_PY\SCRIPTS_PY\

    rem -------------------------------------------------------------------
    rem TEST - 
    rem -------------------------------------------------------------------
    set TEST=
    rem -------------------------------------------------------------------
    rem SCRIPT_NAME - 
    rem -------------------------------------------------------------------
    set SCRIPT_NAME=ftFormatTXT
    rem -------------------------------------------------------------------
    rem script_dir - 
    rem -------------------------------------------------------------------
    rem set script_dir=!SCRIPT_NAME!
    set script_dir=D:\PROJECTS_LYR\CHECK_LIST\DESKTOP\Python\PROJECTS_PY\SCRIPTS_PY\SRC\SCRIPTS_PY\ftFormatTXT\
    rem -------------------------------------------------------------------
    rem FULL_SCRIPT_NAME - 
    rem -------------------------------------------------------------------
    set FULL_SCRIPT_NAME=!script_dir!!script_name!.py
    if defined TEST (
        set FULL_SCRIPT_NAME=!script_dir!!script_name!.py
    )

    set VENV_DIR=D:\PROJECTS_LYR\CHECK_LIST\DESKTOP\Python\PROJECTS_PY\SCRIPTS_PY\.venv\
    rem echo ..P1.. VENV_DIR:!VENV_DIR!
    call :SET_VENV_DIR !project_dir! VENV_DIR !VENV_DIR! || exit /b 1
    call :VENV_START !VENV_DIR! || exit /b 1
    rem call :VENV_UPDATE !VENV_DIR! || exit /b 1

    python "!FULL_SCRIPT_NAME!" !OPTION! !ARGS!

    call :VENV_STOP !VENV_DIR! || exit /b 1

    rem call :PressAnyKey || exit /b 1

    exit /b 0
:end
rem =================================================

rem =================================================
rem ФУНКЦИИ LIB
rem =================================================

rem =================================================
rem LYRConst.bat
rem =================================================
:LYRConstINIT
%LIB_BAT%\LYRConst.bat %*
exit /b 0

rem =================================================
rem LYRPY.bat
rem =================================================
:LYRPYINIT
%LIB_BAT%\LYRPY.bat %*
exit /b 0
:VENV_START
%LIB_BAT%\LYRPY.bat %*
exit /b 0
:VENV_STOP
%LIB_BAT%\LYRPY.bat %*
exit /b 0

rem =================================================
rem LYRDEPLOY.bat
rem =================================================
:REPO_WORK
%LIB_BAT%\LYRDEPLOY.bat %*
exit /b 0
:git_pull
%LIB_BAT%\LYRDEPLOY.bat %*
exit /b 0
:DEPLOY_PROJECT
%LIB_BAT%\LYRDEPLOY.bat %*
exit /b 0

rem =================================================
rem LYRConst.bat
rem =================================================
:SET_LIB
%LIB_BAT%\LYRLIB.bat %*
exit /b 0
:SET_POETRY
%LIB_BAT%\LYRLIB.bat %*
exit /b 0
:SET_KIX
%LIB_BAT%\LYRLIB.bat %*
exit /b 0
:SET_PROJECT_DIR
%LIB_BAT%\LYRPY.bat %*
exit /b 0
:SET_VENV_DIR
%LIB_BAT%\LYRPY.bat %*
exit /b 0

rem =================================================
rem LYRDateTime.bat
rem =================================================
:YYYYMMDDHHMMSS
%LIB_BAT%\LYRDateTime.bat %*
exit /b 0
:DateTime
%LIB_BAT%\LYRDateTime.bat %*
exit /b 0

rem =================================================
rem LYRFileUtils.bat
rem =================================================
:ExtractFileDir
%LIB_BAT%\LYRFileUtils.bat %*
exit /b 0
:FullFileName
%LIB_BAT%\LYRFileUtils.bat %*
exit /b 0
:ExtractFileName
%LIB_BAT%\LYRFileUtils.bat %*
exit /b 0
:ExtractFileNameWithoutExt
%LIB_BAT%\LYRFileUtils.bat %*
exit /b 0
:ExtractFileExt
%LIB_BAT%\LYRFileUtils.bat %*
exit /b 0
:FileAttr
%LIB_BAT%\LYRFileUtils.bat %*
exit /b 0
:FileSize
%LIB_BAT%\LYRFileUtils.bat %*
exit /b 0
:CreateDir
%LIB_BAT%\LYRFileUtils.bat %*
exit /b 0
:CreateFile
%LIB_BAT%\LYRFileUtils.bat %*
exit /b 0
:CheckFile
%LIB_BAT%\LYRFileUtils.bat %*
exit /b 0
:CurrentDir
%LIB_BAT%\LYRFileUtils.bat %*
exit /b 0
:COPY_FILES
%LIB_BAT%\LYRFileUtils.bat %*
exit /b 0
:XCOPY_FILES
%LIB_BAT%\LYRFileUtils.bat %*
exit /b 0

rem =================================================
rem LYRLog.bat
rem =================================================
:FormatStr
%LIB_BAT%\LYRLog.bat %*
exit /b 0
:AddLog
%LIB_BAT%\LYRLog.bat %*
exit /b 0
:AddLogFile
%LIB_BAT%\LYRLog.bat %*
exit /b 0
:StartLogFile
%LIB_BAT%\LYRLog.bat %*
exit /b 0
:StopLogFile
%LIB_BAT%\LYRLog.bat %*
exit /b 0

rem =================================================
rem LYRStrUtils.bat
rem =================================================
:TrimLeft
%LIB_BAT%\LYRStrUtils.bat %*
exit /b 0
:TrimRight
%LIB_BAT%\LYRStrUtils.bat %*
exit /b 0
:Trim
%LIB_BAT%\LYRStrUtils.bat %*
exit /b 0
:Left
%LIB_BAT%\LYRStrUtils.bat %*
exit /b 0
:Mid
%LIB_BAT%\LYRStrUtils.bat %*
exit /b 0
:TrimQuotes
%LIB_BAT%\LYRStrUtils.bat %*
exit /b 0

rem =================================================
rem LYRSupport.bat
rem =================================================
:PressAnyKey
%LIB_BAT%\LYRSupport.bat %*
exit /b 0
:Pause
%LIB_BAT%\LYRSupport.bat %*
exit /b 0
:Read_P
%LIB_BAT%\LYRSupport.bat %*
exit /b 0
:Read_N
%LIB_BAT%\LYRSupport.bat %*
exit /b 0
:Read_F
%LIB_BAT%\LYRSupport.bat %*
exit /b 0
:GetDir
%LIB_BAT%\LYRSupport.bat %*
exit /b 0
:GetFile
%LIB_BAT%\LYRSupport.bat %*
exit /b 0
:FORCicle
%LIB_BAT%\LYRSupport.bat %*
exit /b 0
:GetSET
%LIB_BAT%\LYRSupport.bat %*
exit /b 0
:GetCMD
%LIB_BAT%\LYRSupport.bat %*
exit /b 0

rem =================================================
rem LYRParserINI.bat
rem =================================================
:GetINI
%LIB_BAT%\LYRParserINI.bat %*
exit /b 0
:SetINI
%LIB_BAT%\LYRParserINI.bat %*
exit /b 0
:GetINIParametr
%LIB_BAT%\LYRParserINI.bat %*
exit /b 0
:GetFileParser
%LIB_BAT%\LYRParserINI.bat %*
exit /b 0
rem =================================================
