@echo off
rem -------------------------------------------------------------------
rem �������� ������� Pip
rem pip help                    ������� �� ��������
rem pip search package_name     ����� ������
rem pip show package_name       ���������� �� ������
rem pip install package_name    ��������� ������(��)
rem pip uninstall package_name  �������� ������(��)
rem pip list                    ������ ������������� �������
rem pip install -U              ���������� ������(��)
rem -------------------------------------------------------------------
chcp 1251

rem -------------------------------------------------------------------
:P1
if "%1" == "" goto P1_Input
goto Begin
:P1_Input
set /p P1=������� P1:
if "%P1%" == "" goto P1_Error
goto Begin
:P1_Error
echo �������� ��������� P1 �� �����������
goto Exit
rem -------------------------------------------------------------------

:begin
echo P1=%P1%

:Exit
