@echo off
rem -------------------------------------------------------------------
rem lyrgit_status_long.bat
rem -------------------------------------------------------------------
rem 3.Изучить историю и состояние [***]
rem ----------------------------------------------------------------------------
rem Состояние рабочего каталога и раздела проиндексированных файлов
rem -------------------------------------------------------------------
rem usage: git status [<options>] [--] [<pathspec>...]
rem 
rem     -v, --[no-]verbose    be verbose
rem     -s, --[no-]short      show status concisely
rem     -b, --[no-]branch     show branch information
rem     --[no-]show-stash     show stash information
rem     --[no-]ahead-behind   compute full ahead/behind values
rem     --[no-]porcelain[=<version>]
rem                           machine-readable output
rem     --[no-]long           show status in long format (default)
rem     -z, --[no-]null       terminate entries with NUL
rem     -u, --[no-]untracked-files[=<mode>]
rem                           show untracked files, optional modes: all, normal, no. (Default: all)
rem     --[no-]ignored[=<mode>]
rem                           show ignored files, optional modes: traditional, matching, no. (Default: traditional)
rem     --[no-]ignore-submodules[=<when>]
rem                           ignore changes to submodules, optional when: all, dirty, untracked. (Default: all)
rem     --[no-]column[=<style>]
rem                           list untracked files in columns
rem     --no-renames          do not detect renames
rem     --renames             opposite of --no-renames
rem     -M, --find-renames[=<n>]
rem                           detect renames, optionally set similarity index
rem -------------------------------------------------------------------
chcp 1251

:begin
echo ---------------------------------------------------------------
echo git status --long
echo ---------------------------------------------------------------
rem показывать статус в длинном формате (по умолчанию)
git status --long

:Exit
