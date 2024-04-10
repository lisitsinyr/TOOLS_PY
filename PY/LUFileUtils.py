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
            if (not LFile1.name.startswith ('.')) and (not LFile1.is_symlink ()):
                if LFile1.is_file ():
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
            if (not LFile.name.startswith('.')) and (not LFile.is_symlink()):
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

    LFileSizeSource = LUFile.GetFileSize (LFileNameSource)
    # print (LFileSizeSource)
    LFileTimeSource = LUFile.GetFileDateTime (LFileNameSource)
    # print (LFileTimeSource)

    #--------------------------------------------------------------------------------
    #LDay = EncodeDate(@Year,@MonthNo,@MDayNo)
    #$Y = Val(SUBSTR(LFileTimeSource,1,4))
    #$M = Val(SUBSTR(LFileTimeSource,6,2))
    #$D = Val(SUBSTR(LFileTimeSource,9,2))
    #LFileDaySource = EncodeDate($Y,$M,$D)
    #--------------------------------------------------------------------------------

    #-------------------------------------------------------------------------
    #file modification
    # LFileTimeSource = os.path.getmtime(LFileNameSource)
    #convert timestamp into DateTime object
    # LFileTimeSource = datetime.datetime.fromtimestamp(LFileTimeSource)
    #file creation
    # LFileTimeSource = os.path.getctime(LFileNameSource)
    #convert creation timestamp into DateTime object
    # LFileTimeSource = datetime.datetime.fromtimestamp(LFileTimeSource)
    #-------------------------------------------------------------------------

    #-------------------------------------------------------------------------
    # if Shablon == Shablon1:
    #     #Shablon1: str = '{FullFileDir} {FileName} {FileTime} {FileSize}'
    #     message = Shablon.format(FullFileDir=LFullFileName,FileName=LFileName,FileTime=LFileTimeSource,FileSize=LFileSize)
    #     print (message)
    # #endif
    # if Shablon == Shablon2:
    #     #Shablon2: str = '{FileName={FullFileName}|{FullFileDir}|{FileDir}'
    #     message = Shablon.format(FileName=LFileName,FullFileName=LFullFileName,FullFileDir=LFullFileName,FileDir=LFileDir)
    #     print (message)
    # #endif
    #-------------------------------------------------------------------------
#endfunction

#-------------------------------------------------------------------------------
# ListFile (ASourcePath, AMask, optional _OutFile, optional _Option, optional _FuncFile)
#-------------------------------------------------------------------------------
def ListFile (ASourcePath, AMask='*.*', _OutFile='', _Option=0, _FuncDir=None, _FuncFile=None):
#beginfunction
    LFileCount = 0
    with os.scandir(ASourcePath) as LFiles:
        for LFile in LFiles:
            if (not LFile.name.startswith ('.')) and (not LFile.is_symlink ()):
                if LFile.is_file():
                    # class os.DirEntry - Это файл
                    LFullFileName = LFile.path
                    Lstats = os.stat (LFullFileName)
                    LFileName = LFile.name
                    s = '  ' * (GLevel - 1) + '   ' + LFileName
                    # LULog.LoggerTOOLS_AddLevel (LULog.TEXT, s)
                    LFileCount = LFileCount + 1

                    if (_OutFile) and (_OutFile.upper == 'CONSOLE'):
                       print (s)
                    #endif
                    if (_OutFile) and (_OutFile.upper != 'CONSOLE'):
                        LHandleFile = LUFile.OpenTextFile (_OutFile, '')
                        LHandleFile.write (s+'\n')
                        LUFile.CloseTextFile (LHandleFile)
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
def ListDir (ASourcePath, AMask, _OutFile='', _Option=0, _FuncDir=None, _FuncFile=None, _ALevel: int=sys.maxsize):
#beginfunction
    global GLevel
    GLevel = GLevel + 1

    #------------------------------------------------------------
    # Dir
    #------------------------------------------------------------
    LPath = ASourcePath
    LPath = LUFile.ExpandFileName (ASourcePath)
    LPath = os.path.basename (LPath)
    s = '  '*(GLevel-1)+LPath
    LULog.LoggerTOOLS_AddLevel (LULog.TEXT, s)

    if _Option == 10 or _Option == 11 or _Option == 12:
        if (_OutFile) and (_OutFile.upper == 'CONSOLE'):
            print (s)
        #endif
        if (_OutFile) and (_OutFile.upper != 'CONSOLE'):
            LHandleDir = LUFile.OpenTextFile(_OutFile, '')
            # LRes = WriteLine ($HandleDir, ASourcePath+" "+$DirCount+@CRLF)
            # LHandleDir.write ('\n'.join (s))
            LHandleDir.write (s+'\n')
            LUFile.CloseTextFile(LHandleDir)
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

            if (not LFile.name.startswith('.')) and (not LFile.is_symlink()):
                if LFile.is_dir ():
                    #------------------------------------------------------------
                    # class os.DirEntry - Это каталог
                    #------------------------------------------------------------
                    LPath = os.path.join (ASourcePath, LFile.name)
                    LPath = LUFile.ExpandFileName (LFile.path)
                    Lstats = os.stat (LFile.path)
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
    if (_OutFile) and (_OutFile.upper != 'CONSOLE'):
        LHandleDir = LUFile.OpenTextFile (_OutFile, '')
    #endif
    with os.scandir (ASourcePath) as LFiles:
        for LFile in LFiles:
            if (not LFile.name.startswith ('.')) and (not LFile.is_symlink ()):
                if LFile.is_file():
                    # class os.DirEntry - Это файл
                    LFullFileName = LFile.path
                    Lstats = os.stat (LFullFileName)
                    LFileName = LFile.name
                    s = LFileName
                    LULog.LoggerTOOLS_AddLevel (LULog.TEXT, s)
                    LFileCount = LFileCount + 1

                    LFileNameSource = LFullFileName
                    LFileSizeSource = LUFile.GetFileSize (LFileNameSource)
                    print(LFileSizeSource)
                    LFileTimeSource = LUFile.GetFileTime (LFileNameSource)
                    print(LFileTimeSource)

                    if (_OutFile) and (_OutFile.upper != 'CONSOLE'):
                        LHandleFile.write (s+'\n')
                    #endif
                #endif
            #endif
        #endfor
    #endwith
    if (_OutFile) and (_OutFile.upper != 'CONSOLE'):
        LUFile.CloseTextFile (LHandleDir)
    #endif
