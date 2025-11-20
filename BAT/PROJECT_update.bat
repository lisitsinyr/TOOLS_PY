@echo off
rem -------------------------------------------------------------------
rem PROJECT_PYupdate.bat
rem -------------------------------------------------------------------
rem 
rem Description:
rem   Создание/изменение структуры проекта PROJECT_PY
rem 
rem Usage:
rem   PROJECT_PYupdate.bat <ProjectName>
rem 
rem Arguments:
rem   name - Имя проекта
rem 
rem -------------------------------------------------------------------
chcp 1251>NUL

setlocal enabledelayedexpansion

rem --------------------------------------------------------------------------------
rem 
rem --------------------------------------------------------------------------------
:begin
    set BATNAME=%~nx0
    echo Start !BATNAME! ...

    set DEBUG=

    rem -------------------------------------------------------------------
    rem SCRIPTS_DIR - Каталог скриптов
    rem LIB_BAT - каталог библиотеки скриптов
    rem SCRIPTS_DIR_KIX - Каталог скриптов KIX
    rem -------------------------------------------------------------------
    call :MAIN_INIT %* || exit /b 1

    rem Количество аргументов
    call :Read_N %* || exit /b 1
    rem echo Read_N: !Read_N!

    call :SET_LIB %0 || exit /b 1
    rem echo CURRENT_DIR: !CURRENT_DIR!

    call :StartLogFile || exit /b 1
    set OK=yes
    call :MAIN_SET %* || exit /b 1
    if defined OK if not defined Read_N (
        call :MAIN_CHECK_PARAMETR %* || exit /b 1
    )
    if defined OK (
        call :MAIN %* || exit /b 1
    )
    call :StopLogFile || exit /b 1

    exit /b 0
:end
rem --------------------------------------------------------------------------------

rem -----------------------------------------------
rem procedure MAIN_INIT (FULLFILENAME, DEBUG)
rem -----------------------------------------------
:MAIN_INIT
rem beginfunction
    set FUNCNAME=%0
    set FUNCNAME=MAIN_INIT
    if defined DEBUG (
        echo DEBUG: procedure !FUNCNAME! ...
    )

    rem -------------------------------------------------------------------
    rem SCRIPTS_DIR - Каталог скриптов
    rem -------------------------------------------------------------------
    if not defined SCRIPTS_DIR (
        set SCRIPTS_DIR=D:\TOOLS\TOOLS_BAT
        rem set SCRIPTS_DIR=D:\PROJECTS_LYR\CHECK_LIST\SCRIPT\BAT\PROJECTS_BAT\TOOLS_BAT
    )
    rem echo SCRIPTS_DIR: %SCRIPTS_DIR%
    rem -------------------------------------------------------------------
    rem LIB_BAT - каталог библиотеки скриптов
    rem -------------------------------------------------------------------
    if not defined LIB_BAT (
        set LIB_BAT=!SCRIPTS_DIR!\SRC\LIB
        set LIB_BAT=!SCRIPTS_DIR!\LIB
        rem echo LIB_BAT: !LIB_BAT!
    )
    if not exist !LIB_BAT!\ (
        echo ERROR: Каталог библиотеки LYR !LIB_BAT! не существует...
        exit /b 0
    )
    rem -------------------------------------------------------------------
    rem SCRIPTS_DIR_KIX - Каталог скриптов KIX
    rem -------------------------------------------------------------------
    if not defined SCRIPTS_DIR_KIX (
        set SCRIPTS_DIR_KIX=D:\TOOLS\TOOLS_KIX
        set SCRIPTS_DIR_KIX=D:\PROJECTS_LYR\CHECK_LIST\SCRIPT\KIX\PROJECTS_KIX\TOOLS_KIX
    )
    rem echo SCRIPTS_DIR_KIX: !SCRIPTS_DIR_KIX!

    exit /b 0
rem endfunction

rem --------------------------------------------------------------------------------
rem procedure MAIN_SET ()
rem --------------------------------------------------------------------------------
:MAIN_SET
rem beginfunction
    set FUNCNAME=%0
    set FUNCNAME=MAIN_SET
    if defined DEBUG (
        echo DEBUG: procedure !FUNCNAME! ...
    )

    exit /b 0
rem endfunction

rem --------------------------------------------------------------------------------
rem procedure MAIN ()
rem --------------------------------------------------------------------------------
:MAIN
rem beginfunction
    set FUNCNAME=%0
    if defined DEBUG (
        echo DEBUG: procedure !FUNCNAME! ...
    )

    if defined OK (
        echo ProjectName: !ProjectName!

        call :CurrentDir || exit /b 1

        call :MAIN_CreateDIRs || exit /b 1

        call :MAIN_CreateFILEs || exit /b 1

        call :MAIN_CopyFILEs || exit /b 1

        call :MAIN_SetPOETRY || exit /b 1
    )

    exit /b 0
