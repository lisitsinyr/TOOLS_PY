"""PhotoSort.py"""
# -*- coding: UTF-8 -*-
__annotations__ = """
 =======================================================
 Copyright (c) 2025
 Author:
     Lisitsin Y.R.
 Project:
     SCRIPTS_PY
 Module:
     PhotoSort.py
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
import filecmp

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------
import speedtest
import pyspeedtest

import moviepy
# from moviepy.editor import VideoFileClip

import os
import shutil
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime

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

# Путь к папке с фотографиями
source_folder = r"D:\PROJECTS_LYR\CHECK_LIST\DESKTOP\Python\PROJECTS_PY\SCRIPTS_PY\SRC\00.TEST\PhotoSort\20250324"
destination_folder = r"D:\PROJECTS_LYR\CHECK_LIST\DESKTOP\Python\PROJECTS_PY\SCRIPTS_PY\SRC\00.TEST\PhotoSort\20250324_sort"

#------------------------------------------
# func_pass ()
#------------------------------------------
def func_pass():
    """func_pass"""
#beginfunction
    pass
#endfunction

#------------------------------------------
# get_date(photo_path):
#------------------------------------------
def get_date(photo_path):
    """get_date"""
    # Получение даты съёмки из метаданных или даты создания файла
#beginfunction
    try:
        # Пытаемся получить дату из EXIF
        image = Image.open(photo_path)
        exif_data = image._getexif()
        if exif_data:
            for tag, value in exif_data.items():
                if TAGS.get(tag) == "DateTimeOriginal":
                    return value.split(" ")[0].replace(":", "-")
    except Exception as e:
        print(f"Ошибка чтения EXIF для {photo_path}: {e}")

    # Если EXIF недоступен, используем дату создания файла
    try:
        creation_time = os.path.getctime(photo_path)
        return datetime.fromtimestamp(creation_time).strftime("%Y-%m-%d")
    except Exception as e:
        print(f"Ошибка получения даты создания для {photo_path}: {e}")
        return "unknown"
#endfunction

#------------------------------------------
# sort_photos():
#------------------------------------------
def sort_photos():
    """sort_photos"""
    # Сортировка фотографий
#beginfunction
    for filename in os.listdir(source_folder):
        file_path = os.path.join(source_folder, filename)

        # Проверяем, является ли файл изображением
        if os.path.isfile(file_path) and filename.lower().endswith((".jpg", ".jpeg", ".png")):
            date_folder_name = get_date(file_path)

            # Создаём папку по дате
            date_folder = os.path.join(destination_folder, date_folder_name)
            os.makedirs(date_folder, exist_ok=True)

            # Перемещаем файл
            shutil.move(file_path, os.path.join(date_folder, filename))
            print(f"{filename} → {date_folder}")
#endfunction

#------------------------------------------
def main ():
    """main"""
#beginfunction
    LUConst.SET_LIB(__file__)

    LULog.STARTLogging (LULog.TTypeSETUPLOG.tslINI, 'console', LUConst.GDirectoryLOG, LUConst.GFileNameLOG,
                        LUConst.GFileNameLOGjson)
    LULog.LoggerTOOLS.level = logging.INFO

    LPath = LUFile.ExtractFileDir(__file__)
    print (f'LPath: {LPath}')

    #--------------------------------------------------------------
    #
    #--------------------------------------------------------------
    # Запускаем сортировку
    sort_photos()

    LULog.STOPLogging ()
#endfunction

#------------------------------------------
#
#------------------------------------------
#beginmodule
if __name__ == "__main__":
    main ()
# endif

# endmodule
