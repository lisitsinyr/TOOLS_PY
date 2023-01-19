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
:A_Format_1
if "%1" == "" goto A_Format_2
set Format="%1"
goto A_Format_Exit
:A_Format_2
set Format=1
:A_Format_Exit
rem -------------------------------------------------------------------

rem -------------------------------------------------------------------
:A_NLevel_1
if "%2" == "" goto A_NLevel_2
set NLevel="%2"
goto A_NLevel_Exit
:A_NLevel_2
set NLevel=1
:A_NLevel_Exit
rem -------------------------------------------------------------------

:Begin
rem python.exe ListDir.py "-PYDir='%PYDir%'" -Format=%Format% -NLevel=%NLevel%
set PYTHONPATH=%PYDir%
python.exe ListDir.py -Format=%Format% -NLevel=%NLevel%

:Exit
