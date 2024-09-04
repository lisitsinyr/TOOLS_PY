"""LISTDIR.py"""
# -*- coding: UTF-8 -*-
__annotations__ = """
 =======================================================
 Copyright (c) 2024
 Author:
     Lisitsin Y.R.
 Project:
     TOOLS_SRC_PY
 Module:
     COPYFILE.py

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
# БИБЛИОТЕКА LU
#------------------------------------------
import lyrpy.LUConst as LUConst
import lyrpy.LUDoc as LUDoc
import lyrpy.LULog as LULog
import lyrpy.LUFile as LUFile
import lyrpy.LUParserARG as LUParserARG
import lyrpy.LUFileUtils as LUFileUtils
from lyrpy.LUFileUtils import GMask


#------------------------------------------
#CONST
#------------------------------------------

#------------------------------------------
# FuncDir ()
#------------------------------------------
def FuncDir (ADirectory: str, APathDest: str):
    """FuncDir"""
#beginfunction
    # Lstat = os.stat(ADirectory)
    # LAttr = (LUFile.GetFileAttr (ADirectory))
    # LDirSize = LUFile.GetDirectoryTreeSize (ADirectory)
    # LDirDateTime = LUFile.GetDirDateTime (ADirectory)
    # s = f'{LDirDateTime[2]:%d.%m.%Y  %H:%M} {LDirDateTime[3]:%d.%m.%Y  %H:%M} {LDirSize:d}'
    s = f'{ADirectory:s}'
    LULog.LoggerTOOLS_AddLevel (LULog.TEXT, s)
#endfunction

#------------------------------------------
# FuncFile ()
#------------------------------------------
def FuncFile (AFileName: str, APathDest: str):
    """FuncFile"""
#beginfunction
    # lyrpy.LUFile.SetFileAttr (AFileName, Lflags, True)
    # LULog.LoggerAPPS_AddLevel (LULog.TEXT, f'GFileName = {GFileName}')
    Lstat = os.stat(AFileName)
    # LAttr = LUFile.GetFileAttr(AFileName)
    # Lflags = stat.FILE_ATTRIBUTE_SYSTEM | stat.FILE_ATTRIBUTE_HIDDEN | stat.FILE_ATTRIBUTE_READONLY
    LFileSize = LUFile.GetFileSize (AFileName)
    LFileDateTime = LUFile.GetFileDateTime (AFileName)
    s = f'...{LFileDateTime[2]:%d.%m.%Y  %H:%M} {LFileDateTime[2]:%d.%m.%Y  %H:%M} {LFileSize:d}'
    LFileDirectory = LUFile.GetFileDir(AFileName)
    # LFileDirectory = LUFile.ExtractFileName(LFileDirectory)
    s = f'{LFileDirectory:s}'
    # LULog.LoggerTOOLS_AddLevel (LULog.TEXT, s)
#endfunction

#------------------------------------------
# MAIN
#------------------------------------------
def main ():
#beginfunction
    global GFileName
    global GDirectory
    global GMask

    LULog.STARTLogging (LULog.TTypeSETUPLOG.tslCONFIG,
                        r'D:\PROJECTS_LYR\LOGS',
                        'LISTDIR.log',
                        'LISTDIR_json.log')

    LArgParser = LUParserARG.TArgParser (description = 'Параметры', prefix_chars = '-/')
    LArg = LArgParser.ArgParser.add_argument ('Directory', type = str, default='', help = 'Directory')
    Largs = LArgParser.ArgParser.parse_args ()
    Largs = LArgParser.ArgParser.parse_args ()
    LULog.LoggerAPPS_AddLevel (LULog.TEXT, Largs.__dict__)

    GDirectory = Largs.Directory
    # LULog.LoggerAPPS_AddLevel (LULog.TEXT, f'Directory = {GDirectory}')
    if not LUFile.DirectoryExists(GDirectory):
        print ('LISTDIR: Directory', GDirectory, 'not exist...')
    else:
        LUFileUtils.__ListDir (GDirectory, GMask,
                          True, '', 'CONSOLE', 0, FuncDir, FuncFile)
    #endif

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
