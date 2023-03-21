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

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------
import shutil

#------------------------------------------
# БИБЛИОТЕКА LU
#------------------------------------------
import LUErrors
import LUStrDecode

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

#------------------------------------------
# БИБЛИОТЕКИ python
#------------------------------------------
import os
import win32api

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------
import datetime
import chardet

#------------------------------------------
# БИБЛИОТЕКИ LU
#------------------------------------------
import LUDateTime

def DirectoryExists (APath: str) -> bool:
    """DirectoryExists """
#beginfunction
    return os.path.isdir(APath)
#endfunction

def ForceDirectories (ADir: str) -> bool:
    """ForceDirectories"""
#beginfunction
    # SCannotCreateDir: str = 'Unable to create directory'
    os.makedirs (ADir, exist_ok = True)
    LResult = DirectoryExists (ADir)
    return LResult
#endfunction

def DirectoryDelete (ADirectoryName: str) -> bool:
    """DirectoryDelete"""
#beginfunction
    LResult = False
    if DirectoryExists (ADirectoryName):
        shutil.rmtree (ADirectoryName)
        LResult = True
    #endif
    return LResult
#endfunction

def FileExists (AFileName: str) -> bool:
    """FileExists"""
#beginfunction
    return os.path.isfile(AFileName)
#endfunction

def GetFileDateTime (AFileName: str) -> ():
    """GetFileDateTime"""
#beginfunction
    LTuple = ()
    if os.path.isfile (AFileName):
        # file modification
        LFileTimeMod: datetime = os.path.getmtime (AFileName)
        # convert timestamp into DateTime object
        LFileTimeMod1: datetime = datetime.datetime.fromtimestamp (LFileTimeMod)
        # file creation
        LFileTimeCreate: datetime = os.path.getctime (AFileName)
        # convert creation timestamp into DateTime object
        LFileTimeCreate1: datetime = datetime.datetime.fromtimestamp (LFileTimeCreate)
        LTuple = (LFileTimeMod1, LFileTimeCreate1)
    #endif
    return LTuple
#endfunction

def GetFileSize (AFileName: str) -> int:
    """GetFileSize"""
#beginfunction
    if FileExists (AFileName):
        return os.path.getsize (AFileName)
    else:
        return 0
    #endif
#endfunction

#--------------------------------------------------------------------------------
# WriteStrToFile (AStr: str, AFileName: str):
#--------------------------------------------------------------------------------
def WriteStrToFile (AStr: str, AFileName: str):
    """WriteStrToFile"""
#beginfunction
    if FileExists(AFileName):
        # Откроет для добавления нового содержимого.
        # Создаст новый файл для чтения записи, если не найдет с указанным именем.
        LEncoding = GetFileEncoding (AFileName)
        if LEncoding == '':
            LEncoding = cDefaultEncoding
        LFile = open (AFileName, 'a+', encoding = LEncoding)
        LFile.write (AStr)
        LFile.flush ()
        LFile.close ()
    else:
        raise LUErrors.LUFileError_FileERROR (AFileName)
    #endif
#endfunction

#--------------------------------------------------------------------------------
# ExpandFileName (APath: str) -> str:
#--------------------------------------------------------------------------------
def ExpandFileName (APath: str) -> str:
    """ExpandFileName"""
#beginfunction
    # LResult = os.path.basename(APath)
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
    return LEncoding
#endfunction

def IncludeTrailingBackslash (APath: str) -> str:
    """IncludeTrailingBackslash"""
#beginfunction
    LResult = APath.rstrip('\\')+'\\'
    LResult = APath.rstrip('/')+'/'
    return LResult
#endfunction

def GetDirNameYYMMDD (ARootDir: str, ADate: datetime) -> str:
    """GetDirNameYYMMDD"""
#beginfunction
    # LYMD = LUDateTime.DecodeDate_ (ADate)
    LYMDStr: str = LUDateTime.DateTimeStr(False, ADate, LUDateTime.cFormatDateTimeYYMMDD)
    LResult = IncludeTrailingBackslash(ARootDir)+LYMDStr
    return LResult