:end

rem --------------------------------------------------------------------------------
rem procedure MAIN_CreateDIRs ()
rem --------------------------------------------------------------------------------
:MAIN_CreateDIRs
rem beginfunction
    set FUNCNAME=%0
    if defined DEBUG (
        echo DEBUG: procedure !FUNCNAME! ...
    )

    set LDir=.devcontainer
    call :AddLog !loAll! !TEXT! CreateDir !LDir! || exit /b 1
    call :CreateDir !LDir!
    set LDir=.idea
    call :AddLog !loAll! !TEXT! CreateDir !LDir! || exit /b 1
    call :CreateDir !LDir!
    set LDir=.venv
    call :AddLog !loAll! !TEXT! CreateDir !LDir! || exit /b 1
    call :CreateDir !LDir!
    set LDir=.vscode
    call :AddLog !loAll! !TEXT! CreateDir !LDir! || exit /b 1
    call :CreateDir !LDir!
    set LDir=BUILD
    call :AddLog !loAll! !TEXT! CreateDir !LDir! || exit /b 1
    call :CreateDir !LDir!
    set LDir=CONFIG
    call :AddLog !loAll! !TEXT! CreateDir !LDir! || exit /b 1
    call :CreateDir !LDir!
    set LDir=DATA
    call :AddLog !loAll! !TEXT! CreateDir !LDir! || exit /b 1
    call :CreateDir !LDir!
    set LDir=DIST
    call :AddLog !loAll! !TEXT! CreateDir !LDir! || exit /b 1
    call :CreateDir !LDir!
    set LDir=DOC
    call :AddLog !loAll! !TEXT! CreateDir !LDir! || exit /b 1
    call :CreateDir !LDir!
    set LDir=EXE
    call :AddLog !loAll! !TEXT! CreateDir !LDir! || exit /b 1
    call :CreateDir !LDir!
    set LDir=LOG
    call :AddLog !loAll! !TEXT! CreateDir !LDir! || exit /b 1
    call :CreateDir !LDir!
    set LDir=NOTEBOOKS
    call :AddLog !loAll! !TEXT! CreateDir !LDir! || exit /b 1
    call :CreateDir !LDir!
    set LDir=OUT
    call :AddLog !loAll! !TEXT! CreateDir !LDir! || exit /b 1
    call :CreateDir !LDir!
    set LDir=SRC
    call :AddLog !loAll! !TEXT! CreateDir !LDir! || exit /b 1
    call :CreateDir !LDir!
    set LDir=SRC\!ProjectName!
    call :AddLog !loAll! !TEXT! CreateDir !LDir! || exit /b 1
    call :CreateDir !LDir!
    set LDir=TESTS
    call :AddLog !loAll! !TEXT! CreateDir !LDir! || exit /b 1
    call :CreateDir !LDir!
    set LDir=WORK
    call :AddLog !loAll! !TEXT! CreateDir !LDir! || exit /b 1
    call :CreateDir !LDir!

    exit /b 0
:end

