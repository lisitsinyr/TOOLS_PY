@echo off
rem -------------------------------------------------------------------
rem uv_install_pwsh.bat
rem -------------------------------------------------------------------
chcp 1251>NUL

setlocal enabledelayedexpansion

rem --------------------------------------------------------------------------------
rem 
rem --------------------------------------------------------------------------------
:begin
    set BATNAME=%~nx0
    echo Start !BATNAME! ...

    rem Changing the execution policy allows running a script from the internet.
    rem pwsh.exe -ExecutionPolicy ByPass
    rem powershell -c "irm https://astral.sh/uv/install.ps1 | more"
    rem powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

    rem C:\Users\lyr\AppData\Local\Microsoft\WindowsApps\pwsh.exe
    pwsh -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

    exit /b 0
:end
rem =================================================
