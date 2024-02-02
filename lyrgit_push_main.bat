@echo off
rem -------------------------------------------------------------------
rem lyrgit_push_main.bat
rem ----------------------------------------------------------------------------
rem ***Отправить изменения
rem ----------------------------------------------------------------------------
rem usage: git push [<options>] [<repository> [<refspec>...]]
rem 
rem     -v, --verbose         be more verbose
rem     -q, --quiet           be more quiet
rem     --repo <repository>   repository
rem     --all                 push all refs
rem     --mirror              mirror all refs
rem     -d, --delete          delete refs
rem     --tags                push tags (can't be used with --all or --mirror)
rem     -n, --dry-run         dry run
rem     --porcelain           machine-readable output
rem     -f, --force           force updates
rem     --force-with-lease[=<refname>:<expect>]
rem                           require old value of ref to be at this value
rem     --force-if-includes   require remote updates to be integrated locally
rem     --recurse-submodules (check|on-demand|no)
rem                           control recursive pushing of submodules
rem     --thin                use thin pack
rem     --receive-pack <receive-pack>
rem                           receive pack program
rem     --exec <receive-pack>
rem                           receive pack program
rem     -u, --set-upstream    set upstream for git pull/status
rem     --progress            force progress reporting
rem     --prune               prune locally removed refs
rem     --no-verify           bypass pre-push hook
rem     --follow-tags         push missing but relevant tags
rem     --signed[=(yes|no|if-asked)]
rem                           GPG sign the push
rem     --atomic              request atomic transaction on remote side
rem     -o, --push-option <server-specific>
rem                           option to transmit
rem     -4, --ipv4            use IPv4 addresses only
rem     -6, --ipv6            use IPv6 addresses only
rem -------------------------------------------------------------------
chcp 1251

rem -------------------------------------------------------------------
rem PROJECTS
rem -------------------------------------------------------------------
rem set PROJECTS="D:\PROJECTS_LYR\CHECK_LIST\01_OS\03_UNIX\PROJECTS_UNIX"
set PROJECTS=%~p0
set LOG_BATFileName=%~f0
set BASENAME=%~n0%~x0
rem set LOG_File=%~d0%PROJECTS%LOGS\%BASENAME%.log
set LOG_File=%~d0%~p0LOGS\%~n0%~x0.log
echo %LOG_File%
echo "***" > %LOG_File%

:begin
echo ---------------------------------------------------------------
echo Check 1 parametr
echo ---------------------------------------------------------------
:P1
if "%1" == "" goto P1_Input
set Comment="%1"
goto begin_git
:P1_Input
set /p Comment=Comment:
if "%Comment%" == "" goto P1_Error
goto begin_git
:P1_Error
echo Parametr Comment not set
set Comment=Git Bash commit update

:begin_git
echo ---------------------------------------------------------------
echo ...git add --all
git add --all >> %LOG_File% 

echo ---------------------------------------------------------------
echo ...git commit -m "%Comment%"
git commit -m "%Comment%" >> %LOG_File% 

echo ---------------------------------------------------------------
echo ...git push -u origin main
git push -u origin main >> %LOG_File% 
echo ---------------------------------------------------------------

rem type %LOG_File%

pause

:Exit
