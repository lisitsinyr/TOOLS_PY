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
# func_pass ()
#------------------------------------------
def func_pass():
    """func_pass"""
#beginfunction
    pass
#endfunction

#-----------------------------------------------------------
# get_system_stats ()
#-----------------------------------------------------------
def get_system_stats ():
    """get_system_stats"""
#beginfunction
    stats = {
        "cpu": psutil.cpu_percent (interval=1),
        "memory": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent
    }
    return json.dumps (stats)
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
    # Check the source and destination directories
    #--------------------------------------------------------------
    print (get_system_stats())
    
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
