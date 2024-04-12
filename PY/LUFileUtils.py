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
GDir = ''
GMask = '*.*'
GDirCount = 0
GLevelMAX = sys.maxsize

#-------------------------------------------------------------------------------
# ScanFile (ASourcePath, ADestPath, AMask, optional ACheckSize, optional ADestPathDelta, optional $Delete, optional $ExecFunc, optional $ExecFuncPAR1, optional $OverwriteNewer)
#-------------------------------------------------------------------------------
def ScanFile (ASourcePath, ADestPath, AMask,
              _ACheckSize, _ADestPathDelta, _Delete, _ExecFunc, _OverwriteNewer, _ExecFuncPAR1):
#beginfunction
    print(ASourcePath)
    print(ADestPath)
    if not LUFile.DirectoryExists(ADestPath):
        LUFile.ForceDirectories(ADestPath)
    #endif

    # print(_ADestPathDelta)
    if _ADestPathDelta:
        if not LUFile.DirectoryExists (_ADestPathDelta):
            LUFile.ForceDirectories (_ADestPathDelta)
        #endif
    #endif

    LFileCount = 0
    with os.scandir (ASourcePath) as LSourceFiles:
        for LSourceFile in LSourceFiles:
            if (not LSourceFile.is_symlink ()):
                if LSourceFile.is_file () and LUFile.CheckFileNameMask (LSourceFile.name, AMask):
                    # class os.DirEntry - Это файл
                    LFileCount = LFileCount + 1

                    LFullFileNameSource = LSourceFile.path
                    Lstats = os.stat (LFullFileNameSource)
                    LFileNameSource = LSourceFile.name
                    s = '  ' * (GLevel - 1) + '   ' + LFileNameSource
                    LULog.LoggerTOOLS_AddLevel (LULog.TEXT, s)
                    LFileNameSource = LSourceFile.path
                    LFileSizeSource = LUFile.GetFileSize (LFileNameSource)
                    LFileAttrSource = LUFile.GetFileAttr (LFileNameSource)
                    # print(LFileSizeSource)
                    LFileTimeSource = LUFile.GetFileDateTime (LFileNameSource)[2]
                    LFileNameDest = os.path.join (ADestPath, LSourceFile.name)
                    if _ADestPathDelta:
                        LFileNameDestDelta = os.path.join (_ADestPathDelta, LSourceFile.name)
                    #endif
                    #--------------------------------------------------------------------
                    LResult = LUFile.COMPAREFILETIMES(LFileNameSource, LFileNameDest)
                    # -3 File2 could not be opened (see @ERROR for more information).
                    # -2 File1 could not be opened (see @ERROR for more information).
                    # -1 File1 is older than file2.
                    # 0  File1 and file2 have the same date and time.
                    # 1  File1 is more recent than file2.
                    #--------------------------------------------------------------------
                    # Check Result
                    #--------------------------------------------------------------------
                    LCopy = False
                    LDelete = False
                    if _Delete:
                        if LResult == -3:
                            LDelete = True
                        #endif
                    else:
                        if LResult == -3:
                            LFileSizeDest = "new"
                            LFileTimeDest = "new"
                            LCopy = True
                        else:
                            LFileSizeDest = LUFile.GetFileSize (LFileNameDest)
                            LFileTimeDest = LUFile.GetFileDateTime (LFileNameDest)[2]
                            if LResult == 1:
                                LCopy = True
                            else:
                                if (LResult == -1) and (_OverwriteNewer == 1):
                                    warnOWN = "More recent dest file " + LFileNameDest2 + " is to be overwritten"
                                    LogAdd ("3", LogFile, "F", _warnOWN, "w+/n")
                                    LCopy = True
                                #endif
                                if (_ACheckSize) and (LFileSizeSource != LFileSizeDest):
                                    LCopy = True
                                #endif
                            #endif
                        #endif
                    #endif

                    #--------------------------------------------------------------------
                    # Copy
                    #--------------------------------------------------------------------
                    if LCopy == True:
                        s = LFileNameSource + " ("+str(LFileSizeSource)+"|"+str(LFileTimeSource)+")" + " => " + \
                            LFileNameDest   + " ("+str(LFileSizeDest)+"|"+str(LFileTimeDest)+")"
                        LUFile.FileCopy (LFileNameSource, LFileNameDest,False)
                        Lattr = LUFile.GetFileAttr (LFileNameDest)
                        Lattr = Lattr & stat.FILE_ATTRIBUTE_READONLY
                        # os.chflags (AFileName, 0)
                        LUFile.SetFileAttr (LFileNameDest, Lattr)
                        if _ExecFunc:
                            ResExe = _ExecFunc (LFileNameSource, LFileNameDest, _ExecFuncPAR1)
                        #endif
                        if _ADestPathDelta:
                            s = s + " => " + LFileNameDestDelta
                            LUFile.FileCopy (LFileNameSource, LFileNameDestDelta, False)
                        #endif
                    #endif

                    #--------------------------------------------------------------------
                    # Delete
                    #--------------------------------------------------------------------
                    if LDelete:
                        s = "Delete file "+LFileNameSource + " ("+LFileSizeSource+"|"+LFileTimeSource+")"+" ..."
                        # LUFile.FileDelete (LFileNameSource)
                    #endif
                #endif
            #endif
        #endfor
    #endwith
