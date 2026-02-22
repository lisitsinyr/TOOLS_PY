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
    set PYTHON=py
    set PYTHON=C:\Users\lyr\AppData\Local\Programs\Python\Python313\python.exe

    rem set project_dir=D:\PROJECTS_LYR\CHECK_LIST\DESKTOP\Python\PROJECTS_PY\lyrpy2
    set project_dir=.

    set Directory=!project_dir!\.venv
    if exist !Directory!\ (
        echo Удаление каталога !Directory! ...
        rmdir /s /q !Directory!
    )

    echo Создание каталога !Directory! ...

    !PYTHON! -m venv .venv

    !PYTHON! -m pip install --upgrade pip

    exit /b 0
:end
rem --------------------------------------------------------------------------------
