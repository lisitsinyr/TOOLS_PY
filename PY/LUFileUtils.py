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
def ScanFile (ASourcePath, ADestPath, AMask, _ACheckSize, _ADestPathDelta,
              _Delete, _ExecFunc, _OverwriteNewer, _ExecFuncPAR1):
#beginfunction
    if not LUFile.DirectoryExists(ADestPath):
        LUFile.ForceDirectories(ADestPath)
    #endif

    if ADestPathDelta:
        if not LUFile.DirectoryExists (ADestPathDelta):
            LUFile.ForceDirectories (ADestPathDelta)
        #endif
    #endif
    LFileCount = 0
    with os.scandir (ASourcePath) as LFiles:
        for LFile1 in LFiles:
            if (not LFile1.is_symlink ()):
                if LFile1.is_file () and LUFile.CheckFileNameMask (LFile1.name, AMask):
                    # class os.DirEntry - Это файл
                    LFullFileName1 = LFile1.path
                    Lstats = os.stat (LFullFileName1)
                    LFileName1 = LFile1.name
                    s = '  ' * (GLevel - 1) + '   ' + LFileName1
                    LULog.LoggerTOOLS_AddLevel (LULog.TEXT, s)

                    LFileNameSource1 = LFile1.path
                    # LFileSizeSource1 = GetFileSize (LFileNameSource1)
                    # LFileTimeSource1 = GetFileTime (LFileNameSource1)
                    LFileNameDest2 = os.path.join (ADestPath, LFile1.name)
                    if ADestPathDelta:
                        LFileNameDestDelta2 = os.path.join (ADestPathDelta, LFile1.name)
                    #endif

                    LResult = CompareFileTimes (LFileNameSource1, LFileNameDest2)
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
                            LFileSizeDest2 = "new"
                            LFileTimeDest2 = "new"
                            LCopy = True
                        else:
                            LFileSizeDest2 = GetFileSize (LFileNameDest2)
                            LFileTimeDest2 = GetFileTime (LFileNameDest2)
                            if LResult == 1:
                                LCopy = True
                            else:
                                if (LResult == -1) and (_OverwriteNewer == 1):
                                    warnOWN = "More recent dest file " + LFileNameDest2 + " is to be overwritten"
                                    LogAdd ("3", LogFile, "F", _warnOWN, "w+/n")
                                    LCopy = True
                                #endif
                                if (ACheckSize) and (LFileSizeSource1 != LFileSizeDest2):
                                    LCopy = True
                                #endif
                            #endif
                        #endif
                    #endif
                    #--------------------------------------------------------------------
                    # Copy
                    #--------------------------------------------------------------------
                    if LCopy == True:
                        s = LFileNameSource1 + " ("+LFileSizeSource1+"|"+LFileTimeSource1+")" + " => " + \
                            LFileNameDest2   + " ("+LFileSizeDest2+"|"+LFileTimeDest2+")"
                        LogAdd ("3", LogFile, "F", s, "w+/n")

                        # Copy LFileNameSource1 LFileNameDest2 /r /h

                        if _ExecFunc:
                            if _ExecFuncPAR1:
                                s1 = '$$Res = $ExecFunc ($LFileNameSource, $LFileNameDest, $$ExecFuncPAR1)'
                            else:
                                s1 = '$$Res = $ExecFunc ($LFileNameSource, $LFileNameDest)'
                            #endif
                            # ResExe = execute ($s1)
                        #endif
                        if ADestPathDelta:
                            s = s + " => " + LFileNameDestDelta
                            # Copy LFileNameSource1 LFileNameDestDelta2 /r
                        #endif
                    #endif

                    #--------------------------------------------------------------------
                    # Delete
                    #--------------------------------------------------------------------
                    if LDelete:
                        s = "Delete file "+LFileNameSource1 + " ("+LFileSizeSource1+"|"+LFileTimeSource1+")"+" ..."
                        LogAdd ("3", LogFile, "F", s, "w+/n")
                        # Del LFileNameSource1
                    #endif
                #endif
            #endif
        #endfor
    #endwith
#endfunction