#endfunction

#-------------------------------------------------------------------------------
# DelFiles (ASourcePath, AMask, $Day)
#-------------------------------------------------------------------------------
def DelFiles (ASourcePath, AMask, ADay):
#beginfunction
    ...
"""
   LFile = Dir (ASourcePath+"\\"+AMask)
   L_Day = EncodeDate(@Year,@MonthNo,@MDayNo)
   WHILE @ERROR = 0 AND LFile
      if LFile <> "." AND LFile <> ".."
         if (GetFileAttr (ASourcePath + "\\" + LFile) & 16)=0
            LFileNameSource = ASourcePath + "\\" + LFile
            LFileSizeSource = GetFileSize (LFileNameSource)
            LFileTimeSource = GetFileTime (LFileNameSource)
            $Y = Val(SUBSTR(LFileTimeSource,1,4))
            $M = Val(SUBSTR(LFileTimeSource,6,2))
            $D = Val(SUBSTR(LFileTimeSource,9,2))
            LFileDaySource = EncodeDate($Y,$M,$D)
            LDel = 0
            if ((L_Day-LFileDaySource) => $Day) LDel = 1 #endif
            if LDel
               Del LFileNameSource
               LogAdd ("3", LogFile, "I", "Delete "+LFileNameSource+" "+LFileTimeSource+" Error="+@ERROR+" "+@SError)
            #endif
         #endif
      #endif
      if (@ERROR = 0) or (@ERROR = 5)
         LFile = Dir("")
      #endif
   loop
"""
#endfunction

