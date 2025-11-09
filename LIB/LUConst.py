"""LUConst.py"""
# -*- coding: UTF-8 -*-
__annotations__ = """
 =======================================================
Copyright (c) 2023-2025
  Author:
     Lisitsin Y.R.
 Project:
     TOOLS_SRC_PY
 Module:
     LUConst.py
 =======================================================
"""

#------------------------------------------
# БИБЛИОТЕКИ python
#------------------------------------------
import os

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------

#------------------------------------------
# БИБЛИОТЕКИ LU
#------------------------------------------
import lyrpy.LUFile as LUFile

GSCRIPT_FULLFILENAME = ''
GSCRIPT_BASEFILENAME = ''
GSCRIPT_FILENAME = ''
GSCRIPT_FILEDIR = ''
GSCRIPT_FILEEXT = ''
GAPPName = ''

GDirectoryLOG = ''
GFileNameLOG = ''
GFileNameLOGjson = ''

#--------------------------------------------------------------------------------
#procedure LYRConst ()
#--------------------------------------------------------------------------------
def LYRConst ():
#beginfunction
    ...
#endfunction

#-----------------------------------------------
# procedure SET_LIB (AFileName)
#-----------------------------------------------
def SET_LIB (AFileName: str):
#beginfunction
    __SET_VAR_SCRIPT (AFileName)
    __SET_VAR_DEFAULT ()
    __SET_VAR_PROJECTS ()
    __SET_LOG ()
#endfunction

#--------------------------------------------------------------------------------
# procedure __SET_VAR_SCRIPT (AFileName)
#--------------------------------------------------------------------------------
def __SET_VAR_SCRIPT (AFileName: str):
#beginfunction

    global GSCRIPT_FULLFILENAME
    global GSCRIPT_BASEFILENAME
    global GSCRIPT_FILENAME
    global GSCRIPT_FILEDIR
    global GSCRIPT_FILEEXT
    global GAPPName

    GFULLFILENAME=AFileName

    #-------------------------------------------------------------------
    # GSCRIPT_FULLFILENAME - Файл скрипта [каталог+имя+расширение]
    #-------------------------------------------------------------------
    GSCRIPT_FULLFILENAME=AFileName
    #-------------------------------------------------------------------
    # GSCRIPT_FULLFILENAME - Файл скрипта [каталог+имя+расширение]
    #-------------------------------------------------------------------
    GSCRIPT_FULLFILENAME=AFileName

    #-------------------------------------------------------------------
    # GSCRIPT_BASEFILENAME - Файл скрипта [имя+расширение]
    #-------------------------------------------------------------------
    GSCRIPT_BASEFILENAME=LUFile.ExtractFileName (AFileName)

    #-------------------------------------------------------------------
    # GSCRIPT_FILENAME - Файл скрипта [имя]
    #-------------------------------------------------------------------
    GSCRIPT_FILENAME=LUFile.ExtractFileNameWithoutExt (AFileName)

    #-------------------------------------------------------------------
    # GSCRIPT_FILEDIR - Файл скрипта: каталог
    #-------------------------------------------------------------------
    GSCRIPT_FILEDIR=LUFile.ExtractFileDir (AFileName)

    #-------------------------------------------------------------------
    # GSCRIPT_FILEEXT - Файл скрипта: расширение
    #-------------------------------------------------------------------
    GSCRIPT_FILEEXT=LUFile.ExtractFileExt (AFileName)

    #-------------------------------------------------------------------
    # GAPPName - APP
    #-------------------------------------------------------------------
    GAPPName = os.environ.get ('APPName', LUFile.ExtractFileNameWithoutExt (AFileName))
#endfunction

