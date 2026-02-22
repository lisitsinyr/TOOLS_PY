@echo off
rem -------------------------------------------------------------------
rem lyrpoetry_install.bat
rem     Запуск poetry из глобального виртуального пространства
rem 
rem Description:
rem   Installs the project dependencies.
rem   The install command reads the pyproject.toml file from the current project, resolves the dependencies, and installs them
rem 
rem Usage:
rem   install [options]
rem 
rem Options:
rem       --without=WITHOUT      The dependency groups to ignore. (multiple values allowed)
rem       --with=WITH            The optional dependency groups to include. (multiple values allowed)
rem       --only=ONLY            The only dependency groups to include. (multiple values allowed)
rem       --no-dev               Do not install the development dependencies. (Deprecated)
rem       --sync                 Synchronize the environment with the locked packages and the specified groups.
rem       --no-root              Do not install the root package (the current project).
rem       --no-directory         Do not install any directory path dependencies; useful to install dependencies without source code, e.g. for caching of Docker layers)
rem       --dry-run              Output the operations but do not execute anything (implicitly enables --verbose).
rem       --remove-untracked     Removes packages not present in the lock file. (Deprecated)
rem   -E, --extras=EXTRAS        Extra sets of dependencies to install. (multiple values allowed)
rem       --all-extras           Install all extra dependencies.
rem       --only-root            Exclude all dependencies.
rem       --compile              Compile Python source files to bytecode. (This option has no effect if modern-installation is disabled because the old installer always compiles.)
rem   -h, --help                 Display help for the given command. When no command is given display help for the list command.
rem   -q, --quiet                Do not output any message.
rem   -V, --version              Display this application version.
rem       --ansi                 Force ANSI output.
rem       --no-ansi              Disable ANSI output.
rem   -n, --no-interaction       Do not ask any interactive question.
rem       --no-plugins           Disables plugins.
rem       --no-cache             Disables Poetry source caches.
rem   -C, --directory=DIRECTORY  The working directory for the Poetry command (defaults to the current working directory).
rem   -v|vv|vvv, --verbose       Increase the verbosity of messages: 1 for normal output, 2 for more verbose output and 3 for debug.
rem 
rem Help:
rem   The install command reads the poetry.lock file from
rem   the current directory, processes it, and downloads and installs all the
rem   libraries and dependencies outlined in that file. If the file does not
rem   exist it will look for pyproject.toml and do the same.
rem   
rem   poetry install
rem   
rem   By default, the above command will also install the current project. To install only the
rem   dependencies and not including the current project, run the command with the
rem   --no-root option like below:
rem   
rem    poetry install --no-root
rem   
rem   If you want to use Poetry only for dependency management but not for packaging,
rem   you can set the "package-mode" to false in your pyproject.toml file.
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
    rem echo ..P1.. Read_N: !Read_N!

    call :SET_LIB %0 || exit /b 1
    rem echo ..P1.. CURRENT_DIR: !CURRENT_DIR!

    call :StartLogFile || exit /b 1

    set OK=yes
    
    call :MAIN_SET %* || exit /b 1
    
    call :MAIN_CHECK_PARAMETR %* || exit /b 1
    
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
        rem set SCRIPTS_DIR=D:\PROJECTS_LYR\CHECK_LIST\SCRIPT\BAT\PROJECTS_BAT\TOOLS_SRC_BAT
    )
    rem echo ..P1.. SCRIPTS_DIR: %SCRIPTS_DIR%
    rem -------------------------------------------------------------------
    rem LIB_BAT - каталог библиотеки скриптов
    rem -------------------------------------------------------------------
    if not defined LIB_BAT (
        set LIB_BAT=!SCRIPTS_DIR!\SRC\LIB
        set LIB_BAT=!SCRIPTS_DIR!\LIB
        rem echo ..P1.. LIB_BAT: !LIB_BAT!
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
    rem echo ..P1.. SCRIPTS_DIR_KIX: !SCRIPTS_DIR_KIX!

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

    set tomlFile=pyproject.toml
    call :CheckFile !tomlFile! || exit /b 1
    if not defined CheckFile (
        echo ERROR: Файл !tomlFile! не существует ...
        set OK=
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

    call :SET_POETRY || exit /b 1

    echo Installs the project dependencies ...
    set COMMAND=install
    
    if not defined Read_N (
        set APPRUN=!APP! !COMMAND!!OPTION!!ARGS!
    ) else (
        set APPRUN=!APP! !COMMAND!!OPTION! %*
    )
    echo APPRUN: !APPRUN!
    !APPRUN!

    exit /b 0
rem endfunction

rem --------------------------------------------------------------------------------
rem procedure MAIN_CHECK_PARAMETR ()
rem --------------------------------------------------------------------------------
:MAIN_CHECK_PARAMETR
rem beginfunction
    set FUNCNAME=%0
    if defined DEBUG (
        echo DEBUG: procedure !FUNCNAME! ...
    )

    rem -------------------------------------
    rem OPTION
    rem -------------------------------------
    set without=
    set PN_CAPTION=The dependency groups to ignore. ^(multiple values allowed^)
    call :Read_P without "" || exit /b 1
    rem echo ..P1.. without: !without!
    if defined without (
        set OPTION=!OPTION! --without=!without!
    )
    set with=
    set PN_CAPTION=The optional dependency groups to include. ^(multiple values allowed^)
    call :Read_P with "" || exit /b 1
    rem echo ..P1.. with: !with!
    if defined with (
        set OPTION=!OPTION! --with=!with!
    )
    set only=
    set PN_CAPTION=The only dependency groups to include. ^(multiple values allowed^)
    call :Read_P only "" || exit /b 1
    rem echo ..P1.. only: !only!
    if defined only (
        set OPTION=!OPTION! --only=!only!
    )
    set no-dev=Y
    set PN_CAPTION=Do not install the development dependencies. (Deprecated)
    call :Read_F no-dev "yN" 0 || exit /b 1
    rem echo ..P1.. no-dev: !no-dev!
    if defined no-dev (
        set OPTION=!OPTION! --no-dev
    )
    set sync=N
    set PN_CAPTION=Synchronize the environment with the locked packages and the specified groups
    call :Read_F sync "yN" 0 || exit /b 1
    rem echo ..P1.. sync: !sync!
    if defined sync (
        set OPTION=!OPTION! --sync
    )
    set no-root=Y
    set PN_CAPTION=Do not install the root package (the current project)
    call :Read_F no-root "yN" 0 || exit /b 1
    rem echo ..P1.. no-root: !no-root!
    if defined no-root (
        set OPTION=!OPTION! --no-root
    )
    set no-directory=Y
    set PN_CAPTION=Do not install any directory path dependencies; useful to install dependencies without source code, e.g. for caching of Docker layers
    call :Read_F no-directory "yN" 0 || exit /b 1
    rem echo ..P1.. no-directory: !no-directory!
    if defined no-directory (
        set OPTION=!OPTION! --no-directory
    )
    set dry-run=N
    set PN_CAPTION=Output the operations but do not execute anything ^(implicitly enables --verbose^)
    call :Read_F dry-run "yN" 0 || exit /b 1
    rem echo ..P1.. dry-run: !dry-run!
    if defined dry-run (
        set OPTION=!OPTION! --dry-run
    )
    set remove-untracked=N
    set PN_CAPTION=Removes packages not present in the lock file. ^(Deprecated^)
    call :Read_F remove-untracked "yN" 0 || exit /b 1
    rem echo ..P1.. remove-untracked: !remove-untracked!
    if defined remove-untracked (
        set OPTION=!OPTION! --remove-untracked
    )
    set extras=
    set PN_CAPTION=Extra sets of dependencies to install. ^(multiple values allowed^)
    call :Read_P extras "" || exit /b 1
    rem echo ..P1.. extras: !extras!
    if defined extras (
        set OPTION=!OPTION! --extras=!extras!
    )
    set all-extras=Y
    set PN_CAPTION=Install all extra dependencies
    call :Read_F all-extras "yN" 0 || exit /b 1
    rem echo ..P1.. all-extras: !all-extras!
    if defined all-extras (
        set OPTION=!OPTION! --all-extras
    )
    set only-root=N
    set PN_CAPTION=Exclude all dependencies
    call :Read_F only-root "yN" 0 || exit /b 1
    rem echo ..P1.. only-root: !only-root!
    if defined only-root (
        set OPTION=!OPTION! --only-root
    )
    set compile=N
    set PN_CAPTION=Compile Python source files to bytecode. ^(This option has no effect if modern-installation is disabled because the old installer always compiles.^)
    call :Read_F compile "yN" 0 || exit /b 1
    rem echo ..P1.. compile: !compile!
    if defined compile (
        set OPTION=!OPTION! --compile
    )

    rem -------------------------------------
    rem ARGS
    rem -------------------------------------
    rem Проверка на обязательные аргументы

    exit /b 0
rem endfunction

rem =================================================
rem ФУНКЦИИ LIB
rem =================================================
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
:PressAnyKey
%LIB_BAT%\LYRSupport.bat %*
exit /b 0
rem =================================================
