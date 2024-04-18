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
import logging
import os
import stat
import tempfile
import platform
import re
import ctypes
import pathlib
if platform.system() == 'Windows':
    import win32api
    import win32con
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
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# if not file.endswith(ext):
#     contains_other_ext=True
#--------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
# get_tree_size
#--------------------------------------------------------------------------------
def get_tree_size(path):
    """get_tree_size"""
#beginfunction
    """Return total size of files in given path and subdirs."""
    total = 0
    for entry in os.scandir(path):
        if entry.is_dir(follow_symlinks=False):
            total += get_tree_size(entry.path)
        else:
            total += entry.stat(follow_symlinks=False).st_size
    return total
#endfunction

#--------------------------------------------------------------------------------
# DirectoryDelete
#--------------------------------------------------------------------------------
def DirectoryDelete (ADirectoryName: str) -> bool:
    """DirectoryDelete"""

    # В этом примере показано, как удалить дерево каталогов в Windows,
    # где для некоторых файлов установлен бит только для чтения.
    # Он использует обратный вызов onerror, чтобы очистить бит readonly и повторить попытку удаления.
    def remove_readonly (func, path, _):
        """remove_readonly"""
    #beginfunction
        "Clear the readonly bit and reattempt the removal"
        LULog.LoggerTOOLS_AddLevel(logging.DEBUG, path)
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
    LResult = False
    if DirectoryExists (ADirectoryName):
        LULog.LoggerTOOLS_AddLevel(logging.DEBUG, ADirectoryName)

        # shutil.rmtree (ADirectoryName, ignore_errors = True, onexc = None)
        shutil.rmtree (ADirectoryName, ignore_errors = False, onerror = remove_readonly)

        LResult = True
    #endif
    return LResult
#endfunction

#--------------------------------------------------------------------------------
# DirectoryDelete_walk
#--------------------------------------------------------------------------------
# Delete everything reachable from the directory named in 'top',
# assuming there are no symbolic links.
# CAUTION:  This is dangerous!  For example, if top == '/', it
# could delete all your disk files.
#--------------------------------------------------------------------------------
def DirectoryDelete_walk (ADirectoryName: str) -> bool:
    """DirectoryDelete_walk"""
#beginfunction
    LResult = False
    if DirectoryExists (ADirectoryName):
        for root, dirs, files in os.walk (ADirectoryName, topdown = False):
            for name in files:
                os.remove (os.path.join (root, name))
            #endfor
            for name in dirs:
                os.rmdir (os.path.join (root, name))
            #endfor
        #endfor
        LResult = True
    #endif
    return LResult
#endfunction

#--------------------------------------------------------------------------------
# DirectoryDelete_walk_2
#--------------------------------------------------------------------------------
# Replace with the path to the directory you want to remove
# directory = '/path/to/directory'
def DirectoryDelete_walk_2 (ADirectoryName: str) -> bool:
    """DirectoryDelete_walk_2"""
#beginfunction
    LResult = False
    if DirectoryExists (ADirectoryName):
        # Use os.walk to traverse the directory tree
        for root, dirs, files in os.walk(directory):
            # For each file in the directory
            for file in files:
                # Construct the full path to the file
                file_path = os.path.join(root, file)
                # Delete the file
                os.remove(file_path)
            #endfor
            # For each subdirectory in the directory
            for dir in dirs:
                # Construct the full path to the subdirectory
                dir_path = os.path.join(root, dir)
                # Delete the subdirectory
                os.rmdir(dir_path)
            #endfor
        #endfor
        LResult = True
    #endif
    return LResult
#endfunction
# Delete the top-level directory
# os.rmdir(directory)

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
    if FileExists (AFileName):
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
    if DirectoryExists (AFileName):
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
#
#--------------------------------------------------------------------------------
def GetFileSize (AFileName: str) -> int:
    """GetFileSize"""
#beginfunction
    if FileExists (AFileName):
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
# GetFileAttr
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
        LULog.LoggerTOOLS_AddLevel(logging.DEBUG, s)

        if platform.system() == 'Windows':
            Lattr = LStat.st_file_attributes
            # Lattr = win32api.GetFileAttributes (AFileName)
        else:
            Lattr = 0
        #endif
        s = f'Lattr:{Lattr:d} {hex(Lattr):s} {bin(Lattr):s} {FileAttrStr(Lattr):s}'
        LULog.LoggerTOOLS_AddLevel(logging.DEBUG, s)

        LResult = Lattr
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
    s = f'OpenTextFile: {AFileName:s} ...'
    LULog.LoggerTOOLS_AddLevel (logging.DEBUG, s)

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
    s = f'CloseTextFile: {AFileName:s} ...'
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
