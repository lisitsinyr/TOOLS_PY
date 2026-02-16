@echo off
rem -------------------------------------------------------------------
rem lyr_uv_install_pwsh.bat
rem -------------------------------------------------------------------
chcp 1251>NUL

setlocal enabledelayedexpansion

rem --------------------------------------------------------------------------------
rem 
rem --------------------------------------------------------------------------------
:begin
    set BATNAME=%~nx0
    echo Start !BATNAME! ...

    rem "C:\Program Files\PowerShell\7\pwsh.exe"
    rem C:\Users\lyr\AppData\Local\Microsoft\WindowsApps\pwsh.exe

    rem Changing the execution policy allows running a script from the internet.
    rem pwsh.exe -ExecutionPolicy ByPass
   
    pwsh.exe -WorkingDirectory ~ -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

    rem powershell -WorkingDirectory ~ -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    rem powershell -c "irm https://astral.sh/uv/install.ps1 | more"

    exit /b 0
:end
rem =================================================
