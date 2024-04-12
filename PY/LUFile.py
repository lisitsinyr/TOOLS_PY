"""LUFile.py"""
# -*- coding: UTF-8 -*-
__annotations__ = """
 =======================================================
 Copyright (c) 2023
 Author:
     Lisitsin Y.R.
 Project:
     LU_PY
     Python (LU)
 Module:
     LUFile.py

 =======================================================
"""

#------------------------------------------
# БИБЛИОТЕКИ python
#------------------------------------------
import datetime
import os
import stat
import tempfile
import platform
import re
import ctypes

# import win32api
# import pathlib
# import logging

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------
import shutil
import chardet

#------------------------------------------
# БИБЛИОТЕКА LU
#------------------------------------------
import LUErrors
import LUStrDecode
import LUDateTime
import LUos

"""
f = open(file_name, access_mode, encoding='')
    file_name = имя открываемого файла
    access_mode = режим открытия файла. Он может быть: для чтения, записи и т. д.
    По умолчанию используется режим чтения (r), если другое не указано.
    Далее полный список режимов открытия файла
Режим   Описание
r   Только для чтения.
w   Только для записи. Создаст новый файл, если не найдет с указанным именем.
rb  Только для чтения (бинарный).
wb  Только для записи (бинарный). Создаст новый файл, если не найдет с указанным именем.
r+  Для чтения и записи.
rb+ Для чтения и записи (бинарный).
w+  Для чтения и записи. Создаст новый файл для записи, если не найдет с указанным именем.
wb+ Для чтения и записи (бинарный). Создаст новый файл для записи, если не найдет с указанным именем.
a   Откроет для добавления нового содержимого. Создаст новый файл для записи, если не найдет с указанным именем.
a+  Откроет для добавления нового содержимого. Создаст новый файл для чтения записи, если не найдет с указанным именем.
ab  Откроет для добавления нового содержимого (бинарный). Создаст новый файл для записи, если не найдет с указанным именем.
ab+ Откроет для добавления нового содержимого (бинарный). Создаст новый файл для чтения записи, если не найдет с указанным именем.    

# LFile = open (AFileName, 'r', encoding='utf-8')
# LFile = open (AFileName, 'r', encoding='cp1251')
"""

cDefaultEncoding = 'cp1251'

#--------------------------------------------------------------------------------
# DirectoryExists
#--------------------------------------------------------------------------------
def DirectoryExists (APath: str) -> bool:
    """DirectoryExists """
#beginfunction
    return os.path.isdir(APath)
#endfunction

#--------------------------------------------------------------------------------
# ForceDirectories
#--------------------------------------------------------------------------------
def ForceDirectories (ADir: str) -> bool:
    """ForceDirectories"""
#beginfunction
    # SCannotCreateDir: str = 'Unable to create directory'
    os.makedirs (ADir, exist_ok = True)
    LResult = DirectoryExists (ADir)
    return LResult
#endfunction

#--------------------------------------------------------------------------------
# DirectoryDelete
#--------------------------------------------------------------------------------
def DirectoryDelete (ADirectoryName: str) -> bool:
    """DirectoryDelete"""
#beginfunction
    LResult = False
    if DirectoryExists (ADirectoryName):
        shutil.rmtree (ADirectoryName)
        LResult = True
    #endif
    return LResult
#endfunction

#--------------------------------------------------------------------------------
# FileExists
#--------------------------------------------------------------------------------
def FileExists (AFileName: str) -> bool:
    """FileExists"""
#beginfunction
    return os.path.isfile(AFileName)
#endfunction

#--------------------------------------------------------------------------------
# GetFileDateTime
#--------------------------------------------------------------------------------
def GetFileDateTime (AFileName: str) -> ():
    """GetFileDateTime"""
#beginfunction
    LTuple = ()
    if os.path.isfile (AFileName):
        if platform.system() == 'Windows':
            # file creation
            LFileTimeCreate: datetime = os.path.getctime (AFileName)
            # convert creation timestamp into DateTime object
            LFileTimeCreateDate: datetime = datetime.datetime.fromtimestamp (LFileTimeCreate)
            # file modification
            LFileTimeMod: datetime = os.path.getmtime (AFileName)
            # convert timestamp into DateTime object
            LFileTimeModDate: datetime = datetime.datetime.fromtimestamp (LFileTimeMod)
        else:
            stat = os.stat(AFileName)
            # file modification
            LFileTimeMod: datetime = stat.st_mtime
            # convert timestamp into DateTime object
            LFileTimeModDate: datetime = datetime.datetime.fromtimestamp (LFileTimeMod)
            try:
                LFileTimeCreate: datetime = stat.st_birthtime
                # convert creation timestamp into DateTime object
                LFileTimeCreateDate: datetime = datetime.datetime.fromtimestamp (LFileTimeCreate)
            except AttributeError:
                # We're probably on Linux. No easy way to get creation dates here,
                # so we'll settle for when its content was last modified.
                LFileTimeCreate: datetime = 0
                LFileTimeCreateDate: datetime = 0
            #endtry
        #endif
        LTuple = (LFileTimeMod, LFileTimeCreate, LFileTimeModDate, LFileTimeCreateDate)
    #endif
    return LTuple
