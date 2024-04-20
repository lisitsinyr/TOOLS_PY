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
import os
import platform
import stat
import datetime
import logging
import tempfile
import re
import ctypes
import pathlib
if platform.system() == 'Windows':
    import win32api
    import win32con
#endif
if platform.system() == 'Linux':
    ...
#endif

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
import LULog

"""
#--------------------------------------------------------------------------------
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# if not file.endswith(ext):
#     contains_other_ext=True
#--------------------------------------------------------------------------------
"""

"""
#--------------------------------------------------------------------------------
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
#--------------------------------------------------------------------------------
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
    try:
        os.makedirs (ADir, exist_ok = True)
    except:
        s = f'Unable to create directory {ADir:s} ...'
        LULog.LoggerTOOLS_AddLevel(logging.error, s)
    #endtry
    LResult = DirectoryExists (ADir)
    return LResult
#endfunction

#--------------------------------------------------------------------------------
# GetDirectoryTreeSize
#--------------------------------------------------------------------------------
def GetDirectoryTreeSize(ADir: str) -> int:
    """GetDirectoryTreeSize"""
    """Return total size of files in given path and subdirs"""
#beginfunction
    Ltotal = 0
    for Lentry in os.scandir(ADir):
        if Lentry.is_dir(follow_symlinks=False):
            Ltotal += GetDirectoryTreeSize(Lentry.path)
        else:
            Ltotal += Lentry.stat(follow_symlinks=False).st_size
    return Ltotal
#endfunction

#--------------------------------------------------------------------------------
# DeleteDirectoryTree
#--------------------------------------------------------------------------------
def DeleteDirectoryTree (ADir: str) -> bool:
    """DeleteDirectoryTree"""
    """
    Удалить дерево каталогов в Windows,
    где для некоторых файлов установлен бит только для чтения.
    Он использует обратный вызов onerror, чтобы очистить бит readonly и повторить попытку удаления.
    """
    def remove_readonly (func, path, _):
        """remove_readonly"""
    #beginfunction
        s = f'Clear the readonly bit and reattempt the removal {path:s} ...'
        LULog.LoggerTOOLS_AddLevel(logging.DEBUG, s)
        os.chmod (path, stat.S_IWRITE)
        func (path)
    #endfunction

    def errorRemoveReadonly (func, path, exc):
        """errorRemoveReadonly"""
    #beginfunction
        excvalue = exc [1]
        if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
            # change the file to be readable,writable,executable: 0777
            os.chmod (path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
            # retry
            func (path)
        else:
            # raiseenter code here
            ...
        #endif
    #endfunction

#beginfunction
    if DirectoryExists (ADir):
        s = f'DeleteDirectoryTree {ADir:s} ...'
        LULog.LoggerTOOLS_AddLevel(logging.DEBUG, s)
        try:
            # shutil.rmtree (ADirectoryName, ignore_errors = True, onexc = None)
            shutil.rmtree (ADir, ignore_errors = False, onerror = remove_readonly)
            LResult = True
        except:
            s = f'Unable delete directory {ADir:s} ...'
            LULog.LoggerTOOLS_AddLevel (logging.error, s)
            LResult = False
        #endtry
    #endif
    return LResult
#endfunction

#--------------------------------------------------------------------------------
# DeleteDirectory_walk
#--------------------------------------------------------------------------------
# Delete everything reachable from the directory named in 'top',
# assuming there are no symbolic links.
# CAUTION:  This is dangerous!  For example, if top == '/', it
# could delete all your disk files.
#--------------------------------------------------------------------------------
def ClearDirectory (ADir: str) -> bool:
    """ClearDirectory"""
#beginfunction
    LResult = True
    if DirectoryExists (ADir):
        for root, dirs, files in os.walk (ADir, topdown = False):
            for file in files:
                os.remove (os.path.join (root, file))
            #endfor
            for dir in dirs:
                os.rmdir (os.path.join (root, dir))
            #endfor
        #endfor
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
    LFileTimeCreate = 0
    LFileTimeMod = 0
    LFileTimeCreateDate = 0
    LFileTimeModDate = 0
    if FileExists (AFileName):
        # file creation
        LFileTimeCreate: datetime = os.path.getctime (AFileName)
        # file modification
        LFileTimeMod: datetime = os.path.getmtime (AFileName)
        # convert creation timestamp into DateTime object
        LFileTimeCreateDate: datetime = datetime.datetime.fromtimestamp (LFileTimeCreate)
        # convert timestamp into DateTime object
        LFileTimeModDate: datetime = datetime.datetime.fromtimestamp (LFileTimeMod)
    #endif
    LTuple = (LFileTimeMod, LFileTimeCreate, LFileTimeModDate, LFileTimeCreateDate)
    return LTuple
#endfunction

#--------------------------------------------------------------------------------
# GetDirDateTime
#--------------------------------------------------------------------------------
def GetDirDateTime (AFileName: str) -> ():
    """GetDirDateTime"""
#beginfunction
    LTuple = ()
    LFileTimeCreate = 0
    LFileTimeMod = 0
    LFileTimeCreateDate = 0
    LFileTimeModDate = 0
    if DirectoryExists (AFileName):
        # file creation
        LFileTimeCreate: datetime = os.path.getctime (AFileName)
        # file modification
        LFileTimeMod: datetime = os.path.getmtime (AFileName)
        # convert creation timestamp into DateTime object
        LFileTimeCreateDate: datetime = datetime.datetime.fromtimestamp (LFileTimeCreate)
        # convert timestamp into DateTime object
        LFileTimeModDate: datetime = datetime.datetime.fromtimestamp (LFileTimeMod)
    #endif
    LTuple = (LFileTimeMod, LFileTimeCreate, LFileTimeModDate, LFileTimeCreateDate)
    return LTuple
#endfunction

def cmptimestamps(AFileNameSource: str, AFileNameDest: str, _use_ctime):
    """ Compare time stamps of two files and return True
    if file1 (source) is more recent than file2 (target) """
#beginfunction
    st1 = os.stat (AFileNameSource)
    st2 = os.stat (AFileNameDest)
    mtime_cmp = int((st1.st_mtime - st2.st_mtime) * 1000) > 0
    if _use_ctime:
        return mtime_cmp or int((AFileNameSource.st_ctime - AFileNameDest.st_mtime) * 1000) > 0
    else:
        return mtime_cmp
    #endif
#endfunction

#--------------------------------------------------------------------------------
# COMPAREFILETIMES
#--------------------------------------------------------------------------------
def COMPAREFILETIMES (AFileNameSource: str, AFileNameDest: str) -> int:
    """COMPAREFILETIMES"""
#beginfunction
    if not FileExists (AFileNameSource):
        #-2 File1 could not be opened (see @ERROR for more information).
        return -2
    #endif
    if not FileExists (AFileNameDest):
        #-3 File2 could not be opened (see @ERROR for more information).
        return -3
    #endif

    LFileName1m = GetFileDateTime (AFileNameSource)[0]
    LFileName2m = GetFileDateTime (AFileNameDest)[0]
    LFileName1c = GetFileDateTime (AFileNameSource)[0]
    LFileName2c = GetFileDateTime (AFileNameDest)[0]

    if LFileName1m == LFileName2m:
        #0 File1 and file2 have the same date and time.
        return 0
    else:
        if LFileName1m > LFileName2m:
            #1 File1 is more recent than file2.
            return 1
        else:
            #-1 File1 is older than file2.
            return -1
        #endif
    #endif
    #------------------------------------------------------------------------------
    # if int ((LFileName1m - LFileName2m) * 1000) == 0:
    #     return 0
    # else:
    #     if int ((LFileName1m - LFileName2m) * 1000) > 0:
    #         return 1
    #     else:
    #         return -1
    #     #endif
    # #endif
    #------------------------------------------------------------------------------
#endfunction

#--------------------------------------------------------------------------------
# GetFileSize
#--------------------------------------------------------------------------------
def GetFileSize (AFileName: str) -> int:
    """GetFileSize"""
#beginfunction
    if FileExists (AFileName):
        LResult = os.path.getsize (AFileName)
    else:
        LResult = 0
    #endif
    return LResult
#endfunction

#--------------------------------------------------------------------------------
# ExpandFileName
#--------------------------------------------------------------------------------
def ExpandFileName (APath: str) -> str:
    """ExpandFileName"""
#beginfunction
    LResult = os.path.abspath(APath)
    return LResult
#endfunction

#--------------------------------------------------------------------------------
# ExtractFileDir
#--------------------------------------------------------------------------------
def ExtractFileDir (APath: str) -> str:
    """ExtractFileDir"""
#beginfunction
    LDir, LFileName = os.path.split(APath)
    return LDir
#endfunction

#--------------------------------------------------------------------------------
# ExtractFileName
#--------------------------------------------------------------------------------
def ExtractFileName (APath: str) -> str:
    """ExtractFileName"""
#beginfunction
    LPath, LFileName = os.path.split(APath)
    return LFileName
#endfunction

#-------------------------------------------------------------------------------
# ExtractFileNameWithoutExt
#-------------------------------------------------------------------------------
def ExtractFileNameWithoutExt (AFileName: str) -> str:
    """ExtractFileNameWithoutExt"""
#beginfunction
    LResult = os.path.basename (AFileName).split ('.') [0]
    return LResult
#endfunction

#--------------------------------------------------------------------------------
# ExtractFileExt
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
    #endif
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
    LResult = win32api.GetTempPath()
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
    if ExtractFileDir (AFileName) == '':
        if ExtractFileExt (AFileName) == '':
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
        if ExtractFileExt (AFileName) == '':
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
# FileAttrStr
#-------------------------------------------------------------------------------
def FileAttrStr (Aattr: int) -> str:
    """FileAttrStr"""
#beginfunction
    #-------------------------------------------------------------------------------
    #                                        0x      00       00       20       20
    #                                        0b00000000 00000000 00100000 00100000
    #-------------------------------------------------------------------------------
    #stat.FILE_ATTRIBUTE_NO_SCRUB_DATA       0b00000000 00000010 00000000 00000000
    #stat.FILE_ATTRIBUTE_VIRTUAL             0b00000000 00000001 00000000 00000000

    #stat.FILE_ATTRIBUTE_INTEGRITY_STREAM    0b00000000 00000000 10000000 00000000
    #stat.FILE_ATTRIBUTE_ENCRYPTED           0b00000000 00000000 01000000 00000000
    #stat.FILE_ATTRIBUTE_NOT_CONTENT_INDEXED 0b00000000 00000000 00100000 00000000
    #stat.FILE_ATTRIBUTE_OFFLINE             0b00000000 00000000 00010000 00000000
    #stat.FILE_ATTRIBUTE_COMPRESSED          0b00000000 00000000 00001000 00000000
    #stat.FILE_ATTRIBUTE_REPARSE_POINT       0b00000000 00000000 00000100 00000000
    #stat.FILE_ATTRIBUTE_SPARSE_FILE         0b00000000 00000000 00000010 00000000
    #stat.FILE_ATTRIBUTE_TEMPORARY           0b00000000 00000000 00000001 00000000

    #stat.FILE_ATTRIBUTE_NORMAL              0b00000000 00000000 00000000 10000000
    #stat.FILE_ATTRIBUTE_DEVICE              0b00000000 00000000 00000000 01000000
    #-------------------------------------------------------------------------------
    #stat.FILE_ATTRIBUTE_ARCHIVE             0b00000000 00000000 00000000 00100000
    #-------------------------------------------------------------------------------
    #stat.FILE_ATTRIBUTE_DIRECTORY           0b00000000 00000000 00000000 00010000
    #-------------------------------------------------------------------------------
    #stat.                                   0b00000000 00000000 00000000 00001000
    #-------------------------------------------------------------------------------
    #stat.FILE_ATTRIBUTE_SYSTEM              0b00000000 00000000 00000000 00000100
    #-------------------------------------------------------------------------------
    #stat.FILE_ATTRIBUTE_HIDDEN              0b00000000 00000000 00000000 00000010
    #-------------------------------------------------------------------------------
    #stat.FILE_ATTRIBUTE_READONLY            0b00000000 00000000 00000000 00000001
    #-------------------------------------------------------------------------------
    Lattr = Aattr
    sa = ''
    sa += '????????'
    sa += '1' if Lattr & 0b100000000000000000000000 else '?'
    sa += '1' if Lattr & 0b010000000000000000000000 else '?'
    sa += '1' if Lattr & 0b001000000000000000000000 else '?'
    sa += '1' if Lattr & 0b000100000000000000000000 else '?'
    sa += '1' if Lattr & 0b000010000000000000000000 else '?'
    sa += '1' if Lattr & 0b000001000000000000000000 else '?'
    sa += '1' if Lattr & stat.FILE_ATTRIBUTE_NO_SCRUB_DATA else '.'
    sa += '1' if Lattr & stat.FILE_ATTRIBUTE_VIRTUAL else '.'

    sa += '1' if Lattr & stat.FILE_ATTRIBUTE_INTEGRITY_STREAM else '.'
    sa += '1' if Lattr & stat.FILE_ATTRIBUTE_ENCRYPTED else '.'
    sa += '1' if Lattr & stat.FILE_ATTRIBUTE_NOT_CONTENT_INDEXED else '.'
    sa += '1' if Lattr & stat.FILE_ATTRIBUTE_OFFLINE else '.'
    sa += '1' if Lattr & stat.FILE_ATTRIBUTE_COMPRESSED else '.'
    sa += '1' if Lattr & stat.FILE_ATTRIBUTE_REPARSE_POINT else '.'
    sa += '1' if Lattr & stat.FILE_ATTRIBUTE_SPARSE_FILE else '.'
    sa += '1' if Lattr & stat.FILE_ATTRIBUTE_TEMPORARY else '.'

    sa += '1' if Lattr & stat.FILE_ATTRIBUTE_NORMAL else '.'
    sa += '1' if Lattr & stat.FILE_ATTRIBUTE_DEVICE else '.'
    sa += 'a' if Lattr & stat.FILE_ATTRIBUTE_ARCHIVE else '.'
    sa += 'd' if Lattr & stat.FILE_ATTRIBUTE_DIRECTORY else '.'
    sa += '.'
    sa += 's' if Lattr & stat.FILE_ATTRIBUTE_SYSTEM else '.'
    sa += 'h' if Lattr & stat.FILE_ATTRIBUTE_HIDDEN else '.'
    sa += 'r' if Lattr & stat.FILE_ATTRIBUTE_READONLY else '.'
    return sa
#endfunction

#-------------------------------------------------------------------------------
# FileAttrStrUnix
#-------------------------------------------------------------------------------
def FileAttrStrUnix (Amode: int) -> str:
    """FileAttrStr"""
#beginfunction
    # chmod(path,mode)
    # s = f'stat.S_ISUID: {bin (stat.S_ISUID):s}'
    # LULog.LoggerTOOLS_AddLevel (LULog.TEXT, s)
    # s = f'stat.S_ISGID: {bin (stat.S_ISGID):s}'
    # LULog.LoggerTOOLS_AddLevel (LULog.TEXT, s)
    # s = f'stat.S_ENFMT: {bin (stat.S_ENFMT):s}'
    # LULog.LoggerTOOLS_AddLevel (LULog.TEXT, s)
    # s = f'stat.S_ISVTX: {bin (stat.S_ISVTX):s}'
    # LULog.LoggerTOOLS_AddLevel (LULog.TEXT, s)
    # s = f'stat.S_IREAD: {bin (stat.S_IREAD):s}'
    # LULog.LoggerTOOLS_AddLevel (LULog.TEXT, s)
    # s = f'stat.S_IWRITE: {bin (stat.S_IWRITE):s}'
    # LULog.LoggerTOOLS_AddLevel (LULog.TEXT, s)
    # s = f'stat.S_IEXEC: {bin (stat.S_IEXEC):s}'
    # LULog.LoggerTOOLS_AddLevel (LULog.TEXT, s)
    # s = f'stat.S_IRWXU: {bin (stat.S_IRWXU):s}'
    # LULog.LoggerTOOLS_AddLevel (LULog.TEXT, s)
    # s = f'stat.S_IRUSR: {bin (stat.S_IRUSR):s}'
    # LULog.LoggerTOOLS_AddLevel (LULog.TEXT, s)
    # s = f'stat.S_IWUSR: {bin (stat.S_IWUSR):s}'
    # LULog.LoggerTOOLS_AddLevel (LULog.TEXT, s)
    # s = f'stat.S_IXUSR: {bin (stat.S_IXUSR):s}'
    # LULog.LoggerTOOLS_AddLevel (LULog.TEXT, s)
    # s = f'stat.S_IRWXG: {bin (stat.S_IRWXG):s}'
    # LULog.LoggerTOOLS_AddLevel (LULog.TEXT, s)
    # s = f'stat.S_IRGRP: {bin (stat.S_IRGRP):s}'
    # LULog.LoggerTOOLS_AddLevel (LULog.TEXT, s)
    # s = f'stat.S_IWGRP: {bin (stat.S_IWGRP):s}'
    # LULog.LoggerTOOLS_AddLevel (LULog.TEXT, s)
    # s = f'stat.S_IXGRP: {bin (stat.S_IXGRP):s}'
    # LULog.LoggerTOOLS_AddLevel (LULog.TEXT, s)
    # s = f'stat.S_IRWXO: {bin (stat.S_IRWXO):s}'
    # LULog.LoggerTOOLS_AddLevel (LULog.TEXT, s)
    # s = f'stat.S_IROTH: {bin (stat.S_IROTH):s}'
    # LULog.LoggerTOOLS_AddLevel (LULog.TEXT, s)
    # s = f'stat.S_IWOTH: {bin (stat.S_IWOTH):s}'
    # LULog.LoggerTOOLS_AddLevel (LULog.TEXT, s)
    # s = f'stat.S_IXOTH: {bin (stat.S_IXOTH):s}'
    # LULog.LoggerTOOLS_AddLevel (LULog.TEXT, s)

    #-------------------------------------------------------------------------------
    # stat.S_ISUID − Set user ID on execution
    # stat.S_ISUID:  0b00010000 00000000
    # stat.S_ISGID − Set group ID on execution
    # stat.S_ISGID:  0b00000100 00000000
    # stat.S_ENFMT – Enforced record locking
    # stat.S_ENFMT:  0b00000100 00000000
    # stat.S_ISVTX – After execution, save text image
    # stat.S_ISVTX:  0b00000010 00000000
    #-------------------------------------------------------------------------------
    # stat.S_IREAD − Read by owner
    # stat.S_IREAD:  0b00000001 00000000
    # stat.S_IWRITE − Write by owner
    # stat.S_IWRITE: 0b00000000 10000000
    # stat.S_IEXEC − Execute by owner
    # stat.S_IEXEC:  0b00000000 01000000
    #-------------------------------------------------------------------------------
    # stat.S_IRWXU − Read, write, and execute by owner
    # stat.S_IRWXU:  0b00000001 11000000 Owner
    #-------------------------------------------------------------------------------
    # stat.S_IRUSR − Read by owner
    # stat.S_IRUSR:  0b00000001 00000000
    # stat.S_IWUSR − Write by owner
    # stat.S_IWUSR:  0b00000000 10000000
    # stat.S_IXUSR − Execute by owner
    # stat.S_IXUSR:  0b00000000 01000000
    #-------------------------------------------------------------------------------
    # stat.S_IRWXG − Read, write, and execute by group
    # stat.S_IRWXG:  0b00000000 00111000 Group
    #-------------------------------------------------------------------------------
    # stat.S_IRGRP − Read by group
    # stat.S_IRGRP:  0b00000000 00100000
    # stat.S_IWGRP − Write by group
    # stat.S_IWGRP:  0b00000000 00010000
    # stat.S_IXGRP − Execute by group
    # stat.S_IXGRP:  0b00000000 00001000
    #-------------------------------------------------------------------------------
    # stat.S_IRWXO − Read, write, and execute by others
    # stat.S_IRWXO:  0b00000000 00000111 Others
    #-------------------------------------------------------------------------------
    # stat.S_IROTH − Read by others
    # stat.S_IROTH:  0b00000000 00000100
    # stat.S_IWOTH − Write by others
    # stat.S_IWOTH:  0b00000000 00000010
    # stat.S_IXOTH − Execute by others
    # stat.S_IXOTH:  0b00000000 00000001
    #-------------------------------------------------------------------------------
    Lmode = Amode
    sa = ''
    sa += '1' if Lmode & 0b1000000000000000 else '-'
    sa += '1' if Lmode & 0b0100000000000000 else '-'
    sa += '1' if Lmode & 0b0010000000000000 else '-'

    sa += '1' if Lmode & stat.S_ISUID else '-'
    sa += '1' if Lmode & stat.S_ISGID else '-'
    sa += '1' if Lmode & stat.S_ENFMT else '-'
    sa += '1' if Lmode & stat.S_ISVTX else '-'
    #-------------------------------------------------------------------------------
    sa += 'r' if Lmode & stat.S_IRUSR else '-'
    sa += 'w' if Lmode & stat.S_IWUSR else '-'
    sa += 'x' if Lmode & stat.S_IXUSR else '-'
    #-------------------------------------------------------------------------------
    sa += 'r' if Lmode & stat.S_IRGRP else '-'
    sa += 'w' if Lmode & stat.S_IWGRP else '-'
    sa += 'x' if Lmode & stat.S_IXGRP else '-'
    #-------------------------------------------------------------------------------
    sa += 'r' if Lmode & stat.S_IROTH else '-'
    sa += 'w' if Lmode & stat.S_IWOTH else '-'
    sa += 'x' if Lmode & stat.S_IXOTH else '-'
    return sa
#endfunction

#-------------------------------------------------------------------------------
# GetFileAttr
#-------------------------------------------------------------------------------
def GetFileAttr (AFileName: str) -> int:
    """GetFileAttr"""
#beginfunction
    s = f'GetFileAttr: {AFileName:s}'
    LULog.LoggerTOOLS_AddLevel (logging.DEBUG, s)
    LResult = 0

    if FileExists (AFileName) or DirectoryExists (AFileName):
        LStat = os.stat (AFileName)

        Lmode = LStat.st_mode
        s = f'Lmode: {Lmode:d} {stat.filemode (Lmode):s}'
        LULog.LoggerTOOLS_AddLevel (logging.DEBUG, s)

        if platform.system() == 'Windows':
            Lattr = LStat.st_file_attributes
            LResult = Lattr
            # Lattr = win32api.GetFileAttributes (AFileName)
            s = f'Lattr:{Lattr:d} {hex (Lattr):s} {bin (Lattr):s} {FileAttrStr (Lattr):s}'
        else:
            LResult = Lmode
            s = f'Lmode:{Lmode:d} {hex (Lmode):s} {bin (Lmode):s} {FileAttrStrUnix (Lmode):s}'
            # 2113 Lmode:33204 0x81b4 0b1000000110110100 -------rw-rw-r--
        #endif
        LULog.LoggerTOOLS_AddLevel(logging.DEBUG, s)

    #endif
    return LResult
#endfunction

#-------------------------------------------------------------------------------
# SetFileAttr
#-------------------------------------------------------------------------------
def SetFileAttr (AFileName: str, Aflags: int, AClear: bool):
    """SetFileAttr"""
#beginfunction
    s = f'SetFileAttr: {Aflags:d} {hex (Aflags):s} {bin (Aflags):s}'
    LULog.LoggerTOOLS_AddLevel (logging.DEBUG, s)

    LOSInfo = LUos.TOSInfo ()
    match LOSInfo.system.upper ():
        case 'WINDOWS':
            Lattr = GetFileAttr(AFileName)
            s = f'SetFileAttr: {Aflags:d} {hex (Aflags):s} {bin (Aflags):s}'
            LULog.LoggerTOOLS_AddLevel (logging.DEBUG, s)

            if AClear:
                LattrNew = Lattr & ~Aflags
                s = f'SetFileAttr [clear]: {bin (Aflags):s} {LattrNew:d} {hex (LattrNew):s} {bin (LattrNew):s}'
                LULog.LoggerTOOLS_AddLevel (logging.DEBUG, s)
            else:
                LattrNew = Lattr | Aflags
                s = f'SetFileAttr [set]: {bin (Aflags):s}{LattrNew:d} {hex (LattrNew):s} {bin (LattrNew):s}'
                LULog.LoggerTOOLS_AddLevel (logging.DEBUG, s)
            #endif

            # if os.path.isdir (AFileName):
            #     LResult = ctypes.windll.kernel32.SetFileAttributesW (AFileName, LattrNew)
            # else:
            #     win32api.SetFileAttributes (AFileName, LattrNew)
            # #endif
            LResult = ctypes.windll.kernel32.SetFileAttributesW (AFileName, LattrNew)

            # Change the file's permissions to writable
            # os.chmod (AFileName, os.W_OK)

        case 'LINUX':
            # os.chflags() method in Python used to set the flags of path to the numeric flags;
            # available in Unix only
            # os.UF_HIDDEN
            if AClear:
                LattrNew = Lattr & ~Aflags
                s = f'SetFileAttr [clear]: {bin (Aflags):s} {LattrNew:d} {hex (LattrNew):s} {bin (LattrNew):s}'
                LULog.LoggerTOOLS_AddLevel (logging.DEBUG, s)
            else:
                LattrNew = Lattr | Aflags
                s = f'SetFileAttr [set]: {bin (Aflags):s}{LattrNew:d} {hex (LattrNew):s} {bin (LattrNew):s}'
                LULog.LoggerTOOLS_AddLevel (logging.DEBUG, s)
            #endif
            os.chflags (AFileName, Aflags)
        case _:
            ...
    #endmatch
#endfunction

#-------------------------------------------------------------------------------
# FileDelete
#-------------------------------------------------------------------------------
def FileDelete (AFileName: str) -> bool:
    """FileDelete"""
#beginfunction
    s = f'FileDelete: {AFileName:s}'
    LULog.LoggerTOOLS_AddLevel (logging.DEBUG, s)
    LResult = True

    if FileExists (AFileName):
        try:
            Lattr = GetFileAttr(AFileName)
            if Lattr & stat.FILE_ATTRIBUTE_READONLY:
                s = f'SetFileAttr: {Aflags:d} {hex (Aflags):s} {bin (Aflags):s}'
                LULog.LoggerTOOLS_AddLevel (logging.DEBUG, s)
                # Clear ReadOnly
                LUFile.SetFileAttr (AFileName, stat.FILE_ATTRIBUTE_READONLY, True)
                # FileSetAttr (FileName, FileGetAttr(FileName) and (faReadOnly xor $FF));
                # Change the file's permissions to writable
                # os.chmod (AFileName, os.W_OK)
            #endif
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
    s = f'FileCopy: {AFileNameSource:s} -> {AFileNameDest:s}'
    LULog.LoggerTOOLS_AddLevel (logging.DEBUG, s)

    LDestPath = ExtractFileDir(AFileNameDest)
    if not DirectoryExists(LDestPath):
        ForceDirectories(LDestPath)
    #endif

    # Функция shutil.copy() копирует данные файла и режима доступа к файлу.
    # Другие метаданные, такие как время создания и время изменения файла не сохраняются.
    # Чтобы сохранить все метаданные файла из оригинала, используйте функцию shutil.copy2().

    # unix
    # LFileNameSource_stat = os.stat (AFileNameSource)
    # Lowner = LFileNameSource_stat [stat.ST_UID]
    # Lgroup = LFileNameSource_stat [stat.ST_GID]

    LResult = shutil.copy2 (AFileNameSource, AFileNameDest) != ''
    # LResult = shutil.copy2 (AFileNameSource, LDestPath) != ''

    # LResult = shutil.copy (AFileNameSource, AFileNameDest) != ''
    # shutil.copystat (AFileNameSource, AFileNameDest)

    # unix
    # os.chown (AFileNameDest, Lowner, Lgroup)

    return LResult

#endfunction

#-------------------------------------------------------------------------------
# FileMove
#-------------------------------------------------------------------------------
def FileMove (AFileNameSource: str, APathNameDest: str) -> bool:
    """FileMove"""
#beginfunction
    s = f'FileMove: {AFileNameSource:s} -> {APathNameDest:s}'
    LULog.LoggerTOOLS_AddLevel (logging.DEBUG, s)
    LResult = True

    if not LUFile.DirectoryExists(APathNameDest):
        LUFile.ForceDirectories(APathNameDest)
    #endif
    LFileNameSource = ExtractFileName (AFileNameSource)
    LFileNameDest = os.path.join (APathNameDest, LFileNameSource)

    LResult = shutil.move(AFileNameSource, APathNameDest, copy_function=shutil.copy2())

    # LResult = FileCopy (AFileNameSource, LFileNameDest, True);
    # if Result:
    #     Result = FileDelete (AFileNameSource);
    # #endif
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
    s = f'CreateTextFile: {AFileName:s} ...'
    LULog.LoggerTOOLS_AddLevel (logging.DEBUG, s)

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
    s = f'WriteStrToFile: {AFileName:s} ...'
    LULog.LoggerTOOLS_AddLevel (logging.DEBUG, s)

    # Откроет для добавления нового содержимого.
    # Создаст новый файл для чтения записи, если не найдет с указанным именем.
    LEncoding = GetFileEncoding (AFileName)
    if LEncoding == '':
        LEncoding = cDefaultEncoding
    LHandle = open (AFileName, 'a+', encoding = LEncoding)
    LHandle.write (AStr)
    LHandle.flush ()
    LHandle.close ()
#endfunction

#-------------------------------------------------------------------------------
# OpenTextFile
#-------------------------------------------------------------------------------
def OpenTextFile(AFileName: str, AEncoding: str) -> int:
    """OpenTextFile"""
#beginfunction
    s = f'OpenTextFile: {AFileName:s} ...'
    LULog.LoggerTOOLS_AddLevel (logging.DEBUG, s)

    LEncoding = AEncoding
    if AEncoding == '':
        LEncoding = LUStrDecode.cCP1251
    LHandle = open (AFileName, 'a+', encoding = LEncoding)
    return LHandle
#endfunction

#-------------------------------------------------------------------------------
# WriteTextFile
#-------------------------------------------------------------------------------
def WriteTextFile(AHandle, AStr: str):
    """WriteTextFile"""
#beginfunction
    AHandle.write (AStr+'\n')
    AHandle.flush ()
#endfunction

#-------------------------------------------------------------------------------
# CloseTextFile
#-------------------------------------------------------------------------------
def CloseTextFile (AHandle):
    """CloseTextFile"""
#beginfunction
    s = f'CloseTextFile ...'
    LULog.LoggerTOOLS_AddLevel (logging.DEBUG, s)

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
