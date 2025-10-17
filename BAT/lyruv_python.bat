@echo off
rem -------------------------------------------------------------------
rem lyrpy.bat
rem -------------------------------------------------------------------
chcp 1251>NUL

setlocal enabledelayedexpansion

rem uv python install 3.12

uv python install 3.13

rem uv python install %1

rem -------------------------------------------------------------------
rem Pin a version for your project:
rem -------------------------------------------------------------------
rem cd myproject
rem uv python pin 3.11

rem The .python-version file will be created/updated:
rem 3.11

rem UV will now use this version for all commands in this directory:
rem uv run python --version  # Will use Python 3.11

rem Managing Multiple Installations
rem UV maintains a central location for installed Python versions:

# View Python installation directory
rem uv python dir

# Find specific Python version
rem uv python find 3.11

# Uninstall a version
rem uv python uninstall 3.11.4