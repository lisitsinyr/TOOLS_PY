@echo off
rem -------------------------------------------------------------------
rem lyrpy.bat
rem -------------------------------------------------------------------
chcp 1251>NUL

setlocal enabledelayedexpansion

rem Инициализирует новый Python-проект с дефолтной структурой в текущем каталоге

rem Содержимое директории после создания проекта:
rem .gitignore
rem .python-version
rem hello.py
rem pyproject.toml
rem README.md

uv init --no-workspace
