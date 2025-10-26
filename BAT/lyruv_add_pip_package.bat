@echo off
rem -------------------------------------------------------------------
rem lyrpy.bat
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
    rem SCRIPTS_DIR_SRC - Каталог скриптов BAT
    rem -------------------------------------------------------------------
    if not defined SCRIPTS_DIR_SRC (
        rem set SCRIPTS_DIR=D:\TOOLS\TOOLS_BAT
        set SCRIPTS_DIR_SRC=!PROJECTS_LYR_DIR!\CHECK_LIST\SCRIPT\BAT\PROJECTS_BAT\TOOLS_SRC_BAT\SRC
    )
    rem echo SCRIPTS_DIR_SRC:!SCRIPTS_DIR_SRC!

    rem -------------------------------------------------------------------
    rem LIB_BAT - каталог библиотеки скриптов BAT
    rem -------------------------------------------------------------------
    if not defined LIB_BAT (
        set LIB_BAT=!SCRIPTS_DIR_SRC!\LIB
    )
    rem echo LIB_BAT:!LIB_BAT!
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

    set O1_Name=O1
    set O1_Caption=VENV
    set O1_Default=P313
    set O1=!O1_Default!
    set PN_CAPTION=!O1_Caption!
    call :Read_P O1 !O1! || exit /b 1
    echo O1:!O1!
    if defined O1 (
       set OPTION=!OPTION! -!O1_Name! "!O1!"
    ) else (
        echo INFO: O1 [O1_Name:!O1_Name! O1_Caption:!O1_Caption!] not defined ...
    )
    echo OPTION:!OPTION!

    rem -------------------------------------------------------------------
    rem ENV - 
    rem -------------------------------------------------------------------
    set PY_ENVDIR=D:\PROJECTS_LYR\CHECK_LIST\DESKTOP\Python\VENV\P313
    if exist !O1! (
       set PY_ENVDIR=!O1!
    ) else (
        if !O1!==P313 (
            set PY_ENVDIR=D:\PROJECTS_LYR\CHECK_LIST\DESKTOP\Python\VENV\P313
        ) else (
            if !O1!==P314 (
                set PY_ENVDIR=D:\PROJECTS_LYR\CHECK_LIST\DESKTOP\Python\VENV\P314
            )
        )
    )
    echo PY_ENVDIR:!PY_ENVDIR!
    if not exist !PY_ENVDIR! (
        echo INFO: Dir !PY_ENVDIR! not exist ...
        exit /b 1
    )

    rem -------------------------------------
    rem ARGS
    rem -------------------------------------
    set ARGS=

    set A1_Name=package_name
    set A1_Caption=package_name
    set A1_Default=%1
    set A1=!A1_Default!
    set PN_CAPTION=!A1_Caption!
    call :Read_P A1 !A1! || exit /b 1
    echo A1:!A1!
    if defined A1 (
        set ARGS=!ARGS! "!A1!"
    ) else (
        echo ERROR: A1 [A1_Name:!A1_Name! A1_Caption:!A1_Caption!] not defined ... 
        set OK=
        exit /b 1
    )

    echo ARGS:!ARGS!


    call :PY_ENV_START || exit /b 1

    uv pip install !A1!

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
