@echo off
rem -------------------------------------------------------------------
rem install_pip.bat
rem -------------------------------------------------------------------
chcp 1251>NUL

setlocal enabledelayedexpansion

rem --------------------------------------------------------------------------------
rem 
rem --------------------------------------------------------------------------------
:begin
    rem set PYTHON=python
    set PYTHON=C:\Users\lyr\AppData\Local\Programs\Python\Python313\python.exe

    rem set project_dir=D:\PROJECTS_LYR\CHECK_LIST\DESKTOP\Python\PROJECTS_PY\lyrpy2
    set project_dir=.

    set VENV=!project_dir!\.venv

    call !VENV!\Scripts\activate.bat

    python -m pip install --upgrade pip

    rem python -m pip install build
    rem python -m pip install setuptools
    rem python -m pip install psutil

    rem pip install build
    rem pip install setuptools
    rem pip install psutil

    rem Команда pip install -U <имя пакета> в Python означает «обновить библиотеку до актуальной версии»
    rem pip install -U D:\PROJECTS_LYR\CHECK_LIST\DESKTOP\Python\PROJECTS_PY\lyrpy2

    echo Install packeges requirements.txt ...

    set requirements=!VENV!\requirements.txt
    echo !requirements!
    pip freeze > !requirements!
    pip freeze > requirements.txt
    pip install -r !requirements! > LOG\install.log

    rem pip install --upgrade !project_dir!
    
    pip list >> LOG\install.log

    call !VENV!\Scripts\deactivate.bat

    exit /b 0
:end
rem --------------------------------------------------------------------------------
