"""CreateLNK.py"""
# -*- coding: UTF-8 -*-
__annotations__ = """
 =======================================================
 Copyright (c) 2024
 Author:
     Lisitsin Y.R.
 Project:
     SCRIPTS_PY
 Module:
     CreateLNK.py
 =======================================================
"""

#------------------------------------------
# БИБЛИОТЕКИ python
#------------------------------------------
import os
# Получить текущий рабочий каталог
current_directory = os.getcwd ()
import sys

from pathlib import Path
from win32com.client import Dispatch

# import textwrap
# import stat
# import chardet
# from chardet.universaldetector import UniversalDetector
# from charset_normalizer import detect
# import logging

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------

#------------------------------------------
# БИБЛИОТЕКА LU
#------------------------------------------
import lyrpy.LULog as LULog
import lyrpy.LUConst as LUConst
import lyrpy.LUFile as LUFile
import lyrpy.LUParserARG as LUParserARG
import lyrpy.LUFileUtils as LUFileUtils
from lyrpy.LUFileUtils import GMask

#------------------------------------------
#CONST
#------------------------------------------

import os
import sys
from pathlib import Path
from win32com.client import Dispatch


#-----------------------------------------------------------
# WorkFileName ()
#-----------------------------------------------------------
def WorkFileName (AFilePath: str):
# def create_shortcut(target_path, shortcut_path, icon_path=None, arguments=None, working_directory=None):
    """WorkFileName
    Создает ярлык (.lnk) для указанного пути.
    :param target_path: Путь к целевому файлу/программе.
    :param shortcut_path: Путь для сохранения ярлыка.
    :param icon_path: Путь к иконке (необязательно).
    :param arguments: Аргументы командной строки (необязательно).
    :param working_directory: Рабочая директория (необязательно).
    """
#beginfunction
    # Пример использования
    #create_shortcut(target, shortcut, icon, args, work_dir)

    # Целевой файл
    target = r"C:\Program Files\Notepad++\notepad++.exe"  
    target = AFilePath

    # Путь к ярлыку на рабочем столе
    LFileName = LUFile.ExtractFileName (AFilePath)
    shortcut = Path.home() / "Desktop" / "Notepad++.lnk"  
    shortcut = Path.home() / "Desktop" / LFileName ".lnk"

    # Иконка (можно оставить None)
    icon = r"C:\Program Files\Notepad++\notepad++.exe"    
    icon = AFilePath

    # Аргументы (можно оставить None)
    args = "--multiInst"                                 
    args = ''

    # Рабочая директория (можно оставить None)
    LDirectory = LUFile.ExtractFileDir (AFilePath)
    LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, f'Каталог = {LDirectory}')
    work_dir = r"C:\Program Files\Notepad++"             
    work_dir = LDirectory

    # Создаем объект ярлыка
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortcut(str(shortcut_path))

    # Задаем параметры ярлыка
    shortcut.Targetpath = str(target_path)
    if icon_path:
        shortcut.IconLocation = str(icon_path)
    if arguments:
        shortcut.Arguments = arguments
    if working_directory:
        shortcut.WorkingDirectory = str(working_directory)

    # Сохраняем ярлык
    shortcut.Save()

    print(f"Ярлык успешно создан: {shortcut_path}")
#endfunction

if __name__ == "__main__":
    
#------------------------------------------
# sys.argv[1] - <file>, <directory>, <directory>\<pattern>
# sys.argv[2] - <width>
#------------------------------------------
def main ():
    """main"""
#beginfunction
    LUConst.SET_LIB(__file__)

    LULog.STARTLogging (LULog.TTypeSETUPLOG.tslINI,'console', LUConst.GDirectoryLOG, LUConst.GFileNameLOG,
                        LUConst.GFileNameLOGjson)
    LULog.LoggerTOOLS.level = logging.INFO

    LArgParser = LUParserARG.TArgParser (description = 'Параметры', prefix_chars = '-/')
    LArg = LArgParser.ArgParser.add_argument ('-fp', '--filepath', type = str, default='', help = 'filepath')
    Largs = LArgParser.ArgParser.parse_args ()

    LFilePath = Largs.filepath
    LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, f'FilePath = {LFilePath}')

    #-------------------------------------------------------
    # LFilePath - это файл
    #-------------------------------------------------------
    if os.path.isfile (LFilePath):
        LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, 'это файл ...')

        WorkFileName (LFilePath)
    #endif
    
    LULog.STOPLogging ()
#endfunction

#------------------------------------------
#
#------------------------------------------
#beginmodule
if __name__ == "__main__":
    # print(f'Вызов функции {__name__}')
    main()
#endif

#endmodule
