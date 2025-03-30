"""FileRenamer.py"""
# -*- coding: UTF-8 -*-
__annotations__ = """
 =======================================================
 Copyright (c) 2025
 Author:
     Lisitsin Y.R.
 Project:
     SCRIPTS_PY
 Module:
     FileRenamer.py
 =======================================================
"""

#------------------------------------------
# БИБЛИОТЕКИ python
#------------------------------------------
import os
import sys
import argparse
import logging
import shutil

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------

#------------------------------------------
# БИБЛИОТЕКА lyrpy
#------------------------------------------
import lyrpy.LUos as LUos
import lyrpy.LUDoc as LUDoc
import lyrpy.LULog as LULog
import lyrpy.LUConst as LUConst
import lyrpy.LUDoc as LUDoc
import lyrpy.LULog as LULog
import lyrpy.LUFile as LUFile
import lyrpy.LUParserARG as LUParserARG

#------------------------------------------
# get_exif(filename)
#------------------------------------------
def rename_files_in_directory(directory, prefix, suffix):
    """rename_files_in_directory"""
#beginfunction
    if not os.path.isdir(directory):
        print("Указанная директория не существует.")
        return
    #endif

    # Проходим по всем файлам в директории
    for count, filename in enumerate(os.listdir(directory)):
        # Получаем расширение файла
        file_extension = os.path.splitext(filename)[1]

        # Формируем новое имя файла
        new_name = f"{prefix}_{count + 1}{suffix}{file_extension}"

        # Соединяем директорию и имя файла
        old_file = os.path.join(directory, filename)
        new_file = os.path.join(directory, new_name)

        # Переименовываем файл
        os.rename(old_file, new_file)
        print(f"Переименовано: '{filename}' в '{new_name}'")
    #endfor
#endfunction

#------------------------------------------
def main ():
    """main"""
#beginfunction
    # LUConst.SET_CONST(__file__)
    LUConst.SET_LIB(__file__)

    LULog.STARTLogging (LULog.TTypeSETUPLOG.tslINI, 'console', LUConst.GDirectoryLOG, LUConst.GFileNameLOG,
                        LUConst.GFileNameLOGjson)
    LULog.LoggerTOOLS.level = logging.INFO

    LPath = LUFile.ExtractFileDir(__file__)
    print(f'LPath: {LPath}')

    #-------------------------------------------------
    # Запрашиваем у пользователя параметры
    #-------------------------------------------------
    directory = input("Введите путь к директории: ")
    prefix = input("Введите префикс для новых имен: ")
    suffix = input("Введите суффикс для новых имен: ")

    #-------------------------------------------------
    # Вызываем функцию переименования файлов
    #-------------------------------------------------
    rename_files_in_directory(directory, prefix, suffix)
    
    LULog.STOPLogging ()
#endfunction

#------------------------------------------
#
#------------------------------------------
#beginmodule
if __name__ == "__main__":
    main()
#endif

#endmodule


