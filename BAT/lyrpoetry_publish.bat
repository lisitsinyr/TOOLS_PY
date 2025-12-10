@echo off
rem -------------------------------------------------------------------
rem lyrpoetry_publishbuild.bat
rem -------------------------------------------------------------------
rem Запуск poetry из глобального виртуального пространства
rem -------------------------------------------------------------------
rem 
rem Description:
rem   Publishes a package to a remote repository.
rem   The build command builds the source and wheels archives.
rem 
rem Usage:
rem   publish [options]
rem 
rem Options:
rem   -r, --repository=REPOSITORY    The repository to publish the package to.
rem   -u, --username=USERNAME        The username to access the repository.
rem   -p, --password=PASSWORD        The password to access the repository.
rem       --cert=CERT                Certificate authority to access the repository.
rem       --client-cert=CLIENT-CERT  Client certificate to access the repository.
rem       --dist-dir=DIST-DIR        Dist directory where built artifact are stored. Default is `dist`. [default: "dist"]
rem       --build                    Build the package before publishing.
rem       --dry-run                  Perform all actions except upload the package.
rem       --skip-existing            Ignore errors from files already existing in the repository.
rem   -h, --help                     Display help for the given command. When no command is given display help for the list command.
rem   -q, --quiet                    Do not output any message.
rem   -V, --version                  Display this application version.
rem       --ansi                     Force ANSI output.
rem       --no-ansi                  Disable ANSI output.
rem   -n, --no-interaction           Do not ask any interactive question.
rem       --no-plugins               Disables plugins.
rem       --no-cache                 Disables Poetry source caches.
rem   -C, --directory=DIRECTORY      The working directory for the Poetry command (defaults to the current working directory).
rem   -v|vv|vvv, --verbose           Increase the verbosity of messages: 1 for normal output, 2 for more verbose output and 3 for debug.
rem 
rem Help:
rem   The publish command builds and uploads the package to a remote repository.
rem   
rem   By default, it will upload to PyPI but if you pass the --repository option it will
rem   upload to it instead.
rem   
rem   The --repository option should match the name of a configured repository using
rem   the config command.
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

    echo Publishes a package to a remote repository ...
    set COMMAND=publish
    
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
    set repository=
    set PN_CAPTION=The repository to publish the package to
    call :Read_P repository "" || exit /b 1
    rem echo repository: !repository!
    if defined repository (
        set OPTION=!OPTION! --repository=!repository!
    )
    set username=
    set PN_CAPTION=The username to access the repository
    call :Read_P username "" || exit /b 1
    rem echo username: !username!
    if defined username (
        set OPTION=!OPTION! --username=!username!
    )
    set password=
    set PN_CAPTION=The password to access the repository
    call :Read_P password "" || exit /b 1
    rem echo password: !password!
    if defined password (
        set OPTION=!OPTION! --password=!password!
    )
    set cert=
    set PN_CAPTION=Certificate authority to access the repository
    call :Read_P cert "" || exit /b 1
    rem echo cert: !cert!
    if defined cert (
        set OPTION=!OPTION! --cert=!cert!
    )
    set client-cert=
    set PN_CAPTION=Client certificate to access the repository
    call :Read_P client-cert "" || exit /b 1
    rem echo client-cert: !client-cert!
    if defined client-cert (
        set OPTION=!OPTION! --client-cert=!client-cert!
    )
    set dist-dir=
    set PN_CAPTION=Dist directory where built artifact are stored. Default is `dist`. [default: "dist"]
    call :Read_P dist-dir "" || exit /b 1
    rem echo dist-dir: !dist-dir!
    if defined dist-dir (
        set OPTION=!OPTION! --dist-dir=!dist-dir!
    )
    set build=Y
    set PN_CAPTION=Build the package before publishing
    call :Read_F build "yN" 0 || exit /b 1
    rem echo build: !build!
    if defined build (
        set OPTION=!OPTION! --build
    )
    set dry-run=Y
    set PN_CAPTION=Perform all actions except upload the package
    call :Read_F dry-run "yN" 0 || exit /b 1
    rem echo dry-run: !dry-run!
    if defined dry-run (
        set OPTION=!OPTION! --dry-run
    )
    set skip-existing=N
    set PN_CAPTION=Ignore errors from files already existing in the repository
    call :Read_F skip-existing "yN" 0 || exit /b 1
    rem echo skip-existing: !skip-existing!
    if defined skip-existing (
        set OPTION=!OPTION! --skip-existing
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