#endfunction

#-------------------------------------------------------------------------------
#  ScanDir (ASourcePath, ADestPath, AMask, optional ACheckSize, optional ADestPathDelta, optional $Delete, optional $ExecFunc)
#-------------------------------------------------------------------------------
def ScanDir (ASourcePath, ADestPath, AMask,
             _ACheckSize, _ADestPathDelta, _Delete, _ExecFunc, _OverwriteNewer, _ExecFuncPAR1):
#beginfunction
    global GLevel
    GLevel = GLevel + 1

    #------------------------------------------------------------
    # Dir
    #------------------------------------------------------------
    LPath = ASourcePath
    LPath = LUFile.ExpandFileName (ASourcePath)
    LPath = os.path.basename (LPath)
    s = '    '*(GLevel-1)+LPath+' [DIR]'
    LULog.LoggerTOOLS_AddLevel (LULog.TEXT, s)

    #------------------------------------------------------------
    # список файлов в каталоге
    #------------------------------------------------------------
    ScanFile (ASourcePath, ADestPath, AMask,
          _ACheckSize, _ADestPathDelta, _Delete, _ExecFunc, _OverwriteNewer, _ExecFuncPAR1)

    with os.scandir (ASourcePath) as LFiles:
        for LFile in LFiles:
            Lname = LFile.name
            # print('name:',Lname)
            if (not LFile.is_symlink()):
                if LFile.is_dir ():
                    #------------------------------------------------------------
                    # class os.DirEntry - Это каталог
                    #------------------------------------------------------------
                    LPathName = LFile.name
                    # LFullPathName = os.path.join (ASourcePath, LFile.name)
                    LFullPathName = LUFile.ExpandFileName (LFile.path)
                    print(LFullPathName)
                    Lstats = os.stat (LFullPathName)

                    LDestPath = os.path.join (ADestPath, LFile.name)
                    print(LDestPath)

                    if _ADestPathDelta:
                        LDestPathDelta = os.path.join (_ADestPathDelta, LFile.name)
                        print (LDestPathDelta)
                    else:
                        LDestPathDelta = ''
                    #endif

                    #------------------------------------------------------------
                    # на следующий уровень
                    #------------------------------------------------------------
                    # print(GLevel)
                    ScanDir  (LFile.path, LDestPath, AMask,
                              _ACheckSize, LDestPathDelta, _Delete, _ExecFunc, _OverwriteNewer, _ExecFuncPAR1)
                #endif
            #endif
        #endfor
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
      ScanFile(ASourcePath, ADestPath, AMask,
               _ACheckSize, _ADestPathDelta, _Delete, _ExecFunc, _OverwriteNewer, _ExecFuncPAR1)
   #endif
#endfunction

#-------------------------------------------------------------------------------
#  BacFiles (ASourcePath, ADestPath, AMask, optional ACheckSize, optional ADestPathDelta, optional $Delete, optional $ExecFunc, optional $OverwriteNewer)
#-------------------------------------------------------------------------------
def BacFiles (ASourcePath, ADestPath, AMask,
              _ACheckSize, _ADestPathDelta, _Delete, _ExecFunc, _OverwriteNewer, _ExecFuncPAR1):
#beginfunction
   if (ASourcePath != "") and (ADestPath != ""):
      # if $Debug
      #    LogAdd (Log, LogFile, "I", "BacFiles: "+ASourcePath+" => "+ADestPath+" "+AMask, "w+/n")
      # #endif
      ScanDir (ASourcePath, ADestPath, AMask,
               _ACheckSize, ADestPathDelta, _Delete, _ExecFunc, _OverwriteNewer, _ExecFuncPAR1)
    #endif
#endfunction

#-------------------------------------------------------------------------------
#  BacDirs (ASourcePath, ADestPath, ACheckSize)
#-------------------------------------------------------------------------------
def BacDirs (ASourcePath, ADestPath, ACheckSize):
#beginfunction
    if (ASourcePath != "") and (ADestPath != ""):
        # if $Debug
        #    LogAdd (Log, LogFile, "I", "BacFiles: "+ASourcePath+" => "+ADestPath+" "+AMask, "w+/n")
        # #endif
        ScanDir (ASourcePath, ADestPath, AMask, _ACheckSize)
    #endif
