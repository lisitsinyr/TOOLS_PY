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
# if platform.system() == 'Windows':
#     import win32api
#     print('Windows')
#     import win32con
# #endif
# if platform.system() == 'Linux':
#     ...
# #endif

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
def DirectoryClear (ADir: str) -> bool:
    """DirectoryClear"""
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
# CheckFileExt
#--------------------------------------------------------------------------------
def CheckFileExt (AFileName: str, AExt: str) -> bool:
    """CheckFileExt"""
#beginfunction
    LResult = AFileName.endswith(AExt)
    return LResult
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
    # LResult = win32api.GetTempPath()
    LResult = tempfile.gettempdir ()
    return LResult
#endfunction

#-------------------------------------------------------------------------------
# GetFileAttrStr
#-------------------------------------------------------------------------------
def GetFileAttrStr (Aattr: int) -> str:
    """GetFileAttrStr"""
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
# GetFileModeStrUnix
#-------------------------------------------------------------------------------
def GetFileModeStrUnix (Amode: int) -> str:
    """GetFileModeStrUnix"""
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

        LOSInfo = LUos.TOSInfo ()
        match LOSInfo.system:
            case 'Windows':
                Lmode = LStat.st_mode
                s = f'Lmode: {Lmode:d} {hex (Lmode):s} {bin (Lmode):s} {stat.filemode (Lmode):s}'
                LULog.LoggerTOOLS_AddLevel (logging.DEBUG, s)
                Lattr = LStat.st_file_attributes

                # Lattr = win32api.GetFileAttributes (AFileName)

                s = f'Lattr:{Lattr:d} {hex (Lattr):s} {bin (Lattr):s} {GetFileAttrStr (Lattr):s}'
                LULog.LoggerTOOLS_AddLevel (logging.DEBUG, s)
                LResult = Lattr
            case 'Linux':
                Lmode = LStat.st_mode
                s = f'Lmode:{Lmode:d} {hex (Lmode):s} {bin (Lmode):s} {GetFileModeStrUnix (Lmode):s}'
                LULog.LoggerTOOLS_AddLevel (logging.DEBUG, s)
                LResult = Lmode
            case _:
                s = f'Неизвестная система ...'
                LULog.LoggerTOOLS_AddLevel (logging.DEBUG, s)
                LResult = 0
        #endmatch
    #endif
    return LResult
#endfunction

#-------------------------------------------------------------------------------
# SetFileAttr
#-------------------------------------------------------------------------------
def SetFileAttr (AFileName: str, Aattr: int, AClear: bool):
    """SetFileAttr"""
#beginfunction
    s = f'SetFileAttr: {Aattr:d} {hex (Aattr):s} {bin (Aattr):s}'
    LULog.LoggerTOOLS_AddLevel (logging.DEBUG, s)

    LOSInfo = LUos.TOSInfo ()
    match LOSInfo.system:
        case 'Windows':
            Lattr = GetFileAttr(AFileName)
            s = f'Lattr - current: {Lattr:d} {hex (Lattr):s} {bin (Lattr):s}'
            LULog.LoggerTOOLS_AddLevel (logging.DEBUG, s)

            if AClear:
                LattrNew = Lattr & ~Aattr
                s = f'[clear]: {bin (LattrNew):s} {LattrNew:d} {hex (LattrNew):s} {bin (LattrNew):s}'
                LULog.LoggerTOOLS_AddLevel (logging.DEBUG, s)
            else:
                LattrNew = Lattr | Aflags
                s = f'[set]: {bin (LattrNew):s} {LattrNew:d} {hex (LattrNew):s} {bin (LattrNew):s}'
                LULog.LoggerTOOLS_AddLevel (logging.DEBUG, s)
            #endif

            # if os.path.isdir (AFileName):
            #     LResult = ctypes.windll.kernel32.SetFileAttributesW (AFileName, LattrNew)
            # else:
            #     win32api.SetFileAttributes (AFileName, LattrNew)
            # #endif

            LResult = ctypes.windll.kernel32.SetFileAttributesW (AFileName, LattrNew)
        case 'Linux':
            raise NotImplementedError('SetFileAttr Linux not implemented ...')
        case _:
            s = f'Неизвестная система ...'
            LULog.LoggerTOOLS_AddLevel (logging.DEBUG, s)
    #endmatch
#endfunction

#-------------------------------------------------------------------------------
# SetFileMode
#-------------------------------------------------------------------------------
def SetFileMode (AFileName: str, Amode: int):
    """SetFileMode"""
#beginfunction
    s = f'SetFileMode: {Amode:d} {hex (Amode):s} {bin (Amode):s}'
    LULog.LoggerTOOLS_AddLevel (logging.DEBUG, s)

    LOSInfo = LUos.TOSInfo ()
    match LOSInfo.system:
        case 'Windows':
            # Change the file's permissions to writable
            # os.chmod (AFileName, os.W_OK)
            ...
        case 'Linux':
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
            s = f'Неизвестная система ...'
            LULog.LoggerTOOLS_AddLevel (logging.DEBUG, s)
    #endmatch
#endfunction

#-------------------------------------------------------------------------------
# SetFileFlags
#-------------------------------------------------------------------------------
def SetFileFlags (AFileName: str, Aflags: int):
    """SetFileMode"""
