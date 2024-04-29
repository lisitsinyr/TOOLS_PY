"""LUFileUtils.py"""
# -*- coding: UTF-8 -*-
__annotations__ = """
 =======================================================
 Copyright (c) 2023-2024
 Author:
     Lisitsin Y.R.
 Project:
     LU_PY
     Python (LU)
 Module:
     LUFileUtils.py

 =======================================================
"""

#------------------------------------------
# БИБЛИОТЕКИ python
#------------------------------------------
import os
import stat
import sys
import time
import chardet
import logging

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------
import datetime
import shutil
import platform
# if platform.system() == 'Windows':
#     import win32api
#     import win32con
# #endif

#------------------------------------------
# БИБЛИОТЕКА LU
#------------------------------------------
import lyr.LUErrors as LUErrors
import lyr.LUFile as LUFile
import lyr.LUStrDecode as LUStrDecode
import lyr.LULog as LULog
import lyr.LUDateTime as LUDateTime

#------------------------------------------
#CONST
#------------------------------------------
GLevel = 0
GFileCount = 0
GFileSize = 0
GDir = ''
GMask = '.*'
GDirCount = 0
GLevelMAX = sys.maxsize

#-------------------------------------------------------------------------------
# __OUTFILE
#-------------------------------------------------------------------------------
def __OUTFILE (s: str, _OutFile: str):
#beginfunction
    if (_OutFile) and (s != ''):
        if (_OutFile.upper () == 'CONSOLE'):
            print (s)
        else:
            LUFile.WriteStrToFile (_OutFile, s + '\n')
        #endif
    #endif
#endfunction

#-------------------------------------------------------------------------------
# __ListFile
#-------------------------------------------------------------------------------
def __ListFile (APathSource, AMask, APathDest,
                _OutFile, _Option, _FuncDir, _FuncFile) -> int:
    global GFileCount
    global GFileSize
#beginfunction
    LFileCount = 0
    with os.scandir(APathSource) as LFiles:
        for LFile in LFiles:
            if (not LFile.is_symlink ()):
                if LFile.is_file() and LUFile.CheckFileNameMask (LFile.name, AMask):
                    #------------------------------------------------------------
                    # class os.DirEntry - Это файл
                    #------------------------------------------------------------
                    LBaseName = os.path.basename (LFile.path)
                    LFileTimeSource = LUFile.GetFileDateTime (LFile.path)[2]
                    LFileSizeSource = LUFile.GetFileSize (LFile.path)

                    GFileCount = GFileCount + 1
                    LFileCount = LFileCount + 1
                    GFileSize = GFileSize + LFileSizeSource

                    match _Option:
                        case 1 | 11:
                            s = f'{LFileTimeSource:%d.%m.%Y  %H:%M} {LFileSizeSource:-17,d} {LBaseName:s}'
                        case 2 | 12:
                            s = f'{LFileTimeSource:%d.%m.%Y  %H:%M} {LFileSizeSource:-17,d} {LBaseName:s}'
                        case _:
                            s = ''
                    #endmatch
                    __OUTFILE (s, _OutFile)

                    if _FuncFile:
                        s = f'_FuncFile: {_FuncFile.__name__:s}'
                        # LULog.LoggerTOOLS_AddLevel (logging.DEBUG, s)
                        _FuncFile (LUFile.ExpandFileName (LFile.path), APathDest)
                    #endif
                #endif
            #endif
            if LFile.is_dir ():  # and (not LFile.name.startswith('.')):
                #------------------------------------------------------------
                # class os.DirEntry - Это каталог
                #------------------------------------------------------------
                LBaseName = os.path.basename (LFile.path)
                LPathTimeSource = LUFile.GetDirDateTime (LFile.path) [2]

                match _Option:
                    case 1 | 11:
                        s = f'{LPathTimeSource:%d.%m.%Y  %H:%M} {'   <DIR>':17s} {LBaseName:s}'
                    case 2 | 12:
                        s = f'{LPathTimeSource:%d.%m.%Y  %H:%M} {'   <DIR>':17s} {LBaseName:s}'
                    case _:
                        s = ''
                #endmatch
                __OUTFILE (s, _OutFile)

                #------------------------------------------------------------
                #
                #------------------------------------------------------------
                if _FuncDir:
                    s = f'_FuncDir: {_FuncDir.__name__:s}'
                    # LULog.LoggerTOOLS_AddLevel (logging.DEBUG, s)
                    _FuncDir (LUFile.ExpandFileName (LFile.path), APathDest)
                #endif
            #endif
        #endfor
    #endwith
    return LFileCount
