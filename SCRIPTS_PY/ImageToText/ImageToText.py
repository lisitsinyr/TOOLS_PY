"""ImageToText.py"""
# -*- coding: UTF-8 -*-
__annotations__ = """
 =======================================================
 Copyright (c) 2024
 Author:
     Lisitsin Y.R.
 Project:
     SCRIPTS_PY
 Module:
     ImageToText.py
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

import chardet
from chardet.universaldetector import UniversalDetector
from charset_normalizer import detect

import logging

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------
from PIL import Image
import pytesseract

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

#------------------------------------------
# FuncDir ()
#------------------------------------------
def FuncDir (ADirectory: str, APathDest: str):
    """FuncDir"""
#beginfunction
    # s = f'{ADirectory:s}'
    # LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, s)

    # Lstat = os.stat(ADirectory)
    # LAttr = (LUFile.GetFileAttr (ADirectory))
    # LDirSize = LUFile.GetDirectoryTreeSize (ADirectory)
    # LDirDateTime = LUFile.GetDirDateTime (ADirectory)
    # s = f'{LDirDateTime[2]:%d.%m.%Y  %H:%M}{LDirDateTime[3]:%d.%m.%Y  %H:%M} {LDirSize:d}'

    # Lspisok = ADirectory.split('\\')
    # LDirectory = Lspisok[-1]
    # LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT,LDirectory)
    pass
#endfunction

#------------------------------------------
# FuncFile ()
#------------------------------------------
def FuncFile (AFilePath: str, APathDest: str):
    """FuncFile"""
#beginfunction
    # lyrpy.LUFile.SetFileAttr (AFileName, Lflags, True)

    LFileName = LUFile.ExtractFileName (AFilePath)
    LExt = LUFile.ExtractFileExt (AFilePath)
    Lstat = os.stat(AFilePath)
    Lflags = stat.FILE_ATTRIBUTE_SYSTEM | stat.FILE_ATTRIBUTE_HIDDEN | stat.FILE_ATTRIBUTE_READONLY
    LAttr = LUFile.GetFileAttr(AFilePath)
    LFileSize = LUFile.GetFileSize (AFilePath)

    LFileDateTime = LUFile.GetFileDateTime (AFilePath)
    s = f'...{LFileDateTime[2]:%d.%m.%Y  %H:%M} {LFileDateTime[2]:%d.%m.%Y  %H:%M} {LFileSize:d}'
    # LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, s)

    # LFileDirectory = LUFile.GetFileDir(AFilePath)
    # LFileDirectory = LUFile.ExtractFileName(LFileDirectory)
    # LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, f'LFileDirectory:{LFileDirectory:s}')

    WorkFileName (AFilePath)
#endfunction

#-----------------------------------------------------------
# WorkFileName ()
#-----------------------------------------------------------
def WorkFileName (AFilePath: str):
    """WorkFileName"""
#beginfunction
    LFileDir = LUFile.ExtractFileDir (AFilePath)
    LFileName = LUFile.ExtractFileNameWithoutExt (AFilePath)
    print (f'FileName:{LFileName}')
    LExt = LUFile.ExtractFileExt (AFilePath)
    print (f'Ex:{LExt}')

    try:
        with Image.open (AFilePath) as img:
            # Это графический файл
            LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, '... '+LFileName)

            LFormat = img.format.lower ()
            LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, f'... формат файла: {LFormat}')
            # print ("Формат файла:", LFormat)

        if LFormat.lower() in ('png', 'jpg', 'jpeg', 'bmp'):
            # Конвертация картинки в текст
            # LText = pytesseract.image_to_string (AFilePath, timeout=2)
            LText = pytesseract.image_to_string (Image.open (AFilePath), timeout=2)
            print (LText)

            # Открываем файл в режиме записи ('w')
            LFilePathOut = LFileDir+'\\'+LFileName+'.txt'
            print (LFilePathOut)
            with open (LFilePathOut, "w", encoding="utf-8") as file:
                file.write (LText)

        else:
            # Этот файл будет пропущен
            LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, f'Этот файл будет пропущен: {LFileName}')
            pass
        #endif
    except Exception as e:
        # print ("Ошибка при определении формата:", e)
        pass

#endfunction

#------------------------------------------
# sys.argv[1] - <file>, <directory>, <directory>\<pattern>
# sys.argv[2] - <width>
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
    LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, f'FilePath = {LFilePath}')
    LFileMask = Largs.filemask
    LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, f'FileMask = {LFileMask}')

    #-------------------------------------------------------
    # LFilePath - это файл
    #-------------------------------------------------------
    if os.path.isfile (LFilePath):
        LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, 'это файл ...')
        LDirectory = LUFile.ExtractFileDir (LFilePath)
        LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, f'Каталог = {LDirectory}')
        WorkFileName (LFilePath)
    #endif

    #-------------------------------------------------------
    # LFilePath - это каталог
    #-------------------------------------------------------
    if LUFile.DirectoryExists(LFilePath) and LFilePath != current_directory:
        LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, 'это каталог ...')
        LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, 'Это мы пока не будем делать ...')
        LDirectory = LFilePath
        LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, f'Каталог = {LDirectory}')
        # if LFileMask == '':
        #     LFileMask = '^.*..*$'  # *.* - все символы
        #     LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, f'FileMask = {LFileMask}')
        # #endif
        # LUFileUtils.__ListDir (LFilePath, LFileMask, False, '', 'CONSOLE', 0,
        #                        FuncDir, FuncFile)
    #endif

    #-------------------------------------------------------
    # LFilePath - это текущий каталог
    #-------------------------------------------------------
    # print(f'{LFilePath}')
    # print(f'{current_directory}')
    # print(LFilePath == '')
    # print(LFilePath == current_directory)
    # if LFilePath == '' or LFilePath == current_directory:
    if LFilePath == '':
        LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, 'это текущий каталог ...')
        LDirectory = current_directory
        LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, f'Каталог = {LDirectory}')
        os.chdir (LDirectory)
        LMask = '^.*..*$'  # *.* - все символы
        LUFileUtils.__ListDir (LDirectory, LMask,False, '', 'CONSOLE', 0,
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