#-------------------------------------------------------------------------------
#  ScanDir (ASourcePath, ADestPath, AMask, optional ACheckSize, optional ADestPathDelta, optional $Delete, optional $ExecFunc)
#-------------------------------------------------------------------------------
def ScanDir (ASourcePath, ADestPath, AMask, _ACheckSize, _ADestPathDelta, _Delete, _ExecFunc, _OverwriteNewer, _ExecFuncPAR1):
#beginfunction
    #------------------------------------------------------------
    # Dir
    #------------------------------------------------------------
    LPath = ASourcePath
    LPath = LUFile.ExpandFileName (ASourcePath)
    LPath = os.path.basename (LPath)
    s = '  ' * (GLevel - 1) + LPath
    LULog.LoggerTOOLS_AddLevel (LULog.TEXT, s)

    with os.scandir (ASourcePath) as LFiles:
        for LFile in LFiles:
            Lname = LFile.name
            # print('name:',Lname)
            if (not LFile.is_symlink()):
                if LFile.is_dir ():
                    #------------------------------------------------------------
                    # class os.DirEntry - Это каталог
                    #------------------------------------------------------------
                    LPath = os.path.join (ASourcePath, LFile.name)
                    LPath = LUFile.ExpandFileName (LFile.path)

                    LSourcePath = os.path.join (ASourcePath, LFile.name)
                    LDestPath = os.path.join (ADestPath, LFile)
                    if ADestPathDelta:
                        LDestPathDelta = os.path.join (ADestPathDelta, LFile.name)
                    else:
                        LDestPathDelta = ''
                    #endif
                    #------------------------------------------------------------
                    # список файлов в каталоге
                    #------------------------------------------------------------
                    ScanFile (LSourcePath, LDestPath, AMask, _ACheckSize, LDestPathDelta, _Delete, _ExecFunc, _OverwriteNewer, _ExecFuncPAR1)
                    ScanDir  (LSourcePath, LDestPath, AMask, _ACheckSize, LDestPathDelta, _Delete, _ExecFunc, _OverwriteNewer, _ExecFuncPAR1)
                #endif
            #endif
        #endfor
    #endwith
#endfunction

#-------------------------------------------------------------------------------
#  BacDirs (ASourcePath, ADestPath, ACheckSize)
#-------------------------------------------------------------------------------
def BacDirs (ASourcePath, ADestPath, ACheckSize) -> int:
#beginfunction
    ...
"""
   if LSourcePath = 0
      if IsDeclared (ASourcePath)
         LSourcePath = ASourcePath
      else
         return 1
      #endif
   #endif
   if LDestPath = 0
      if IsDeclared (ADestPath)
         LDestPath = ADestPath
      else
         return 1
      #endif
   #endif
   LMask = "*.*"
   if IsDeclared (ACheckSize)
      LCheckSize = ACheckSize
   else
      LCheckSize = False
   #endif

   LFile = Dir (ASourcePath+"\\"+LMask)
   WHILE @ERROR = 0 AND LFile
      if LFile <> "." AND LFile <> ".."
         if GetFileAttr (ASourcePath + "\\" + LFile) & 16    # is it a directory ?
            LSourcePath = ASourcePath
            LDestPath = ADestPath

            LSourcePath = ASourcePath + "\\" + LFile
            LDestPath = ADestPath + "\\" + LFile

            BacDirs(LSourcePath, LDestPath, ACheckSize)

            ASourcePath = LSaveLSourcePath
            ADestPath = LSaveLDestPath
         else
            LFileNameSource = ASourcePath + "\\" + LFile
            LFileNameDest = ADestPath + "\\" + LFile
            if 0=EXIST(ADestPath)
               MD ADestPath
            #endif
            LCopy = False
            LResult = CompareFileTimes(LFileNameSource, LFileNameDest)
            if $Result = 1 Or LResult = -3
               LCopy = True
            else
               LFileSizeSource = GetFileSize (LFileNameSource)
               LFileSizeDest = GetFileSize (LFileNameDest)
               if (LCheckSize=True) and (LFileSizeSource<>LFileSizeDest)
                  LCopy = True
               #endif
            #endif
            if LCopy = True
               ? LFileNameSource+" => "+LFileNameDest+" ..."
               Copy LFileNameSource LFileNameDest /r
            #endif
         #endif
      #endif
      if @ERROR = 0
         LFile = Dir("")
      #endif
   loop
"""
#endfunction

#-------------------------------------------------------------------------------
#  BacFiles (ASourcePath, ADestPath, AMask, optional ACheckSize, optional ADestPathDelta, optional $Delete, optional $ExecFunc, optional $OverwriteNewer)
#-------------------------------------------------------------------------------
def BacFiles (ASourcePath, ADestPath, AMask, _ACheckSize, _ADestPathDelta, _Delete, _ExecFunc, _OverwriteNewer, _ExecFuncPAR1):
#beginfunction
    ...
