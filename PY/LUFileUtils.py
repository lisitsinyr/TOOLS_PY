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
GDir = ''
GMask = '*.*'
GDirCount = 0
GLevelMAX = sys.maxsize


#-------------------------------------------------------------------------------
# ListDir (ASourcePath, AMask, optional _OutFile, optional _Option, optional _FuncDir, optional _FuncFile)
#-------------------------------------------------------------------------------
def __ListDir (ASourcePath, AMask, ASubdir, ADestPath, _OutFile, _Option, _FuncDir, _FuncFile):
#beginfunction
    global GLevel
    global GFileCount

    GFileCount = 0
    #------------------------------------------------------------
    # Dir
    #------------------------------------------------------------
    LPath = ASourcePath
    LFullPath = LUFile.ExpandFileName (ASourcePath)
    LBaseName = os.path.basename (LFullPath)

    Lstat = os.stat (LFullPath)
    LmTime = Lstat.st_mtime

    LFileTimeSource = LUFile.GetFileDateTime (LFullPath)[2]

    s = ''
    match _Option:
        case 1 | 11:
            s = ('    ' * GLevel + '<DIR> ' + LBaseName)
            s = ('    ' * GLevel + LUDateTime.DateTimeStr(False,LFileTimeSource,
                                                         ('%d.%m.%Y  %H:%M','%d.%m.%Y  %H:%M'),False)
                 + '    <DIR> ' + '.')
            s = (LUDateTime.DateTimeStr(False,LFileTimeSource,
                                                         ('%d.%m.%Y  %H:%M','%d.%m.%Y  %H:%M'),False)
                 + '    <DIR> ' + '.')

        case 2 | 12:
            s = (LUDateTime.DateTimeStr(False,LFileTimeSource,
                                                         ('%d.%m.%Y  %H:%M','%d.%m.%Y  %H:%M'),False)
                 + '    <DIR> ' + '.')
        case _:
            ...
    #endmatch
    if (_OutFile) and (s != ''):
        if (_OutFile.upper () == 'CONSOLE'):
            print (s)
        else:
            LUFile.WriteStrToFile (_OutFile, s + '\n')
        #endif
        LULog.LoggerTOOLS_AddLevel (LULog.TEXT, s)
    #endif

    #------------------------------------------------------------
    # список файлов в каталоге
    #------------------------------------------------------------
    # LFileCount = __ListFile (ASourcePath, AMask, ADestPath, _OutFile, _Option, _FuncFile)

    with os.scandir(ASourcePath) as LFiles:
        for LFile in LFiles:
            if (not LFile.is_symlink()):
                if LFile.is_file(): # and (not LFile.name.startswith('.')):
                    #------------------------------------------------------------
                    # class os.DirEntry - Это файл
                    #------------------------------------------------------------
                    LFileName = LFile.name
                    LFullFileName = LUFile.ExpandFileName (LFile.path)
                    LBaseName = os.path.basename (LFullFileName)
                    # print(LFullFileName)
                    LFileTimeSource = LUFile.GetFileDateTime (LFullFileName)[2]
                    LFileSizeSource = LUFile.GetFileSize (LFullFileName)

                    GFileCount = GFileCount + 1
                    s = ''
                    match _Option:
                        case 1 | 11:
                            s = ('    ' * GLevel + LUDateTime.DateTimeStr (False, LFileTimeSource,
                                                                   ('%d.%m.%Y  %H:%M', '%d.%m.%Y  %H:%M'), False)
                                 + '          '+str(LFileSizeSource)+' ' + LBaseName)
                            s = (LUDateTime.DateTimeStr (False, LFileTimeSource,
                                                                   ('%d.%m.%Y  %H:%M', '%d.%m.%Y  %H:%M'), False)
                                 + '          ' + str (LFileSizeSource) + ' ' + LBaseName)
                        case 2 | 12:
                            s = ('    ' * GLevel + LUDateTime.DateTimeStr (False, LFileTimeSource,
                                                                   ('%d.%m.%Y  %H:%M', '%d.%m.%Y  %H:%M'), False)
                                 + '          '+str(LFileSizeSource)+' ' + LBaseName)
                            s = (LUDateTime.DateTimeStr (False, LFileTimeSource,
                                                 ('%d.%m.%Y  %H:%M', '%d.%m.%Y  %H:%M'), False)
                                 + '          ' + str (LFileSizeSource) + ' ' + LBaseName)
                        case _:
                            ...
                    #endmatch
                    if (_OutFile) and (s != ''):
                        if (_OutFile.upper () == 'CONSOLE'):
                            print (s)
                        else:
                            LUFile.WriteStrToFile (_OutFile, s + '\n')
                        #endif
                        LULog.LoggerTOOLS_AddLevel (LULog.TEXT, s)
                    #endif

                    if _FuncFile:
                        print(_FuncFile.__name__)
                        _FuncFile (LFullFileName, 100)
                    #endif

                #endif
                if LFile.is_dir (): # and (not LFile.name.startswith('.')):
                    #------------------------------------------------------------
                    # class os.DirEntry - Это каталог
                    #------------------------------------------------------------
                    LPath = LFile.path
                    LFullPath = LUFile.ExpandFileName (LPath)
                    LBaseName = os.path.basename (LFullPath)
                    # print(LFullFileName)

                    if _FuncDir:
                        print(_FuncDir.__name__)
                        _FuncDir (LFullPath)
                    #endif
                    # __WorkDir (LFile, ADestPath, _OutFile, _Option, _FuncDir)

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
#  BacFile (ASourcePath, ADestPath, AMask, optional ACheckSize, optional ADestPathDelta, optional $Delete, optional $ExecFunc, optional $OverwriteNewer)
#-------------------------------------------------------------------------------
def BacFile (ASourcePath, ADestPath, AMask,
             _ACheckSize, _ADestPathDelta, _Delete, _ExecFunc, _OverwriteNewer, _ExecFuncPAR1):
