"""ftFormatTXT.py"""
# -*- coding: UTF-8 -*-
__annotations__ = """
 =======================================================
 Copyright (c) 2024
 Author:
     Lisitsin Y.R.
 Project:
     SCRIPTS_PY
 Module:
     ftFormatTXT.py
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
cDefaultwidth = 80
cDefaultEncoding = 'utf8'
cExt = ['.ini', '.mhtml', '.py', '.html', '.htm', '.toml',
        '.sh', '.bat', '.cmd', '.out', '.log', '.qwen',
        '.ht', '.json', '.svg', '.as'
        ]
Gwidth = cDefaultwidth

cFileName = ['.editorconfig', '.env', '.gitignore', '.gitmodules',
             'LICENSE',
             '.pypirc', 'requirements.txt']

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

#-----------------------------------------------------------
# detect_encoding_with_charset_normalizer ()
#-----------------------------------------------------------
def detect_encoding_with_charset_normalizer (AFilePath):
#beginfunction
    with open (AFilePath, 'rb') as f:
        raw_data = f.read ()
        result = detect (raw_data)
        encoding = result ['encoding']
        # print (f"Encoding: {encoding}")
    return encoding
#endfunction

#-----------------------------------------------------------
# GetFileEncoding ()
#-----------------------------------------------------------
def is_text_file_by_content(AFilePath) -> bool:
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

    WorkFileName (AFilePath, Gwidth)
#endfunction

#-----------------------------------------------------------
# WorkFileName ()
#-----------------------------------------------------------
def WorkFileName (AFilePath: str, Awidth: int):
    """WorkFileName"""
#beginfunction
    LFileName = LUFile.ExtractFileName (AFilePath)
    LExt = LUFile.ExtractFileExt (AFilePath)
    # print (LFileName, LExt)
    if (LExt not in cExt) and (LFileName not in cFileName):
        if is_text_file_by_content (AFilePath):
            # Это текстовый файл
            LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, '... '+LFileName)

            LencodingFILE = GetFileEncoding (AFilePath)
            # LencodingFILE = detect_encoding_with_charset_normalizer (AFilePath)
            LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, f'encoding: {LencodingFILE}')

            with open (AFilePath, 'r', encoding = 'utf-8') as file:
                content = file.read ()
            #endwith

            paragraphs = content.split ('\n')
            formatted_paragraphs = []
            for paragraph in paragraphs:
                substring = "https://"
                if substring in paragraph:
                    # Подстрока найдена
                    s = paragraph
                else:
                    # Подстрока не найдена
                    s = textwrap.fill (paragraph, width = Awidth)
                #endif
                # print(s)
                formatted_paragraphs.append (s)
            #endfor

            with open(AFilePath, 'w', encoding='utf-8') as file:
                file.write('\n'.join(formatted_paragraphs))
            #endwith

            if not LExt in ['.md',]:
                LFilePath = AFilePath+'.md'
                # Переименование файла
                os.rename (AFilePath, LFilePath)
            #endif
        else:
            # Это не текстовый файл
            # LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, f'Это не текстовый файл: {LFileName}')
            pass
        #endif
    else:
        # Этот файл будет пропущен
        # LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, f'Этот файл будет пропущен: {LFileName}')
        pass
    #endif

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
    LArg = LArgParser.ArgParser.add_argument ('-w', '--width', type = int, default=60, help = 'width')
    Largs = LArgParser.ArgParser.parse_args ()

    LFilePath = Largs.filepath
    LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, f'FilePath = {LFilePath}')
    LFileMask = Largs.filemask
    LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, f'FileMask = {LFileMask}')
    Gwidth = Largs.width
    LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, f'width = {Gwidth}')

    #-------------------------------------------------------
    # LFilePath - это файл
    #-------------------------------------------------------
    if os.path.isfile (LFilePath):
        LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, 'это файл ...')
        LDirectory = LUFile.ExtractFileDir (LFilePath)
        LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, f'Каталог = {LDirectory}')
        WorkFileName (LFilePath, Gwidth)
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
    if LFilePath == '' or LFilePath == current_directory:
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
