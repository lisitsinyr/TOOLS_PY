@echo off
rem -------------------------------------------------------------------
rem lyrpoetry_add.bat
rem -------------------------------------------------------------------
rem Запуск poetry из глобального виртуального пространства
rem -------------------------------------------------------------------
rem 
rem Description:
rem   Adds a new dependency to pyproject.toml.
rem   The add command adds required packages to your pyproject.toml and installs them.
rem 
rem Usage:
rem   add [options] [--] <name>...
rem 
rem Arguments:
rem   name                       The packages to add.
rem 
rem Options:
rem   -G, --group=GROUP          The group to add the dependency to. [default: "main"]
rem   -D, --dev                  Add as a development dependency. (Deprecated) Use --group=dev instead.
rem   -e, --editable             Add vcs/path dependencies as editable.
rem   -E, --extras=EXTRAS        Extras to activate for the dependency. (multiple values allowed)
rem       --optional             Add as an optional dependency.
rem       --python=PYTHON        Python version for which the dependency must be installed.
rem       --platform=PLATFORM    Platforms for which the dependency must be installed.
rem       --source=SOURCE        Name of the source to use to install the package.
rem       --allow-prereleases    Accept prereleases.
rem       --dry-run              Output the operations but do not execute anything (implicitly enables --verbose).
rem       --lock                 Do not perform operations (only update the lockfile).
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
rem   The add command adds required packages to your pyproject.toml and installs them.
rem   
rem   If you do not specify a version constraint, poetry will choose a suitable one based on the available package versions.
rem   
rem   You can specify a package in the following forms:
rem     - A single name (requests)
rem     - A name and a constraint (requests@^2.23.0)
rem     - A git url (git+https://github.com/python-poetry/poetry.git)
rem     - A git url with a revision (git+https://github.com/python-poetry/poetry.git#develop)
rem     - A git SSH url (git+ssh://github.com/python-poetry/poetry.git)
rem     - A git SSH url with a revision (git+ssh://github.com/python-poetry/poetry.git#develop)
rem     - A file path (../my-package/my-package.whl)
rem     - A directory (../my-package/)
rem     - A url (https://example.com/packages/my-package-0.1.0.tar.gz)
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
rem procedure MAIN_CHECK_PARAMETR ()
rem --------------------------------------------------------------------------------
:MAIN_CHECK_PARAMETR
rem beginfunction
    set FUNCNAME=%0
    set FUNCNAME=MAIN_CHECK_PARAMETR
    if defined DEBUG (
        echo DEBUG: procedure !FUNCNAME! ...
    )

    rem -------------------------------------
    rem OPTION
    rem -------------------------------------
    set group=
    set PN_CAPTION=The group to add the dependency to
    set PN_CAPTION=Группа, в которую нужно добавить зависимость
    call :Read_P group "" || exit /b 1
    rem echo group: !group!
    if defined group (
        set OPTION=!OPTION! --group !group!
    )
    set dev=N
    set PN_CAPTION=Add as a development dependency. (Deprecated) Use --group=dev instead
    set PN_CAPTION=Добавить в качестве зависимости от разработки. (Deprecated) Use --group=dev instead
    call :Read_F dev "yN" 0 || exit /b 1
    rem echo dev: !dev!
    if defined editable (
        set OPTION=!OPTION! --dev
    )
    set editable=N
    set PN_CAPTION=Add vcs/path dependencies as editable
    set PN_CAPTION=Добавьте зависимости vcs/path в качестве редактируемых
    call :Read_F editable "yN" 0 || exit /b 1
    rem echo editable: !editable!
    if defined editable (
        set OPTION=!OPTION! --editable
    )
    set extras=
    set PN_CAPTION=Extras to activate for the dependency. ^(multiple values allowed^)
    set PN_CAPTION=Дополнительные функции, которые необходимо активировать для зависимости. ^(multiple values allowed^)
    call :Read_P extras "" || exit /b 1
    rem echo extras: !extras!
    if defined extras  (
        set OPTION=!OPTION! --extras !extras!
    )
    set optional=N
    set PN_CAPTION=Add as an optional dependency
    set PN_CAPTION=Добавить в качестве необязательной зависимости
    call :Read_F optional "yN" 0 || exit /b 1
    rem echo optional: !optional!
    if defined optional (
        set OPTION=!OPTION! --optional
    )
    set python=
    set PN_CAPTION=Python version for which the dependency must be installed
    set PN_CAPTION=Версия Python, для которой должна быть установлена зависимость
    call :Read_P python "" || exit /b 1
    rem echo python: !python!
    if defined python (
        set OPTION=!OPTION! --python !python!
    )
    set platform=
    set PN_CAPTION=Platforms for which the dependency must be installed
    set PN_CAPTION=Платформы, для которых должна быть установлена зависимость
    call :Read_P platform "" || exit /b 1
    rem echo platform: !platform!
    if defined platform (
        set OPTION=!OPTION! --platform !platform!
    )
    set source=
    set PN_CAPTION=Name of the source to use to install the package
    set PN_CAPTION=Имя источника, используемого для установки пакета
    call :Read_P source "" || exit /b 1
    rem echo source: !source!
    if defined source (
        set OPTION=!OPTION! --source !source!
    )
    set allow-prereleases=N
    set PN_CAPTION=Accept prereleases
    set PN_CAPTION=Принимать предварительные релизы
    call :Read_F allow-prereleases "yN" 0 || exit /b 1
    rem echo allow-prereleases: !allow-prereleases!
    if defined allow-prereleases (
        set OPTION=!OPTION! --allow-prereleases
    )
    set dry-run=N
    set PN_CAPTION=Output the operations but do not execute anything ^(implicitly enables -verbose^)
    set PN_CAPTION=Выводите операции, но ничего не выполняйте ^(implicitly enables -verbose^)
    call :Read_F dry-run "yN" 0 || exit /b 1
    rem echo dry-run: !dry-run!
    if defined dry-run (
        set OPTION=!OPTION! --dry-run
    )
    set lock=N
    set PN_CAPTION=Do not perform install [only update the lockfile]
    set PN_CAPTION=Не выполняйте установку [only update the lockfile]
    call :Read_F lock "yN" 0 || exit /b 1
    rem echo lock: !lock!
    if defined lock (
        set OPTION=!OPTION! --lock
    )

    rem -------------------------------------
    rem ARGS
    rem -------------------------------------
    rem Проверка на обязательные аргументы
    set names=
    set PN_CAPTION=The packages to add
    set PN_CAPTION=Пакеты для добавления
    call :Read_P names "" || exit /b 1
    rem echo names: !names!
    if defined names (
        set ARGS=!ARGS! !names!
    ) else (
        echo ERROR: names not defined ...
        set OK=yes
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

    set CAPTION=Adds a new dependency to pyproject.toml ...
    set CAPTION=Добавляет новую зависимость к pyproject.toml...
    echo !CAPTION!
    set COMMAND=add

    if not defined Read_N (
        set APPRUN=!APP! !COMMAND!!OPTION!!ARGS!
    ) else (
        set APPRUN=!APP! !COMMAND!!OPTION! %*
    )
    echo APPRUN: !APPRUN!
    !APPRUN!

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