#endfunction

#-------------------------------------------------------------------------------
# __ListDir
#-------------------------------------------------------------------------------
def __ListDir (APathSource, AMask, ASubdir, APathDest,
               _OutFile, _Option, _FuncDir, _FuncFile):
#beginfunction
    global GLevel
    global GFileCount
    global GFileSize

    #------------------------------------------------------------
    # Dir
    #------------------------------------------------------------
    LBaseName = os.path.basename (APathSource)
    LPathTimeSource = LUFile.GetDirDateTime (APathSource)[2]

    GFileCount = 0
    GFileSize = 0

    #------------------------------------------------------------
    # список файлов в каталоге
    #------------------------------------------------------------
    if _Option != 0:
        s = f"\nСодержимое папки {APathSource:s}\n"
        __OUTFILE (s, _OutFile)
    #endif
    match _Option:
        case 1 | 11:
            s = f'{LPathTimeSource:%d.%m.%Y  %H:%M} {'   <DIR>':17s} {LBaseName:s}'
        case 2 | 12:
            s = f'{LPathTimeSource:%d.%m.%Y  %H:%M} {'   <DIR>':17s} {LBaseName:s}'
        case _:
            s = ''
    #endmatch
    __OUTFILE (s, _OutFile)

    LFileCount = __ListFile (APathSource, AMask, APathDest, _OutFile, _Option, _FuncDir, _FuncFile)

    match _Option:
        case 1 | 11:
            s = f'{GFileCount:16d} файлов {GFileSize:16,d} байт'
        case 2 | 12:
            s = f'{GFileCount:16d} файлов {GFileSize:16,d} байт'
        case _:
            s = ''
    #endmatch
    __OUTFILE (s, _OutFile)
    #------------------------------------------------------------

    with os.scandir(APathSource) as LFiles:
        for LFile in LFiles:
            if (not LFile.is_symlink()):
                if LFile.is_dir (): # and (not LFile.name.startswith('.')):
                    #------------------------------------------------------------
                    # class os.DirEntry - Это каталог
                    #------------------------------------------------------------
                    LBaseName = os.path.basename (LFile.path)
                    LPathTimeSource = LUFile.GetFileDateTime (LFile.path)[2]

                    #------------------------------------------------------------
                    # на следующий уровень
                    #------------------------------------------------------------
                    if ASubdir:
                        GLevel = GLevel + 1
                        if APathDest != '':
                            LPathDest = os.path.join (APathDest, LFile.name)
                        else:
                            LPathDest = ''
                        #endif
                        __ListDir (LFile.path, AMask, ASubdir, LPathDest, _OutFile, _Option, _FuncDir, _FuncFile)
                    #endif
                #endif
            #endif
        #endfor
        GLevel = GLevel - 1
    #endwith
#endfunction

