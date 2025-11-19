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

    set VENV=!project_dir!\.venv

    call !VENV!\Scripts\activate.bat

    python --version

    python -m pip install --upgrade pip
    rem pip install --upgrade pip

    pip list

    echo --------------------------------
    uv self version
    echo --------------------------------

    uv python pin !python!

    echo Install packeges requirements.txt ...

    set requirements=!VENV!\requirements.txt
    echo !requirements!
    uv pip freeze > !requirements!
    uv pip freeze > requirements.txt
    uv pip install -r !requirements! > LOG\install.log
    rem uv pip sync !requirements! > LOG\install.log

    rem pip install --upgrade !project_dir!
    
    uv pip list >> LOG\install.log

    exit /b 0
:end
rem --------------------------------------------------------------------------------