#endfunction

#--------------------------------------------------------------------------------
# COMPAREFILETIMES
#--------------------------------------------------------------------------------
def COMPAREFILETIMES (AFileName1: str, AFileName2: str) -> int:
    """COMPAREFILETIMES"""
#beginfunction
    #-3 File2 could not be opened (see @ERROR for more information).
    #-2 File1 could not be opened (see @ERROR for more information).
    #-1 File1 is older than file2.
    #0 File1 and file2 have the same date and time.
    #1 File1 is more recent than file2.
    if not FileExists (AFileName1):
        return -2
    #endif
    if not FileExists (AFileName2):
        return -3
    #endif
    LFileName1m = GetFileDateTime (AFileName1)[0]
    LFileName2m = GetFileDateTime (AFileName2)[0]
    if LFileName1m == LFileName2m:
        return 0
    else:
        if LFileName1m > LFileName2m:
            return -1
        else:
            return 1
        #endif
    #endif
#endfunction

#--------------------------------------------------------------------------------
#
#--------------------------------------------------------------------------------
def GetFileSize (AFileName: str) -> int:
    """GetFileSize"""
#beginfunction
    if os.path.isfile (AFileName):
        if platform.system() == 'Windows':
            if FileExists (AFileName):
                return os.path.getsize (AFileName)
            else:
                return 0
        else:
            stat = os.stat(AFileName)
            return stat.st_size
        #endif
    else:
        return 0
    #endif
#endfunction

#--------------------------------------------------------------------------------
# ExpandFileName (APath: str) -> str:
#--------------------------------------------------------------------------------
def ExpandFileName (APath: str) -> str:
    """ExpandFileName"""
#beginfunction
    # LResult = os.path.basename(APath)
    LResult = os.path.abspath(APath)
    return LResult
#endfunction

#--------------------------------------------------------------------------------
# ExtractFileDir (APath: str) -> str:
#--------------------------------------------------------------------------------
def ExtractFileDir (APath: str) -> str:
    """ExtractFileDir"""
#beginfunction
    LDir, LFileName = os.path.split(APath)
    return LDir
#endfunction

#--------------------------------------------------------------------------------
# ExtractFileName (APath: str) -> str:
#--------------------------------------------------------------------------------
def ExtractFileName (APath: str) -> str:
    """ExtractFileName"""
#beginfunction
    LPath, LFileName = os.path.split(APath)
    return LFileName
#endfunction

#-------------------------------------------------------------------------------
# ExtractFileNameWithoutExt (AFileName: str) -> str:
#-------------------------------------------------------------------------------
def ExtractFileNameWithoutExt (AFileName: str) -> str:
    """ExtractFileNameWithoutExt"""
#beginfunction
    LResult = os.path.basename (AFileName).split ('.') [0]
    return LResult
#endfunction

#--------------------------------------------------------------------------------
# ExtractFileExt (APath: str) -> str:
#--------------------------------------------------------------------------------
def ExtractFileExt (AFileName: str) -> str:
    """ExtractFileExt"""
#beginfunction
    LResult = os.path.basename(AFileName)
    LFileName, LFileExt = os.path.splitext(LResult)
    return LFileExt
#endfunction

#---------------------------------------------------------------------------------------------
# GetFileDir (APath: str) -> str:
#---------------------------------------------------------------------------------------------
def GetFileDir (APath: str) -> str:
    """GetFileDir"""
#beginfunction
    return ExtractFileDir (APath)
#endfunction

#--------------------------------------------------------------------------------
# GetFileName (APath: str) -> str:
#--------------------------------------------------------------------------------
def GetFileName (APath: str) -> str:
    """GetFileName"""
#beginfunction
    return ExtractFileNameWithoutExt (APath)
#endfunction

#-------------------------------------------------------------------------------
# GetFileNameWithoutExt (AFileName: str) -> str:
#-------------------------------------------------------------------------------
def GetFileNameWithoutExt (AFileName: str) -> str:
    """GetFileNameWithoutExt"""