"""
function BacCopy (const APathSource, APathDest: string; CheckSize, Log: Boolean; Delta: Integer): Boolean;
var
    PS: string;
    PD: string;
    N: string;
    E: string;
    i: Integer;
   { }
    TS: TSearchRec;
    ResTS: Integer;
    FNS: string;
    DTS: TDateTime;
    InfoS: string;
   { }
    TD: TSearchRec;
    FND: string;
    DTD: TDateTime;
    InfoD: string;
    FC: Boolean;
begin
    PS := ExtractFilePath (ExpandFileName(APathSource));
    PD := ExpandFileName (APathDest);
    N := ExtractFileName (APathSource);
    E := ExtractFileExt (APathSource);
    WriteLN (APathSource, ' -> ', APathDest, ' (CheckSize=', CheckSize, ')',
        ' (Log=', Log, ')', ' (Delta=', Delta, ')');
    Result := True;
    try
        ForceDirectories (APathDest);
        FillChar (TS, SizeOf(TS), $00);
        ResTS := FindFirst (IncludeTrailingBackslash(PS) + N, faAnyFile, TS);
        i := 0;
        while (ResTS = 0) do
        begin
            if (TS.Attr and faDirectory) = 0 then
            begin
            { It is File }
            { }
                FNS := IncludeTrailingBackslash (PS) + TS.Name;
                DTS := FileDateToDateTime (TS.Time);
                FND := IncludeTrailingBackslash (PD) + TS.Name;
                if not FileExists (FND) then
                begin
                    InfoD := Format ('%-28s  ',
                        ['----------------------------']);
                    FC := True;
                    InfoD := InfoD + ' N';
                end else begin
                    FillChar (TD, SizeOf(TD), $00);
                    FindFirst (FND, faAnyFile, TD);
                    SysUtils.FindClose (TD);
                    DTD := FileDateToDateTime (TD.Time);
                    InfoD := Format ('%17s %10d  ',
                        [DateTimeToStr(DTD), TD.Size]);
                    FileSetAttr (FND, FileGetAttr(FND) and
                        (faReadOnly xor $FF));
                    FC := False;
                    if ((TS.Time - TD.Time) >= Delta) then
                    begin
                        FC := True;
                        InfoD := InfoD + ' T';
                    end;
                    if CheckSize and (TS.Size <> TD.Size) then
                    begin
                        FC := True;
                        InfoD := InfoD + ' S';
                    end;
                end;

                if FC then
                begin
                    Inc (i);
                    InfoS := Format ('%3d %-12s %17s %10d',
                        [i, TS.Name, DateTimeToStr(DTS), TS.Size]);
                    if Log then
                        WriteLN (InfoS + ' ' + InfoD);
                    if not Windows.CopyFile (PChar(FNS), PChar(FND),
                        LongBool(False)) then
                    begin
                        Result := False;
                        if Log then
                            WriteLN ('Error copy!');
                    end;
                end;
            end;
            ResTS := FindNext (TS);
        end;
        SysUtils.FindClose (TS);
    except
        Result := False;
    end;
end;
"""

