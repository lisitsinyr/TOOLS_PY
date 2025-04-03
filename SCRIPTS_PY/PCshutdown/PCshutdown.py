"""PCshutdown.py"""
# -*- coding: UTF-8 -*-
__annotations__ = """
 =======================================================
 Copyright (c) 2025
 Author:
     Lisitsin Y.R.
 Project:
     SCRIPTS_PY
 Module:
     PCshutdown.py
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
# shutdown ()
#------------------------------------------
def shutdown () -> None:
    """shutdown"""
#beginfunction
    os.system("shutdown /s /t 1")
#endfunction

#------------------------------------------
# schedule_shutdown (minutes: int) -> None
#------------------------------------------
def schedule_shutdown(minutes: int) -> None:
    """schedule_shutdown"""
#beginfunction
    sec_in_minute = 60
    print(f'Компьютер выключится через {minutes} минут(ы)')
    time.sleep(minutes * sec_in_minute)
    print('\nКомпьютер будет выключен!')
    time.sleep(3)
    shutdown()
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
    try:
        set_time = int(input("Введите время до выключения (в минутах): "))
        if set_time <= 0:
            print("Время должно быть больше нуля.")
            return
        schedule_shutdown(set_time)
    except ValueError:
        print("Пожалуйста, введите корректное число минут.")
    
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
