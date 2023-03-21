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
import win32api
import platform
import sys
import time

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------
import datetime
import shutil

#------------------------------------------
# БИБЛИОТЕКА LU
#------------------------------------------
import LUErrors
import LUFile
import LUStrDecode

#------------------------------------------
# БИБЛИОТЕКИ python
#------------------------------------------
import os
import win32api
import platform

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------
import datetime
import chardet

#------------------------------------------
# БИБЛИОТЕКИ LU
#------------------------------------------
import LUDateTime

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
#-------------------------------------------------------------------------------
#  BacDirs (ASourcePath, ADestPath, ACheckSize)
#-------------------------------------------------------------------------------
def BacDirs (ASourcePath, ADestPath, ACheckSize) -> int:
#beginfunction
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
#endfunction
"""

"""
#-------------------------------------------------------------------------------
# ScanFile (ASourcePath, ADestPath, AMask, optional ACheckSize, optional ADestPathDelta, optional $Delete, optional $ExecFunc, optional $ExecFuncPAR1, optional $OverwriteNewer)
#-------------------------------------------------------------------------------
def ScanFile (ASourcePath, ADestPath, AMask, optional ACheckSize, optional ADestPathDelta, optional $Delete, optional $ExecFunc, optional $OverwriteNewer, optional $ExecFuncPAR1)
   Dim LResult
#beginfunction
   LFile = Dir (ASourcePath+"\\"+AMask)

   if EXIST(ADestPath)=0
      MD ADestPath
   #endif

   if ADestPathDelta
      if EXIST(ADestPathDelta)=0
         MD ADestPathDelta
      #endif
   #endif

   WHILE (@ERROR = 0) AND LFile

      if LFile <> "." AND LFile <> ".."

         LAttr = GetFileAttr (ASourcePath + "\\" + LFile)

         if $Debug
            LogAdd ("3", LogFile, "F", ASourcePath+"\\"+LFile+"_"+LAttr, "w+/n")
         #endif

         if (LAttr & 16)=0
            LFileNameSource = ASourcePath + "\\" + LFile
            LFileSizeSource = GetFileSize (LFileNameSource)
            LFileTimeSource = GetFileTime (LFileNameSource)
            LFileNameDest   = ADestPath + "\\" + LFile
            if ADestPathDelta
               LFileNameDestDelta = ADestPathDelta + "\\" + LFile
            #endif

            #--------------------------------------------------------------------
            LResult = CompareFileTimes(LFileNameSource, LFileNameDest)
            if $Debug
               LogAdd ("3", LogFile, "F", "LResult="+LResult, "w+/n")
            #endif

            #--------------------------------------------------------------------
            # Check Result
            #--------------------------------------------------------------------
            LCopy = False
            LDelete = False
            if $Delete 
               if LResult = -3
                  LDelete = True
               #endif
            else
               if LResult = -3
                  LFileSizeDest = "new"
                  LFileTimeDest = "new"
                  LCopy = True
               else
                  LFileSizeDest = GetFileSize (LFileNameDest)
                  LFileTimeDest = GetFileTime (LFileNameDest)
                  if LResult = 1 
                     LCopy = True
                  else
                     if (LResult = -1) and ($OverwriteNewer=1) 
                        $warnOWN = "More recent dest file " + LFileNameDest + " is to be overwritten"
                        LogAdd ("3", LogFile, "F", $warnOWN, "w+/n")
                        LCopy = True
                     #endif
                     if (ACheckSize=True) and (LFileSizeSource<>LFileSizeDest)
                        LCopy = True
                     #endif
                  #endif
               #endif
            #endif

            #--------------------------------------------------------------------
            # Copy
            #--------------------------------------------------------------------
            if LCopy = True
               $s = LFileNameSource + " ("+LFileSizeSource+"|"+LFileTimeSource+")" + " => " +
                    LFileNameDest   + " ("+LFileSizeDest+"|"+LFileTimeDest+")"
               LogAdd ("3", LogFile, "F", $s, "w+/n")

               Copy LFileNameSource LFileNameDest /r /h

               if $ExecFunc

                  if $ExecFuncPAR1
                     $s1 = '$$Res = $ExecFunc ($LFileNameSource, $LFileNameDest, $$ExecFuncPAR1)'
                  else
                     $s1 = '$$Res = $ExecFunc ($LFileNameSource, $LFileNameDest)'
                  #endif

                  if $Debug
                     LogAdd (Log, LogFile, "I", $s1)
                  #endif
                  $ResExe = execute ($s1)
               #endif

               if ADestPathDelta
                  $s = $s + " => " + LFileNameDestDelta
                  if $Debug
                     LogAdd ("3", LogFile, "F", $s)
                  #endif
                  Copy LFileNameSource LFileNameDestDelta /r
               #endif
            #endif

            #--------------------------------------------------------------------
            # Delete
            #--------------------------------------------------------------------
            if LDelete = True
               $s = "Delete file "+LFileNameSource + " ("+LFileSizeSource+"|"+LFileTimeSource+")"+" ..."
               LogAdd ("3", LogFile, "F", $s, "w+/n")
               Del LFileNameSource
            #endif

         #endif

      #endif

      if @ERROR = 0

         LFile = Dir("")

         #if $Debug
         #   LogAdd ("3", LogFile, "F", @SERROR+"_"+@ERROR+"_"+LFile+"!", "w+/n")
         ##endif

      #endif

   loop