#endfunction

# -------------------------------------------------------------------------------
# __WorkFile (AFile_path)
# -------------------------------------------------------------------------------
def __WorkFile (AFullFileName):
    # global Shablon
#beginfunction
    LFileNameSource: str = AFullFileName
    LFullFileName: str = LFileNameSource
    LFileName: str = os.path.basename(LFullFileName)
    LFileDir: str = os.path.dirname(LFullFileName)
    #--------------------------------------------------------------------------------
    LFileSizeSource = LUFile.GetFileSize (LFileNameSource)
    LFileTimeSource = LUFile.GetFileDateTime (LFileNameSource)
    #--------------------------------------------------------------------------------
    #$Y = Val(SUBSTR(LFileTimeSource[2],1,4))
    #$M = Val(SUBSTR(LFileTimeSource[2],6,2))
    #$D = Val(SUBSTR(LFileTimeSource[2],9,2))
    #LFileDaySource = EncodeDate($Y,$M,$D)
    #--------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------
    #LDay = EncodeDate(@Year,@MonthNo,@MDayNo)
    #--------------------------------------------------------------------------------
#endfunction

#-------------------------------------------------------------------------------
# ListFile (ASourcePath, AMask, optional _OutFile, optional _Option, optional _FuncFile)
#-------------------------------------------------------------------------------
def ListFile (ASourcePath, AMask='^.*..*$', _OutFile='', _Option=0, _FuncDir=None, _FuncFile=None):
#beginfunction
    LFileCount = 0
    with os.scandir(ASourcePath) as LFiles:
        for LFile in LFiles:
            if (not LFile.is_symlink ()):
                if LFile.is_file() and LUFile.CheckFileNameMask (LFile.name, AMask):
                    # Lresult = LUFile.CheckFileNameMask (LFile.name, AMask)
                    #------------------------------------------------------------
                    # class os.DirEntry - Это файл
                    #------------------------------------------------------------
                    LFileCount = LFileCount + 1
                    LFileName = LFile.name
                    # LFullPathName = os.path.join (ASourcePath, LFile.name)
                    LFullFileName = LUFile.ExpandFileName (LFile.path)
                    Lstats = os.stat (LFullFileName)
                    s = '    ' * (GLevel - 1) + '    ' + LFileName
                    LULog.LoggerTOOLS_AddLevel (LULog.TEXT, s)
                    if (_OutFile) and (_OutFile.upper() == 'CONSOLE'):
                       print (s)
                    #endif
                    if (_OutFile) and (_OutFile.upper() != 'CONSOLE'):
                        LUFile.WriteStrToFile(_OutFile, s+'\n')
                    #endif
                    __WorkFile (LFullFileName)
                    if _FuncFile:
                        _FuncFile (LFile)
                    #endif
                #endif
            #endif
        #endfor
    #endwith
    return LFileCount
#endfunction

#-------------------------------------------------------------------------------
# ListDir (ASourcePath, AMask, optional _OutFile, optional _Option, optional _FuncDir, optional _FuncFile)
#-------------------------------------------------------------------------------
def ListDir (ASourcePath, AMask, _OutFile='', _Option=10, _FuncDir=None, _FuncFile=None, _ALevel: int=sys.maxsize):
#beginfunction
    global GLevel
    GLevel = GLevel + 1

    #------------------------------------------------------------
    # Dir
    #------------------------------------------------------------
    LPath = ASourcePath
    LPath = LUFile.ExpandFileName (ASourcePath)
    LPath = os.path.basename (LPath)
    s = '    '*(GLevel-1)+LPath+' [DIR]'
    LULog.LoggerTOOLS_AddLevel (LULog.TEXT, s)

    if _Option == 10 or _Option == 11 or _Option == 12:
        if (_OutFile) and (_OutFile.upper() == 'CONSOLE'):
            print (s)
        #endif
        if (_OutFile) and (_OutFile.upper() != 'CONSOLE'):
            LUFile.WriteStrToFile (_OutFile, s + '\n')
        #endif
    #endif

    #------------------------------------------------------------
    # список файлов в каталоге
    #------------------------------------------------------------
    LFileCount = ListFile (ASourcePath, AMask, _OutFile, _Option, _FuncDir, _FuncFile)

    with os.scandir(ASourcePath) as LFiles:
        for LFile in LFiles:
            Lname = LFile.name
            # print('name:',Lname)
            Lpath = LFile.path
            # print('path:',Lpath)
            Linode = LFile.inode()
            # print('inode:',Linode)
            Lis_dir = LFile.is_dir()
            # print('is_dir:',Lis_dir)
            Lis_file = LFile.is_file()
            # print('is_file:',Lis_file)
            Lis_symlink = LFile.is_symlink()
            # print('is_symlink:',Lis_symlink)
            Lstat = LFile.stat()
            # print('stat:',Lstat)

            if (not LFile.is_symlink()):
                if LFile.is_dir () and (not LFile.name.startswith('.')):
                    #------------------------------------------------------------
                    # class os.DirEntry - Это каталог
                    #------------------------------------------------------------
                    LPathName = LFile.name
                    # LFullPathName = os.path.join (ASourcePath, LFile.name)
                    LFullPathName = LUFile.ExpandFileName (LFile.path)
                    Lstats = os.stat (LFullPathName)

                    if _FuncDir:
                        _FuncDir(LFile)
                    #endif
                    
                    #------------------------------------------------------------
                    # на следующий уровень
                    #------------------------------------------------------------
                    # print(GLevel, _ALevel)
                    if GLevel < _ALevel:
                        ListDir (LFile.path, AMask, _OutFile, _Option, _FuncDir, _FuncFile, _ALevel)
                    #endif
                #endif
            #endif
        #endfor
        GLevel = GLevel - 1
    #endwith
