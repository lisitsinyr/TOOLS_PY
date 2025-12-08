@echo off
rem -------------------------------------------------------------------
rem chk.bat
rem -------------------------------------------------------------------
chcp 1251>NUL

setlocal enabledelayedexpansion

rem --------------------------------------------------------------------------------
rem 
rem --------------------------------------------------------------------------------
:begin
    set BATNAME=%~nx0
    echo Start !BATNAME! ...

    rem docker run --rm -it -v "%cd%:/app" -w /app python:3.13-slim bash -lc "pip install -r requirements.txt && python GetMessage.py

    rem docker run --rm -it -v "%cd%:/app" -w /app python:3.13-slim bash -lc "pip install -r requirements.txt && python GetMessage.py

    docker run --rm -it python:3.11-slim python -c "print('Hello, world')"
    
    exit /b 0
:end
rem --------------------------------------------------------------------------------
