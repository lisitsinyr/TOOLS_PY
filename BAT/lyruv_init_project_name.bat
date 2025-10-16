@echo off
rem -------------------------------------------------------------------
rem lyrpy.bat
rem -------------------------------------------------------------------
chcp 1251>NUL

setlocal enabledelayedexpansion

rem Инициализирует новый Python-проект с дефолтной структурой

rem Содержимое директории после создания проекта:
rem .gitignore
rem .python-version
rem hello.py
rem pyproject.toml
rem README.md

rem uv init project_name

uv init %1