"""
function BacCopyS (const APathSource, APathDest: string; CheckSize, Log: Boolean; Delta: Integer): Boolean;
{ BacCopyS }
var
    PS: string;
    PD: string;
    N: string;
    E: string;
    i: Integer;

    procedure Scan (APS, APD, AN: string);
    var
        LTS: TSearchRec;
        LResTS: Integer;
        LFND: string;
        LFNS: string;
        LDTS: TDateTime;
        LTD: TSearchRec;
        LDTD: TDateTime;
        LInfoD: string;
        LInfoS: string;
        LFC: Boolean;
    begin
        FillChar (LTS, SizeOf(LTS), $00);
        LResTS := FindFirst (IncludeTrailingBackslash(APS) + AN,
            faAnyFile, LTS);
        while (LResTS = 0) do
        begin
            if (LTS.Attr and faDirectory) = 0 then
            begin
            { Это файл }
                LFNS := IncludeTrailingBackslash (APS) + LTS.Name;
                LDTS := FileDateToDateTime (LTS.Time);

                LFND := IncludeTrailingBackslash (APD) + LTS.Name;
                if not FileExists (LFND) then
                begin
                    LInfoD := Format ('%-28s  ',
                        ['----------------------------']);
                    LInfoD := LInfoD + ' N';
                    LFC := True;
                end else begin
                    FillChar (LTD, SizeOf(LTD), $00);
                    FindFirst (LFND, faAnyFile, LTD);
                    SysUtils.FindClose (LTD);
                    LDTD := FileDateToDateTime (LTD.Time);
                    LInfoD := Format ('%17s %10d  ',
                        [DateTimeToStr(LDTD), LTD.Size]);
                    FileSetAttr (LFND, FileGetAttr(LFND) and
                        (faReadOnly xor $FF));
                    LFC := False;
                    if ((LTS.Time - LTD.Time) >= Delta) then
                    begin
                        LInfoD := LInfoD + ' T';
                        LFC := True;
                    end;
                    if CheckSize and (LTS.Size <> LTD.Size) then
                    begin
                        LInfoD := LInfoD + ' S';
                        LFC := True;
                    end;
                end;
                if LFC then
                begin
                    Inc (i);
                    LInfoS := Format ('%3d %-12s %17s %10d',
                        [i, LTS.Name, DateTimeToStr(LDTS), LTS.Size]);
                    if Log then
                        WriteLN (LInfoS + ' ' + LInfoD);
                    if not Windows.CopyFile (PChar(LFNS), PChar(LFND),
                        LongBool(False)) then
                    begin
                        if Log then
                            WriteLN ('Error copy!');
                    end;
                end;
            end else begin
            { Это каталог }
                if (LTS.Name <> '.') and (LTS.Name <> '..') then
                begin
                    ForceDirectories (IncludeTrailingBackslash(APD) + LTS.Name);
                    Scan (IncludeTrailingBackslash(APS) + LTS.Name,
                        IncludeTrailingBackslash(APD) + LTS.Name, AN);
                end;
            end;
            LResTS := FindNext (LTS);
        end;
        SysUtils.FindClose (LTS);
    end;

    procedure ScanFile (APS, APD, AN: string);
    var
        LTS: TSearchRec;
        LResTS: Integer;
        LFND: string;
        LFNS: string;
        LDTS: TDateTime;
        LTD: TSearchRec;
        LDTD: TDateTime;
        LInfoD: string;
        LInfoS: string;
        LFC: Boolean;
    begin
        FillChar (LTS, SizeOf(LTS), $00);
        LResTS := FindFirst (IncludeTrailingBackslash(APS) + AN,
            faAnyFile, LTS);
        while (LResTS = 0) do
        begin
            if (LTS.Attr and faDirectory) = 0 then
            begin
            { Это файл }
                LFNS := IncludeTrailingBackslash (APS) + LTS.Name;
                LDTS := FileDateToDateTime (LTS.Time);

                LFND := IncludeTrailingBackslash (APD) + LTS.Name;
                if not FileExists (LFND) then
                begin
                    LInfoD := Format ('%-28s  ',
                        ['----------------------------']);
                    LInfoD := LInfoD + ' N';
                    LFC := True;
                end else begin
                    FillChar (LTD, SizeOf(LTD), $00);
                    FindFirst (LFND, faAnyFile, LTD);
                    SysUtils.FindClose (LTD);
                    LDTD := FileDateToDateTime (LTD.Time);
                    LInfoD := Format ('%17s %10d  ',
                        [DateTimeToStr(LDTD), LTD.Size]);
                    FileSetAttr (LFND, FileGetAttr(LFND) and
                        (faReadOnly xor $FF));
                    LFC := False;
                    if ((LTS.Time - LTD.Time) >= Delta) then
                    begin
                        LInfoD := LInfoD + ' T';
                        LFC := True;
                    end;
                    if CheckSize and (LTS.Size <> LTD.Size) then
                    begin
                        LInfoD := LInfoD + ' S';
                        LFC := True;
                    end;
                end;
                if LFC then
                begin
                    ForceDirectories (IncludeTrailingBackslash(APD));
                    Inc (i);
                    LInfoS := Format ('%3d %-12s %17s %10d',
                        [i, LTS.Name, DateTimeToStr(LDTS), LTS.Size]);
                    if Log then
                        WriteLN (LInfoS + ' ' + LInfoD);
                    if not Windows.CopyFile (PChar(LFNS), PChar(LFND),
                        LongBool(False)) then
                    begin
                        if Log then
                            WriteLN ('Error copy!');
                    end;
                end;
            end else begin
            { Это каталог }
            end;
            LResTS := FindNext (LTS);
        end;
        SysUtils.FindClose (LTS);
    end;

    procedure ScanDir (APS, APD, AN: string);
    var
        LSR: TSearchRec;
        LFound: Integer;
    begin
        LFound := FindFirst (IncludeTrailingBackslash(APS) + '*.*',
            faAnyFile, LSR);
        while (LFound = 0) do
        begin
            if (LSR.Name <> '.') and (LSR.Name <> '..') then
            begin
                if (LSR.Attr and faDirectory) <> 0 then
                begin
               { It is Directory }
                    if AN <> '' then
                        ScanFile (IncludeTrailingBackslash(APS) + LSR.Name,
                            IncludeTrailingBackslash(APD) + LSR.Name, AN);
                    ScanDir (IncludeTrailingBackslash(APS) + LSR.Name,
                        IncludeTrailingBackslash(APD) + LSR.Name, AN);
                end;
            end;
            LFound := FindNext (LSR);
        end;
        SysUtils.FindClose (LSR);
    end;

begin
    PS := ExtractFilePath (ExpandFileName(APathSource));
    PD := ExpandFileName (APathDest);
    N := ExtractFileName (APathSource);
    E := ExtractFileExt (APathSource);
    WriteLN (PS, ' -> ', PD, ' (CheckSize=', CheckSize, ')', ' (Log=', Log, ')',
        ' (Delta=', Delta, ')');
    ForceDirectories (PD);
    i := 0;
    ScanDir (PS, PD, N);
    if N <> '' then
        ScanFile (IncludeTrailingBackslash(PS),
            IncludeTrailingBackslash(PD), N);
    Result := True;
end;
"""