#beginfunction
    s = f'SetFileMode: {Aflags:d} {hex (Aflags):s} {bin (Aflags):s}'
    LULog.LoggerTOOLS_AddLevel (logging.DEBUG, s)

    LOSInfo = LUos.TOSInfo ()
    match LOSInfo.system:
        case 'Windows':
            raise NotImplementedError('SetFileAttr Windows not implemented...')
        case 'Linux':
            # os.chflags() method in Python used to set the flags of path to the numeric flags;
            # available in Unix only
            # os.UF_HIDDEN

            Lattr = 0

            if AClear:
                LflagsNew = Lattr & ~Aflags
                s = f'[clear]: {bin (LflagsNew):s} {LflagsNew:d} {hex (LflagsNew):s} {bin (LflagsNew):s}'
                LULog.LoggerTOOLS_AddLevel (logging.DEBUG, s)
            else:
                LflagsNew = Lflags | Aflags
                s = f'[set]: {bin (LflagsNew):s} {LflagsNew:d} {hex (LflagsNew):s} {bin (LflagsNew):s}'
                LULog.LoggerTOOLS_AddLevel (logging.DEBUG, s)
            #endif
            os.chflags (AFileName, LflagsNew)
        case _:
            s = f'Неизвестная система ...'
            LULog.LoggerTOOLS_AddLevel (logging.DEBUG, s)
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
        LOSInfo = LUos.TOSInfo ()
        match LOSInfo.system:
            case 'Windows':
                try:
                    Lattr = GetFileAttr (AFileName)
                    if Lattr & stat.FILE_ATTRIBUTE_READONLY:
                        s = f'Clear ReadOnly ...'
                        LULog.LoggerTOOLS_AddLevel (logging.DEBUG, s)
                        LUFile.SetFileAttr (AFileName, stat.FILE_ATTRIBUTE_READONLY, True)

                        # FileSetAttr (FileName, FileGetAttr(FileName) and (faReadOnly xor $FF));
                        # Change the file's permissions to writable
                        # os.chmod (AFileName, os.W_OK)
                    #endif
                    os.remove (AFileName)
                    LResult = True
                except:
                    s = f'ERROR: FileDelete ...'
                    LULog.LoggerTOOLS_AddLevel (logging.DEBUG, s)
                    LResult = False
                #endtry
            case 'Linux':
                raise NotImplementedError('FileDelete Linux not implemented...')
            case _:
                s = f'Неизвестная система ...'
                LULog.LoggerTOOLS_AddLevel (logging.DEBUG, s)
        #endmatch
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

    if FileExists (AFileNameSource):

        LDestPath = ExtractFileDir (AFileNameDest)
        if not DirectoryExists (LDestPath):
            ForceDirectories (LDestPath)
        #endif

        LOSInfo = LUos.TOSInfo ()
        match LOSInfo.system:
            case 'Windows':
                try:
                    # Функция shutil.copy() копирует данные файла и режима доступа к файлу.
                    # Другие метаданные, такие как время создания и время изменения файла не сохраняются.
                    # Чтобы сохранить все метаданные файла из оригинала, используйте функцию shutil.copy2().

                    # LResult = shutil.copy (AFileNameSource, AFileNameDest) != ''

                    LResult = shutil.copy2 (AFileNameSource, AFileNameDest) != ''
                    # LResult = shutil.copy2 (AFileNameSource, LDestPath) != ''
                    # shutil.copystat (AFileNameSource, AFileNameDest)

                    LResult = True
                except:
                    s = f'ERROR: FileCopy ...'
                    LULog.LoggerTOOLS_AddLevel (logging.DEBUG, s)
                    LResult = False
                #endtry
            case 'Linux':
                # unix
                LFileNameSource_stat = os.stat (AFileNameSource)
                Lowner = LFileNameSource_stat [stat.ST_UID]
                Lgroup = LFileNameSource_stat [stat.ST_GID]
                # os.chown (AFileNameDest, Lowner, Lgroup)
                raise NotImplementedError('FileCopy Linux not implemented...')
            case _:
                s = f'Неизвестная система ...'
                LULog.LoggerTOOLS_AddLevel (logging.DEBUG, s)
        #endmatch
    #endif
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
        # LEncoding = LUStrDecode.cCP1251
        LEncoding = cDefaultEncoding
    #endif
    if len(AText) > 0:
        LHandle = open (AFileName, 'w', encoding = LEncoding)
        LHandle.write (AText + '\n')
        LHandle.flush ()
        LHandle.close ()
    else:
        FileDelete (AFileName)
        LHandle = open (AFileName, 'w', encoding = LEncoding)
        LHandle.flush ()
        LHandle.close ()
   #endif
#endfunction

#--------------------------------------------------------------------------------
# WriteStrToFile
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
        # LEncoding = LUStrDecode.cCP1251
        LEncoding = cDefaultEncoding
    #endif

    if len(AText) > 0:
        LHandle = open (AFileName, 'a+', encoding = LEncoding)
        LHandle.write (AStr + '\n')
        LHandle.flush ()
        LHandle.close ()
    #endif
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
        # LEncoding = LUStrDecode.cCP1251
        LEncoding = cDefaultEncoding
    #endif
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

#--------------------------------------------------------------------------------
# TestPathlib
#--------------------------------------------------------------------------------
def TestPathlib (APath: str) -> str:
    """TestPathlib"""
#beginfunction
    LResult = pathlib.WindowsPath (APath)
    return LResult
#endfunction

#-------------------------------------------------------------------------------
# FileSearch
#-------------------------------------------------------------------------------
def FileSearch (AFileName: str, APath: str) -> str:
    """FileSearch"""
#beginfunction
    try:
        # int = SearchPath(path, fileName , fileExt )
        #   The return value is a tuple of (string, int).
        #   string - представляет собой полный путь. int — смещение в строке базового имени файла.
        # L = win32api.SearchPath (APath, AFileName, None)
        print('L = win32api.SearchPath (APath, AFileName, None)')

        LResult = L [0]
    except:
        LResult = ''
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

        LResult = L[0]
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
# TEST_pathlib
#-------------------------------------------------------------------------------
def TEST_pathlib ():
    """TEST_pathlib"""
