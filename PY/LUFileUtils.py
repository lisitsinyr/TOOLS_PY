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
# ListDir (ASourcePath, AMask, optional _OutFile, optional _Option, optional _FuncDir, optional _FuncFile)
#-------------------------------------------------------------------------------
def __OUTFILE (s: str, _OutFile: str):
#beginfunction
    if (_OutFile) and (s != ''):
        if (_OutFile.upper () == 'CONSOLE'):
            print (s)
        else:
            LUFile.WriteStrToFile (_OutFile, s + '\n')
        #endif
        # LULog.LoggerTOOLS_AddLevel (LULog.TEXT, s)
    #endif
#endfunction

#-------------------------------------------------------------------------------
# ListFile (ASourcePath, AMask, optional _OutFile, optional _Option, optional _FuncFile)
#-------------------------------------------------------------------------------
def __ListFile (ASourcePath, AMask='^.*..*$', ADestPath='',
                _OutFile='', _Option=1, _FuncDir=None, _FuncFile=None):
    global GFileCount
    global GFileSize
#beginfunction
    LFileCount = 0
    with os.scandir(ASourcePath) as LFiles:
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
                            s = f"{LFileTimeSource:%d.%m.%Y  %H:%M} {LFileSizeSource:-17,d} {LBaseName:s}"
                        case 2 | 12:
                            s = f"{LFileTimeSource:%d.%m.%Y  %H:%M} {LFileSizeSource:-17,d} {LBaseName:s}"
                        case _:
                            s = ''
                    #endmatch
                    __OUTFILE (s, _OutFile)

                    if _FuncFile:
                        # print(_FuncFile.__name__)
                        _FuncFile (LUFile.ExpandFileName (LFile.path))
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
                        s = f"{LPathTimeSource:%d.%m.%Y  %H:%M} {'   <DIR>':17s} {LBaseName:s}"
                    case 2 | 12:
                        s = f"{LPathTimeSource:%d.%m.%Y  %H:%M} {'   <DIR>':17s} {LBaseName:s}"
                    case _:
                        s = ''
                #endmatch
                __OUTFILE (s, _OutFile)

                #------------------------------------------------------------
                #
                #------------------------------------------------------------
                if _FuncDir:
                    # print(_FuncDir.__name__)
                    _FuncDir (LUFile.ExpandFileName (LFile.path))
                #endif
            #endif
        #endfor
    #endwith
    return LFileCount
#endfunction

#-------------------------------------------------------------------------------
# ListDir (ASourcePath, AMask, optional _OutFile, optional _Option, optional _FuncDir, optional _FuncFile)
#-------------------------------------------------------------------------------
def __ListDir (ASourcePath, AMask, ASubdir, ADestPath, _OutFile, _Option, _FuncDir, _FuncFile):
#beginfunction
    global GLevel
    global GFileCount
    global GFileSize

    #------------------------------------------------------------
    # Dir
    #------------------------------------------------------------
    LBaseName = os.path.basename (ASourcePath)
    LPathTimeSource = LUFile.GetFileDateTime (ASourcePath)[2]

    GFileCount = 0
    GFileSize = 0

    #------------------------------------------------------------
    # список файлов в каталоге
    #------------------------------------------------------------
    s = f"\nСодержимое папки {ASourcePath:s}\n"
    __OUTFILE (s, _OutFile)
    match _Option:
        case 1 | 11:
            s = f"{LPathTimeSource:%d.%m.%Y  %H:%M} {'   <DIR>':17s} {LBaseName:s}"
        case 2 | 12:
            s = f"{LPathTimeSource:%d.%m.%Y  %H:%M} {'   <DIR>':17s} {LBaseName:s}"
        case _:
            s = ''
    #endmatch
    __OUTFILE (s, _OutFile)

    LFileCount = __ListFile (ASourcePath, AMask, ADestPath, _OutFile, _Option, _FuncDir, _FuncFile)

    match _Option:
        case 1 | 11:
            s = f"{GFileCount:16d} файлов {GFileSize:16,d} байт"
        case 2 | 12:
            s = f"{GFileCount:16d} файлов {GFileSize:16,d} байт"
        case _:
            s = ''
    #endmatch
    __OUTFILE (s, _OutFile)
    #------------------------------------------------------------

    with os.scandir(ASourcePath) as LFiles:
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
                        if ADestPath != '':
                            LPathDest = os.path.join (ADestPath, LFile.name)
                        else:
                            LPathDest = ''
                        #endif
                        __ListDir (LFile.path, AMask, LPathDest, ASubdir, _OutFile, _Option, _FuncDir, _FuncFile)
                    #endif
                #endif
            #endif
        #endfor
        GLevel = GLevel - 1
    #endwith
#endfunction

#-------------------------------------------------------------------------------
# BacFiles (ASourcePath, ADestPath, AMask, optional ACheckSize, optional ADestPathDelta, optional $Delete, optional $ExecFunc, optional $OverwriteNewer)
#-------------------------------------------------------------------------------
def BacFiles (ASourcePath, ADestPath, AMask, ASubDir,
              _OutFile, _Option):

    #-------------------------------------------------------------------------------
    # FuncDir
    #-------------------------------------------------------------------------------
    def FuncDir (APath: str):
    #beginfunction
        LPathTimeSource = LUFile.GetFileDateTime (APath) [2]
    #endfunction

    #-------------------------------------------------------------------------------
    # FuncFile 
    #-------------------------------------------------------------------------------
    def FuncFile (AFileName: str):
    #beginfunction
        LFileTimeSource = LUFile.GetFileDateTime (AFileName) [2]
    #endfunction

#beginfunction
    if (ASourcePath != "") and (ADestPath != ""):
        # if $Debug
        #    LogAdd (Log, LogFile, "I", "BacFiles: "+ASourcePath+" => "+ADestPath+" "+AMask, "w+/n")
        # #endif
        # __ScanDir (ASourcePath, ADestPath, AMask,
        #        _ACheckSize, ADestPathDelta, _Delete, _ExecFunc, _OverwriteNewer, _ExecFuncPAR1)
        __ListDir (ASourcePath, '.*', '', ASubDir, _OutFile, _Option, FuncDir, FuncFile)
    #endif
#endfunction

#-------------------------------------------------------------------------------
#  DirFiles (ASourcePath, AMask, optional $OutFile)
#-------------------------------------------------------------------------------
def DirFiles (ASourcePath, AMask, ASubDir,
              _OutFile, _Option, _FuncDir, _FuncFile):
#beginfunction
    if (ASourcePath != ""):
        __ListDir(ASourcePath, AMask, ASubDir, '', _OutFile, _Option, None, None)
    #endif
#endfunction

#-------------------------------------------------------------------------------
# DelFiles (ASourcePath, AMask, $Day)
#-------------------------------------------------------------------------------
def DelFiles (ASourcePath, AMask, ASubDir, _OutFile, _Option, _Older: int):

    #-------------------------------------------------------------------------------
    # DelFiles (ASourcePath, AMask, $Day)
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
    if (ASourcePath != ""):
        __ListDir (ASourcePath, AMask, ASubDir, '', _OutFile, _Option, None, DelFile)
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
