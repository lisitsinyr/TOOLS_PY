rem Инициализирует новый Python-проект с дефолтной структурой

rem Содержимое директории после создания проекта:
rem .gitignore
rem .python-version
rem hello.py
rem pyproject.toml
rem README.md

rem uv init --no-workspace d:\work\project
rem cd d:\work\project

uv init --no-workspace %1
cd %1