#beginfunction
    return ExtractFileNameWithoutExt (AFileName)
#endfunction

#---------------------------------------------------------------------------------------------
# GetFileExt (AFileName: str) -> str:
#---------------------------------------------------------------------------------------------
def GetFileExt (AFileName: str) -> str:
    """GetFileExt"""
#beginfunction
    return ExtractFileExt (AFileName)
#endfunction

"""
# #import codecs
#
# f = codecs.open(filename, 'r', 'cp1251')
# u = f.read()   # now the contents have been transformed to a Unicode string
# out = codecs.open(output, 'w', 'utf-8')
# out.write(u)   # and now the contents have been output as UTF-8
"""

#--------------------------------------------------------------------------------
# GetFileEncoding (AFileName: str) -> str:
#--------------------------------------------------------------------------------
def GetFileEncoding (AFileName: str) -> str:
    """GetFileEncoding"""
#beginfunction
    LEncoding = ''
    if FileExists(AFileName):
        LFile = open (AFileName, 'rb')
        LRawData = LFile.read ()
        LResult = chardet.detect (LRawData)
        LEncoding = LResult ['encoding']
        LFile.close ()
    return LEncoding
#endfunction

#--------------------------------------------------------------------------------
# IncludeTrailingBackslash
#--------------------------------------------------------------------------------
def IncludeTrailingBackslash (APath: str) -> str:
    """IncludeTrailingBackslash"""
#beginfunction
    LResult = APath.rstrip('\\')+'\\'

    # LResult = pathlib.WindowsPath (APath)

    # LResult = APath.rstrip('/')+'/'

    return LResult
#endfunction

#--------------------------------------------------------------------------------
# GetDirNameYYMMDD
#--------------------------------------------------------------------------------
def GetDirNameYYMMDD (ARootDir: str, ADate: datetime.datetime) -> str:
    """GetDirNameYYMMDD"""
#beginfunction
    # LYMD = LUDateTime.DecodeDate_ (ADate)
    LYMDStr: str = LUDateTime.DateTimeStr(False, ADate, LUDateTime.cFormatDateYYMMDD_02, False)
    LResult = IncludeTrailingBackslash(ARootDir)+LYMDStr
    return LResult
#endfunction

#--------------------------------------------------------------------------------
# GetDirNameYYMM
#--------------------------------------------------------------------------------
def GetDirNameYYMM (ARootDir: str, ADate: datetime.datetime) -> str:
    """GetDirNameYYMM"""
#beginfunction
    LYMDStr: str = LUDateTime.DateTimeStr(False, ADate, LUDateTime.cFormatDateYYMM_02, False)
    LResult = IncludeTrailingBackslash(ARootDir)+LYMDStr
    return LResult
#endfunction

#--------------------------------------------------------------------------------
# GetTempDir
#--------------------------------------------------------------------------------
def GetTempDir () -> str:
    """GetTempDir"""
#beginfunction
    # LResult = win32api.GetTempPath()
    LResult = tempfile.gettempdir ()
    return LResult
#endfunction

#--------------------------------------------------------------------------------
# SearchFile
#--------------------------------------------------------------------------------
def SearchFile (AFileName: str, ADefaultExt: str) -> str:
    """SearchFile"""
#beginfunction
    LResult = AFileName
    if ExtractFileDir (LResult) == '':
        if ExtractFileExt (LResult) == '':
            LResult = LResult + ADefaultExt
        #endif
        # int = SearchPath(path, fileName , fileExt )
        #   The return value is a tuple of (string, int).
        #   string - представляет собой полный путь. int — смещение в строке базового имени файла.

        # L = win32api.SearchPath (None, LResult, None)
        print('L = win32api.SearchPath (None, LResult, None)')
        LResult = ''
        #L = ''
        #if L[0] != '':
        #    LResult = L[0]
        #else:
        #    LResult = ''
        ##endif
    else:
        if ExtractFileExt (LResult) == '':
            LResult = LResult + ADefaultExt
        #endif
        LResult = ExpandFileName (LResult)
        if not FileExists (LResult):
            LResult = ''
        #endif
    #endif
    return LResult
#endfunction

#--------------------------------------------------------------------------------
# SearchINIFile
#--------------------------------------------------------------------------------
def SearchINIFile (AFileName: str) -> str:
    """SearchINIFile"""
#beginfunction
    LResult = SearchFile (AFileName, '.ini')
    return LResult
#endfunction

#-------------------------------------------------------------------------------
# SearchEXEFile
#-------------------------------------------------------------------------------
def SearchEXEFile (AFileName: str) -> str:
    """SearchEXEFile"""