#--------------------------------------------------------------------------------
# procedure __SET_VAR_DEFAULT ()
#--------------------------------------------------------------------------------
def __SET_VAR_DEFAULT ():
#beginfunction
    APP=''
    COMMAND=''
    OPTION=''
    ARGS=''
    APPRUN=''

    touchRUN=r'touch -f'
    touchRUN=r'D:\TOOLS\EXE\touch.exe'
    SetINIAPP=r'D:\TOOLS\EXE\setini.exe'
    GetINIAPP=r'D:\TOOLS\EXE\getini.exe'

    #-------------------------------------------------------------------
    # GDATETIME_STAMP - формат имени файла журнала [YYYYMMDDHHMMSS]
    #-------------------------------------------------------------------
    # DATETIME_STAMP=%date:~6,4%%date:~3,2%%date:~0,2%%TIME:~0,2%%TIME:~3,2%%TIME:~6,2%

    #-------------------------------------------------------------------
    # GSLEEP - Number
    #-------------------------------------------------------------------
    GSLEEP=0

    #-------------------------------------------------------------------
    # GREPO_INI - Файл с параметрами репозитария
    #-------------------------------------------------------------------
    GREPO_INI='REPO.ini'

    #-------------------------------------------------------------------
    # GREPO_NAME - Имя репозитария
    #-------------------------------------------------------------------
    GREPO_NAME=''

    #-------------------------------------------------------------------
    # GPROJECT_INI - Файл с параметрами проекта
    #-------------------------------------------------------------------
    GPROJECT_INI='PROJECT.ini'

    #-------------------------------------------------------------------
    # GPROJECT_NAME - Имя проекта
    #-------------------------------------------------------------------
    GPROJECT_NAME=''

    #-------------------------------------------------------------------
    # GPOETRY_INI - Файл с параметрами проекта
    #-------------------------------------------------------------------
    GPOETRY_INI='POETRY.ini'

    #-------------------------------------------------------------------
    # GPOETRY_NAME - Имя проекта
    #-------------------------------------------------------------------
    GPOETRY_NAME=''
#endfunction

#--------------------------------------------------------------------------------
#procedure __SET_VAR_PROJECTS ()
#--------------------------------------------------------------------------------
def __SET_VAR_PROJECTS ():
#beginfunction
    #-------------------------------------------------------------------
    # GPROJECTS_LYR_DIR -
    #-------------------------------------------------------------------
    GPROJECTS_LYR_DIR=r'D:\PROJECTS_LYR'

    #-------------------------------------------------------------------
    # GPROJECT - проект
    #-------------------------------------------------------------------
    GPROJECT=''
  
    #-------------------------------------------------------------------
    # GPROJECT_DIR -
    #-------------------------------------------------------------------
    GPROJECT_DIR=''

    #-------------------------------------------------------------------
    # GCURRENT_SYSTEM -
    #-------------------------------------------------------------------
    # GCURRENT_SYSTEM=%OS%

    #-------------------------------------------------------------------
    # GUNAME - COMPUTERNAME
    #-------------------------------------------------------------------
    # GUNAME=%COMPUTERNAME%

    #-------------------------------------------------------------------
    # GUSERNAME - USERNAME
    #-------------------------------------------------------------------
    # GUSERNAME=%USERNAME%

    #-------------------------------------------------------------------
    # GCURRENT_DIR - Текущий каталог
    #-------------------------------------------------------------------
    # GCURRENT_DIR=%CD%

    #-------------------------------------------------------------------
    # GTEMP_DIR - Временный каталог
    #-------------------------------------------------------------------
    # GTEMP_DIR=%temp%
#endfunction