"""
   if (ASourcePath <> "") and (ADestPath <> "")
      if $Debug
         LogAdd (Log, LogFile, "I", "BacFiles: "+ASourcePath+" => "+ADestPath+" "+AMask, "w+/n")
      #endif
      ScanFile(ASourcePath, ADestPath, AMask, ACheckSize, ADestPathDelta, $Delete, $ExecFunc, $OverwriteNewer, $ExecFuncPAR1)
      ScanDir (ASourcePath, ADestPath, AMask, ACheckSize, ADestPathDelta, $Delete, $ExecFunc, $OverwriteNewer, $ExecFuncPAR1)
   #endif
"""
#endfunction

#-------------------------------------------------------------------------------
#  BacFile (ASourcePath, ADestPath, AMask, optional ACheckSize, optional ADestPathDelta, optional $Delete, optional $ExecFunc, optional $OverwriteNewer)
#-------------------------------------------------------------------------------
def BacFile (ASourcePath, ADestPath, AMask, _ACheckSize, _ADestPathDelta, _Delete, _ExecFunc, _OverwriteNewer, _ExecFuncPAR1):
#beginfunction
    ...
"""
   if (ASourcePath <> "") and (ADestPath <> "")
      if $Debug
         LogAdd (Log, LogFile, "I", "BacFile: "+ASourcePath+" => "+ADestPath+" "+AMask, "w+/n")
      #endif
      ScanFile(ASourcePath, ADestPath, AMask, ACheckSize, ADestPathDelta, $Delete, $ExecFunc, $OverwriteNewer, $ExecFuncPAR1)
   #endif
"""
#endfunction

#-------------------------------------------------------------------------------
# SyncFile(Array, optional $Delete, optional $OverwriteNewer)
#-------------------------------------------------------------------------------
def SyncFile(Array, _Delete, _OverwriteNewer):
#beginfunction
    ...
"""
   #LogAdd(Log, LogFile, "I", "Array="+UBound(Array))
   for Each $Item in Array
      #LogAdd(Log, LogFile, "I", "Item="+UBound($Item))
      if UBound($Item) > 0
         if ($Item[0] <> "") and ($Item[1] <> "")
            LogAdd(Log, LogFile, "I", $Item[0]+"\\"+$Item[2]+" => "+$Item[1])
            #---------------------------------------
            #
            #---------------------------------------
            if UBound($Item) > 3
               if UCase($Item[3]) = "S"
                  #---------------------------------------
                  # with subdir
                  #---------------------------------------
                  if UBound($Item) > 4
                     BacFiles ($Item[0], $Item[1], $Item[2], True, , 0,  $Item[4], $OverwriteNewer, $Item[5])
                  else
                     BacFiles ($Item[0], $Item[1], $Item[2], True, , 0,  $Item[4], $OverwriteNewer,)
                  #endif
               else                                                             
                  if UBound($Item) > 4
                     BacFile  ($Item[0], $Item[1], $Item[2], True, , 0,  $Item[4], $OverwriteNewer, $Item[5])
                  else
                     BacFile  ($Item[0], $Item[1], $Item[2], True, , 0,  $Item[4], $OverwriteNewer,)
                  #endif
               #endif
            else
               if UCase($Item[3]) = "S"
                  #---------------------------------------
                  # with subdir
                  #---------------------------------------
                  BacFiles ($Item[0], $Item[1], $Item[2], True, , 0, , $OverwriteNewer,)
               else
                  BacFile  ($Item[0], $Item[1], $Item[2], True, , 0, , $OverwriteNewer,)
               #endif
            #endif
      
            #---------------------------------------
            #
            #---------------------------------------
            if $Delete
               LogAdd(Log, LogFile, "I", "Delete ..."+$Item[1]+"\\"+$Item[2]+" "+$Item[0])
               if UCase($Item[3]) = "S"
                  #---------------------------------------
                  # with subdir
                  #---------------------------------------
                  BacFiles ($Item[1], $Item[0], $Item[2], , , 1, , $OverwriteNewer,)
               else
                  BacFile ($Item[1], $Item[0], $Item[2], , , 1, , $OverwriteNewer,)
               #endif
            #endif

         #endif   
      else
         #---------------------------------------------------
         LogAdd(Log, LogFile, "I", $Item)
         #---------------------------------------------------
      #endif
   next
"""
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
    # print (LFileSizeSource)
    LFileTimeSource = LUFile.GetFileDateTime (LFileNameSource)
    # print (LFileTimeSource)
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

                        # LHandleFile = LUFile.OpenTextFile (_OutFile, '')
                        # LHandleFile.write (s+'\n')
                        # LUFile.CloseTextFile (LHandleFile)
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
                    
                    # print(GLevel, _ALevel)
                    # на следующий уровень
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
