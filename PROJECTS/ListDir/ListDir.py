#=======================================================================================
#ListDir.py
#python.exe ListDir.py "PYDir=%PYDIR%" "Format=%1" "NLevel=%2"
#=======================================================================================

#------------------------------------------
#БИБЛИОТЕКИ
#------------------------------------------
import argparse
import datetime
#------------------------------------------
#БИБЛИОТЕКИ python
#------------------------------------------
import os
import sys

#------------------------------------------
# Разбор аргументов
#------------------------------------------
parser = argparse.ArgumentParser(description='Параметры')
parser.add_argument('-PYDir', type=str, nargs='?', default='', dest='PYDir', help='Библиотека')
parser.add_argument('-Format', type=int, nargs='?', default=-1, dest='Format', help='Номер шаблона')
parser.add_argument('-NLevel', type=int, nargs='?', default=-1, dest='NLevel', help='Уровень')
args = parser.parse_args()
print('-PYDir  = '+args.PYDir)
print('-Format =',args.Format)
print('-NLevel =',args.NLevel)
#------------------------------------------
PYDir = 'D:\\PROJECTS_LYR\\CHECK_LIST\\05_DESKTOP\\02_Python\\PROJECTS_PY\\TOOLS_PY\\PY'
if args.PYDir != "":
    PYDir = args.PYDir
#endif
sys.path.append(PYDir)
print(PYDir)
print(sys.path)
#------------------------------------------
Format: int = 0
if args.Format != -1:
    Format = args.Format
#endif
#------------------------------------------
NLevel: int = 1
if args.NLevel != -1:
    NLevel = args.NLevel
#endif
if NLevel is None:
    NLevel = 0
#endif
#------------------------------------------

#------------------------------------------
#БИБЛИОТЕКА LU
#------------------------------------------
import LUConst
import LUStrings
import LUSupport
#------------------------------------------

#------------------------------------------
#CONST
#------------------------------------------
Level: int = 0
Mask: str = "*.*"
Log: str = ""
#------------------------------------------
DirName: str = ""
Shablon: str = ""
Shablon0: str = 'call arjd.bat \"{DirName}\"'
Shablon1: str = "{FullFileDir} {FileName} {FileTime} {FileSize}"
Shablon2: str = "{FileName={FullFileName}|{FullFileDir}|{FileDir}"
#------------------------------------------

def GetFileName (AFileSpec: str):
    pass
    # LGetFileName = AFileSpec
    # bash = instrRev (AFileSpec, "\\")
    # if bash or instrRev (AFileSpec, "."):
    #  GetFileName = substr (AFileSpec, bash+1)
    # endif
#endfunction

# -------------------------------------------------------------------------------
# WorkFile (AFile_path)
# -------------------------------------------------------------------------------
def WorkFile (AFile_path):
    global Shablon
#beginfunction
    LFileNameSource: str = AFile_path
    LFullFileName: str = LFileNameSource
    LFileName: str = os.path.basename(LFullFileName)
    LFileSize: int = os.path.getsize(LFullFileName)
    LFileDir: str = os.path.dirname(LFullFileName)

    #-------------------------------------------------------------------------
    #LFileTimeSource = GetFileTime(LFileNameSource)
    #-------------------------------------------------------------------------
    #file modification
    LFileTimeSource = os.path.getmtime(LFileNameSource)
    #convert timestamp into DateTime object
    LFileTimeSource = datetime.datetime.fromtimestamp(LFileTimeSource)
    #file creation
    LFileTimeSource = os.path.getctime(LFileNameSource)
    #convert creation timestamp into DateTime object
    LFileTimeSource = datetime.datetime.fromtimestamp(LFileTimeSource)

    #-------------------------------------------------------------------------
    if Shablon == Shablon1:
        #Shablon1: str = '{FullFileDir} {FileName} {FileTime} {FileSize}'
        message = Shablon.format(FullFileDir=LFullFileName,FileName=LFileName,FileTime=LFileTimeSource,FileSize=LFileSize)
        print (message)
    #endif
    if Shablon == Shablon2:
        #Shablon2: str = '{FileName={FullFileName}|{FullFileDir}|{FileDir}'
        message = Shablon.format(FileName=LFileName,FullFileName=LFullFileName,FullFileDir=LFullFileName,FileDir=LFileDir)
        print (message)
    #endif
#endfunction

#-------------------------------------------------------------------------------
# ListFile (ASourcePath, AMask)
#-------------------------------------------------------------------------------
def ListFile (ASourcePath, AMask):
#beginfunction
    LFiles: LListFiles [str] = os.listdir (ASourcePath)
    for LFile in LFiles:
        LSourcePath = os.sep.join ([ASourcePath, LFile])
        if os.path.isfile (LSourcePath):
            #Это файл
            #Lstats = os.stat (LSourcePath)
            WorkFile (LSourcePath)
        #endif
    #endfor
#endfunction

#-------------------------------------------------------------------------------
# ListDir (ASourcePath, AMask)
#-------------------------------------------------------------------------------
def ListDir (ASourcePath, AMask):
    global Level
#beginfunction
    Level = Level + 1
    #------------------------------------------------------------
    # Dir
    #------------------------------------------------------------
    #DirName = GetFileName(ASourcePath)
    LDirName = os.path.basename (ASourcePath)
    LFullDirName = ASourcePath
    if Level > NLevel:
        if Shablon == Shablon0:
            message = Shablon.format (DirName=LDirName)
            print (1,message)
        #endif
    #endif
    LFiles: LListFiles[str] = os.listdir (ASourcePath)
    for LFile in LFiles:
        LSourcePath = os.sep.join ([ASourcePath, LFile])
        #Lstats = os.stat (LSourcePath)
        if os.path.isdir (LSourcePath):
            #Это каталог
            ListFile (LSourcePath, AMask)
            #WorkFile(LSourcePath)
            #--------------------------------------------------------
            #if Shablon == Shablon0:
            #    message = Shablon.format(DirName=LFile)
            #    print(2,message)
            ##endif
            #--------------------------------------------------------
            if NLevel >= Level:
                ListDir (LSourcePath, AMask)
            #endif
        #endif
    #endfor
    Level = Level - 1
#endfunction

def main():
#beginfunction
    global Log
    global Shablon
    print (LUConst.Userid)
    print ("Кодировка")
    Dir = 'D:\\PROJECTS_LYR\\CHECK_LIST\\05_DESKTOP\\02_Python\\PROJECTS_PY\\TOOLS_PY'
    Dir = os.getcwd()
    match Format:
        case 1:
            Log = 'sfile.ini'
            Shablon = Shablon1
        case 2:
            Log = 'sfile.ini'
            Shablon = Shablon2
        case _:
            Log = 'sdir.bat'
            Shablon = Shablon0
    #endmatch
    print ('PYDir   = '+PYDir)
    print ('Log     = '+Log)
    print ('Dir     = '+Dir)
    print ('Format  = ',Format)
    print ('NLevel  = ',NLevel)
    print ('Mask    = '+Mask)
    print ('Shablon = '+Shablon)
    ListDir (Dir, Mask)
#endfunction

#------------------------------------------
# Делаем изменение в первом branch
# Делаем изменение в первом branch 11.01.2023
#------------------------------------------
#beginmodule
if __name__ == "__main__":
    main()
#endif

#endmodule