"""
function CheckFile (const APathSource, APathDest: string; Delete, Log: Boolean): Boolean;
{ CheckFile }
var
    PS: string;
    PD: string;
    N: string;
    E: string;
    i: Integer;

    procedure ScanFile (APS, APD, AN: string);
    var
        LTS: TSearchRec;
        LResTS: Integer;
        LFND: string;
        LFNS: string;
        LInfoS: string;
    begin
        FillChar (LTS, SizeOf(LTS), $00);
        LResTS := FindFirst (IncludeTrailingBackslash(APS) + AN,
            faAnyFile, LTS);
        while (LResTS = 0) do
        begin
            if (LTS.Attr and faDirectory) = 0 then
            begin
            { Это файл }
                LFNS := IncludeTrailingBackslash (APS) + LTS.Name;
                FileDateToDateTime (LTS.Time);
                LFND := IncludeTrailingBackslash (APD) + LTS.Name;
                if not FileExists (LFND) then
                begin
                    Inc (i);
                    LInfoS := Format ('%3d %-12s %10d',
                        [i, LTS.Name, LTS.Size]);
                    if Log then
                        WriteLN (LInfoS);
                    if Delete then
                        FileDelete (LFNS);
                end;
            end;
            LResTS := FindNext (LTS);
        end;
        SysUtils.FindClose (LTS);
    end;

    procedure ScanDir (APS, APD, AN: string);
    var
        LSR: TSearchRec;
        LFound: Integer;
    begin
        LFound := FindFirst (IncludeTrailingBackslash(APS) + '*.*',
            faAnyFile, LSR);
        while (LFound = 0) do
        begin
            if (LSR.Name <> '.') and (LSR.Name <> '..') then
            begin
                if (LSR.Attr and faDirectory) <> 0 then
                begin
               { It is Directory }
                    if AN <> '' then
                        ScanFile (IncludeTrailingBackslash(APS) + LSR.Name,
                            IncludeTrailingBackslash(APD) + LSR.Name, AN);
                    ScanDir (IncludeTrailingBackslash(APS) + LSR.Name,
                        IncludeTrailingBackslash(APD) + LSR.Name, AN);
                end;
            end;
            LFound := FindNext (LSR);
        end;
        SysUtils.FindClose (LSR);
    end;

begin
    PS := ExtractFilePath (ExpandFileName(APathSource));
    PD := ExpandFileName (APathDest);
    N := ExtractFileName (APathSource);
    E := ExtractFileExt (APathSource);
    WriteLN (PS, ' -> ', PD, ' (Delete=', Delete, ')', ' (Log=', Log, ')');
    i := 0;
    ScanDir (PS, PD, N);
    if N <> '' then
        ScanFile (IncludeTrailingBackslash(PS),
            IncludeTrailingBackslash(PD), N);
    Result := True;
end;
"""

"""
procedure CorectFile (const FileName: string; Off: DWORD; Len: Integer; var AData);
var
    F: file;
    Size, Blocks: Integer;
    buffer: Pointer;
type
    ArrayOfByte = array [0 .. 0] of Byte;
begin
    try
        AssignFile (F, FileName);
        Reset (F, 1);
        Size := FileSize (F);
        GetMem (buffer, Size + 1);
        if IOResult = 0 then
        begin
            BlockRead (F, buffer^, Size, Blocks);
            CloseFile (F);
            AssignFile (F, FileName);
            Rewrite (F, 1);
            Move (AData, ArrayOfByte(buffer^)[Off], Len);
            BlockWrite (F, buffer^, Size, Blocks);
            CloseFile (F);
        end;
    finally
        FreeMem (buffer);
    end;
end;
"""

"""
function CheckDestFileName (const FileName, DestPath: string; NLimit: Integer): string;
{ CheckDestFileName }
var
    LFileName: string;
    LDirName: string;
    LPathName: string;
    i: Integer;
    LN: Integer;
begin
    LN := Length (IntToStr(NLimit));
    LFileName := ExtractFileName (FileName);
    LDirName := DestPath;
    LPathName := IncludeTrailingBackslash (LDirName) +
        FileNameWithoutExt (LFileName) + ExtractFileExt (LFileName);
    if (FileExists(LPathName)) then
    begin
        i := 0;
        while (FileExists(LPathName)) and (i < NLimit) do
        begin
            Inc (i);
            LPathName := IncludeTrailingBackslash (LDirName) +
                FileNameWithoutExt (LFileName) + '~' +
                AddChar ('0', IntToStr(i), LN) + ExtractFileExt (LFileName);
        end;
    end;
    Result := LPathName;
end;
"""

"""
{ FileLink }
const
    IID_IPersistFile: TGUID = (D1: $0000010B; D2: $0000; D3: $0000;
        D4: ($C0, $00, $00, $00, $00, $00, $00, $46));
"""