#-------------------------------------------------------------------------------
# BacFiles
#-------------------------------------------------------------------------------
def BacFiles (APathSource, AMask, ASubDir, APathDest,
              _OutFile, _Option, _ASync: bool=False):

    #-------------------------------------------------------------------------------
    # FuncDir
    #-------------------------------------------------------------------------------
    def FuncDir (_APathSource: str, _APathDest: str):
    #beginfunction
        LPathSource = _APathSource
        LBaseName = os.path.basename (_APathSource)
        LPathDest = os.path.join (_APathDest, LBaseName)
        LPathTimeSource = LUFile.GetFileDateTime (_APathSource) [2]
        Lattr = LUFile.GetFileAttr (_APathSource)
        if not _ASync:
            if not LUFile.DirectoryExists(LPathDest):
                s = f'Create {LPathDest:s} ...'
                LULog.LoggerTOOLS_AddLevel (logging.DEBUG, s)
                LUFile.ForceDirectories(LPathDest)
                LUFile.SetFileAttr(LPathDest, Lattr, False)
            #endif
        else:
            if not LUFile.DirectoryExists(LPathDest):
                s = f'Delete {LPathSource:s} ...'
                LULog.LoggerTOOLS_AddLevel (logging.DEBUG, s)
                LUFile.DirectoryDelete(LPathSource)
            #endif
        #endif
    #endfunction

    #-------------------------------------------------------------------------------
    # FuncFile 
    #-------------------------------------------------------------------------------
    def FuncFile (AFileName: str, _APathDest: str):
    #beginfunction
        LFileNameSource = AFileName
        LBaseName = os.path.basename (AFileName)
        LFileTimeSource = LUFile.GetFileDateTime (AFileName) [2]
        LFileSizeSource = LUFile.GetFileSize (AFileName)
        LFileAttrSource = LUFile.GetFileAttr (AFileName)

        LFileNameDest = os.path.join (_APathDest, LBaseName)

        #--------------------------------------------------------------------
        LResult = LUFile.COMPAREFILETIMES(LFileNameSource, LFileNameDest)
        #--------------------------------------------------------------------
        # Check Result
        #--------------------------------------------------------------------
        match LResult:
            case -3:
                # -3 File2 could not be opened (see @ERROR for more information).
                LFileSizeDest = 0
                LFileTimeDest = 0
                LDelete = False
                LCopy = True
                if _ASync:
                    LCopy = False
                    LDelete = True
                #endif
            case -2:
                # -2 File1 could not be opened (see @ERROR for more information).
                LDelete = False
                LCopy = False
            case -1:
                # -1 File1 is older than file2.
                LDelete = False
                LCopy = False
            case 0:
                # 0  File1 and file2 have the same date and time.
                LDelete = False
                LCopy = False
                LFileTimeDest = LUFile.GetFileDateTime (LFileNameDest) [2]
                LFileSizeDest = LUFile.GetFileSize (LFileNameDest)
                LFileAttrDest = LUFile.GetFileAttr (LFileNameDest)
                if (LFileSizeSource != LFileSizeDest):
                    LCopy = True
                else:
                    LUFile.SetFileAttr(LFileNameDest, LFileAttrSource, False)
                    # shutil.copystat (LFileNameSource, LFileNameDest)
                #endif
            case 1:
                # 1  File1 is more recent than file2.
                LDelete = False
                LCopy = True
        #endmatch

        #--------------------------------------------------------------------
        # Copy
        #--------------------------------------------------------------------
        if LCopy == True:
            s = f'Copy {LFileNameSource:s} -> {LFileNameDest:s} ...'
            LULog.LoggerTOOLS_AddLevel (logging.DEBUG, s)
            LUFile.FileCopy (LFileNameSource, LFileNameDest, True)
        #endif

        #--------------------------------------------------------------------
        # Delete
        #--------------------------------------------------------------------
        if LDelete == True:
            s = f'Delete {LFileNameSource:s} ...'
            LULog.LoggerTOOLS_AddLevel (logging.DEBUG, s)
            LUFile.FileDelete (LFileNameSource)
        #endif
    #endfunction

#beginfunction
    if (APathSource != "") and (APathDest != ""):
        LBaseName = os.path.basename (APathSource)
        LPathDest = APathDest
        s = f'BacFiles: {APathSource:s} {AMask:s} => {APathDest:s} ...'
        LULog.LoggerTOOLS_AddLevel (LULog.TEXT, s)
        __ListDir (APathSource, AMask, ASubDir, LPathDest, _OutFile, _Option, FuncDir, FuncFile)
    #endif
#endfunction

#-------------------------------------------------------------------------------
# SyncFiles
#-------------------------------------------------------------------------------
def SyncFiles (APathSource, AMask, APathDest, _OutFile, _Option):
#beginfunction
    s = f'SyncFiles: {APathSource:s} {AMask:s} => {APathDest:s} ...'
    LULog.LoggerTOOLS_AddLevel (LULog.TEXT, s)

    BacFiles (APathSource, AMask, True, APathDest, _OutFile, _Option, False)
    BacFiles (APathDest, AMask, True, APathSource, _OutFile, _Option, True)
#endfunction

#-------------------------------------------------------------------------------
# DirFiles
#-------------------------------------------------------------------------------
def DirFiles (APathSource, AMask, ASubDir,
              _OutFile, _Option, _FuncDir, _FuncFile):
#beginfunction
    if (APathSource != ""):
        s = f'DirFiles: {APathSource:s} {AMask:s} ...'
        LULog.LoggerTOOLS_AddLevel (LULog.TEXT, s)
        __ListDir(APathSource, AMask, ASubDir, '', _OutFile, _Option, _FuncDir, _FuncFile)
    #endif
#endfunction

