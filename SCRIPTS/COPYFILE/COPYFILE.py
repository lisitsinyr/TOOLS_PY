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
    # print ('DEBUG: function ',sys._getframe (0).f_code.co_name, '...')
    Lstat = os.stat(ADir)
    LAttr = (LUFile.GetFileAttr (ADir))
    LDirSize = LUFile.GetDirectoryTreeSize (ADir)
    LDirDateTime = LUFile.GetDirDateTime (ADir)
    s = f'{LDirDateTime[2]:%d.%m.%Y  %H:%M} {LDirDateTime[3]:%d.%m.%Y  %H:%M} {LDirSize:d}'
    # s = f'{ADir:%s}'
    # LULog.LoggerTOOLS_AddLevel (LULog.TEXT, s)
#endfunction

#------------------------------------------
# FuncFile ()
#------------------------------------------
def FuncFile (AFileName: str, APathDest: str):
    """FuncFile"""
#beginfunction
    # print ('DEBUG: function ',sys._getframe (0).f_code.co_name, '...')
    Lstat = os.stat(AFileName)
    LAttr = LUFile.GetFileAttr(AFileName)
    # Lflags = stat.FILE_ATTRIBUTE_SYSTEM | stat.FILE_ATTRIBUTE_HIDDEN | stat.FILE_ATTRIBUTE_READONLY
    # lyrpy.LUFile.SetFileAttr (AFileName, Lflags, True)

    # LPureWindowsPath = LUFile.GetPureWindowsPath (AFileName)
    # s = f'{LPureWindowsPath:%s}'
    # LULog.LoggerTOOLS_AddLevel (LULog.TEXT, s)

    # LFileSize = LUFile.GetFileSize (AFileName)
    # LFileDateTime = LUFile.GetFileDateTime (AFileName)
    # s = f'...{LFileDateTime[2]:%d.%m.%Y  %H:%M} {LFileDateTime[2]:%d.%m.%Y  %H:%M} {LFileSize:d}'
    s = LUFile.GetFileDir(AFileName)
    LULog.LoggerTOOLS_AddLevel (LULog.TEXT, s)
#endfunction

#------------------------------------------
# MAIN
#------------------------------------------
def main ():
#beginfunction
    LULog.STARTLogging (LULog.TTypeSETUPLOG.tslINI,
                        r'D:\PROJECTS_LYR\LOGS',
                        'COPYFILE_FILEINI.log',
                        'COPYFILE_FILEINI_json.log')

    # print ('DEBUG: function ',sys._getframe (0).f_code.co_name, '...')
    # LUDoc.PrintInfoObject('-----main----')
    # LUDoc.PrintInfoObject(main)

    #----------------------------------------------------------------
    global GDir
    global GMask

    # s = f'sys.argv = {sys.argv}'
    # LULog.LoggerAPPS_AddLevel (LULog.TEXT, s)

    #----------------------------------------------------------------
    # GDir = LUParserARG.GetParam ('PDir', "")
    # LULog.LoggerAPPS_AddLevel (LULog.TEXT, f'PDir = {GDir}')
    # GMask = LUParserARG.GetParam ('PMask', "")
    # LULog.LoggerAPPS_AddLevel (LULog.TEXT, f'PMask = {GMask}')
    #----------------------------------------------------------------

    #----------------------------------------------------------------
    # Lparser = argparse.ArgumentParser (description = 'Параметры', prefix_chars = '-/')
    # Lparser.add_argument ('PDir', type = str, default = '', help = 'PDir')
    # Lparser.add_argument ('PMask', type = str, default = '', help = 'PMask')
    # #Lparser.add_argument ('-PDir', type = str, nargs = '?', default = '', dest = 'PDir', help = 'PDir')
    # #Lparser.add_argument ('-PMask', type = str, nargs = '?', default = '', dest = 'PMask', help = 'PMask')
    # Largs = Lparser.parse_args ()
    # GDir = Largs.PDir
    # LULog.LoggerAPPS_AddLevel (LULog.TEXT, f'PDir = {GDir}')
    # GMask = Largs.PMask
    # LULog.LoggerAPPS_AddLevel (LULog.TEXT, f'PMask = {GMask}')
    #----------------------------------------------------------------

    #----------------------------------------------------------------
    LArgParser = LUParserARG.TArgParser (description = 'Параметры', prefix_chars = '-/')
    LArg = LArgParser.ArgParser.add_argument ('PDir', type = str, default = '', help = 'PDir')
    # LULog.LoggerAPPS_AddLevel (LULog.TEXT, LArg)
    LArg = LArgParser.ArgParser.add_argument ('PMask', type = str, default = '', help = 'PMask')
    # LULog.LoggerAPPS_AddLevel (LULog.TEXT, LArg)
    Largs = LArgParser.ArgParser.parse_args ()
    GDir = Largs.PDir
    s = f'Dir = {GDir}'
    LULog.LoggerAPPS_AddLevel (LULog.TEXT, s)
    GMask = Largs.PMask
    s = f'Mask = {GMask}'
    LULog.LoggerAPPS_AddLevel (LULog.TEXT, s)
    #----------------------------------------------------------------

    _Option = 1
    _Option = 0
    _OutFile = 'ListDir.txt'
    _OutFile = 'CONSOLE'
    LUFile.FileDelete (_OutFile)

    LULog.LoggerTOOLS.setLevel (logging.INFO)

    LUFileUtils.__ListDir (GDir, GMask, True, '', _OutFile, _Option, FuncDir, FuncFile)

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