"""
procedure FileLink (const FileName, Arg, DisplayName, Folder: string);
var
    ShellLink: IShellLink;
    PersistFile: IPersistFile;
    FileDestPath: string;
    FileNameW: array [0 .. MAX_PATH] of WideChar;
begin
    CoInitialize (nil);
    try
        OleCheck (CoCreateInstance(CLSID_ShellLink, nil, CLSCTX_SERVER,
            IID_IShellLinkA, ShellLink));
        try
            OleCheck (ShellLink.QueryInterface(IID_IPersistFile, PersistFile));
            try
                FileDestPath := Folder + '\' + DisplayName + '.lnk';
                ShellLink.SetPath (PChar(FileName));
                ShellLink.SetIconLocation (PChar(FileName), 0);
                ShellLink.SetWorkingDirectory
                    (PChar(ExtractFilePath(FileName)));
                ShellLink.SetArguments (PChar(Arg));
                MultiByteToWideChar (CP_ACP, 0, PAnsiChar(FileDestPath), - 1,
                    FileNameW, MAX_PATH);
                OleCheck (PersistFile.Save(FileNameW, True));
            finally
                PersistFile := nil;
            end;
        finally
            ShellLink := nil;
        end;
    finally
        CoUninitialize;
    end;
end;
"""

"""
function CreateFileLink (const FileName, Arg, WorkPath, IconFile, Name, DestPath: string): string;
{ CreateFileLink }
var
    LShellLink: IShellLink;
    LPersistFile: IPersistFile;
    LFileDestPath: string;
    LFileNameW: array [0 .. MAX_PATH] of WideChar;
    LDescription: string;
    LFileExt: string;
    LFileNameS: string;
begin
    Result := '';
    CoInitialize (nil);
    try
        OleCheck (CoCreateInstance(CLSID_ShellLink, nil, CLSCTX_SERVER,
            IID_IShellLinkA, LShellLink));
        try
            OleCheck (LShellLink.QueryInterface(IID_IPersistFile,
                LPersistFile));
            try
                LFileExt := ExtractFileExt (FileName);
                if (UpperCase(LFileExt) = '.BAT') then
                begin
                    if IsNT then
                        LFileDestPath := DestPath + '\' + name + '.lnk'
                    else
                        LFileDestPath := DestPath + '\' + name + '.pif';
                end else if (UpperCase(LFileExt) = '.EXE') then
                begin
                    if IsNT then
                        LFileDestPath := DestPath + '\' + name + '.lnk'
                    else
                        LFileDestPath := DestPath + '\' + name + '.pif';
                end else begin
                    if IsNT then
                        LFileDestPath := DestPath + '\' + name + '.lnk'
                    else
                        LFileDestPath := DestPath + '\' + name + '.pif';
                end;

                LShellLink.SetPath (PChar(FileName));
                LShellLink.SetIconLocation (PChar(IconFile), 0);
                LShellLink.SetWorkingDirectory (PChar(WorkPath));
                LShellLink.SetArguments (PChar(Arg));
                LShellLink.SetDescription (PChar(LDescription));
                MultiByteToWideChar (CP_ACP, 0, PAnsiChar(LFileDestPath), - 1,
                    LFileNameW, MAX_PATH);
                OleCheck (LPersistFile.Save(LFileNameW, True));

                if IsNT then
                begin
                    SetLength (LFileNameS, MAX_PATH * 2 + 1);
               { ????OleCheck(LPersistFile.GetCurFile(PWideChar(LFileNameS))); }
                    Result := WideCharToStr (PWideChar(LFileNameS), 0);
                end else begin
                    Result := LFileDestPath;
                end;

            finally
                LPersistFile := nil;
            end;
        finally
            LShellLink := nil;
        end;
    finally
        CoUninitialize;
    end;
end;
"""

"""
#----------------------------------------------------------------------------
# CreateLink ($CommandLine, $Name, $IconFile, $IconIndex, $WorkDir, $Minimize, $Replace, $RunInOwnSpace)
#----------------------------------------------------------------------------
#  $Minimize      = [0,1]   
#  $Replace       = [0,1]   
#  $RunInOwnSpace = [0,1]   
#----------------------------------------------------------------------------
def CreateLink ($CommandLine, $Name, $IconFile, $IconIndex, $WorkDir, $Minimize, $Replace, $RunInOwnSpace)
#beginfunction
   $CreateLink = AddProgramItem ($CommandLine, $Name, $IconFile, $IconIndex, $WorkDir, $Minimize, $Replace, $RunInOwnSpace)
#endfunction
"""

