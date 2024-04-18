"""LUFileUtils.py"""
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
# import date
import shutil
import win32api
import platform

#------------------------------------------
# БИБЛИОТЕКА LU
#------------------------------------------
import LUErrors
import LUFile
import LUStrDecode
import LULog

#------------------------------------------
# БИБЛИОТЕКИ LU
#------------------------------------------
import LUDateTime

#------------------------------------------
#CONST
#------------------------------------------
GLevel = 0
GFileCount = 0
GFileSize = 0
GDir = ''
GMask = '*.*'
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
                _OutFile, _Option, _FuncDir, _FuncFile):
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
                        LULog.LoggerTOOLS_AddLevel (logging.DEBUG, s)
                        _FuncFile (LUFile.ExpandFileName (LFile.path), APathDest)
                    #endif
                #endif
            #endif
            if LFile.is_dir ():  # and (not LFile.name.startswith('.')):
                #------------------------------------------------------------
                # class os.DirEntry - Это каталог
                #------------------------------------------------------------
                LBaseName = os.path.basename (LFile.path)
                LPathTimeSource = LUFile.GetFileDateTime (LFile.path) [2]

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
                    LULog.LoggerTOOLS_AddLevel (logging.DEBUG, s)
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
    LPathTimeSource = LUFile.GetFileDateTime (APathSource)[2]

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
        LBaseName = os.path.basename (_APathSource)
        LPathDest = os.path.join (_APathDest, LBaseName)
        LPathTimeSource = LUFile.GetFileDateTime (_APathSource) [2]
        LULog.LoggerTOOLS_AddLevel (LULog.TEXT, _APathSource)
        if not _ASync:
            if not LUFile.DirectoryExists(LPathDest):
                s = f'Create {LPathDest:s} ...'
                LULog.LoggerTOOLS_AddLevel (LULog.TEXT, s)
                LUFile.ForceDirectories(LPathDest)
            #endif
        else:
            if not LUFile.DirectoryExists(LPathDest):
                s = f'Delete {LPathDest:s} ...'
                LULog.LoggerTOOLS_AddLevel (LULog.TEXT, s)
                # LUFile.DirectoryDelete(LPathDest)
                ...
            #endif
        #endif
    #endfunction

    #-------------------------------------------------------------------------------
    # FuncFile 
    #-------------------------------------------------------------------------------
    def FuncFile (AFileName: str, _APathDest: str):
    #beginfunction
        LBaseName = os.path.basename (AFileName)
        LFileTimeSource = LUFile.GetFileDateTime (AFileName) [2]
        LFileSizeSource = LUFile.GetFileSize (AFileName)
        LFileNameSource = AFileName
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
                if (LFileSizeSource != LFileSizeDest):
                    LCopy = True
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
            LULog.LoggerTOOLS_AddLevel (LULog.TEXT, s)
            LUFile.FileCopy (LFileNameSource, LFileNameDest, True)
        #endif
        #--------------------------------------------------------------------
        # Delete
        #--------------------------------------------------------------------
        if LDelete == True:
            s = f'Delete {LFileNameSource:s} ...'
            LULog.LoggerTOOLS_AddLevel (LULog.TEXT, s)
            LUFile.FileDelete (LFileNameSource)
        #endif
    #endfunction

#beginfunction
    if (APathSource != "") and (APathDest != ""):
        LBaseName = os.path.basename (APathSource)
        LPathDest = os.path.join (APathDest, LBaseName)
        stat = f'BacFiles: {APathSource:s} {AMask:s} => {APathDest:s} ...'
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
            print('Delete',AFileName,'...')
            LUFile.FileDelete(AFileName)
        #endif
    #endfunction

#beginfunction
    if (APathSource != ""):
        stat = f'DelFiles: {APathSource:s} {AMask:s} ...'
        LULog.LoggerTOOLS_AddLevel (LULog.TEXT, s)
        __ListDir (APathSource, AMask, ASubDir, '', _OutFile, _Option, None, DelFile)
    #endif
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