#endfunction

def GetDirNameYYMM (ARootDir: str, ADate: datetime) -> str:
    """GetDirNameYYMM"""
#beginfunction
    LYMDStr: str = LUDateTime.DateTimeStr(False, ADate, LUDateTime.cFormatDateTimeYYMM)
    LResult = IncludeTrailingBackslash(ARootDir)+LYMDStr
    return LResult
#endfunction

def GetTempDir () -> str:
    """GetTempDir"""
#beginfunction
    LResult = win32api.GetTempPath()
    return LResult
#endfunction

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
        L = win32api.SearchPath (None, LResult, None)
        if L[0] != '':
            LResult = L[0]
        else:
            LResult = ''
        #endif
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

def SearchINIFile (AFileName: str) -> str:
    """SearchINIFile"""
#beginfunction
    LResult = SearchFile (AFileName, '.ini')
    return LResult
#endfunction

def SearchEXEFile (AFileName: str) -> str:
    """SearchEXEFile"""
#beginfunction
    LResult = SearchFile (AFileName, '.exe')
    return LResult
#endfunction

def FileSearch (AFileName: str, APath: str) -> str:
    """FileSearch"""
#beginfunction
    try:
        L = win32api.SearchPath (APath, AFileName, None)
        if L [0] != '':
            LResult = L [0]
        else:
            LResult = ''
        #endif
    except:
        LResult = ''
    return LResult
#endfunction

def FileDelete (AFileName: str) -> bool:
    """FileDelete"""
#beginfunction
    LResult = True
    if FileExists (AFileName):
        try:
            # Clear ReadOnly
            # FileSetAttr (FileName, FileGetAttr(FileName) and (faReadOnly xor $FF));
            os.remove (AFileName)
            LResult = True
        except:
            LResult = False
        #endtry
    #endif
    return LResult
#endfunction

#-------------------------------------------------------------------------------
# CreateTextFile
#-------------------------------------------------------------------------------
def CreateTextFile(AFileName: str, AText: str, AEncoding: str):
    """CreateTextFile"""
#beginfunction
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

"""
function FileCopy (const FileName, DestPathName: string; Overwrite: Boolean): Boolean;
{ FileCopy }
function FileCopy (const FileName, DestPathName: string;
    Overwrite: Boolean): Boolean;
var
    FNS, FND: string;
    LDestPathName: string;
begin
    if Trim (DestPathName) = '' then
        LDestPathName := GetCurrentDir
    else
        LDestPathName := ExpandFileName (DestPathName);
    FNS := FileName;
    FND := IncludeTrailingBackslash (LDestPathName) +
        ExtractFileName (FileName);
   { New }
    Result := File2File (FNS, FND, Overwrite);
end;
"""

"""
function FileMove (const FileName, DestPathName: string): Boolean;
{ FileMove }
begin
   { Clear ReadOnly }
    FileSetAttr (FileName, FileGetAttr(FileName) and (faReadOnly xor $FF));
    Result := FileCopy (FileName, DestPathName, True);
    if Result then
        Result := FileDelete (FileName);
end;
"""

"""
function File2File (const FileNameS, FileNameD: string; Overwrite: Boolean): Boolean;
{ File2File }
var
    FNS, FND: string;
    PNS, PND: string;
begin
    PNS := ExtractFilePath (FileNameS);
    PND := ExtractFilePath (FileNameD);
    FNS := FileNameS;
    FND := FileNameD;

    try
        if not DirectoryExists (PND) then
            ForceDirectories (PND);
        if Windows.CopyFile (PChar(FNS), PChar(FND), LongBool(not Overwrite))
        then
        begin
         { Clear ReadOnly }
            FileSetAttr (FND, FileGetAttr(FND) and (faReadOnly xor $FF));
            Result := True;
        end else begin
            Result := False; { Error Copy! }
        end;
    except
        Result := False; { Error Copy! }
    end;
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