"""
#----------------------------------------------------------------------------
# CreateLinkLU (Links, $DestPath, $name, $targetpath, optional Arguments, optional $startdir, optional $iconpath, optional $style, optional $description)
#----------------------------------------------------------------------------
def CreateLinkLU(Links, $DestPath, $name, $targetpath, optional Arguments, optional $startdir, optional $iconpath, optional $style, optional $description)
#beginfunction
   $s = 'Links -f "$targetpath" -a "Arguments" -w "$startdir" -i "$iconpath" -d "$DestPath" -n "$Name"'
   # ? $s
   Shell $s
   $CreateLinkLU = 0
#endfunction
"""

"""
#---------------------------------------------------------------------------------
# wshShortCut($shortcutname,$targetpath,optional Arguments, optional $startdir, optional $iconpath, optional $style, optional $description)
#---------------------------------------------------------------------------------
def wshShortCut($shortcutname, $CommandFile, optional Arguments, optional $startdir, optional $iconpath, optional $style, optional $description)
   dim $shell, $desktop, $shortcut, $index, $iconinfo, $iconindex, $scdir, $pif
#beginfunction
   $shell = createobject("wscript.shell")
   $wshshortcut=""
   if $shell
      if ucase(right($shortcutname,4))=".URL" or ucase(right($shortcutname,4))=".LNK"
         #do nothing
      else
         if ucase(left($CommandFile,5))="HTTP:" or ucase(left($CommandFile,6))="HTTPS:" or ucase(left($CommandFile,4))="FTP:"
            $shortcutname=$shortcutname + ".url"
         else
            $shortcutname=$shortcutname + ".lnk"
         #endif
      #endif

      if instr($shortcutname,".lnk") and not exist($CommandFile)
         exit 2
      #endif

      if instr($shortcutname,"\\")=0
         $Desktop = $shell.SpecialFolders("Desktop")
         $shortcutname=$desktop + "\\" + $shortcutname
      else
         $scdir=substr($shortcutname,1,instrrev($shortcutname,"\\"))
         if not exist($scdir)
            md $scdir
            if @error
               exit @error
            #endif
         #endif
      #endif

      select
         case (@ProductType = "Windows 98") or (@ProductType = "Windows 95")
            if instr($shortcutname,".lnk")
               $pif=substr($shortcutname,1,instrrev($shortcutname,".lnk")-1)+".pif"
               if Exist ($pif)
                  Del ($pif)
               #endif 
            #endif
         case 1
            if Exist ($shortcutname)
               Del ($shortcutname)
            #endif 
      EndSelect

      $shortcut = $shell.createshortcut($shortcutname)
      if $shortcut
         $shortcut.targetpath = $CommandFile
         if $iconpath
            $shortcut.iconlocation = $iconpath
         #endif
         if Arguments
            $shortcut.arguments = Arguments
         #endif
         if $startdir
            $shortcut.workingdirectory = $startdir
         #endif
         if $style
            $shortcut.windowstyle = $style
         else
            $shortcut.windowstyle = 1
         #endif
         if $description
            $shortcut.description = $description
         else
            $shortcut.description = ""
         #endif
         $shortcut.save
         if @error
            exit @error
         #endif
         if instrrev($shortcutname,".url") and $iconpath
            $index=instrrev($iconpath,",")
            if $index=0
               $iconindex=0
            else
               $iconindex=split($iconpath,",")[1]
               $iconpath=split($iconpath,",")[0]
            #endif
            $=writeprofilestring($shortcutname,"InternetShortcut","IconFile",$iconpath)
            $=writeprofilestring($shortcutname,"InternetShortcut","IconIndex",$iconindex)
         else
         #endif
         #$wshshortcut=$shortcut.FullName
         $wshshortcut = 0
         $shortcut = 0
      else
         exit @error
      #endif 
   else
      exit @error
   #endif 
#endfunction 

"""

"""
function GetFileOwner (FileName: string; var Domain, Username: string): Boolean;
{ GetFileOwner(FileName }
var
    SecDescr: PSecurityDescriptor;
    SizeNeeded, SizeNeeded2: DWORD;
    OwnerSID: PSID;
    OwnerDefault: BOOL;
    OwnerName, DomainName: PChar;
    OwnerType: SID_NAME_USE;
begin
    Result := False;
    GetMem (SecDescr, 1024);
    GetMem (OwnerSID, SizeOf(PSID));
    GetMem (OwnerName, 1024);
    GetMem (DomainName, 1024);
    try
        if not GetFileSecurity (PChar(FileName), OWNER_SECURITY_INFORMATION,
            SecDescr, 1024, SizeNeeded) then
            Exit;
        if not GetSecurityDescriptorOwner (SecDescr, OwnerSID, OwnerDefault)
        then
            Exit;
        SizeNeeded := 1024;
        SizeNeeded2 := 1024;
        if not LookupAccountSid (nil, OwnerSID, OwnerName, SizeNeeded,
            DomainName, SizeNeeded2, OwnerType) then
            Exit;
        Domain := DomainName;
        Username := OwnerName;
    finally
        FreeMem (SecDescr);
        FreeMem (OwnerName);
        FreeMem (DomainName);
    end;
    Result := True;
end;
"""