#endfunction

#-------------------------------------------------------------------------------
#  DirFiles (ASourcePath, AMask, optional $OutFile)
#-------------------------------------------------------------------------------
def DirFiles (ASourcePath, AMask, _OutFile):
#beginfunction
    LFileCount = 0
    with os.scandir (ASourcePath) as LFiles:
        for LFile in LFiles:
            if (not LFile.is_symlink ()):
                if LFile.is_dir () and (not LFile.name.startswith('.')):
                    #------------------------------------------------------------
                    # class os.DirEntry - Это каталог
                    #------------------------------------------------------------
                    LPathName = LFile.name
                    # LFullPathName = os.path.join (ASourcePath, LFile.name)
                    LFullPathName = LUFile.ExpandFileName (LFile.path)
                    Lstats = os.stat (LFullPathName)
                    if (_OutFile) and (_OutFile.upper() == 'CONSOLE'):
                        print (LPathName)
                    #endif
                    if (_OutFile) and (_OutFile.upper() != 'CONSOLE'):
                        LUFile.WriteStrToFile (_OutFile, LPathName + '\n')
                    #endif
                #endif
                if LFile.is_file () and LUFile.CheckFileNameMask (LFile.name, AMask):
                    #------------------------------------------------------------
                    # class os.DirEntry - Это файл
                    #------------------------------------------------------------
                    LFileCount = LFileCount + 1
                    LFileName = LFile.name
                    # LFullPathName = os.path.join (ASourcePath, LFile.name)
                    LFullFileName = LUFile.ExpandFileName (LFile.path)
                    Lstats = os.stat (LFullFileName)
                    if (_OutFile) and (_OutFile.upper() == 'CONSOLE'):
                        print (LFileName)
                    #endif
                    if (_OutFile) and (_OutFile.upper() != 'CONSOLE'):
                        LUFile.WriteStrToFile (_OutFile, LFileName + '\n')
                    #endif
                    __WorkFile (LFullFileName)
                #endif
            #endif
        #endfor
    #endwith
#endfunction

#-------------------------------------------------------------------------------
# DelFiles (ASourcePath, AMask, $Day)
#-------------------------------------------------------------------------------
def DelFiles (ASourcePath, AMask, _OutFile, ADay):
#beginfunction
    L_Day = LUDateTime.Now()
    LFileCount = 0
    with (os.scandir (ASourcePath) as LFiles):
        for LFile in LFiles:
            if (not LFile.is_symlink ()):
                if LFile.is_file () and LUFile.CheckFileNameMask (LFile.name, AMask):
                    #------------------------------------------------------------
                    # class os.DirEntry - Это файл
                    #------------------------------------------------------------
                    LFileCount = LFileCount + 1
                    LFileName = LFile.name
                    # LFullPathName = os.path.join (ASourcePath, LFile.name)
                    LFullFileName = LUFile.ExpandFileName (LFile.path)
                    Lstats = os.stat (LFullFileName)
                    if (_OutFile) and (_OutFile.upper() == 'CONSOLE'):
                        print (LFileName)
                    #endif
                    if (_OutFile) and (_OutFile.upper() != 'CONSOLE'):
                        LUFile.WriteStrToFile (_OutFile, LFileName + '\n')
                    #endif
                    # __WorkFile (LFullFileName)

                    LFileTimeSource = LUFile.GetFileDateTime (LFullFileName) [3]
                    print((L_Day - LFileTimeSource).days)
                    if (L_Day - LFileTimeSource).days > ADay:
                        # os.remove (LFileNameSource)
                        ...
                    #endif
                #endif
            #endif
        #endfor
    #endwith
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