#beginfunction
    LResult = SearchFile (AFileName, '.exe')
    return LResult
#endfunction

#-------------------------------------------------------------------------------
# FileSearch
#-------------------------------------------------------------------------------
def FileSearch (AFileName: str, APath: str) -> str:
    """FileSearch"""
#beginfunction
    try:
        # L = win32api.SearchPath (APath, AFileName, None)
        print('L = win32api.SearchPath (APath, AFileName, None)')
        L = ''
        if L [0] != '':
            LResult = L [0]
        else:
            LResult = ''
        #endif
    except:
        LResult = ''
    return LResult
#endfunction

#-------------------------------------------------------------------------------
# SetFileAttr
#-------------------------------------------------------------------------------
def SetFileAttr (AFileName: str, Aflags) -> bool:
    """SetFileAttr"""
#beginfunction
    LResult = True
    LOSInfo = LUos.TOSInfo ()
    match LOSInfo.system.upper ():
        case 'LINUX':
            # os.chflags() method in Python used to set the flags of path to the numeric flags;
            # available in Unix only
            os.chflags (AFileName, Aflags)
        case 'WINDOWS':
            FILE_ATTRIBUTE_HIDDEN = 0x02
            LResult = ctypes.windll.kernel32.SetFileAttributesW (AFileName, FILE_ATTRIBUTE_HIDDEN)
            ...
        case _:
            ...
    #endmatch
    return LResult
#endfunction

#-------------------------------------------------------------------------------
# GetFileAttr
#-------------------------------------------------------------------------------
def GetFileAttr (AFileName: str) -> int:
    """GetFileAttr"""
#beginfunction
    LResult = 0
    if FileExists (AFileName):
        LStat = os.stat (AFileName)
        Lmode = LStat.st_mode

        # print ('Lmode:', Lmode, stat.filemode (Lmode))

        Lattr = LStat.st_file_attributes
        print ('Lattr:', Lattr, hex(Lattr), bin(Lattr))
        print ('stat.FILE_ATTRIBUTE_ARCHIVE',bin(stat.FILE_ATTRIBUTE_ARCHIVE))
        print ('stat.FILE_ATTRIBUTE_SYSTEM',bin(stat.FILE_ATTRIBUTE_SYSTEM))
        print ('stat.FILE_ATTRIBUTE_HIDDEN',bin(stat.FILE_ATTRIBUTE_HIDDEN))
        print ('stat.FILE_ATTRIBUTE_READONLY',bin(stat.FILE_ATTRIBUTE_READONLY))

        # print (stat.FILE_ATTRIBUTE_READONLY)
        # print ("Attributes of:", AFileName)
        if LStat.st_file_attributes & stat.FILE_ATTRIBUTE_ARCHIVE:  print (" - archive")
        if LStat.st_file_attributes & stat.FILE_ATTRIBUTE_SYSTEM:   print (" - system")
        if LStat.st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN:   print (" - hidden")
        if LStat.st_file_attributes & stat.FILE_ATTRIBUTE_READONLY: print (" - read only")

        # LAccess = os.access (AFileName, os.R_OK)
        # LAccess = os.access (AFileName, os.W_OK)
        # Clear ReadOnly
        # FileSetAttr (FileName, FileGetAttr(FileName) and (faReadOnly xor $FF));
        # import win32con
        # import win32api
        # attrs = win32api.GetFileAttributes (filepath)
        # attrs & win32con.FILE_ATTRIBUTE_SYSTEM
        # attrs & win32con.FILE_ATTRIBUTE_HIDDEN

        # Change the file's permissions to writable
        # os.chmod (AFileName, os.W_OK)

        LResult = Lattr
    #endif
    return LResult
#endfunction

#-------------------------------------------------------------------------------
# FileDelete
#-------------------------------------------------------------------------------
def FileDelete (AFileName: str) -> bool:
    """FileDelete"""
#beginfunction
    LResult = True
    if FileExists (AFileName):
        try:
            # Clear ReadOnly
            # FileSetAttr (FileName, FileGetAttr(FileName) and (faReadOnly xor $FF));

            # Change the file's permissions to writable
            os.chmod (AFileName, os.W_OK)
            # Remove the file
            os.remove (AFileName)
            LResult = True
        except:
            LResult = False
        #endtry
    #endif
    return LResult
#endfunction

#-------------------------------------------------------------------------------
# FileCopy
#-------------------------------------------------------------------------------
def FileCopy (AFileNameSource: str, AFileNameDest: str, Overwrite: bool) -> bool:
    """FileCopy"""