"""
function GetFileOwner_02 (const FileName: string; var Domain, Username: string)
    : Boolean; overload;
var
    SecDescr: PSecurityDescriptor;
    SizeNeeded, SizeNeeded2: DWORD;
    OwnerSID: PSID;
    OwnerDefault: BOOL;
    OwnerName, DomainName: PChar;
    OwnerType: SID_NAME_USE;
begin
   // result := false;
    GetMem (SecDescr, 1024);
    GetMem (OwnerSID, SizeOf(PSID));
    GetMem (OwnerName, 1024);
    GetMem (DomainName, 1024);
    try
        Result := GetFileSecurity (PChar(FileName), OWNER_SECURITY_INFORMATION,
            SecDescr, 1024, SizeNeeded);
        if not Result then
            Exit;
        Result := GetSecurityDescriptorOwner (SecDescr, OwnerSID, OwnerDefault);
        if not Result then
            Exit;
        SizeNeeded := 1024;
        SizeNeeded2 := 1024;
        Result := LookupAccountSid (nil, OwnerSID, OwnerName, SizeNeeded,
            DomainName, SizeNeeded2, OwnerType);
        if not Result then
            Exit;
        Domain := DomainName;
        Username := OwnerName;
    finally
        FreeMem (SecDescr);
        FreeMem (OwnerName);
        FreeMem (DomainName);
    end;
    Result := True;
end;
"""

"""
function GetFileOwner_02 (const FileName: string): string; overload;
var
    Domain, User: string;
begin
    if GetFileOwner (FileName, Domain, User) then
        Result := Domain + '\' + User
    else
        Result := '<error>';
end;
"""

"""
function SetFileOwner (FileName: string; const Domain, Username: string): Boolean;
{ SetFileOwner(FileName }
var
    SecDescr: PSecurityDescriptor;
    SizeNeeded, SizeNeeded2: DWORD;
    OwnerSID: PSID;
    OwnerDefault: BOOL;
    OwnerName, DomainName: PChar;
    OwnerType: SID_NAME_USE;
   // SecurityInformation: SECURITY_INFORMATION;
begin
    Result := False;
    GetMem (SecDescr, 1024);
    GetMem (OwnerSID, SizeOf(PSID));
    GetMem (OwnerName, 1024);
    GetMem (DomainName, 1024);
    try
        if not GetFileSecurity (PChar(FileName), OWNER_SECURITY_INFORMATION,
            SecDescr, 1024, SizeNeeded) then
            Exit;
        if not GetSecurityDescriptorOwner (SecDescr, OwnerSID, OwnerDefault)
        then
            Exit;
        SizeNeeded := 1024;
        SizeNeeded2 := 1024;
        if not LookupAccountSid (nil, OwnerSID, OwnerName, SizeNeeded,
            DomainName, SizeNeeded2, OwnerType) then
            Exit;
    finally
        FreeMem (SecDescr);
        FreeMem (OwnerName);
        FreeMem (DomainName);
    end;
    Result := True;
end;
"""

"""
function SetFileOwner_02 (const FileName: string; const Domain, Username: string): Boolean; overload;
var
    sd: PSecurityDescriptor;
    OwnerSID: PSID;
begin
    Result := GetUserSID_02 (Domain, Username, OwnerSID);
    if not Result then
        Exit;
    GetMem (sd, 1024);
    try
        Result := InitializeSecurityDescriptor (sd,
            SECURITY_DESCRIPTOR_REVISION);
        Result := Result and SetSecurityDescriptorOwner (sd, OwnerSID,
            True{ ? });
        Result := Result and SetFileSecurity (PChar(FileName),
            OWNER_SECURITY_INFORMATION, sd);
    finally
        FreeMem (sd);
    end;
end;
"""

"""
function SetFileOwner_02 (const FileName: string; Username: string) : Boolean; overload;
var
    Domain: string;
begin
    DivideUserName_02 (Username, Domain, Username);
    Result := SetFileOwner_02 (FileName, Domain, Username);
end;
"""

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