#endfunction

#-------------------------------------------------------------------------------
#  ScanDir (ASourcePath, ADestPath, AMask, optional ACheckSize, optional ADestPathDelta, optional $Delete, optional $ExecFunc)
#-------------------------------------------------------------------------------
def ScanDir (ASourcePath, ADestPath, AMask, optional ACheckSize, optional ADestPathDelta, optional $Delete, optional $ExecFunc, optional $OverwriteNewer, optional $ExecFuncPAR1)
#beginfunction
   LFile = Dir (ASourcePath+"\*.*")
   WHILE @ERROR = 0 AND LFile
      if LFile <> "." AND LFile <> ".."
         if GetFileAttr (ASourcePath + "\\" + LFile) & 16    # is it a directory ?

            LSourcePath = ASourcePath + "\\" + LFile
            LDestPath = ADestPath + "\\" + LFile
            if ADestPathDelta
               LDestPathDelta = ADestPathDelta + "\\" + LFile
               if $Debug
                  LogAdd ("3", LogFile, "D", LSourcePath+" => "+LDestPath+" "+LDestPathDelta)
               #endif
            else
               LDestPathDelta = ""
            #endif

            ScanFile(LSourcePath, LDestPath, AMask, ACheckSize, LDestPathDelta, $Delete, $ExecFunc, $OverwriteNewer, $ExecFuncPAR1)
            ScanDir(LSourcePath, LDestPath, AMask, ACheckSize, LDestPathDelta, $Delete, $ExecFunc, $OverwriteNewer, $ExecFuncPAR1)
         #endif
      #endif
      if @ERROR = 0
         LFile = Dir("")
      #endif
   loop
#endfunction

#-------------------------------------------------------------------------------
#  BacFiles (ASourcePath, ADestPath, AMask, optional ACheckSize, optional ADestPathDelta, optional $Delete, optional $ExecFunc, optional $OverwriteNewer)
#-------------------------------------------------------------------------------
def BacFiles (ASourcePath, ADestPath, AMask, optional ACheckSize, optional ADestPathDelta, optional $Delete, optional $ExecFunc, optional $OverwriteNewer, optional $ExecFuncPAR1)
#beginfunction
   if (ASourcePath <> "") and (ADestPath <> "")
      if $Debug
         LogAdd (Log, LogFile, "I", "BacFiles: "+ASourcePath+" => "+ADestPath+" "+AMask, "w+/n")
      #endif
      ScanFile(ASourcePath, ADestPath, AMask, ACheckSize, ADestPathDelta, $Delete, $ExecFunc, $OverwriteNewer, $ExecFuncPAR1)
      ScanDir (ASourcePath, ADestPath, AMask, ACheckSize, ADestPathDelta, $Delete, $ExecFunc, $OverwriteNewer, $ExecFuncPAR1)
   #endif
#endfunction

#-------------------------------------------------------------------------------
#  BacFile (ASourcePath, ADestPath, AMask, optional ACheckSize, optional ADestPathDelta, optional $Delete, optional $ExecFunc, optional $OverwriteNewer)
#-------------------------------------------------------------------------------
def BacFile (ASourcePath, ADestPath, AMask, optional ACheckSize, optional ADestPathDelta, optional $Delete, optional $ExecFunc, optional $OverwriteNewer, optional $ExecFuncPAR1)
#beginfunction
   if (ASourcePath <> "") and (ADestPath <> "")
      if $Debug
         LogAdd (Log, LogFile, "I", "BacFile: "+ASourcePath+" => "+ADestPath+" "+AMask, "w+/n")
      #endif
      ScanFile(ASourcePath, ADestPath, AMask, ACheckSize, ADestPathDelta, $Delete, $ExecFunc, $OverwriteNewer, $ExecFuncPAR1)
   #endif
#endfunction

#-------------------------------------------------------------------------------
# SyncFile(Array, optional $Delete, optional $OverwriteNewer)
#-------------------------------------------------------------------------------
def SyncFile(Array, optional $Delete, optional $OverwriteNewer)
#beginfunction
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
#endfunction

