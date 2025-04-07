"""CountdownTimer.py"""
# -*- coding: UTF-8 -*-
__annotations__ = """
 =======================================================
 Copyright (c) 2025
 Author:
     Lisitsin Y.R.
 Project:
     SCRIPTS_PY
 Module:
     CountdownTimer.py
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

import time

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
#
#------------------------------------------
def countdown(time_sec):
    """countdown"""
#beginfunction
    while time_sec:
        mins, secs = divmod (time_sec, 60)
        timeformat = '{:02d}: {:02d}'.format(mins, secs)
        print(timeformat, end='\n')
        time.sleep(1)
        time_sec -= 1

    print("stop")
#endfunction

#------------------------------------------
#
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
    num=int(input("Set Your Timer in Sec: "))
    countdown(num)

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
