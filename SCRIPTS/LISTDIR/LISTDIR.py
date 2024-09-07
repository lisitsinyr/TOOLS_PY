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
import logging

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------

#------------------------------------------
# БИБЛИОТЕКА LU
#------------------------------------------
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
    Lspisok = ADirectory.split('\\')
    LDirectory = Lspisok[-1]
    LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, LDirectory)
#endfunction

#------------------------------------------
# FuncFile ()
#------------------------------------------
def FuncFile (AFileName: str, APathDest: str):
    """FuncFile"""
#beginfunction
    # lyrpy.LUFile.SetFileAttr (AFileName, Lflags, True)
    # LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, f'GFileName = {GFileName}')
    # Lstat = os.stat(AFileName)
    # LAttr = LUFile.GetFileAttr(AFileName)
    # Lflags = stat.FILE_ATTRIBUTE_SYSTEM | stat.FILE_ATTRIBUTE_HIDDEN | stat.FILE_ATTRIBUTE_READONLY
    # LFileSize = LUFile.GetFileSize (AFileName)
    # LFileDateTime = LUFile.GetFileDateTime (AFileName)
    # s = f'...{LFileDateTime[2]:%d.%m.%Y  %H:%M} {LFileDateTime[2]:%d.%m.%Y  %H:%M} {LFileSize:d}'
    # LFileDirectory = LUFile.GetFileDir(AFileName)
    # LFileDirectory = LUFile.ExtractFileName(LFileDirectory)
    # s = f'{LFileDirectory:s}'
    # LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, s)
    pass
#endfunction

#------------------------------------------
# MAIN
#------------------------------------------
def main ():
#beginfunction
    # global GDirectory

    LULog.STARTLogging (LULog.TTypeSETUPLOG.tslCONFIG,
                        r'D:\PROJECTS_LYR\LOGS',
                        'LISTDIR.log',
                        'LISTDIR_json.log')

    LArgParser = LUParserARG.TArgParser (description = 'Параметры', prefix_chars = '-/')
    LArg = LArgParser.ArgParser.add_argument ('Directory', type = str, default='', help = 'Directory')

    Largs = LArgParser.ArgParser.parse_args ()

    LULog.LoggerTOOLS.level = logging.INFO

    LDirectory = Largs.Directory
    # LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, f'Directory = {LDirectory}')
    if not LUFile.DirectoryExists(LDirectory):
        print ('LISTDIR: Directory', LDirectory, 'not exist...')
    else:
        LUFileUtils.__ListDir (LDirectory, GMask,
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
