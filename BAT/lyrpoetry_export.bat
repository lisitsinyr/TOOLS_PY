@echo off
rem -------------------------------------------------------------------
rem lyrpoetry_export.bat
rem -------------------------------------------------------------------
rem Запуск poetry из глобального виртуального пространства
rem -------------------------------------------------------------------
rem 
rem Description:
rem   Exports the lock file to alternative formats.
rem   This command exports the lock file to other formats.
rem 
rem Usage:
rem   export [options]
rem 
rem Options:
rem   -f, --format=FORMAT        Format to export to. Currently, only constraints.txt and requirements.txt are supported. [default: "requirements.txt"]
rem   -o, --output=OUTPUT        The name of the output file.
rem       --without-hashes       Exclude hashes from the exported file.
rem       --without-urls         Exclude source repository urls from the exported file.
rem       --dev                  Include development dependencies. (Deprecated)
rem       --without=WITHOUT      The dependency groups to ignore. (multiple values allowed)
rem       --with=WITH            The optional dependency groups to include. (multiple values allowed)
rem       --only=ONLY            The only dependency groups to include. (multiple values allowed)
rem   -E, --extras=EXTRAS        Extra sets of dependencies to include. (multiple values allowed)
rem       --all-extras           Include all sets of extra dependencies.
rem       --with-credentials     Include credentials for extra indices.
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
        set SCRIPTS_DIR=D:\PROJECTS_LYR\CHECK_LIST\SCRIPT\BAT\PROJECTS_BAT\TOOLS_BAT
    )
    rem echo SCRIPTS_DIR: %SCRIPTS_DIR%
    rem -------------------------------------------------------------------
    rem LIB_BAT - каталог библиотеки скриптов
    rem -------------------------------------------------------------------
    if not defined LIB_BAT (
        set LIB_BAT=!SCRIPTS_DIR!\SRC\LIB
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

    echo Exports the lock file to alternative formats ...
    set COMMAND=export
    
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
    set format=
    set PN_CAPTION=Format to export to. Currently, only constraints.txt and requirements.txt are supported. [default: "requirements.txt"]
    call :Read_P format "" || exit /b 1
    rem echo format: !format!
    if not "!format!"=="" (
        set OPTION=!OPTION! --format=!format!
    )
    set output=
    set PN_CAPTION=The name of the output file
    call :Read_P output "" || exit /b 1
    rem echo output: !output!
    if not "!output!"=="" (
        set OPTION=!OPTION! --output=!output!
    )
    set without-hashes=Y
    set PN_CAPTION=Exclude hashes from the exported file
    call :Read_F without-hashes "yN" 0 || exit /b 1
    rem echo without-hashes: !without-hashes!
    if not "!without-hashes!"=="" (
        set OPTION=!OPTION! --without-hashes
    )
    set without-urls=Y
    set PN_CAPTION=Exclude source repository urls from the exported file
    call :Read_F without-urls "yN" 0 || exit /b 1
    rem echo without-urls: !without-urls!
    if not "!without-urls!"=="" (
        set OPTION=!OPTION! --without-urls
    )
    set dev=Y
    set PN_CAPTION=Include development dependencies. ^(Deprecated^)
    call :Read_F dev "yN" 0 || exit /b 1
    rem echo dev: !dev!
    if not "!dev!"=="" (
        set OPTION=!OPTION! --dev
    )
    set without=
    set PN_CAPTION=The dependency groups to ignore. ^(multiple values allowed^)
    call :Read_P without "" || exit /b 1
    rem echo without: !without!
    if not "!without!"=="" (
        set OPTION=!OPTION! --without=!without!
    )
    set with=
    set PN_CAPTION=The optional dependency groups to include. ^(multiple values allowed^)
    call :Read_P with "" || exit /b 1
    rem echo with: !with!
    if not "!with!"=="" (
        set OPTION=!OPTION! --with=!with!
    )
    set only=
    set PN_CAPTION=The only dependency groups to include. ^(multiple values allowed^)
    call :Read_P only "" || exit /b 1
    rem echo only: !only!
    if not "!only!"=="" (
        set OPTION=!OPTION! --only=!only!
    )
    set extras=
    set PN_CAPTION=Extra sets of dependencies to include. ^(multiple values allowed^)
    call :Read_P extras "" || exit /b 1
    rem echo extras: !extras!
    if not "!extras!"=="" (
        set OPTION=!OPTION! --extras=!extras!
    )
    set all-extras=Y
    set PN_CAPTION=Include all sets of extra dependencies
    call :Read_F all-extras "yN" 0 || exit /b 1
    rem echo all-extras: !all-extras!
    if not "!all-extras!"=="" (
        set OPTION=!OPTION! --all-extras
    )
    set with-credentials=Y
    set PN_CAPTION=Include credentials for extra indices
    call :Read_F with-credentials "yN" 0 || exit /b 1
    rem echo with-credentials: !with-credentials!
    if not "!with-credentials!"=="" (
        set OPTION=!OPTION! --with-credentials
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
%LIB_BAT%\LYRConst.bat %*
exit /b 0
:SET_POETRY
%LIB_BAT%\LYRConst.bat %*
exit /b 0
:SET_KIX
%LIB_BAT%\LYRConst.bat %*
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
