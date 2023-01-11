@echo on
rem -------------------------------------------------------------------
rem
rem -------------------------------------------------------------------
chcp 65001

rem -------------------------------------------------------------------
:PYDir_1
if "%PYDir%" == "" goto PYDir_2
goto PYDir_Exit
:PYDir_2
echo Значение переменной среды PYDIR не установлено
if "%COMPUTERNAME%" == "%USERDOMAIN%" goto PYDir_Local
:PYDir_Network
set PYDir=\\S73FS01\APPInfo\tools
goto PYDir_Exit
:PYDir_Local
set PYDir=D:\PROJECTS_LYR\CHECK_LIST\05_DESKTOP\02_Python\PROJECTS_PY\TOOLS_PY\PY
:PYDir_Exit
rem -------------------------------------------------------------------

rem -------------------------------------------------------------------
:A_Command_1
if "%1" == "" goto A_Command_2
set Command="%1"
goto A_Command_Exit
:A_Command_2
set Command="%1"
:A_Command_Exit
rem -------------------------------------------------------------------

:Begin
set Command=""
python.exe GITPY.py "-PYDir='%PYDir%'"

:Exit
