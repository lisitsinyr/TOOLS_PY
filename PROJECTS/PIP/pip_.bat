@echo off
rem -------------------------------------------------------------------
rem Основные команды Pip
rem pip help                    Справка по командам
rem pip search package_name     Поиск пакета
rem pip show package_name       Информация об пакете
rem pip install package_name    Установка пакета(ов)
rem pip uninstall package_name  Удаление пакета(ов)
rem pip list                    Список установленных пакетов
rem pip install -U              Обновление пакета(ов)
rem -------------------------------------------------------------------
chcp 1251

rem -------------------------------------------------------------------
:P1
if "%1" == "" goto P1_Input
goto Begin
:P1_Input
set /p P1=Введите P1:
if "%P1%" == "" goto P1_Error
goto Begin
:P1_Error
echo Значение параметра P1 не установлено
goto Exit
rem -------------------------------------------------------------------

:begin
echo P1=%P1%

:Exit