#--------------------------------------------------------------------------------
#procedure __SET_LOG ()
#--------------------------------------------------------------------------------
def __SET_LOG ():
#beginfunction
    global GDirectoryLOG
    global GFileNameLOG
    global GFileNameLOGjson

    #------------------------------------------------------
    # GLOG_FILESCRIPT - Файл первого скрипта [имя]
    #------------------------------------------------------
    GLOG_FILESCRIPT=''

    #-------------------------------------------------------------------
    # GLOG_DT_FORMAT_DEFAULT -
    #-------------------------------------------------------------------
    # GLOG_DT_FORMAT_DEFAULT='%Y%m%d'
    # GLOG_DT_FORMAT_DEFAULT=%date:~6,4%%date:~3,2%%date:~0,2%

    #-------------------------------------------------------------------
    # GLOG_FILE_ADD - Параметры журнала [0]
    #-------------------------------------------------------------------
    # if not defined GLOG_FILE_ADD (
    #     GLOG_FILE_ADD=0
    # )

    #-------------------------------------------------------------------
    # GLOG_FILE_DT - Параметры журнала [0]
    #-------------------------------------------------------------------
    # if not defined GLOG_FILE_DT (
    #     GLOG_FILE_DT=0
    # )

    #-------------------------------------------------------------------
    # GLOG_DT_FORMAT -
    #-------------------------------------------------------------------
    # GLOG_DT_FORMAT=
    # if not defined GLOG_DT_FORMAT (
    #     LOG_DT_FORMAT=!GLOG_DT_FORMAT_DEFAULT!
    # )

    #-------------------------------------------------------------------
    # GLOG_FILENAME_FORMAT - Формат имени файла журнала [FILENAME,DATETIME,...]
    #-------------------------------------------------------------------
    # GLOG_FILENAME_FORMAT=
    # if not defined GLOG_FILENAME_FORMAT (
    #     GLOG_FILENAME_FORMAT='FILENAME'
    # )

    #-------------------------------------------------------------------
    # GLOG_DIR - Каталог журнала [каталог]
    #-------------------------------------------------------------------
    # if not defined GLOG_DIR (
    #     GLOG_DIR=!GPROJECTS_LYR_DIR!\LOGS
    # )
    # if not exist !GLOG_DIR! (
    #     mkdir "!GLOG_DIR!"
    #     if not !ERRORLEVEL! EQU 0 (
    #         echo ERROR: Dir !LOG_DIR! not created...
    #         exit /b 1
    #     )
    # )

    #-------------------------------------------------------------------
    # GLOG_FILENAME - Файл журнала [имя]
    #-------------------------------------------------------------------
    # if not defined GLOG_FILENAME (
    #     if "!GLOG_FILENAME_FORMAT!"=="FILENAME" (
    #         GLOG_FILENAME=!GSCRIPT_FILENAME!
    #     ) else (
    #         if "!GLOG_FILENAME_FORMAT!"=="DATETIME" (
    #             GLOG_FILENAME=!GDATETIME_STAMP!
    #         ) else (
    #             echo ERROR: GLOG_FILENAME_FORMAT not set...
    #             exit /b 1
    #         )
    #     )
    # )
    # if "!GLOG_FILENAME_FORMAT!"=="FILENAME" (
    #     if GLOG_FILE_DT==1 (
    #        GLOG_FILENAME=!GDATETIME_STAMP!_!GLOG_FILENAME!
    #     )
    # )

    #-------------------------------------------------------------------
    # GLOG_FULLFILENAME - Файл журнала [каталог+имя+расширение]
    #-------------------------------------------------------------------
    # GLOG_FULLFILENAME=!GLOG_DIR!\!GLOG_FILENAME!.log
   
    #-------------------------------------------------------------------
    # GDirectoryLOG - Каталог журнала
    #-------------------------------------------------------------------
    GDirectoryLOG = os.environ.get ('DirectoryLOG', '')
    if GDirectoryLOG == '' or not LUFile.DirectoryExists (GDirectoryLOG):
        GDirectoryLOG = r'D:\PROJECTS_LYR\LOGS'
    #endif
    #-------------------------------------------------------------------
    # GFileNameLOG - Файл журнала
    #-------------------------------------------------------------------
    GFileNameLOG = os.environ.get ('FileNameLOG', GAPPName + '.log')
    GFileNameLOGjson = os.environ.get ('FileNameLOGjson', GAPPName + '_json.log')
#endfunction

# #-------------------------------------------------------------------------------
# # SET_CONST
# #-------------------------------------------------------------------------------
# def SET_CONST (AFileName: str):
# #beginfunction
#     global GAPPName
#     global GDirectoryLOG
#     global GFileNameLOG
#     global GFileNameLOGjson
#
#     GAPPName = os.environ.get ('APPName', LUFile.ExtractFileNameWithoutExt (AFileName))
#
#     #-------------------------------------------------------------------
#     #DirectoryLOG - Каталог журнала
#     #-------------------------------------------------------------------
#     GDirectoryLOG = os.environ.get ('DirectoryLOG', '')
#     if GDirectoryLOG == '' or not LUFile.DirectoryExists (GDirectoryLOG):
#         GDirectoryLOG = r'D:\PROJECTS_LYR\LOGS'
#     #endif
#     #-------------------------------------------------------------------
#     #FileNameLOG - Файл журнала
#     #-------------------------------------------------------------------
#     GFileNameLOG = os.environ.get ('FileNameLOG', GAPPName + '.log')
#     GFileNameLOGjson = os.environ.get ('FileNameLOGjson', GAPPName + '_json.log')
# #endfunction

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def main ():
#beginfunction
    print('main LUConst.py ...')
#endfunction

#------------------------------------------
#
#------------------------------------------
#beginmodule
if __name__ == "__main__":
    main()
#endif

#endmodule
