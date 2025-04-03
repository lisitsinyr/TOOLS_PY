"""Macros.py"""
# -*- coding: UTF-8 -*-
__annotations__ = """
 =======================================================
 Copyright (c) 2025
 Author:
     Lisitsin Y.R.
 Project:
     SCRIPTS_PY
 Module:
     Macros.py
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

from pynput import mouse, keyboard
import time
import json

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

events = []

#------------------------------------------
# on_click(x, y, button, pressed)
#------------------------------------------
def on_click(x, y, button, pressed) -> None:
    """on_click"""
#beginfunction
    global events
    events.append({
        "type": "click",
        "x": x,
        "y": y,
        "button": str(button),
        "pressed": pressed,
        "timestamp": time.time()
    })
#endfunction

#------------------------------------------
# on_press(key) -> None:
#------------------------------------------
def on_press(key) -> None:
    """get_public_ip"""
#beginfunction
    global events
    print ('key:', key)
    events.append({
        "type": "key",
        "key": str(key),
        "timestamp": time.time()
    })
    if key == keyboard.Key.esc:
        print("Exiting...")
        sys.exit()
#endfunction

#------------------------------------------
def main ():
    """main"""
#beginfunction
    global text_result
    global pass_length
    global lbl_alert
    global events

    LUConst.SET_LIB(__file__)

    LULog.STARTLogging (LULog.TTypeSETUPLOG.tslINI, 'console', LUConst.GDirectoryLOG, LUConst.GFileNameLOG,
                        LUConst.GFileNameLOGjson)
    LULog.LoggerTOOLS.level = logging.INFO

    LPath = LUFile.ExtractFileDir(__file__)
    print(f'LPath: {LPath}')

    #--------------------------------------------------------------
    # 
    #--------------------------------------------------------------
    print("🔴 Запись началась. Нажмите ESC для завершения.")

    start_time = time.time()
    with mouse.Listener(on_click=on_click) as ml, keyboard.Listener(on_press=on_press) as kl:
        kl.join()

    # Сохраняем макрос
    with open(r"D:\PROJECTS_LYR\CHECK_LIST\DESKTOP\Python\PROJECTS_PY\SCRIPTS_PY\SRC\00.TEST\Macros\macro.json", "w") as f:
        json.dump(events, f)

    print("✅ Макрос сохранён: macro.json")
    
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
