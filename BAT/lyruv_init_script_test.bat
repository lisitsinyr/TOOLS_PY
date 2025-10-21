@echo off
rem -------------------------------------------------------------------
rem lyrpy.bat
rem -------------------------------------------------------------------
chcp 1251>NUL

setlocal enabledelayedexpansion

rem Type project{app,lib,bare,script}
set O1=script

rem python
set O4=3.13

rem [package]
set O2=

rem [no-workspace]
set O3=

rem script_dir
set O5=D:\PROJECTS_LYR\CHECK_LIST\DESKTOP\Python\PROJECTS_PY
rem script.py
set O6=

call D:\PROJECTS_LYR\CHECK_LIST\DESKTOP\Python\PROJECTS_PY\UV\SRC\BAT\lyruv_init.bat
