"""COPYFILE.py"""
# -*- coding: UTF-8 -*-
__annotations__ = """
 =======================================================
 Copyright (c) 2024
 Author:
     Lisitsin Y.R.
 Project:
     SCRIPTS_PY
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

    # LPureWindowsPath = LUFile.GetPureWindowsPath (AFileName)
    # s = f'{LPureWindowsPath:%s}'
    # if GFileName != AFileName:
    #     LFileName = os.path.join (LFileDirectory, GMask)
    #     s = f'Copy {GMask:s} -> {LFileName:s} ...'
    #     LULog.LoggerTOOLS_AddLevel (LULog.TEXT, s)
    #     shutil.copy2 (GFileName, LFileName)
    # #endif
#endfunction

#------------------------------------------
# MAIN
#------------------------------------------
def main ():
#beginfunction
    # LUConst.SET_CONST(__file__)
    LUConst.SET_LIB(__file__)

    LULog.STARTLogging (LULog.TTypeSETUPLOG.tslINI, 'console', LUConst.GDirectoryLOG, LUConst.GFileNameLOG,
                        LUConst.GFileNameLOGjson)
    LULog.LoggerTOOLS.level = logging.INFO

    LArgParser = LUParserARG.TArgParser (description = 'Параметры', prefix_chars = '-/')
    LArgParser.ArgParser.add_argument ('FileName', type = str, default = '', help = 'FileName')
    LArgParser.ArgParser.add_argument ('Directory', type = str, default = '', help = 'Directory')
    Largs = LArgParser.ArgParser.parse_args ()
    GFileName = Largs.FileName
    LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, f'FileName = {GFileName}')
    GDirectory = Largs.Directory
    LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, f'Directory = {GDirectory}')

    if not LUFile.FileExists(GFileName):
        print ('COPYFILE: FileName', GFileName, 'not exist...')
    else:
        GFileName = LUFile.ExpandFileName(Largs.FileName)
        GMask = LUFile.ExtractFileName(GFileName)
        if not LUFile.DirectoryExists(GDirectory):
            print ('COPYFILE: Directory', GDirectory, 'not exist...')
        else:
            LUFileUtils.__ListDir (GDirectory, GMask,
                          True, '', 'CONSOLE', 0,
                          FuncDir, FuncFile)
        #endif
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
