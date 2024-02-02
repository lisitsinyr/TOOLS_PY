@echo off
rem -------------------------------------------------------------------
rem lyrgit_remote_v.bat
rem ----------------------------------------------------------------------------
rem 6.Сотрудничать [***]
rem ----------------------------------------------------------------------------
rem Верифицируем что удаленный репозитарий связан с нашим
rem ----------------------------------------------------------------------------
rem usage: git remote [-v | --verbose]
rem    or: git remote add [-t <branch>] [-m <master>] [-f] [--tags | --no-tags] [--mirror=<fetch|push>] <name> <url>
rem    or: git remote rename [--[no-]progress] <old> <new>
rem    or: git remote remove <name>
rem    or: git remote set-head <name> (-a | --auto | -d | --delete | <branch>)
rem    or: git remote [-v | --verbose] show [-n] <name>
rem    or: git remote prune [-n | --dry-run] <name>
rem    or: git remote [-v | --verbose] update [-p | --prune] [(<group> | <remote>)...]
rem    or: git remote set-branches [--add] <name> <branch>...
rem    or: git remote get-url [--push] [--all] <name>
rem    or: git remote set-url [--push] <name> <newurl> [<oldurl>]
rem    or: git remote set-url --add <name> <newurl>
rem    or: git remote set-url --delete <name> <url>
rem 
rem     -v, --verbose         be verbose; must be placed before a subcommand
rem -------------------------------------------------------------------
chcp 1251

:begin
echo ---------------------------------------------------------------
echo git remote -v
echo ---------------------------------------------------------------
git remote -v

:Exit