rem --------------------------------------------------------------------------------
rem procedure MAIN_CreateFILEs ()
rem --------------------------------------------------------------------------------
:MAIN_CreateFILEs
rem beginfunction
    set FUNCNAME=%0
    if defined DEBUG (
        echo DEBUG: procedure !FUNCNAME! ...
    )

    set LFileName=.gitmodules
    call :AddLog !loAll! !TEXT! CreateFile !LFileName! || exit /b 1
    call :CreateFile !LFileName!
    set LFileName=.pypirc
    call :AddLog !loAll! !TEXT! CreateFile !LFileName! || exit /b 1
    call :CreateFile !LFileName!
    set LFileName=src\!ProjectName!\__init__.py
    call :AddLog !loAll! !TEXT! CreateFile !LFileName! || exit /b 1
    call :CreateFile !LFileName!
    set LFileName=tests\__init__.py
    call :AddLog !loAll! !TEXT! CreateFile !LFileName! || exit /b 1
    call :CreateFile !LFileName!
    set LFileName=UPDATE_!ProjectName!.bat
    call :AddLog !loAll! !TEXT! CreateFile !LFileName! || exit /b 1
    call :CreateFile !LFileName!

    set LFileName=README.md
    call :AddLog !loAll! !TEXT! CreateFile !LFileName! || exit /b 1
    call :CreateFile !LFileName!
    call :FileSize !LFileName!
    if !FileSize!==0 (
        echo !ProjectName! >> !LFileName!
        echo ---------- >> !LFileName!
        echo You can use [GitHub-flavored Markdown]^(https://guides.github.com/features/mastering-markdown/^) >> !LFileName!
    )

    set LFileName=POETRY.ini
    call :AddLog !loAll! !TEXT! CreateFile !LFileName! || exit /b 1
    call :CreateFile !LFileName!
    call :FileSize !LFileName!
    if !FileSize!==0 (
        echo [general] >> !LFileName!
        echo POETRY_NAME=!ProjectName! >> !LFileName!
    )
    call :AddLog !loAll! !TEXT! SetINI !LFileName! || exit /b 1
    rem D:\TOOLS\EXE\setini.exe !LFileName! general POETRY_NAME !ProjectName!
    rem %SetINIAPP% !LFileName! general POETRY_NAME !ProjectName!
    call :SetINI !LFileName! general POETRY_NAME !ProjectName! || exit /b 1

    set LFileName=PROJECT.ini
    call :AddLog !loAll! !TEXT! CreateFile !LFileName! || exit /b 1
    call :CreateFile !LFileName!
    call :FileSize !LFileName!
    if !FileSize!==0 (
        echo [general] >> !LFileName!
        echo PROJECT_NAME=!ProjectName! >> !LFileName!
    )
    call :AddLog !loAll! !TEXT! SetINI !LFileName! || exit /b 1
    rem D:\TOOLS\EXE\setini.exe !LFileName! general PROJECT_NAME !ProjectName!
    call :SetINI !LFileName! general POETRY_NAME !ProjectName! || exit /b 1

    set LFileName=REPO.ini
    call :AddLog !loAll! !TEXT! CreateFile !LFileName! || exit /b 1
    call :CreateFile !LFileName!
    call :FileSize !LFileName!
    if !FileSize!==0 (
        echo [general] >> !LFileName!
        echo REPO_NAME=!ProjectName! >> !LFileName!
    )
    call :AddLog !loAll! !TEXT! SetINI !LFileName! || exit /b 1
    rem D:\TOOLS\EXE\setini.exe !LFileName! general REPO_NAME !ProjectName!
    call :SetINI !LFileName! general POETRY_NAME !ProjectName! || exit /b 1

    exit /b 0
:end

rem --------------------------------------------------------------------------------
rem procedure MAIN_CopyFILEs ()
rem --------------------------------------------------------------------------------
:MAIN_CopyFILEs
rem beginfunction
    set FUNCNAME=%0
    if defined DEBUG (
        echo DEBUG: procedure !FUNCNAME! ...
    )

    rem ------------------------------------------------------
    set DIR_TO=!CurrentDir!
    rem echo DIR_TO: !DIR_TO!
    rem ------------------------------------------------------
    set DIR_FROM=D:\PROJECTS_LYR\CHECK_LIST\GIT\PROJECTS_GIT\TOOLS_GIT\BAT\A.WORK
    rem echo DIR_FROM: !DIR_FROM!
    set LFileName=lyrgit_push_main.bat
    call :AddLog !loAll! !TEXT! CopyFile !LFileName! || exit /b 1
    copy "!DIR_FROM!\!LFileName!" "!DIR_TO!" > NUL
    set LFileName=lyrgit_init.bat
    call :AddLog !loAll! !TEXT! CopyFile !LFileName! || exit /b 1
    copy "!DIR_FROM!\!LFileName!" "!DIR_TO!" > NUL

    set DIR_FROM=D:\PROJECTS_LYR\CHECK_LIST\DESKTOP\Python\PROJECTS_PY\PATTERN_PY
    rem echo DIR_FROM: !DIR_FROM!
    set LFileName=.gitignore
    call :AddLog !loAll! !TEXT! CopyFile !LFileName! || exit /b 1
    copy "!DIR_FROM!\!LFileName!" "!DIR_TO!" > NUL
    set LFileName=LICENSE
    call :AddLog !loAll! !TEXT! CopyFile !LFileName! || exit /b 1
    copy "!DIR_FROM!\!LFileName!" "!DIR_TO!" > NUL
    set LFileName=pyproject.toml
    call :AddLog !loAll! !TEXT! CopyFile !LFileName! || exit /b 1
    copy "!DIR_FROM!\!LFileName!" "!DIR_TO!" > NUL

    rem ------------------------------------------------------
    set DIR_TO=!CurrentDir!\SRC\!ProjectName!
    rem echo DIR_TO: !DIR_TO!
    rem ------------------------------------------------------
    set DIR_FROM=D:\PROJECTS_LYR\CHECK_LIST\DESKTOP\Python\PROJECTS_PY\PATTERN_PY\SRC\PATTERN_PY
    rem echo DIR_FROM: !DIR_FROM!
    set LFileName=PATTERN_PY.py
    call :AddLog !loAll! !TEXT! CopyFile !LFileName! || exit /b 1
    copy "!DIR_FROM!\!LFileName!" "!DIR_TO!"\!ProjectName!.py > NUL
        
    rem ------------------------------------------------------
    set DIR_TO=!CurrentDir!\SRC
    rem echo DIR_TO: !DIR_TO!
    rem ------------------------------------------------------
    set DIR_FROM=D:\PROJECTS_LYR\CHECK_LIST\DESKTOP\Python\PROJECTS_PY\PATTERN_PY\SRC
    rem echo DIR_FROM: !DIR_FROM!
    set LFileName=README.md
    call :AddLog !loAll! !TEXT! CopyFile !LFileName! || exit /b 1
    copy "!DIR_FROM!\!LFileName!" "!DIR_TO!" > NUL
    set DIR_FROM=D:\PROJECTS_LYR\CHECK_LIST\DESKTOP\Python\BATPY
    rem echo DIR_FROM: !DIR_FROM!
    set LFileName=PROJECT_PYupdate.bat
    call :AddLog !loAll! !TEXT! CopyFile !LFileName! || exit /b 1
    copy "!DIR_FROM!\!LFileName!" "!DIR_TO!" > NUL

    exit /b 0
:end

rem --------------------------------------------------------------------------------
rem procedure MAIN_SetPOETRY ()
rem --------------------------------------------------------------------------------
:MAIN_SetPOETRY
rem beginfunction
    set FUNCNAME=%0
    if defined DEBUG (
        echo DEBUG: procedure !FUNCNAME! ...
    )

    set LFileName=pyproject.toml
    call :AddLog !loAll! !TEXT! :SetINI !LFileName! || exit /b 1
    rem D:\TOOLS\EXE\setini.exe !LFileName! tool.poetry name !ProjectName!
    call :SetINI !LFileName! tool.poetry name !ProjectName! || exit /b 1

    rem call :AddLog !loAll! !TEXT! GetINI !LFileName! || exit /b 1
    rem call :GetINI !LFileName! || exit /b 1

    rem call :AddLog !loAll! !TEXT! GetINIParametr !LFileName! || exit /b 1
    rem call :GetINIParametr !LFileName! name || exit /b 1
    rem echo name: !name!

    exit /b 0
:end

rem --------------------------------------------------------------------------------
rem procedure MAIN_CHECK_PARAMETR ()
rem --------------------------------------------------------------------------------
:MAIN_CHECK_PARAMETR
rem beginfunction
    set FUNCNAME=%0
    if defined DEBUG (
        echo DEBUG: procedure !FUNCNAME! ...
    )

    echo OK: !OK!

    rem -------------------------------------
    rem OPTION
    rem -------------------------------------

    rem -------------------------------------
    rem ARGS
    rem -------------------------------------
    if not defined PROJECT_NAME (
        set PN_CAPTION=Имя проекта
        set ProjectName=PATTERN_PY
        call :Read_P ProjectName %1 || exit /b 1
        rem echo ProjectName: !ProjectName!

        if not defined ProjectName (
            echo ERROR: ProjectName not defined ...
            set OK=
        ) else (
            set OK=yes
        )
    ) else (
        set ProjectName=!PROJECT_NAME!
    )

    exit /b 0

rem endfunction

rem =================================================
rem ФУНКЦИИ LIB
rem =================================================

rem =================================================
rem LYRPY.bat
rem =================================================
:LYRPY
%LIB_BAT%\LYRPY.bat %*
exit /b 0
:VENV_START
%LIB_BAT%\LYRPY.bat %*
exit /b 0
:VENV_STOP
%LIB_BAT%\LYRPY.bat %*
exit /b 0
:VENV_UPDATE
%LIB_BAT%\LYRPY.bat %*
exit /b 0
:SET_PROJECT_DIR
%LIB_BAT%\LYRPY.bat %*
exit /b 0
:SET_VENV_DIR
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

rem =================================================
rem LYRSupport.bat
rem =================================================
:PressAnyKey
%LIB_BAT%\LYRSupport.bat %*
exit /b 0
:Pause
%LIB_BAT%\LYRSupport.bat %*
exit /b 0
:Check_P
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
:GetINI
%LIB_BAT%\LYRSupport.bat %*
exit /b 0
:SetINI
%LIB_BAT%\LYRSupport.bat %*
exit /b 0
:GetINIParametr
%LIB_BAT%\LYRSupport.bat %*
exit /b 0
rem =================================================
