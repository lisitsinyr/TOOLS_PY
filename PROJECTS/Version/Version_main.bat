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
set PYDir=D:\TOOLS\TOOLS_PY\PY
:PYDir_Exit
rem -------------------------------------------------------------------

rem -------------------------------------------------------------------
:A_P1_1
if "%1" == "" goto A_P1_2
set P1="%1"
goto A_P1_Exit
:A_P1_2
set P1=C:\Program Files\Far Manager\Far.exe
:A_P1_Exit
rem -------------------------------------------------------------------

:Begin
set PYTHONPATH=%PYDir%
python.exe Version_main.py -P1="%P1%"

:Exit
