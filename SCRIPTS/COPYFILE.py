"""COPYFILE.py"""
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

#------------------------------------------
#CONST
#------------------------------------------

#------------------------------------------
# FuncDir ()
#------------------------------------------
def FuncDir (ADir: str, APathDest: str):
    """FuncDir"""
#beginfunction
    # Lstat = os.stat(ADir)
    # LAttr = (LUFile.GetFileAttr (ADir))
    # LDirSize = LUFile.GetDirectoryTreeSize (ADir)
    # LDirDateTime = LUFile.GetDirDateTime (ADir)
    # s = f'{LDirDateTime[2]:%d.%m.%Y  %H:%M} {LDirDateTime[3]:%d.%m.%Y  %H:%M} {LDirSize:d}'
    # s = f'{ADir:%s}'
    # LULog.LoggerTOOLS_AddLevel (LULog.TEXT, s)
    pass
#endfunction

#------------------------------------------
# FuncFile ()
#------------------------------------------
def FuncFile (AFileName: str, APathDest: str):
    """FuncFile"""
#beginfunction
    # lyrpy.LUFile.SetFileAttr (AFileName, Lflags, True)

    Lstat = os.stat(AFileName)
    # LAttr = LUFile.GetFileAttr(AFileName)
    # Lflags = stat.FILE_ATTRIBUTE_SYSTEM | stat.FILE_ATTRIBUTE_HIDDEN | stat.FILE_ATTRIBUTE_READONLY
    LFileSize = LUFile.GetFileSize (AFileName)
    LFileDateTime = LUFile.GetFileDateTime (AFileName)
    s = f'...{LFileDateTime[2]:%d.%m.%Y  %H:%M} {LFileDateTime[2]:%d.%m.%Y  %H:%M} {LFileSize:d}'

    LFileDirectory = LUFile.GetFileDir(AFileName)
    s = f'{LFileDirectory:s}'
    LULog.LoggerTOOLS_AddLevel (LULog.TEXT, s)

    # LPureWindowsPath = LUFile.GetPureWindowsPath (AFileName)
    # s = f'{LPureWindowsPath:%s}'
#endfunction

#------------------------------------------
# MAIN
#------------------------------------------
def main ():
#beginfunction
    global GFileName
    global GDirectory

    LULog.STARTLogging (LULog.TTypeSETUPLOG.tslINI,
                        r'D:\PROJECTS_LYR\LOGS',
                        'COPYFILE_FILEINI.log',
                        'COPYFILE_FILEINI_json.log')

    LArgParser = LUParserARG.TArgParser (description = 'Параметры', prefix_chars = '-/')
    LArgParser.ArgParser.add_argument ('FileName', type = str, default = '', help = 'FileName')
    LArgParser.ArgParser.add_argument ('Directory', type = str, default = '', help = 'Directory')
    Largs = LArgParser.ArgParser.parse_args ()
    GFileName = Largs.FileName
    LULog.LoggerAPPS_AddLevel (LULog.TEXT, f'FileName = {GFileName}')
    GDirectory = Largs.Directory
    LULog.LoggerAPPS_AddLevel (LULog.TEXT, f'Directory = {GDirectory}')

    GDirectory = LUFile.GetPureWindowsPath (GDirectory)
    print (GDirectory)
    # s = f'{LPureWindowsPath:s}'
    # LULog.LoggerTOOLS_AddLevel (LULog.TEXT, s)

    LUFileUtils.__ListDir (GDirectory, GFileName,
                          True, '', 'CONSOLE', 0,
                           FuncDir, FuncFile)

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