#-------------------------------------------------------------------------------
# __FakeFile
#-------------------------------------------------------------------------------
def __FakeFile (APathSource,
                _OutFile, _Option, _FuncDir, _FuncFile):
    global GLevel
#beginfunction
    for LFileCount in range(0, 2):
        s = f'FakeFile_{str(GLevel+1):s}_{str(LFileCount+1):s}.txt'
        LFileName = os.path.join (APathSource, s)

        LHahdle = LUFile.OpenTextFile(LFileName, '')
        LUFile.WriteTextFile(LHahdle, 'test')
        LUFile.WriteTextFile(LHahdle, 'тест')
        LUFile.CloseTextFile(LHahdle)

        if _FuncFile:
            s = f'_FuncFile: {_FuncFile.__name__:s}'
            # LULog.LoggerTOOLS_AddLevel (logging.DEBUG, s)
            _FuncFile (LFileName)
        #endif
    #endfor
#endfunction

#-------------------------------------------------------------------------------
# __FakeDir
#-------------------------------------------------------------------------------
def __FakeDir (APathSource,
               _OutFile, _Option, _FuncDir, _FuncFile):
#beginfunction
    global GLevel

    #------------------------------------------------------------
    # Dir
    #------------------------------------------------------------
    LBaseName = os.path.basename (APathSource)
    LULog.LoggerTOOLS_AddLevel (LULog.TEXT, LUFile.ExpandFileName (APathSource))

    #------------------------------------------------------------
    #
    #------------------------------------------------------------
    if _FuncDir:
        s = f'_FuncDir: {_FuncDir.__name__:s}'
        # LULog.LoggerTOOLS_AddLevel (logging.DEBUG, s)
        _FuncDir (LUFile.ExpandFileName (APathSource))
    #endif

    __FakeFile (APathSource, _OutFile, _Option, _FuncDir, _FuncFile)

    #------------------------------------------------------------
    # на следующий уровень
    #------------------------------------------------------------
    if GLevel < 3:
        for LDirCount in range (0, 2):
            s = f'FakeDir_{str(GLevel+1):s}_{str(LDirCount+1):s}'
            LPathSource = os.path.join (APathSource, s)
            LUFile.ForceDirectories(LPathSource)

            GLevel = GLevel + 1
            __FakeDir(LPathSource, _OutFile, _Option, _FuncDir, _FuncFile)
        #endfor
    #endif
    GLevel = GLevel - 1
#endfunction

#-------------------------------------------------------------------------------
# FakeFiles
#-------------------------------------------------------------------------------
def FakeFiles (APathSource,
              _OutFile, _Option, _FuncDir, _FuncFile):
#beginfunction
    if (APathSource != ""):
        s = f'FakeFiles: {APathSource:s} ...'
        LULog.LoggerTOOLS_AddLevel (LULog.TEXT, s)
        __FakeDir(APathSource, _OutFile, _Option, _FuncDir, _FuncFile)
    #endif
#endfunction

#-------------------------------------------------------------------------------
# DelFiles
#-------------------------------------------------------------------------------
def DelFiles (APathSource, AMask, ASubDir, _OutFile, _Option, _Older: int):
#beginfunction

    #-------------------------------------------------------------------------------
    # DelFile
    #-------------------------------------------------------------------------------
    def DelFile (AFileName: str):
    #beginfunction
        LDay = LUDateTime.Now ()
        # print(LUFile.GetFileDateTime (AFileName))
        LFileTimeSource = LUFile.GetFileDateTime (AFileName) [2]
        # print ((LDay - LFileTimeSource).days)
        if (LDay - LFileTimeSource).days > _Older:
            s = f'Delete {AFileName:s} ...'
            LULog.LoggerTOOLS_AddLevel (logging.DEBUG, s)
            LUFile.FileDelete(AFileName)
        #endif
    #endfunction

#beginfunction
    if (APathSource != ""):
        stat = f'DelFiles: {APathSource:s} {AMask:s} ...'
        LULog.LoggerTOOLS_AddLevel (lyr.LULog.TEXT, s)
        __ListDir (APathSource, AMask, ASubDir, '', _OutFile, _Option, None, DelFile)
    #endif
#endfunction

#------------------------------------------
def main ():
#beginfunction
    print('main LUFileUtils.py ...')
#endfunction

#------------------------------------------
#
#------------------------------------------
#beginmodule
if __name__ == "__main__":
    main()
#endif

#endmodule