#-------------------------------------------------------------------------------
#  DelFile (ASourcePath, AMask, $Day)
#-------------------------------------------------------------------------------
def DelFile (ASourcePath, AMask, $Day)
   Dim LResult
#beginfunction
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
#endfunction

#-------------------------------------------------------------------------------
#  ListFile (ASourcePath, AMask, optional $OutFile, optional $Option, optional FuncFile)
#-------------------------------------------------------------------------------
def ListFile (ASourcePath, AMask, optional $OutFile, optional $Option, optional FuncFile)
   Dim LResult
#beginfunction
   if ($OutFile) and (UCase($OutFile) <> "CONSOLE")
      $HandleFile = FreeFileHandle
      $Res = Open ($HandleFile, $OutFile, 1+4)
   #endif

   LDay = EncodeDate(@Year,@MonthNo,@MDayNo)
   LFile = Dir (ASourcePath+"\\"+AMask)

   WHILE @ERROR = 0 AND LFile
      if LFile <> "." AND LFile <> ".."
         if (GetFileAttr (ASourcePath + "\\" + LFile) & 16)=0
            ListFile = ListFile + 1
            LFileNameSource = ASourcePath + "\\" + LFile
            LFileSizeSource = GetFileSize (LFileNameSource)
            LFileTimeSource = GetFileTime (LFileNameSource)

            if $OutFile
               if UCase($OutFile) = "CONSOLE"
                  select
                     case $Option = 1 or $Option = 11
                        ? LFile
                     case $Option = 2 or $Option = 12
                        ? LFileNameSource+" "+LFileTimeSource+" "+LFileSizeSource
                  endselect
               else
                  select
                     case $Option = 1 or $Option = 11
                        $Res = WriteLine ($HandleFile, LFile+@CRLF)
                     case $Option = 2 or $Option = 12
                        $Res = WriteLine ($HandleFile, LFileNameSource+" "+LFileTimeSource+" "+LFileSizeSource+" "+ListFile+@CRLF)
                  endselect
               #endif
            #endif

            if FuncFile
               $s = '$$Res = FuncFile ($ListFile, $LFileNameSource, $LFileTimeSource, $LFileSizeSource)'
               $ResExe = execute ($s)
            #endif

            #--------------------------------------------------------------------------------
            #$Y = Val(SUBSTR(LFileTimeSource,1,4))
            #$M = Val(SUBSTR(LFileTimeSource,6,2))
            #$D = Val(SUBSTR(LFileTimeSource,9,2))
            #LFileDaySource = EncodeDate($Y,$M,$D)
            #--------------------------------------------------------------------------------

         #endif
      #endif

      if (@ERROR = 0) or (@ERROR = 5)
         LFile = Dir("")
      #endif
   loop

   if ($OutFile) and (UCase($OutFile) <> "CONSOLE")
      $Res = Close ($HandleFile)
   #endif

#endfunction

#-------------------------------------------------------------------------------
#  ListDir (ASourcePath, AMask, optional $OutFile, optional $Option, optional FuncDir, optional FuncFile)
#-------------------------------------------------------------------------------
def ListDir (ASourcePath, AMask, optional $OutFile, optional $Option, optional FuncDir, optional FuncFile)
#beginfunction
   Level = Level + 1
   $DirCount = $DirCount + 1

   # FileCount = ListFile(ASourcePath, AMask, $OutFile, $Option, FuncFile)

   if $Option = 10 or $Option = 11 or $Option = 12
      if ($OutFile) and (UCase($OutFile) <> "CONSOLE")
         $HandleDir = FreeFileHandle
         $Res = Open ($HandleDir, $OutFile, 1+4)
      #endif
      if $OutFile
         if UCase($OutFile) = "CONSOLE"
            ? ASourcePath
         else
            $Res = WriteLine ($HandleDir, ASourcePath+" "+$DirCount+@CRLF)
         #endif
      #endif
      if ($OutFile) and (UCase($OutFile) <> "CONSOLE")
         $Res = Close ($HandleDir)
      #endif
   #endif

   LFile = Dir (ASourcePath+"\*.*")
   WHILE @ERROR = 0 AND LFile
      if LFile <> "." AND LFile <> ".."
         if GetFileAttr (ASourcePath + "\\" + LFile) & 16    # Это каталог....
            LSourcePath = ASourcePath + "\\" + LFile

            FileCount = ListFile(LSourcePath, AMask, $OutFile, $Option, FuncFile)
            if FuncDir
               $s = '$$Res = FuncDir ($$DirCount, $LSourcePath, $FileCount)'
               $ResExe = execute ($s)
            #endif

            ListDir (LSourcePath, AMask, $OutFile, $Option, FuncDir, FuncFile)

            Level = Level - 1
         #endif
      #endif
      if (@ERROR = 0) 
         LFile = Dir("")
      #endif
   loop