#beginfunction
   if (ASourcePath != "") and (ADestPath != ""):
      # if $Debug
      #    LogAdd (Log, LogFile, "I", "BacFile: "+ASourcePath+" => "+ADestPath+" "+AMask, "w+/n")
      # #endif
      __ScanFile(ASourcePath, ADestPath, AMask,
               _ACheckSize, _ADestPathDelta, _Delete, _ExecFunc, _OverwriteNewer, _ExecFuncPAR1)
   #endif
#endfunction

#-------------------------------------------------------------------------------
#  BacFiles (ASourcePath, ADestPath, AMask, optional ACheckSize, optional ADestPathDelta, optional $Delete, optional $ExecFunc, optional $OverwriteNewer)
#-------------------------------------------------------------------------------
def BacFiles (ASourcePath, ADestPath, AMask, ASubDir, _OutFile, _Option,
              _ACheckSize, _ADestPathDelta, _Delete, _ExecFunc, _OverwriteNewer, _ExecFuncPAR1):
#beginfunction
    if (ASourcePath != "") and (ADestPath != ""):
        # if $Debug
        #    LogAdd (Log, LogFile, "I", "BacFiles: "+ASourcePath+" => "+ADestPath+" "+AMask, "w+/n")
        # #endif
        # __ScanDir (ASourcePath, ADestPath, AMask,
        #        _ACheckSize, ADestPathDelta, _Delete, _ExecFunc, _OverwriteNewer, _ExecFuncPAR1)
        __ListDir (ASourcePath, '.*', '', ASubDir, _OutFile, _Option, None, None)
    #endif
#endfunction

#-------------------------------------------------------------------------------
#  BacDirs (ASourcePath, ADestPath, ACheckSize)
#-------------------------------------------------------------------------------
def BacDirs (ASourcePath, AMask, ASubDir, ADestPath, _OutFile, _Option,
             _ACheckSize):
#beginfunction
    if (ASourcePath != "") and (ADestPath != ""):
        # if $Debug
        #    LogAdd (Log, LogFile, "I", "BacFiles: "+ASourcePath+" => "+ADestPath+" "+AMask, "w+/n")
        # #endif
        # __ScanDir (ASourcePath, ADestPath, AMask, _ACheckSize)
        __ListDir (ASourcePath, AMask, ADestPath, ASubDir, _OutFile, _Option,None, None)
    #endif
#endfunction

#-------------------------------------------------------------------------------
#  DirFiles (ASourcePath, AMask, optional $OutFile)
#-------------------------------------------------------------------------------
def DirFiles (ASourcePath, AMask, ASubDir, _OutFile, _Option):
#beginfunction
    '''
    Содержимое папки D:\PROJECTS_LYR\CHECK_LIST\05_DESKTOP\02_Python\PROJECTS_PY\TESTS_PY\TEST_LU\ListDir

    15.04.2024  15:39    <DIR>          .
    15.04.2024  15:39    <DIR>          ..
    09.04.2024  18:17             2070 ListDir.bat
    15.04.2024  14:54             4349 ListDir.py
    15.04.2024  14:05               266 ListDir.txt
    09.04.2024  18:17             2073 ListDir2.bat
    10.04.2024  15:05             5714 ListDir2.py
    09.04.2024  18:18             2035 ListDir3.bat
    15.04.2024  14:07             4710 ListDir3.py
    15.04.2024  15:39               284 ListDir3.txt
    15.04.2024  15:39           188455 LOGGING_FILEINI.log
    10.04.2024  15:25                 0 LOGGING_FILEINI_json.log
    10.04.2024  15:06    <DIR>          OLD
                  10 файлов        209956 байт
                   3 папок  686997602304 байт свободно
    '''

    if (ASourcePath != ""):
        __ListDir(ASourcePath, AMask, ASubDir, '', _OutFile, _Option,None, None)
    #endif
#endfunction

#-------------------------------------------------------------------------------
# DelFiles (ASourcePath, AMask, $Day)
#-------------------------------------------------------------------------------
def DelFiles (ASourcePath, AMask, ASubDir, _OutFile, _Option, _Older: int):
#beginfunction
    if (ASourcePath != ""):
        __ListDir (ASourcePath, AMask, ASubDir, '', _OutFile, _Option, None, LUFile.FileDelete)
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
