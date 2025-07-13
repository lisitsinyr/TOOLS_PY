"""GULLIVER.py"""
# -*- coding: UTF-8 -*-
__annotations__ = """
 =======================================================
 Copyright (c) 2024
 Author:
     Lisitsin Y.R.
 Project:
     SCRIPTS_PY
 Module:
     GULLIVER.py
 =======================================================
"""

#------------------------------------------
# БИБЛИОТЕКИ python
#------------------------------------------
import os
# Получить текущий рабочий каталог
current_directory = os.getcwd ()
import textwrap
import sys
import stat
import re

import chardet
from chardet.universaldetector import UniversalDetector
from charset_normalizer import detect

import logging

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------

#------------------------------------------
# БИБЛИОТЕКА LU
#------------------------------------------
import lyrpy.LULog as LULog
import lyrpy.LUConst as LUConst
import lyrpy.LUFile as LUFile
import lyrpy.LUParserARG as LUParserARG
import lyrpy.LUFileUtils as LUFileUtils
from lyrpy.LUFileUtils import GMask

#------------------------------------------
#CONST
#------------------------------------------
cOutputFile = 'gulliver.cvs'
cseparator = ';'

#-----------------------------------------------------------
# is_float(s) -> bool:
#-----------------------------------------------------------
def is_float(s) -> bool:
    """is_text_file_by_content"""
#beginfunction
    return re.fullmatch(r'[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?', s.strip()) is not None
#endfunction

#-----------------------------------------------------------
# is_text_file_by_content(AFilePath) -> bool:
#-----------------------------------------------------------
def is_text_file_by_content(AFilePath) -> bool:
    """is_text_file_by_content"""
#beginfunction
    try:
        with open(AFilePath, 'r', encoding='utf-8') as file:
            file.read()
            return True
        #endwith
    except UnicodeDecodeError:
        return False
    #endtry
#endfunction

#--------------------------------------------------------------------------------
# GetFileEncoding ()
#--------------------------------------------------------------------------------
def GetFileEncoding (AFilePath: str) -> str:
    """GetFileEncoding"""
#beginfunction
    try:
        with open(AFilePath, 'rb') as LFile:
            LRawData = LFile.read ()

            # LResult = chardet.detect (LRawData)
            LResult = detect (LRawData)

            LEncoding = LResult ['encoding']
        #endwith
        return LEncoding
    except UnicodeDecodeError:
        return ''
    #endtry
#endfunction

#------------------------------------------
# FuncDir (ADirectory: str, APathDest: str):
#------------------------------------------
def FuncDir (ADirectory: str, APathDest: str):
    """FuncDir"""
#beginfunction
    # s = f'{ADirectory:s}'
    # LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, s)
    pass
#endfunction

#------------------------------------------
# FuncFile (AFilePath: str, APathDest: str):
#------------------------------------------
def FuncFile (AFilePath: str, APathDest: str):
    """FuncFile"""
#beginfunction
    LFileName = LUFile.ExtractFileName (AFilePath)
    LExt = LUFile.ExtractFileExt (AFilePath)
    Lstat = os.stat(AFilePath)
    Lflags = stat.FILE_ATTRIBUTE_SYSTEM | stat.FILE_ATTRIBUTE_HIDDEN | stat.FILE_ATTRIBUTE_READONLY
    LAttr = LUFile.GetFileAttr(AFilePath)
    LFileSize = LUFile.GetFileSize (AFilePath)
    LFileDateTime = LUFile.GetFileDateTime (AFilePath)
    s = f'...{LFileDateTime[2]:%d.%m.%Y  %H:%M} {LFileDateTime[2]:%d.%m.%Y  %H:%M} {LFileSize:d}'
    # LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, s)

    WorkFileName (AFilePath)
#endfunction

#-----------------------------------------------------------
# WorkFileName (AFilePath: str):
#-----------------------------------------------------------
def WorkFileName (AFilePath: str):
    """WorkFileName"""
