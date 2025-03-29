@echo off
rem -------------------------------------------------------------------
rem CLOCK.bat
rem -------------------------------------------------------------------
chcp 1251>NUL

setlocal enabledelayedexpansion

:begin
    set BATNAME=%~nx0
    echo Старт !BATNAME! ...

    python CLOCK.py

    exit /b 0
:end

rem ===================================================================
