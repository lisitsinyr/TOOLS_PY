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
    
    rem set file_stop=G:\___ÐÀÇÁÎÐ\YOUTUBE\TELEGRAM\stop
    set file_stop=G:\___ÐÀÇÁÎÐ\TELEGRAM\stop

    rem echo ..P1.. off > !file_stop! & echo on

    rem type nul > !file_stop!

    copy nul !file_stop! > nul

    rem rem. > !file_stop!

    rem wininit > !file_stop!

    rem fsutil file createnew !file_stop! 0 > nul

    rem break > !file_stop!

    exit /b 0
:end
rem --------------------------------------------------------------------------------
