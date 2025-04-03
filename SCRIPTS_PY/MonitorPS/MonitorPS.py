"""Monitor.py"""
# -*- coding: UTF-8 -*-
__annotations__ = """
 =======================================================
 Copyright (c) 2025
 Author:
     Lisitsin Y.R.
 Project:
     SCRIPTS_PY
 Module:
     Monitor.py
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

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------
from tqdm import tqdm
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

#------------------------------------------
# list_processes ():
#------------------------------------------
def list_processes ():
    """list_processes"""
    """Отображает список всех запущенных процессов с их ID и названием."""
#beginfunction
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        processes.append(proc.info)
    return processes
#endfunction

#------------------------------------------
# search_process_by_name (name):
#------------------------------------------
def search_process_by_name (name):
    """search_process_by_name"""
    """Ищет процесс по имени."""
#beginfunction
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        if name.lower() in proc.info['name'].lower():
            print(f"PID: {proc.info['pid']} | Name:{proc.info['name']} | User: {proc.info['username']}")
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
    print(f'LPath: {LPath}')

    #--------------------------------------------------------------
    # 
    #--------------------------------------------------------------
    print("Список всех процессов:")
    processes = list_processes()
    for proc in processes:
        print(f"PID: {proc['pid']} | Name: {proc['name']} | User: {proc['username']}")

    name_filter = input("\nВведите название процесса для поиска (или оставить пустым для поиска всех): ")

    if name_filter:
        print("\nРезультаты поиска:")
        search_process_by_name(name_filter)
    
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