#endfunction

#-------------------------------------------------------------------------------
#  DirFile (ASourcePath, AMask, optional $OutFile)
#-------------------------------------------------------------------------------
def DirFile (ASourcePath, AMask, optional $OutFile)
   Dim LResult
#beginfunction
   if $OutFile
      del $OutFile
      $Handle = FreeFileHandle
      Open ($Handle, $OutFile, 1+4)
   #endif
   LDay = EncodeDate(@Year,@MonthNo,@MDayNo)
   LFile = Dir (ASourcePath+"\\"+AMask)
   WHILE @ERROR = 0 AND LFile
      if LFile <> "." AND LFile <> ".."
         if (GetFileAttr (ASourcePath + "\\" + LFile) & 16)=0
            LFileNameSource = ASourcePath + "\\" + LFile
            LFileSizeSource = GetFileSize (LFileNameSource)
            LFileTimeSource = GetFileTime (LFileNameSource)
            if $OutFile
               WriteLine ($Handle, LFile+@CRLF)
            #endif
            # LogAdd ("3", LogFile, "I", LFile)
         #endif
      #endif
      if (@ERROR = 0) or (@ERROR = 5)
         LFile = Dir("")
      #endif
   loop
   if $OutFile
      Close ($Handle)
   #endif
#endfunction

#-------------------------------------------------------------------------------
# Associate($Extension, $Type, $Description, $OCmd, OPTIONAL $ECmd, OPTIONAL AddFlag, OPTIONAL $System)
#-------------------------------------------------------------------------------
def Associate($Extension, $Type, $Description, $OCmd, OPTIONAL $ECmd, OPTIONAL AddFlag, OPTIONAL $System)
#beginfunction
   # make sure the "dot" is specified
   if Left($Extension, 1) <> "."
      $Extension = "." + $Extension
   #endif

   # insure that "$System" has the right format if it's specified
   if $Server <> ""
      if Left($System,2) <> "\\" $System = "\\" + $System #endif
      if Right($System,1) <> "\\" $System = $System + "\\" #endif
   #endif

   # Obtain the Windows System Path value from the target system
   $WSPath = ReadValue($System + "HKEY_Local_Machine\SOFTWARE\Microsoft\Windows NT\CurrentVersion", "SystemRoot")

   # Define the Extension
   $RTN = DelTree($System + "HKEY_CLASSES_ROOT\\" + $Extension)
   $RTN = AddKey($System + "HKEY_CLASSES_ROOT\\" + $Extension)
   $RTN = WriteValue($System + "HKEY_CLASSES_ROOT\\" + $Extension, "", $Type, "REG_SZ")

   # just return if we're adding a new Extension to an existing association
   if AddFlag = 0
      Exit 0
   #endif

   # Create the definitions for the OPEN command
   $RTN = DelTree($System + "HKEY_CLASSES_ROOT\\" + $Type)
   $RTN = AddKey($System + "HKEY_CLASSES_ROOT\\" + $Type)
   $RTN = AddKey($System + "HKEY_CLASSES_ROOT\\" + $Type + "\DefaultIcon")
   $RTN = AddKey($System + "HKEY_CLASSES_ROOT\\" + $Type + "\Shell")
   $RTN = AddKey($System + "HKEY_CLASSES_ROOT\\" + $Type + "\Shell\Open")
   $RTN = AddKey($System + "HKEY_CLASSES_ROOT\\" + $Type + "\Shell\Open\Command")
   
   $RTN = WriteValue($System + "HKEY_CLASSES_ROOT\\" + $Type, "", $Description, "REG_SZ")
   $RTN = WriteValue($System + "HKEY_CLASSES_ROOT\\" + $Type + "\DefaultIcon", "", $WSPath + "\system32\SHELL32.dll,21", "REG_SZ")
   $RTN = WriteValue($System + "HKEY_CLASSES_ROOT\\" + $Type + "\Shell\Open\Command", "", $OCmd, "REG_EXPAND_SZ")

   # Create the association for the EDIT command, if specified
   if $ECmd <> ""
      $RTN = AddKey($System + "HKEY_CLASSES_ROOT\\" + $Type + "\Shell\Edit")
      $RTN = AddKey($System + "HKEY_CLASSES_ROOT\\" + $Type + "\Shell\Edit\Command")
      $RTN = WriteValue($System + "HKEY_CLASSES_ROOT\\" + $Type + "\Shell\Edit\Command", "", $ECmd, "REG_EXPAND_SZ")
   #endif
#endfunction
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
