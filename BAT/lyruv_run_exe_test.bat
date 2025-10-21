@echo off
rem -------------------------------------------------------------------
rem lyrpy.bat
rem -------------------------------------------------------------------
chcp 1251>NUL

setlocal enabledelayedexpansion

rem app.exe
set A1=D:\TOOLS\KIX\kix32.exe

rem call D:\PROJECTS_LYR\CHECK_LIST\DESKTOP\Python\PROJECTS_PY\UV\SRC\BAT\lyruv_run.bat

uv run !A1!

rem app.exe
set A1=ListFiles.bat
uv run !A1!
