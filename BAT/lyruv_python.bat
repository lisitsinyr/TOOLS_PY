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

    if not defined O1 (
        set O1_Name=O1
        set O1_Caption=python version
        set O1_Default=3.13.9
        set O1=!O1_Default!
        set PN_CAPTION=!O1_Caption!
        rem call :Read_P O1 || exit /b 1
    )
    echo O1:!O1!
    if defined O1 (
        set OPTION=!OPTION! "!O1!"
    ) else (
        echo INFO: O1 [O1_Name:!O1_Name! O1_Caption:!O1_Caption!] not defined ...
    )

    rem echo OPTION:!OPTION!

    rem -------------------------------------
    rem ARGS
    rem -------------------------------------
    set ARGS=

    rem if not defined A1 (
    rem     set A1_Name=script
    rem     set A1_Caption=script
    rem     set A1_Default=%1
    rem     set A1=!A1_Default!
    rem     set PN_CAPTION=!A1_Caption!
    rem     call :Read_P A1 !A1! || exit /b 1
    rem )
    rem echo A1:!A1!
    rem if defined A1 (
    rem     set ARGS=!ARGS! "!A1!"
    rem ) else (
    rem     echo ERROR: A1 [A1_Name:!A1_Name! A1_Caption:!A1_Caption!] not defined ... 
    rem     set OK=
    rem     exit /b 1
    rem )

    rem echo ARGS:!ARGS!

    set ChoiceOperation=

    rem ------------------------------------------
    :WHILE
    rem ------------------------------------------
    if not !ChoiceOperation!==10 (
        call :ChoiceOperation || exit /b 1
        goto :WHILE
    )

    rem call :PressAnyKey || exit /b 1
    
    exit /b 0
:end
rem =================================================

rem --------------------------------------------------------------------------------
rem function ChoiceOperation () -> Read_N
rem --------------------------------------------------------------------------------
:ChoiceOperation
rem beginfunction
    set FUNCNAME=%0
    set FUNCNAME=ChoiceOperation
    if defined DEBUG (
        echo DEBUG: procedure !FUNCNAME! ...
    )
    set !FUNCNAME!=

    rem ------------------------------------------
    rem Меню
    rem ------------------------------------------
    echo 1.UV_python_list
    echo 2.UV_python_install
    echo 3.UV_python_uninstall
    echo 4.UV_python_run
    echo 5.UV_python_upgrade
    echo 6.UV_python_find
    echo 7.UV_python_dir
    echo 8.UV_python_
    echo 9.UV_python_pin
    echo Q.Quit

    set C1_Name=C1
    set C1_List=123456789Q
    set C1_Caption=operation
    set C1_Default=Q
    rem set C1=!O1_Default!
    set PN_CAPTION=!C1_Caption!
    rem procedure Read_F (P_Name, P_List, ADefault, ACaption, Atimeout)
    call :Read_F C1 !C1_List! !C1_Default! !C1_Caption! 10 || exit /b 1
    echo C1:!C1!
    set ChoiceOperation=!C1!

    rem ------------------------------------------
    rem CASE
    rem ------------------------------------------
    if !C1!==1 (
        call :UV_python_list || exit /b 1
        exit /b 0
    )
    if !C1!==2 (
        call :UV_python_install !O1! || exit /b 1
        exit /b 0
    )
    if !C1!==3 (
        call :UV_python_uninstall !O1! || exit /b 1
        exit /b 0
    )
    if !C1!==4 (
        call :UV_python_run || exit /b 1
        exit /b 0
    )
    if !C1!==5 (
        call :UV_python_upgrade || exit /b 1
        exit /b 0
    )
    if !C1!==6 (
        call :UV_python_find !O1! || exit /b 1
        exit /b 0
    )
    if !C1!==7 (
        call :UV_python_dir !O1! || exit /b 1
        exit /b 0
    )
    if !C1!==8 (
        call :UV_python_ !O1! || exit /b 1
        exit /b 0
    )
    if !C1!==9 (
        call :UV_python_pin !O1! || exit /b 1
        exit /b 0
    )
    if !C1!==10 (
        exit /b 0
    )

    exit /b 0
rem endfunction

rem =================================================
rem LIB
rem =================================================

rem =================================================
rem LYRUV.bat
rem =================================================
:LYRUV
%LIB_BAT%\LYRUV.bat %*
exit /b 0
:UV_python_list
%LIB_BAT%\LYRUV.bat %*
exit /b 0
:UV_python_install
%LIB_BAT%\LYRUV.bat %*
exit /b 0
:UV_python_uninstall
%LIB_BAT%\LYRUV.bat %*
exit /b 0
:UV_python_run
%LIB_BAT%\LYRUV.bat %*
exit /b 0
:UV_python_upgrade
%LIB_BAT%\LYRUV.bat %*
exit /b 0
:UV_python_find
%LIB_BAT%\LYRUV.bat %*
exit /b 0
:UV_python_dir
%LIB_BAT%\LYRUV.bat %*
exit /b 0
:UV_python_
%LIB_BAT%\LYRUV.bat %*
exit /b 0
:UV_python_pin
%LIB_BAT%\LYRUV.bat %*
exit /b 0
:UV_help
%LIB_BAT%\LYRUV.bat %*
exit /b 0
:UV_help_cmd
%LIB_BAT%\LYRUV.bat %*
exit /b 0
:UV_version
%LIB_BAT%\LYRUV.bat %*
exit /b 0
:UV_self
%LIB_BAT%\LYRUV.bat %*
exit /b 0
:UV_self_version
%LIB_BAT%\LYRUV.bat %*
exit /b 0
:UV_install_self
%LIB_BAT%\LYRUV.bat %*
exit /b 0
:UV_install_other
%LIB_BAT%\LYRUV.bat %*
exit /b 0
:UV_update_self
%LIB_BAT%\LYRUV.bat %*
exit /b 0
:UV_install_pip
%LIB_BAT%\LYRUV.bat %*
exit /b 0
:UV_upgrade_pip
%LIB_BAT%\LYRUV.bat %*
exit /b 0

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
:PY_ENV_UPDATE
%LIB_BAT%\LYRPY.bat %*
exit /b 0
:PROJECT_DIR
%LIB_BAT%\LYRPY.bat %*
exit /b 0
:VENV_DIR
%LIB_BAT%\LYRPY.bat %*
exit /b 0
:GET_project_dir
%LIB_BAT%\LYRPY.bat %*
exit /b 0
:GET_venv_dir
%LIB_BAT%\LYRPY.bat %*
exit /b 0
:GET_python_dir
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