#beginfunction
    LFileName = LUFile.ExtractFileName (AFilePath)
    LExt = LUFile.ExtractFileExt (AFilePath)
    LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, '... '+LFileName)
    with open (AFilePath, 'r', encoding = 'utf-8') as file:
        line = file.readline ()

        while line:
            s = line.rstrip ()
            if 'Ульяновск' in s:
                Npp = 0
                # Заголовок чека
                title = s
                print (title)
                address = ''.join(title.split (' ')[1:6])
                date = title.split (' ')[-2]
                DDMMYYYY = date.split ('.')
                YYYYMMDD = ''.join(DDMMYYYY [::-1])
                line = file.readline ()
            #endif
            # item
            Npp += 1
            s = line.rstrip ()
            item = s
            # Количество
            line = file.readline ()
            s = line.rstrip ()
            count = s.replace ('.', ',')
            # Стоимость
            line = file.readline ()
            s = line.rstrip ()
            coast = s.replace ('.', ',')
            d = YYYYMMDD+cseparator+address+cseparator+str(Npp)+cseparator+item+cseparator+str(count)+cseparator+str(coast)
            LUFile.WriteStrToFile(cOutputFile, d)
            line = file.readline ()
            s = line.rstrip ()
            if 'руб.' in s:
                # Итог
                line = file.readline ()
            #endif
        #endwhile
    #endwith
#endfunction

#------------------------------------------
# main ():
#------------------------------------------
def main ():
    global Gwidth
#beginfunction
    LUConst.SET_LIB(__file__)

    LULog.STARTLogging (LULog.TTypeSETUPLOG.tslINI,
                        'console', LUConst.GDirectoryLOG, LUConst.GFileNameLOG,
                        LUConst.GFileNameLOGjson)
    LULog.LoggerTOOLS.level = logging.INFO

    LArgParser = LUParserARG.TArgParser (description = 'Параметры', prefix_chars = '-/')
    LArg = LArgParser.ArgParser.add_argument ('-fp', '--filepath', type = str, default='', help = 'filepath')
    LArg = LArgParser.ArgParser.add_argument ('-fm', '--filemask', type = str, default='^.*..*$', help = 'filemask')
    Largs = LArgParser.ArgParser.parse_args ()

    LFilePath = Largs.filepath
    LFilePath = current_directory+'\\DATA\\TXT'
    LFilePath = r'D:\PROJECTS_LYR\CHECK_LIST\DESKTOP\Python\PROJECTS_PY\SCRIPTS_PY\SRC\SCRIPTS_PY\GULLIVER\DATA\TXT'
    LFilePath = current_directory
    LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, f'FilePath = {LFilePath}')

    LFileMask = Largs.filemask
    LFileMask = '^.*..txt$'  # *.* - все символы
    LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, f'FileMask = {LFileMask}')

    if LUFile.FileExists (LFilePath+'\\'+cOutputFile):
        print(f'Удаление файла {LFilePath+'\\'+cOutputFile}')
        LUFile.FileDelete (LFilePath+'\\'+cOutputFile)
    #endif

    #-------------------------------------------------------
    # LFilePath - это файл
    #-------------------------------------------------------
    if os.path.isfile (LFilePath):
        LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, 'это файл ...')
        LDirectory = LUFile.ExtractFileDir (LFilePath)
        LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, f'Каталог = {LDirectory}')
        WorkFileName (LFilePath)
    else:
        #-------------------------------------------------------
        # LFilePath - это каталог
        #-------------------------------------------------------
        # LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, 'это текущий каталог ...')
        LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, f'Каталог = {LFilePath}')
        os.chdir (LFilePath)
        LUFileUtils.__ListDir (LFilePath, LFileMask, False, '', 'CONSOLE', 0,
                               FuncDir, FuncFile)
    #endif

    LULog.STOPLogging ()
#endfunction

#------------------------------------------
#
#------------------------------------------
#beginmodule
if __name__ == "__main__":
    # print(f'Вызов функции {__name__}')
    main()
#endif

#endmodule
