@echo off
rem -------------------------------------------------------------------
rem create_venv.bat
rem -------------------------------------------------------------------
chcp 1251>NUL

setlocal enabledelayedexpansion

rem --------------------------------------------------------------------------------
rem 
rem --------------------------------------------------------------------------------
:begin
    set python=3.13
    rem set UV_MANAGED_PYTHON=!python!

    rem set project_dir=D:\PROJECTS_LYR\CHECK_LIST\DESKTOP\Python\PROJECTS_PY\lyrpy2
    set project_dir=.

    set Directory=!project_dir!\.venv
    if exist !Directory!\ (
        echo Удаление каталога !Directory! ...
        rmdir /s /q !Directory!
    )

    rem echo ..P1.. --------------------------------
    rem uv --version
    rem echo ..P1.. --------------------------------

    echo --------------------------------
    uv self version
    echo --------------------------------

    rem echo ..P1.. --------------------------------
    rem uv self update
    rem echo ..P1.. --------------------------------

    echo Создание каталога !Directory! ...

    uv python pin !python!

    set OPTION=--python !python!
    rem uv venv !OPTION! !project_dir!\.venv
    uv venv !project_dir!\.venv

    uv pip install pip

    exit /b 0
:end
rem --------------------------------------------------------------------------------
