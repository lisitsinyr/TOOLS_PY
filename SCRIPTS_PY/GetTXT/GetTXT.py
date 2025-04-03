"""GetTXT.py"""
# -*- coding: UTF-8 -*-
__annotations__ = """
 =======================================================
 Copyright (c) 2025
 Author:
     Lisitsin Y.R.
 Project:
     SCRIPTS_PY
 Module:
     GetTXT.py
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
import psutil
import time

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------
import random
import string
import tkinter as tk
import pyperclip
import requests # Импортируем библиотеку requests для выполнения HTTP- запросов
import urllib.request as urllib2
import json
import cv2
import pytesseract

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
# get_public_ip()
#------------------------------------------
def get_public_ip() -> None:
    """get_public_ip"""
#beginfunction
    pass
#endfunction

#------------------------------------------
def main ():
    """main"""
#beginfunction
    global text_result
    global pass_length
    global lbl_alert

    LUConst.SET_LIB(__file__)

    LULog.STARTLogging (LULog.TTypeSETUPLOG.tslINI, 'console', LUConst.GDirectoryLOG, LUConst.GFileNameLOG,
                        LUConst.GFileNameLOGjson)
    LULog.LoggerTOOLS.level = logging.INFO

    LPath = LUFile.ExtractFileDir(__file__)
    print(f'LPath: {LPath}')

    #--------------------------------------------------------------
    # 
    #--------------------------------------------------------------
    # Укажите путь к Tesseract (если требуется, например, в Windows)
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    # Путь к изображению (замените на свой файл)
    image_path = r"D:\PROJECTS_LYR\CHECK_LIST\DESKTOP\Python\PROJECTS_PY\SCRIPTS_PY\SRC\00.TEST\GetTXT\test.jpg"

    # Загружаем изображение
    image = cv2.imread(image_path)

    # Преобразуем в оттенки серого для улучшения OCR
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Увеличиваем контраст и убираем шум (адаптивная бинаризация)
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY |
    cv2.THRESH_OTSU)[1]

    # Распознаем текст
    text = pytesseract.image_to_string(gray, lang="eng")  # Можно заменить на "rus" для русского текста

    # Выводим результат
    print("Распознанный текст:\n", text)

    # Отображаем изображение
    # cv2.imshow("Изображение", gray)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
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