#beginfunction
    #Finding Files in the Current Directory
    # list_dirs.py
    here = pathlib.Path (".")
    files = here.glob ("*")
    for item in files:
        print (item)
    #endfor

    #Searching for Files Recursively in Python
    # list_dirs_recursive.py
    here = pathlib.Path (".")
    files = here.glob ("**/*")
    for item in files:
        print (item)
    #endfor

    #Finding a Single File Recursively
    # find_file.py
    here = pathlib.Path (".")
    files = here.glob ("**/something.txt")
    for item in files:
        print (item)

    #Finding an Absolute Path
    """Display some known relative and absolute paths"""
    here = pathlib.Path (".")
    file_path = Path ("my_subdirectory/something.txt")
    print (f"The absolute path to {here} is {here.resolve ()}")
    print (f"The absolute path to {file_path} is {file_path.resolve ()}")
    # Output:
    # The absolute path to . is /Users/johnlockwood/paths-demo
    # The absolute path to my_subdirectory/something.txt is /Users/johnlockwood/paths-demo/my_subdirectory/something.txt

    #Getting the Directory of the Currently Executing File
    # print_path.py
    print (__file__)
    # Output:
    # /Users/johnlockwood/paths-demo/print_path.py

    # print_directory.py
    file_path = pathlib.Path(__file__)
    print(f"The file {file_path.name} is located in directory {file_path.parent}.")
    # Output:
    # The file print_directory.py is located in directory /Users/johnlockwood/paths-demo.

    #Creating a File In the Same Directory As a Python File
    output_path = pathlib.Path (__file__).parent/"output.txt"

    #Working with Files and Directories
    """Display the current and parent directory"""
    here = pathlib.Path (".").resolve ()
    print (f"You are here: {here}, a sub-directory of {here.parent}.")
    # output:
    # You are here: /Users/johnlockwood/paths-demo, a sub - directory of/Users/ johnlockwood.

    #Recursively Listing Files and Directories in Python:
    """Recursively list files and directories"""
    here = pathlib.Path (".")
    for path in sorted (here.glob ("**/*")):
        path_type = "?"
        if path.is_file ():
            path_type = "F"
        elif path.is_dir ():
            path_type = "D"
        print (f"{path_type} {path}")

    #Finding Other Files and Directories

    #Get the User’s Home Directory in Python
    """Display the user's home directory"""
    print (pathlib.Path.home ())

    #Getting the Current Working Directory
    default = pathlibPath.home ()/".aws"
    print (default.exists ())

    #Creating a Directory in the User Home Directory in Python
    """Creates a .codesolid directory in the user's home directory"""
    DIRECTORY_NAME = ".codesolid"
    config_directory = pathlib.Path.home () / DIRECTORY_NAME
    if not config_directory.exists ():
        config_directory.mkdir ()
        print (f"Directory {config_directory} created.")
    else:
        print (f"Directory {config_directory} already exists, skipping.")

    #Finding Python Module Paths and Files

    #Exploring the PYTHONPATH and sys.path Variables
    # $ export PYTHONPATH=/Users/johnlockwood/source/CodeSolid
    # $ python
    # ...
    # >>> import os
    # >>> os.environ ["PYTHONPATH"]
    # '/Users/johnlockwood/source/CodeSolid'

    #>>> import sys
    # >>> sys.path
    # ['', '/Users/johnlockwood/source/CodeSolid', '/Users/johnlockwood/.pyenv/versions/3.11.0a6/lib/python311.zip', '/Users/johnlockwood/.pyenv/versions/3.11.0a6/lib/python3.11', '/Users/johnlockwood/.pyenv/versions/3.11.0a6/lib/python3.11/lib-dynload', '/Users/johnlockwood/.pyenv/versions/3.11.0a6/lib/python3.11/site-packages']

    #Finding the Filename from Which a Python Module Was Loaded
    # >>> import json
    # >>> json.__file__
    # '/Users/johnlockwood/.pyenv/versions/3.11.0a6/lib/python3.11/json/__init__.py'

    """Shows how find_spec can sometimes be used to get a file load location path"""
    from importlib.util import find_spec
    for module in ['os', 'json', 'module.file_in_module']:
        spec = find_spec (module)
        print (f"{module} origin: {spec.origin}")
    #Sample output:
    # os origin: frozen
    # json origin: /Users/johnlockwood/.pyenv/versions/3.11.0a6/lib/python3.11/json/__init__.py
    # module.file_in_module origin: /Users/johnlockwood/paths-demo/module/file_in_module.py

    #pathlib — Object-oriented filesystem paths

    #Basic use

    #Importing the main class:

    # >>>
    # from pathlib import Path
    # Listing subdirectories:
    #
    # >>>
    # p = Path('.')
    # [x for x in p.iterdir() if x.is_dir()]
    # [PosixPath('.hg'), PosixPath('docs'), PosixPath('dist'),
    #  PosixPath('__pycache__'), PosixPath('build')]
    # Listing Python source files in this directory tree:
    #
    # >>>
    # list(p.glob('**/*.py'))
    # [PosixPath('test_pathlib.py'), PosixPath('setup.py'),
    #  PosixPath('pathlib.py'), PosixPath('docs/conf.py'),
    #  PosixPath('build/lib/pathlib.py')]
    # Navigating inside a directory tree:
    #
    # >>>
    # p = Path('/etc')
    # q = p / 'init.d' / 'reboot'
    # q
    # PosixPath('/etc/init.d/reboot')
    # q.resolve()
    # PosixPath('/etc/rc.d/init.d/halt')
    # Querying path properties:
    #
    # >>>
    # q.exists()
    # True
    # q.is_dir()
    # False
    # Opening a file:
    #
    # >>>
    # with q.open() as f: f.readline()
    #
    # '#!/bin/bash\n'

    #Pure paths

    #---------------------------------------------------------------------------
    #class pathlib.PurePath(*pathsegments)
    #---------------------------------------------------------------------------
    # A generic class that represents the system’s path flavour (instantiating it creates either a PurePosixPath or a PureWindowsPath):
    #
    # >>>
    # PurePath('setup.py')      # Running on a Unix machine
    # PurePosixPath('setup.py')
    # Each element of pathsegments can be either a string representing a path segment, or an object implementing the os.PathLike interface where the __fspath__() method returns a string, such as another path object:
    #
    # >>>
    # PurePath('foo', 'some/path', 'bar')
    # PurePosixPath('foo/some/path/bar')
    # PurePath(Path('foo'), Path('bar'))
    # PurePosixPath('foo/bar')
    # When pathsegments is empty, the current directory is assumed:
    #
    # >>>
    # PurePath()
    # PurePosixPath('.')
    # If a segment is an absolute path, all previous segments are ignored (like os.path.join()):
    #
    # >>>
    # PurePath('/etc', '/usr', 'lib64')
    # PurePosixPath('/usr/lib64')
    # PureWindowsPath('c:/Windows', 'd:bar')
    # PureWindowsPath('d:bar')
    # On Windows, the drive is not reset when a rooted relative path segment (e.g., r'\foo') is encountered:
    #
    # >>>
    # PureWindowsPath('c:/Windows', '/Program Files')
    # PureWindowsPath('c:/Program Files')
    # Spurious slashes and single dots are collapsed, but double dots ('..') and leading double slashes ('//') are not, since this would change the meaning of a path for various reasons (e.g. symbolic links, UNC paths):
    #
    # >>>
    # PurePath('foo//bar')
    # PurePosixPath('foo/bar')
    # PurePath('//foo/bar')
    # PurePosixPath('//foo/bar')
    # PurePath('foo/./bar')
    # PurePosixPath('foo/bar')
    # PurePath('foo/../bar')
    # PurePosixPath('foo/../bar')
    # (a naïve approach would make PurePosixPath('foo/../bar') equivalent to PurePosixPath('bar'), which is wrong if foo is a symbolic link to another directory)
    #
    # Pure path objects implement the os.PathLike interface, allowing them to be used anywhere the interface is accepted.

    #---------------------------------------------------------------------------
    #class pathlib.PurePosixPath(*pathsegments)¶
    #---------------------------------------------------------------------------
    # A subclass of PurePath, this path flavour represents non-Windows filesystem paths:
    #
    # >>>
    # PurePosixPath('/etc')
    # PurePosixPath('/etc')

    #---------------------------------------------------------------------------
    #class pathlib.PureWindowsPath(*pathsegments)
    #---------------------------------------------------------------------------
    # A subclass of PurePath, this path flavour represents Windows filesystem paths, including UNC paths:
    #
    # >>>
    # PureWindowsPath('c:/Program Files/')
    # PureWindowsPath('c:/Program Files')
    # PureWindowsPath('//server/share/file')
    # PureWindowsPath('//server/share/file')

    #---------------------------------------------------------------------------
    #General properties
    #---------------------------------------------------------------------------
    #Paths are immutable and hashable. Paths of a same flavour are comparable and orderable. These properties respect the flavour’s case-folding semantics:
    # >>>
    # PurePosixPath('foo') == PurePosixPath('FOO')
    # False
    # PureWindowsPath('foo') == PureWindowsPath('FOO')
    # True
    # PureWindowsPath('FOO') in { PureWindowsPath('foo') }
    # True
    # PureWindowsPath('C:') < PureWindowsPath('d:')
    # True
    # Paths of a different flavour compare unequal and cannot be ordered:
    #
    # >>>
    # PureWindowsPath('foo') == PurePosixPath('foo')
    # False
    # PureWindowsPath('foo') < PurePosixPath('foo')
    # Traceback (most recent call last):
    #   File "<stdin>", line 1, in <module>
    # TypeError: '<' not supported between instances of 'PureWindowsPath' and 'PurePosixPat

    #Operators

    #The slash operator helps create child paths, like os.path.join(). If the argument is an absolute path, the previous path is ignored. On Windows, the drive is not reset when the argument is a rooted relative path (e.g., r'\foo'):
    # >>>
    # p = PurePath('/etc')
    # p
    # PurePosixPath('/etc')
    # p / 'init.d' / 'apache2'
    # PurePosixPath('/etc/init.d/apache2')
    # q = PurePath('bin')
    # '/usr' / q
    # PurePosixPath('/usr/bin')
    # p / '/an_absolute_path'
    # PurePosixPath('/an_absolute_path')
    # PureWindowsPath('c:/Windows', '/Program Files')
    # PureWindowsPath('c:/Program Files')
    # A path object can be used anywhere an object implementing os.PathLike is accepted:
    #
    # >>>
    # import os
    # p = PurePath('/etc')
    # os.fspath(p)
    # '/etc'
    # The string representation of a path is the raw filesystem path itself (in native form, e.g. with backslashes under Windows), which you can pass to any function taking a file path as a string:
    #
    # >>>
    # p = PurePath('/etc')
    # str(p)
    # '/etc'
    # p = PureWindowsPath('c:/Program Files')
    # str(p)
    # 'c:\\Program Files'
    # Similarly, calling bytes on a path gives the raw filesystem path as a bytes object, as encoded by os.fsencode():
    #
    # >>>
    # bytes(p)
    # b'/etc'
    # Note Calling bytes is only recommended under Unix. Under Windows, the unicode form is the canonical representation of filesystem paths.

    #Accessing individual parts

    #To access the individual “parts” (components) of a path, use the following property:

    # PurePath.parts
    # A tuple giving access to the path’s various components:
    #
    # >>>
    # p = PurePath('/usr/bin/python3')
    # p.parts
    # ('/', 'usr', 'bin', 'python3')
    #
    # p = PureWindowsPath('c:/Program Files/PSF')
    # p.parts
    # ('c:\\', 'Program Files', 'PSF')

    #Methods and properties

    #Pure paths provide the following methods and properties:

    # PurePath.drive
    # A string representing the drive letter or name, if any:
    #
    # >>>
    # PureWindowsPath('c:/Program Files/').drive
    # 'c:'
    # PureWindowsPath('/Program Files/').drive
    # ''
    # PurePosixPath('/etc').drive
    # ''
    # UNC shares are also considered drives:
    #
    # >>>
    # PureWindowsPath('//host/share/foo.txt').drive
    # '\\\\host\\share'
    # PurePath.root
    # A string representing the (local or global) root, if any:
    #
    # >>>
    # PureWindowsPath('c:/Program Files/').root
    # '\\'
    # PureWindowsPath('c:Program Files/').root
    # ''
    # PurePosixPath('/etc').root
    # '/'
    # UNC shares always have a root:
    #
    # >>>
    # PureWindowsPath('//host/share').root
    # '\\'
    # If the path starts with more than two successive slashes, PurePosixPath collapses them:
    #
    # >>>
    # PurePosixPath('//etc').root
    # '//'
    # PurePosixPath('///etc').root
    # '/'
    # PurePosixPath('////etc').root
    # '/'
    # Note This behavior conforms to The Open Group Base Specifications Issue 6, paragraph 4.11 Pathname Resolution:
    # “A pathname that begins with two successive slashes may be interpreted in an implementation-defined manner, although more than two leading slashes shall be treated as a single slash.”
    #
    # PurePath.anchor
    # The concatenation of the drive and root:
    #
    # >>>
    # PureWindowsPath('c:/Program Files/').anchor
    # 'c:\\'
    # PureWindowsPath('c:Program Files/').anchor
    # 'c:'
    # PurePosixPath('/etc').anchor
    # '/'
    # PureWindowsPath('//host/share').anchor
    # '\\\\host\\share\\'
    # PurePath.parents
    # An immutable sequence providing access to the logical ancestors of the path:
    #
    # >>>
    # p = PureWindowsPath('c:/foo/bar/setup.py')
    # p.parents[0]
    # PureWindowsPath('c:/foo/bar')
    # p.parents[1]
    # PureWindowsPath('c:/foo')
    # p.parents[2]
    # PureWindowsPath('c:/')
    # Changed in version 3.10: The parents sequence now supports slices and negative index values.
    #
    # PurePath.parent
    # The logical parent of the path:
    #
    # >>>
    # p = PurePosixPath('/a/b/c/d')
    # p.parent
    # PurePosixPath('/a/b/c')
    # You cannot go past an anchor, or empty path:
    #
    # >>>
    # p = PurePosixPath('/')
    # p.parent
    # PurePosixPath('/')
    # p = PurePosixPath('.')
    # p.parent
    # PurePosixPath('.')
    # Note This is a purely lexical operation, hence the following behaviour:
    # >>>
    # p = PurePosixPath('foo/..')
    # p.parent
    # PurePosixPath('foo')
    # If you want to walk an arbitrary filesystem path upwards, it is recommended to first call Path.resolve() so as to resolve symlinks and eliminate ".." components.
    #
    # PurePath.name
    # A string representing the final path component, excluding the drive and root, if any:
    #
    # >>>
    # PurePosixPath('my/library/setup.py').name
    # 'setup.py'
    # UNC drive names are not considered:
    #
    # >>>
    # PureWindowsPath('//some/share/setup.py').name
    # 'setup.py'
    # PureWindowsPath('//some/share').name
    # ''
    # PurePath.suffix
    # The file extension of the final component, if any:
    #
    # >>>
    # PurePosixPath('my/library/setup.py').suffix
    # '.py'
    # PurePosixPath('my/library.tar.gz').suffix
    # '.gz'
    # PurePosixPath('my/library').suffix
    # ''
    # PurePath.suffixes
    # A list of the path’s file extensions:
    #
    # >>>
    # PurePosixPath('my/library.tar.gar').suffixes
    # ['.tar', '.gar']
    # PurePosixPath('my/library.tar.gz').suffixes
    # ['.tar', '.gz']
    # PurePosixPath('my/library').suffixes
    # []
    # PurePath.stem
    # The final path component, without its suffix:
    #
    # >>>
    # PurePosixPath('my/library.tar.gz').stem
    # 'library.tar'
    # PurePosixPath('my/library.tar').stem
    # 'library'
    # PurePosixPath('my/library').stem
    # 'library'
    # PurePath.as_posix()
    # Return a string representation of the path with forward slashes (/):
    #
    # >>>
    # p = PureWindowsPath('c:\\windows')
    # str(p)
    # 'c:\\windows'
    # p.as_posix()
    # 'c:/windows'
    # PurePath.as_uri()
    # Represent the path as a file URI. ValueError is raised if the path isn’t absolute.
    #
    # >>>
    # p = PurePosixPath('/etc/passwd')
    # p.as_uri()
    # 'file:///etc/passwd'
    # p = PureWindowsPath('c:/Windows')
    # p.as_uri()
    # 'file:///c:/Windows'
    # PurePath.is_absolute()
    # Return whether the path is absolute or not. A path is considered absolute if it has both a root and (if the flavour allows) a drive:
    #
    # >>>
    # PurePosixPath('/a/b').is_absolute()
    # True
    # PurePosixPath('a/b').is_absolute()
    # False
    #
    # PureWindowsPath('c:/a/b').is_absolute()
    # True
    # PureWindowsPath('/a/b').is_absolute()
    # False
    # PureWindowsPath('c:').is_absolute()
    # False
    # PureWindowsPath('//some/share').is_absolute()
    # True
    # PurePath.is_relative_to(other)
    # Return whether or not this path is relative to the other path.
    #
    # >>>
    # p = PurePath('/etc/passwd')
    # p.is_relative_to('/etc')
    # True
    # p.is_relative_to('/usr')
    # False
    # This method is string-based; it neither accesses the filesystem nor treats “..” segments specially. The following code is equivalent:
    #
    # >>>
    # u = PurePath('/usr')
    # u == p or u in p.parents
    # False
    # New in version 3.9.
    #
    # Deprecated since version 3.12, will be removed in version 3.14: Passing additional arguments is deprecated; if supplied, they are joined with other.
    #
    # PurePath.is_reserved()
    # With PureWindowsPath, return True if the path is considered reserved under Windows, False otherwise. With PurePosixPath, False is always returned.
    #
    # >>>
    # PureWindowsPath('nul').is_reserved()
    # True
    # PurePosixPath('nul').is_reserved()
    # False
    # File system calls on reserved paths can fail mysteriously or have unintended effects.
    #
    # PurePath.joinpath(*pathsegments)
    # Calling this method is equivalent to combining the path with each of the given pathsegments in turn:
    #
    # >>>
    # PurePosixPath('/etc').joinpath('passwd')
    # PurePosixPath('/etc/passwd')
    # PurePosixPath('/etc').joinpath(PurePosixPath('passwd'))
    # PurePosixPath('/etc/passwd')
    # PurePosixPath('/etc').joinpath('init.d', 'apache2')
    # PurePosixPath('/etc/init.d/apache2')
    # PureWindowsPath('c:').joinpath('/Program Files')
    # PureWindowsPath('c:/Program Files')
    # PurePath.match(pattern, *, case_sensitive=None)
    # Match this path against the provided glob-style pattern. Return True if matching is successful, False otherwise.
    #
    # If pattern is relative, the path can be either relative or absolute, and matching is done from the right:
    #
    # >>>
    # PurePath('a/b.py').match('*.py')
    # True
    # PurePath('/a/b/c.py').match('b/*.py')
    # True
    # PurePath('/a/b/c.py').match('a/*.py')
    # False
    # If pattern is absolute, the path must be absolute, and the whole path must match:
    #
    # >>>
    # PurePath('/a.py').match('/*.py')
    # True
    # PurePath('a/b.py').match('/*.py')
    # False
    # The pattern may be another path object; this speeds up matching the same pattern against multiple files:
    #
    # >>>
    # pattern = PurePath('*.py')
    # PurePath('a/b.py').match(pattern)
    # True
    # Changed in version 3.12: Accepts an object implementing the os.PathLike interface.
    #
    # As with other methods, case-sensitivity follows platform defaults:
    #
    # >>>
    # PurePosixPath('b.py').match('*.PY')
    # False
    # PureWindowsPath('b.py').match('*.PY')
    # True
    # Set case_sensitive to True or False to override this behaviour.
    #
    # Changed in version 3.12: The case_sensitive parameter was added.
    #
    # PurePath.relative_to(other, walk_up=False)
    # Compute a version of this path relative to the path represented by other. If it’s impossible, ValueError is raised:
    #
    # >>>
    # p = PurePosixPath('/etc/passwd')
    # p.relative_to('/')
    # PurePosixPath('etc/passwd')
    # p.relative_to('/etc')
    # PurePosixPath('passwd')
    # p.relative_to('/usr')
    # Traceback (most recent call last):
    #   File "<stdin>", line 1, in <module>
    #   File "pathlib.py", line 941, in relative_to
    #     raise ValueError(error_message.format(str(self), str(formatted)))
    # ValueError: '/etc/passwd' is not in the subpath of '/usr' OR one path is relative and the other is absolute.
    # When walk_up is False (the default), the path must start with other. When the argument is True, .. entries may be added to form the relative path. In all other cases, such as the paths referencing different drives, ValueError is raised.:
    #
    # >>>
    # p.relative_to('/usr', walk_up=True)
    # PurePosixPath('../etc/passwd')
    # p.relative_to('foo', walk_up=True)
    # Traceback (most recent call last):
    #   File "<stdin>", line 1, in <module>
    #   File "pathlib.py", line 941, in relative_to
    #     raise ValueError(error_message.format(str(self), str(formatted)))
    # ValueError: '/etc/passwd' is not on the same drive as 'foo' OR one path is relative and the other is absolute.
    # Warning This function is part of PurePath and works with strings. It does not check or access the underlying file structure. This can impact the walk_up option as it assumes that no symlinks are present in the path; call resolve() first if necessary to resolve symlinks.
    # Changed in version 3.12: The walk_up parameter was added (old behavior is the same as walk_up=False).
    #
    # Deprecated since version 3.12, will be removed in version 3.14: Passing additional positional arguments is deprecated; if supplied, they are joined with other.
    #
    # PurePath.with_name(name)
    # Return a new path with the name changed. If the original path doesn’t have a name, ValueError is raised:
    #
    # >>>
    # p = PureWindowsPath('c:/Downloads/pathlib.tar.gz')
    # p.with_name('setup.py')
    # PureWindowsPath('c:/Downloads/setup.py')
    # p = PureWindowsPath('c:/')
    # p.with_name('setup.py')
    # Traceback (most recent call last):
    #   File "<stdin>", line 1, in <module>
    #   File "/home/antoine/cpython/default/Lib/pathlib.py", line 751, in with_name
    #     raise ValueError("%r has an empty name" % (self,))
    # ValueError: PureWindowsPath('c:/') has an empty name
    # PurePath.with_stem(stem)
    # Return a new path with the stem changed. If the original path doesn’t have a name, ValueError is raised:
    #
    # >>>
    # p = PureWindowsPath('c:/Downloads/draft.txt')
    # p.with_stem('final')
    # PureWindowsPath('c:/Downloads/final.txt')
    # p = PureWindowsPath('c:/Downloads/pathlib.tar.gz')
    # p.with_stem('lib')
    # PureWindowsPath('c:/Downloads/lib.gz')
    # p = PureWindowsPath('c:/')
    # p.with_stem('')
    # Traceback (most recent call last):
    #   File "<stdin>", line 1, in <module>
    #   File "/home/antoine/cpython/default/Lib/pathlib.py", line 861, in with_stem
    #     return self.with_name(stem + self.suffix)
    #   File "/home/antoine/cpython/default/Lib/pathlib.py", line 851, in with_name
    #     raise ValueError("%r has an empty name" % (self,))
    # ValueError: PureWindowsPath('c:/') has an empty name
    # New in version 3.9.
    #
    # PurePath.with_suffix(suffix)
    # Return a new path with the suffix changed. If the original path doesn’t have a suffix, the new suffix is appended instead. If the suffix is an empty string, the original suffix is removed:
    #
    # >>>
    # p = PureWindowsPath('c:/Downloads/pathlib.tar.gz')
    # p.with_suffix('.bz2')
    # PureWindowsPath('c:/Downloads/pathlib.tar.bz2')
    # p = PureWindowsPath('README')
    # p.with_suffix('.txt')
    # PureWindowsPath('README.txt')
    # p = PureWindowsPath('README.txt')
    # p.with_suffix('')
    # PureWindowsPath('README')
    # PurePath.with_segments(*pathsegments)
    # Create a new path object of the same type by combining the given pathsegments. This method is called whenever a derivative path is created, such as from parent and relative_to(). Subclasses may override this method to pass information to derivative paths, for example:
    #
    # from pathlib import PurePosixPath
    #
    # class MyPath(PurePosixPath):
    #     def __init__(self, *pathsegments, session_id):
    #         super().__init__(*pathsegments)
    #         self.session_id = session_id
    #
    #     def with_segments(self, *pathsegments):
    #         return type(self)(*pathsegments, session_id=self.session_id)
    #
    # etc = MyPath('/etc', session_id=42)
    # hosts = etc / 'hosts'
    # print(hosts.session_id)  # 42
    # New in version 3.12.
    #
    # Concrete paths
    # Concrete paths are subclasses of the pure path classes. In addition to operations provided by the latter, they also provide methods to do system calls on path objects. There are three ways to instantiate concrete paths:
    #
    # class pathlib.Path(*pathsegments)
    # A subclass of PurePath, this class represents concrete paths of the system’s path flavour (instantiating it creates either a PosixPath or a WindowsPath):
    #
    # >>>
    # Path('setup.py')
    # PosixPath('setup.py')
    # pathsegments is specified similarly to PurePath.
    #
    # class pathlib.PosixPath(*pathsegments)
    # A subclass of Path and PurePosixPath, this class represents concrete non-Windows filesystem paths:
    #
    # >>>
    # PosixPath('/etc')
    # PosixPath('/etc')
    # pathsegments is specified similarly to PurePath.
    #
    # class pathlib.WindowsPath(*pathsegments)
    # A subclass of Path and PureWindowsPath, this class represents concrete Windows filesystem paths:
    #
    # >>>
    # WindowsPath('c:/Program Files/')
    # WindowsPath('c:/Program Files')
    # pathsegments is specified similarly to PurePath.
    #
    # You can only instantiate the class flavour that corresponds to your system (allowing system calls on non-compatible path flavours could lead to bugs or failures in your application):
    #
    # >>>
    # import os
    # os.name
    # 'posix'
    # Path('setup.py')
    # PosixPath('setup.py')
    # PosixPath('setup.py')
    # PosixPath('setup.py')
    # WindowsPath('setup.py')
    # Traceback (most recent call last):
    #   File "<stdin>", line 1, in <module>
    #   File "pathlib.py", line 798, in __new__
    #     % (cls.__name__,))
    # NotImplementedError: cannot instantiate 'WindowsPath' on your system
    # Methods
    # Concrete paths provide the following methods in addition to pure paths methods. Many of these methods can raise an OSError if a system call fails (for example because the path doesn’t exist).
    #
    # Changed in version 3.8: exists(), is_dir(), is_file(), is_mount(), is_symlink(), is_block_device(), is_char_device(), is_fifo(), is_socket() now return False instead of raising an exception for paths that contain characters unrepresentable at the OS level.
    #
    # classmethod Path.cwd()
    # Return a new path object representing the current directory (as returned by os.getcwd()):
    #
    # >>>
    # Path.cwd()
    # PosixPath('/home/antoine/pathlib')
    # classmethod Path.home()
    # Return a new path object representing the user’s home directory (as returned by os.path.expanduser() with ~ construct). If the home directory can’t be resolved, RuntimeError is raised.
    #
    # >>>
    # Path.home()
    # PosixPath('/home/antoine')
    # New in version 3.5.
    #
    # Path.stat(*, follow_symlinks=True)
    # Return a os.stat_result object containing information about this path, like os.stat(). The result is looked up at each call to this method.
    #
    # This method normally follows symlinks; to stat a symlink add the argument follow_symlinks=False, or use lstat().
    #
    # >>>
    # p = Path('setup.py')
    # p.stat().st_size
    # 956
    # p.stat().st_mtime
    # 1327883547.852554
    # Changed in version 3.10: The follow_symlinks parameter was added.
    #
    # Path.chmod(mode, *, follow_symlinks=True)
    # Change the file mode and permissions, like os.chmod().
    #
    # This method normally follows symlinks. Some Unix flavours support changing permissions on the symlink itself; on these platforms you may add the argument follow_symlinks=False, or use lchmod().
    #
    # >>>
    # p = Path('setup.py')
    # p.stat().st_mode
    # 33277
    # p.chmod(0o444)
    # p.stat().st_mode
    # 33060
    # Changed in version 3.10: The follow_symlinks parameter was added.
    #
    # Path.exists(*, follow_symlinks=True)
    # Return True if the path points to an existing file or directory.
    #
    # This method normally follows symlinks; to check if a symlink exists, add the argument follow_symlinks=False.
    #
    # >>>
    # Path('.').exists()
    # True
    # Path('setup.py').exists()
    # True
    # Path('/etc').exists()
    # True
    # Path('nonexistentfile').exists()
    # False
    # Changed in version 3.12: The follow_symlinks parameter was added.
    #
    # Path.expanduser()
    # Return a new path with expanded ~ and ~user constructs, as returned by os.path.expanduser(). If a home directory can’t be resolved, RuntimeError is raised.
    #
    # >>>
    # p = PosixPath('~/films/Monty Python')
    # p.expanduser()
    # PosixPath('/home/eric/films/Monty Python')
    # New in version 3.5.
    #
    # Path.glob(pattern, *, case_sensitive=None)
    # Glob the given relative pattern in the directory represented by this path, yielding all matching files (of any kind):
    #
    # >>>
    # sorted(Path('.').glob('*.py'))
    # [PosixPath('pathlib.py'), PosixPath('setup.py'), PosixPath('test_pathlib.py')]
    # sorted(Path('.').glob('*/*.py'))
    # [PosixPath('docs/conf.py')]
    # Patterns are the same as for fnmatch, with the addition of “**” which means “this directory and all subdirectories, recursively”. In other words, it enables recursive globbing:
    #
    # >>>
    # sorted(Path('.').glob('**/*.py'))
    # [PosixPath('build/lib/pathlib.py'),
    #  PosixPath('docs/conf.py'),
    #  PosixPath('pathlib.py'),
    #  PosixPath('setup.py'),
    #  PosixPath('test_pathlib.py')]
    # This method calls Path.is_dir() on the top-level directory and propagates any OSError exception that is raised. Subsequent OSError exceptions from scanning directories are suppressed.
    #
    # By default, or when the case_sensitive keyword-only argument is set to None, this method matches paths using platform-specific casing rules: typically, case-sensitive on POSIX, and case-insensitive on Windows. Set case_sensitive to True or False to override this behaviour.
    #
    # Note Using the “**” pattern in large directory trees may consume an inordinate amount of time.
    # Raises an auditing event pathlib.Path.glob with arguments self, pattern.
    #
    # Changed in version 3.11: Return only directories if pattern ends with a pathname components separator (sep or altsep).
    #
    # Changed in version 3.12: The case_sensitive parameter was added.
    #
    # Path.group()
    # Return the name of the group owning the file. KeyError is raised if the file’s gid isn’t found in the system database.
    #
    # Path.is_dir()
    # Return True if the path points to a directory (or a symbolic link pointing to a directory), False if it points to another kind of file.
    #
    # False is also returned if the path doesn’t exist or is a broken symlink; other errors (such as permission errors) are propagated.
    #
    # Path.is_file()
    # Return True if the path points to a regular file (or a symbolic link pointing to a regular file), False if it points to another kind of file.
    #
    # False is also returned if the path doesn’t exist or is a broken symlink; other errors (such as permission errors) are propagated.
    #
    # Path.is_junction()
    # Return True if the path points to a junction, and False for any other type of file. Currently only Windows supports junctions.
    #
    # New in version 3.12.
    #
    # Path.is_mount()
    # Return True if the path is a mount point: a point in a file system where a different file system has been mounted. On POSIX, the function checks whether path’s parent, path/.., is on a different device than path, or whether path/.. and path point to the same i-node on the same device — this should detect mount points for all Unix and POSIX variants. On Windows, a mount point is considered to be a drive letter root (e.g. c:\), a UNC share (e.g. \\server\share), or a mounted filesystem directory.
    #
    # New in version 3.7.
    #
    # Changed in version 3.12: Windows support was added.
    #
    # Path.is_symlink()
    # Return True if the path points to a symbolic link, False otherwise.
    #
    # False is also returned if the path doesn’t exist; other errors (such as permission errors) are propagated.
    #
    # Path.is_socket()
    # Return True if the path points to a Unix socket (or a symbolic link pointing to a Unix socket), False if it points to another kind of file.
    #
    # False is also returned if the path doesn’t exist or is a broken symlink; other errors (such as permission errors) are propagated.
    #
    # Path.is_fifo()
    # Return True if the path points to a FIFO (or a symbolic link pointing to a FIFO), False if it points to another kind of file.
    #
    # False is also returned if the path doesn’t exist or is a broken symlink; other errors (such as permission errors) are propagated.
    #
    # Path.is_block_device()
    # Return True if the path points to a block device (or a symbolic link pointing to a block device), False if it points to another kind of file.
    #
    # False is also returned if the path doesn’t exist or is a broken symlink; other errors (such as permission errors) are propagated.
    #
    # Path.is_char_device()
    # Return True if the path points to a character device (or a symbolic link pointing to a character device), False if it points to another kind of file.
    #
    # False is also returned if the path doesn’t exist or is a broken symlink; other errors (such as permission errors) are propagated.
    #
    # Path.iterdir()
    # When the path points to a directory, yield path objects of the directory contents:
    #
    # >>>
    # p = Path('docs')
    # for child in p.iterdir(): child
    #
    # PosixPath('docs/conf.py')
    # PosixPath('docs/_templates')
    # PosixPath('docs/make.bat')
    # PosixPath('docs/index.rst')
    # PosixPath('docs/_build')
    # PosixPath('docs/_static')
    # PosixPath('docs/Makefile')
    # The children are yielded in arbitrary order, and the special entries '.' and '..' are not included. If a file is removed from or added to the directory after creating the iterator, whether a path object for that file be included is unspecified.
    #
    # Path.walk(top_down=True, on_error=None, follow_symlinks=False)
    # Generate the file names in a directory tree by walking the tree either top-down or bottom-up.
    #
    # For each directory in the directory tree rooted at self (including self but excluding ‘.’ and ‘..’), the method yields a 3-tuple of (dirpath, dirnames, filenames).
    #
    # dirpath is a Path to the directory currently being walked, dirnames is a list of strings for the names of subdirectories in dirpath (excluding '.' and '..'), and filenames is a list of strings for the names of the non-directory files in dirpath. To get a full path (which begins with self) to a file or directory in dirpath, do dirpath / name. Whether or not the lists are sorted is file system-dependent.
    #
    # If the optional argument top_down is true (which is the default), the triple for a directory is generated before the triples for any of its subdirectories (directories are walked top-down). If top_down is false, the triple for a directory is generated after the triples for all of its subdirectories (directories are walked bottom-up). No matter the value of top_down, the list of subdirectories is retrieved before the triples for the directory and its subdirectories are walked.
    #
    # When top_down is true, the caller can modify the dirnames list in-place (for example, using del or slice assignment), and Path.walk() will only recurse into the subdirectories whose names remain in dirnames. This can be used to prune the search, or to impose a specific order of visiting, or even to inform Path.walk() about directories the caller creates or renames before it resumes Path.walk() again. Modifying dirnames when top_down is false has no effect on the behavior of Path.walk() since the directories in dirnames have already been generated by the time dirnames is yielded to the caller.
    #
    # By default, errors from os.scandir() are ignored. If the optional argument on_error is specified, it should be a callable; it will be called with one argument, an OSError instance. The callable can handle the error to continue the walk or re-raise it to stop the walk. Note that the filename is available as the filename attribute of the exception object.
    #
    # By default, Path.walk() does not follow symbolic links, and instead adds them to the filenames list. Set follow_symlinks to true to resolve symlinks and place them in dirnames and filenames as appropriate for their targets, and consequently visit directories pointed to by symlinks (where supported).
    #
    # Note Be aware that setting follow_symlinks to true can lead to infinite recursion if a link points to a parent directory of itself. Path.walk() does not keep track of the directories it has already visited.
    # Note Path.walk() assumes the directories it walks are not modified during execution. For example, if a directory from dirnames has been replaced with a symlink and follow_symlinks is false, Path.walk() will still try to descend into it. To prevent such behavior, remove directories from dirnames as appropriate.
    # Note Unlike os.walk(), Path.walk() lists symlinks to directories in filenames if follow_symlinks is false.
    # This example displays the number of bytes used by all files in each directory, while ignoring __pycache__ directories:
    #
    # from pathlib import Path
    # for root, dirs, files in Path("cpython/Lib/concurrent").walk(on_error=print):
    #   print(
    #       root,
    #       "consumes",
    #       sum((root / file).stat().st_size for file in files),
    #       "bytes in",
    #       len(files),
    #       "non-directory files"
    #   )
    #   if '__pycache__' in dirs:
    #         dirs.remove('__pycache__')
    # This next example is a simple implementation of shutil.rmtree(). Walking the tree bottom-up is essential as rmdir() doesn’t allow deleting a directory before it is empty:
    #
    # # Delete everything reachable from the directory "top".
    # # CAUTION:  This is dangerous! For example, if top == Path('/'),
    # # it could delete all of your files.
    # for root, dirs, files in top.walk(top_down=False):
    #     for name in files:
    #         (root / name).unlink()
    #     for name in dirs:
    #         (root / name).rmdir()
    # New in version 3.12.
    #
    # Path.lchmod(mode)
    # Like Path.chmod() but, if the path points to a symbolic link, the symbolic link’s mode is changed rather than its target’s.
    #
    # Path.lstat()
    # Like Path.stat() but, if the path points to a symbolic link, return the symbolic link’s information rather than its target’s.
    #
    # Path.mkdir(mode=0o777, parents=False, exist_ok=False)
    # Create a new directory at this given path. If mode is given, it is combined with the process’ umask value to determine the file mode and access flags. If the path already exists, FileExistsError is raised.
    #
    # If parents is true, any missing parents of this path are created as needed; they are created with the default permissions without taking mode into account (mimicking the POSIX mkdir -p command).
    #
    # If parents is false (the default), a missing parent raises FileNotFoundError.
    #
    # If exist_ok is false (the default), FileExistsError is raised if the target directory already exists.
    #
    # If exist_ok is true, FileExistsError will not be raised unless the given path already exists in the file system and is not a directory (same behavior as the POSIX mkdir -p command).
    #
    # Changed in version 3.5: The exist_ok parameter was added.
    #
    # Path.open(mode='r', buffering=-1, encoding=None, errors=None, newline=None)
    # Open the file pointed to by the path, like the built-in open() function does:
    #
    # >>>
    # p = Path('setup.py')
    # with p.open() as f:
    #     f.readline()
    #
    # '#!/usr/bin/env python3\n'
    # Path.owner()
    # Return the name of the user owning the file. KeyError is raised if the file’s uid isn’t found in the system database.
    #
    # Path.read_bytes()
    # Return the binary contents of the pointed-to file as a bytes object:
    #
    # >>>
    # p = Path('my_binary_file')
    # p.write_bytes(b'Binary file contents')
    # 20
    # p.read_bytes()
    # b'Binary file contents'
    # New in version 3.5.
    #
    # Path.read_text(encoding=None, errors=None)
    # Return the decoded contents of the pointed-to file as a string:
    #
    # >>>
    # p = Path('my_text_file')
    # p.write_text('Text file contents')
    # 18
    # p.read_text()
    # 'Text file contents'
    # The file is opened and then closed. The optional parameters have the same meaning as in open().
    #
    # New in version 3.5.
    #
    # Path.readlink()
    # Return the path to which the symbolic link points (as returned by os.readlink()):
    #
    # >>>
    # p = Path('mylink')
    # p.symlink_to('setup.py')
    # p.readlink()
    # PosixPath('setup.py')
    # New in version 3.9.
    #
    # Path.rename(target)
    # Rename this file or directory to the given target, and return a new Path instance pointing to target. On Unix, if target exists and is a file, it will be replaced silently if the user has permission. On Windows, if target exists, FileExistsError will be raised. target can be either a string or another path object:
    #
    # >>>
    # p = Path('foo')
    # p.open('w').write('some text')
    # 9
    # target = Path('bar')
    # p.rename(target)
    # PosixPath('bar')
    # target.open().read()
    # 'some text'
    # The target path may be absolute or relative. Relative paths are interpreted relative to the current working directory, not the directory of the Path object.
    #
    # It is implemented in terms of os.rename() and gives the same guarantees.
    #
    # Changed in version 3.8: Added return value, return the new Path instance.
    #
    # Path.replace(target)
    # Rename this file or directory to the given target, and return a new Path instance pointing to target. If target points to an existing file or empty directory, it will be unconditionally replaced.
    #
    # The target path may be absolute or relative. Relative paths are interpreted relative to the current working directory, not the directory of the Path object.
    #
    # Changed in version 3.8: Added return value, return the new Path instance.
    #
    # Path.absolute()
    # Make the path absolute, without normalization or resolving symlinks. Returns a new path object:
    #
    # >>>
    # p = Path('tests')
    # p
    # PosixPath('tests')
    # p.absolute()
    # PosixPath('/home/antoine/pathlib/tests')
    # Path.resolve(strict=False)
    # Make the path absolute, resolving any symlinks. A new path object is returned:
    #
    # >>>
    # p = Path()
    # p
    # PosixPath('.')
    # p.resolve()
    # PosixPath('/home/antoine/pathlib')
    # “..” components are also eliminated (this is the only method to do so):
    #
    # >>>
    # p = Path('docs/../setup.py')
    # p.resolve()
    # PosixPath('/home/antoine/pathlib/setup.py')
    # If the path doesn’t exist and strict is True, FileNotFoundError is raised. If strict is False, the path is resolved as far as possible and any remainder is appended without checking whether it exists. If an infinite loop is encountered along the resolution path, RuntimeError is raised.
    #
    # Changed in version 3.6: The strict parameter was added (pre-3.6 behavior is strict).
    #
    # Path.rglob(pattern, *, case_sensitive=None)
    # Glob the given relative pattern recursively. This is like calling Path.glob() with “**/” added in front of the pattern, where patterns are the same as for fnmatch:
    #
    # >>>
    # sorted(Path().rglob("*.py"))
    # [PosixPath('build/lib/pathlib.py'),
    #  PosixPath('docs/conf.py'),
    #  PosixPath('pathlib.py'),
    #  PosixPath('setup.py'),
    #  PosixPath('test_pathlib.py')]
    # By default, or when the case_sensitive keyword-only argument is set to None, this method matches paths using platform-specific casing rules: typically, case-sensitive on POSIX, and case-insensitive on Windows. Set case_sensitive to True or False to override this behaviour.
    #
    # Raises an auditing event pathlib.Path.rglob with arguments self, pattern.
    #
    # Changed in version 3.11: Return only directories if pattern ends with a pathname components separator (sep or altsep).
    #
    # Changed in version 3.12: The case_sensitive parameter was added.
    #
    # Path.rmdir()
    # Remove this directory. The directory must be empty.
    #
    # Path.samefile(other_path)
    # Return whether this path points to the same file as other_path, which can be either a Path object, or a string. The semantics are similar to os.path.samefile() and os.path.samestat().
    #
    # An OSError can be raised if either file cannot be accessed for some reason.
    #
    # >>>
    # p = Path('spam')
    # q = Path('eggs')
    # p.samefile(q)
    # False
    # p.samefile('spam')
    # True
    # New in version 3.5.
    #
    # Path.symlink_to(target, target_is_directory=False)
    # Make this path a symbolic link pointing to target.
    #
    # On Windows, a symlink represents either a file or a directory, and does not morph to the target dynamically. If the target is present, the type of the symlink will be created to match. Otherwise, the symlink will be created as a directory if target_is_directory is True or a file symlink (the default) otherwise. On non-Windows platforms, target_is_directory is ignored.
    #
    # >>>
    # p = Path('mylink')
    # p.symlink_to('setup.py')
    # p.resolve()
    # PosixPath('/home/antoine/pathlib/setup.py')
    # p.stat().st_size
    # 956
    # p.lstat().st_size
    # 8
    # Note The order of arguments (link, target) is the reverse of os.symlink()’s.
    # Path.hardlink_to(target)
    # Make this path a hard link to the same file as target.
    #
    # Note The order of arguments (link, target) is the reverse of os.link()’s.
    # New in version 3.10.
    #
    # Path.touch(mode=0o666, exist_ok=True)
    # Create a file at this given path. If mode is given, it is combined with the process’ umask value to determine the file mode and access flags. If the file already exists, the function succeeds if exist_ok is true (and its modification time is updated to the current time), otherwise FileExistsError is raised.
    #
    # Path.unlink(missing_ok=False)
    # Remove this file or symbolic link. If the path points to a directory, use Path.rmdir() instead.
    #
    # If missing_ok is false (the default), FileNotFoundError is raised if the path does not exist.
    #
    # If missing_ok is true, FileNotFoundError exceptions will be ignored (same behavior as the POSIX rm -f command).
    #
    # Changed in version 3.8: The missing_ok parameter was added.
    #
    # Path.write_bytes(data)
    # Open the file pointed to in bytes mode, write data to it, and close the file:
    #
    # >>>
    # p = Path('my_binary_file')
    # p.write_bytes(b'Binary file contents')
    # 20
    # p.read_bytes()
    # b'Binary file contents'
    # An existing file of the same name is overwritten.
    #
    # New in version 3.5.
    #
    # Path.write_text(data, encoding=None, errors=None, newline=None)
    # Open the file pointed to in text mode, write data to it, and close the file:
    #
    # >>>
    # p = Path('my_text_file')
    # p.write_text('Text file contents')
    # 18
    # p.read_text()
    # 'Text file contents'
    # An existing file of the same name is overwritten. The optional parameters have the same meaning as in open().

    #Correspondence to tools in the os module
    #-----------------------------------------------------------------------------
    # os and os.path                      pathlib
    # -----------------------------------------------------------------------------
    # os.path.abspath()                   Path.absolute() [1]
    # os.path.realpath()                  Path.resolve()
    # os.chmod()                          Path.chmod()
    # os.mkdir()                          Path.mkdir()
    # os.makedirs()                       Path.mkdir()
    # os.rename()                         Path.rename()
    # os.replace()                        Path.replace()
    # os.rmdir()                          Path.rmdir()
    # os.remove(), os.unlink()            Path.unlink()
    # os.getcwd()                         Path.cwd()
    # os.path.exists()                    Path.exists()
    # os.path.expanduser()                Path.expanduser() and Path.home()
    # os.listdir()                        Path.iterdir()
    # os.walk()                           Path.walk()
    # os.path.isdir()                     Path.is_dir()
    # os.path.isfile()                    Path.is_file()
    # os.path.islink()                    Path.is_symlink()
    # os.link()                           Path.hardlink_to()
    # os.symlink()                        Path.symlink_to()
    # os.readlink()                       Path.readlink()
    # os.path.relpath()                   PurePath.relative_to() [2]
    # os.stat()                           Path.stat(), Path.owner(), Path.group()
    # os.path.isabs()                     PurePath.is_absolute()
    # os.path.join()                      PurePath.joinpath()
    # os.path.basename()                  PurePath.name
    # os.path.dirname()                   PurePath.parent
    # os.path.samefile()                  Path.samefile()
    # os.path.splitext()                  PurePath.stem and PurePath.suffix










#endfunction

#-------------------------------------------------------------------------------
# main
#-------------------------------------------------------------------------------
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
