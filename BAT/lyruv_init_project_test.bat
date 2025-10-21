@echo off
rem -------------------------------------------------------------------
rem lyrpy.bat
rem -------------------------------------------------------------------
chcp 1251>NUL

setlocal enabledelayedexpansion

rem Type project{app,lib,bare,script}
set O1=app

rem python
set O4=3.13

rem [package]
set O2=package

rem [no-workspace]
set O3=

rem projects_dir
set O5=D:\PROJECTS_LYR\CHECK_LIST\DESKTOP\Python\PROJECTS_PY
rem project_name
set O6=

call D:\PROJECTS_LYR\CHECK_LIST\DESKTOP\Python\PROJECTS_PY\UV\SRC\BAT\lyruv_init.bat