#beginfunction
    LDestPath = ExtractFileDir(AFileNameDest)
    if not DirectoryExists(LDestPath):
        ForceDirectories(LDestPath)
    #endif
    LResult = shutil.copy (AFileNameSource, AFileNameDest)
    return LResult
#endfunction

#-------------------------------------------------------------------------------
# FileMove
#-------------------------------------------------------------------------------
def FileMove (AFileNameSource: str, APathNameDest: str) -> bool:
    """FileMove"""
#beginfunction
    if not LUFile.DirectoryExists(APathNameDest):
        LUFile.ForceDirectories(APathNameDest)
    #endif
    LFileNameSource = ExtractFileName (AFileNameSource)
    LFileNameDest = os.path.join (APathNameDest, LFileNameSource)
    LResult = FileCopy (AFileNameSource, LFileNameDest, True);
    if Result:
        Result = FileDelete (AFileNameSource);
    #endif
    return LResult
#endfunction

#-------------------------------------------------------------------------------
# CheckFileNameMask
#-------------------------------------------------------------------------------
def CheckFileNameMask (AFileName: str, AMask: str) -> bool:
    """CheckFileNameMask"""
#beginfunction
    LFileName = AFileName
    # LMask = '^[a-zA-Z0-9]+.py$'         # *.py - только латинские буквы и цифры
    # LMask = '^.*..*$'                   # *.* - все символы
    # LMask = '^.*.py$'                   # *.py - все символы
    # LMask = '^[\\S ]*.py$'              # *.py - все символы включая пробелы
    # LMask = '^[a-zA-Z0-9]*.py$'         # *.py - только латинские буквы и цифры
    LMask = AMask
    #-------------------------------------------------------------------------------
    # regex = re.compile (LMask)
    # Lresult = regex.match(LFileName)
    #-------------------------------------------------------------------------------
    # эквивалентно
    #-------------------------------------------------------------------------------
    Lresult = re.match (LMask, LFileName)
    # Lresult = re.search (LMask, LFileName)
    #-------------------------------------------------------------------------------

    # regex = re.compile (LMask)
    # if regex.match(LFileName):
    #     print(LFileName + ' ok!')
    # else:
    #     print(LFileName + ' not match')
    # #endif
    # matches = re.finditer (regex, AFileName, re.MULTILINE)
    return Lresult
#endfunction

#-------------------------------------------------------------------------------
# CreateTextFile
#-------------------------------------------------------------------------------
def CreateTextFile(AFileName: str, AText: str, AEncoding: str):
    """CreateTextFile"""
#beginfunction
    LEncoding = AEncoding
    if AEncoding == '':
        LEncoding = LUStrDecode.cCP1251
    if len(AText) > 0:
        LFile = open (AFileName, 'w', encoding = LEncoding)
        LFile.write (AText + '\n')
        LFile.flush ()
        LFile.close ()
    else:
        FileDelete (AFileName)
        LFile = open (AFileName, 'w', encoding = LEncoding)
        LFile.flush ()
        LFile.close ()
   #endif
#endfunction

#--------------------------------------------------------------------------------
# WriteStrToFile (AStr: str, AFileName: str):
#--------------------------------------------------------------------------------
def WriteStrToFile (AFileName: str, AStr: str):
    """WriteStrToFile"""
#beginfunction
    # Откроет для добавления нового содержимого.
    # Создаст новый файл для чтения записи, если не найдет с указанным именем.
    LEncoding = GetFileEncoding (AFileName)
    if LEncoding == '':
        LEncoding = cDefaultEncoding
    LFile = open (AFileName, 'a+', encoding = LEncoding)
    LFile.write (AStr)
    LFile.flush ()
    LFile.close ()
#endfunction

#-------------------------------------------------------------------------------
# OpenTextFile
#-------------------------------------------------------------------------------
def OpenTextFile(AFileName: str, AEncoding: str):
    """OpenTextFile"""
#beginfunction
    LEncoding = AEncoding
    if AEncoding == '':
        LEncoding = LUStrDecode.cCP1251
    LHandle = open (AFileName, 'a+', encoding = LEncoding)
    return LHandle
#endfunction

#-------------------------------------------------------------------------------
# CloseTextFile
#-------------------------------------------------------------------------------
def CloseTextFile (AHandle):
    """CloseTextFile"""
#beginfunction
    AHandle.flush ()
    AHandle.close ()
#endfunction

#------------------------------------------
def main ():
#beginfunction
    ...
#endfunction

#------------------------------------------
#
#------------------------------------------
#beginmodule
if __name__ == "__main__":
    main()
#endif

#endmodule
