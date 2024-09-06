"""LISTDIR.py"""
# -*- coding: UTF-8 -*-
__annotations__ = """
 =======================================================
 Copyright (c) 2024
 Author:
     Lisitsin Y.R.
 Project:
     TOOLS_SRC_PY
 Module:
     COPYFILE.py

 =======================================================
"""

#------------------------------------------
# БИБЛИОТЕКИ python
#------------------------------------------
import logging

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------

#------------------------------------------
# БИБЛИОТЕКА LU
#------------------------------------------
import lyrpy.LULog as LULog
import lyrpy.LUFile as LUFile
import lyrpy.LUParserARG as LUParserARG
import lyrpy.LUFileUtils as LUFileUtils
from lyrpy.LUFileUtils import GMask

#------------------------------------------
#CONST
#------------------------------------------
FileNameSET = r'D:\PROJECTS_LYR\CHECK_LIST\01_OS\03_UNIX\PROJECTS_UNIX\COMMANDS_SH\SRC\TOOLS\TOOLS_SET.sh'

#------------------------------------------
# FuncDir ()
#------------------------------------------
def FuncDir (ADirectory: str, APathDest: str):
    """FuncDir"""
#beginfunction
    # Lstat = os.stat(ADirectory)
    # LAttr = (LUFile.GetFileAttr (ADirectory))
    # LDirSize = LUFile.GetDirectoryTreeSize (ADirectory)
    # LDirDateTime = LUFile.GetDirDateTime (ADirectory)
    # s = f'{LDirDateTime[2]:%d.%m.%Y  %H:%M} {LDirDateTime[3]:%d.%m.%Y  %H:%M} {LDirSize:d}'
    Lspisok = ADirectory.split('\\')
    Litem = Lspisok[-1]
    if Litem != 'LISTDIR':
        if '[' in Litem:
            end=Litem.find(']')
            s = 'PART_'+Litem[0:end+1]+'='+"'"+Litem+"'"
        else:
            end=Litem.find('-')
            s = 'COMMAND_'+Litem[0:end-1]+'='+"'"+Litem+"'"
        #endif
        LUFile.WriteStrToFile (FileNameSET, s)
    #endif
#endfunction

#------------------------------------------
# FuncFile ()
#------------------------------------------
def FuncFile (AFileName: str, APathDest: str):
    """FuncFile"""
#beginfunction
    # lyrpy.LUFile.SetFileAttr (AFileName, Lflags, True)
    # LULog.LoggerAPPS_AddLevel (LULog.TEXT, f'GFileName = {GFileName}')
    # Lstat = os.stat(AFileName)
    # LAttr = LUFile.GetFileAttr(AFileName)
    # Lflags = stat.FILE_ATTRIBUTE_SYSTEM | stat.FILE_ATTRIBUTE_HIDDEN | stat.FILE_ATTRIBUTE_READONLY
    # LFileSize = LUFile.GetFileSize (AFileName)
    # LFileDateTime = LUFile.GetFileDateTime (AFileName)
    # s = f'...{LFileDateTime[2]:%d.%m.%Y  %H:%M} {LFileDateTime[2]:%d.%m.%Y  %H:%M} {LFileSize:d}'
    # LFileDirectory = LUFile.GetFileDir(AFileName)
    # LFileDirectory = LUFile.ExtractFileName(LFileDirectory)
    # s = f'{LFileDirectory:s}'
    # LULog.LoggerTOOLS_AddLevel (LULog.TEXT, s)
    pass
#endfunction

#------------------------------------------
# BEGIN ()
#------------------------------------------
def BEGIN ():
    """BEGIN"""
#beginfunction
    LUFile.WriteStrToFile (FileNameSET, "#!\\bin\\bash")
    LUFile.WriteStrToFile (FileNameSET, "# -----------------------------------------------")
    LUFile.WriteStrToFile (FileNameSET, "# TOOLS_SET.sh")
    LUFile.WriteStrToFile (FileNameSET, "# -----------------------------------------------")
    LUFile.WriteStrToFile (FileNameSET, "")
    LUFile.WriteStrToFile (FileNameSET, "#--------------------------------------------------------------------------------")
    LUFile.WriteStrToFile (FileNameSET, "# CONST")
    LUFile.WriteStrToFile (FileNameSET, "#--------------------------------------------------------------------------------")
    LUFile.WriteStrToFile (FileNameSET, "    SHOWLIST='YyNn'")
    LUFile.WriteStrToFile (FileNameSET, "    SHOWCAPTION='Продолжить?'")
    LUFile.WriteStrToFile (FileNameSET, "    SHOWDELAY=3")
    LUFile.WriteStrToFile (FileNameSET, "    SHOWDEFAULT='Y'")
    LUFile.WriteStrToFile (FileNameSET, "    TIMEOUT=$SHOWDELAY")
    LUFile.WriteStrToFile (FileNameSET, "    PRESSANYKEY_BASH=1")
    LUFile.WriteStrToFile (FileNameSET, "#--------------------------------------------------------------------------------")
    LUFile.WriteStrToFile (FileNameSET, "# VAR")
    LUFile.WriteStrToFile (FileNameSET, "#--------------------------------------------------------------------------------")
    LUFile.WriteStrToFile (FileNameSET, "    Show='N'")
    LUFile.WriteStrToFile (FileNameSET, "    Show='Y'")
    LUFile.WriteStrToFile (FileNameSET, "    Show=")
    LUFile.WriteStrToFile (FileNameSET, "")
    LUFile.WriteStrToFile (FileNameSET, "#--------------------------------------------------------------------------------")
    LUFile.WriteStrToFile (FileNameSET, "#")
    LUFile.WriteStrToFile (FileNameSET, "#--------------------------------------------------------------------------------")
    LUFile.WriteStrToFile (FileNameSET, "#begin")
#endfunction

#------------------------------------------
# END ()
#------------------------------------------
def END ():
    """END"""
#beginfunction
    LUFile.WriteStrToFile (FileNameSET, "")
    LUFile.WriteStrToFile (FileNameSET, "#read -n 1 -s -r -p $'Press any key to continue ...\\n'")
    LUFile.WriteStrToFile (FileNameSET, "")
    LUFile.WriteStrToFile (FileNameSET, "#end")
    LUFile.WriteStrToFile (FileNameSET, "#--------------------------------------------------------------------------------")
#endfunction

#------------------------------------------
# MAIN
#------------------------------------------
def main ():
#beginfunction
    # global GDirectory

    LULog.STARTLogging (LULog.TTypeSETUPLOG.tslCONFIG,
                        r'D:\PROJECTS_LYR\LOGS',
                        'LISTDIR.log',
                        'LISTDIR_json.log')

    LArgParser = LUParserARG.TArgParser (description = 'Параметры', prefix_chars = '-/')
    LArg = LArgParser.ArgParser.add_argument ('Directory', type = str, default='', help = 'Directory')
    print('...',LArg.dest)

    Largs = LArgParser.ArgParser.parse_args ()


    # When set on a logger, indicates that ancestor loggers are to be consulted to determine the effective level. If that still resolves to NOTSET, then all events are logged. When set on a handler, all events are handled.
    # logging.NOTSET 0
    # Detailed information, typically only of interest to a developer trying to diagnose a problem.
    # logging.DEBUG 10
    # Confirmation that things are working as expected.
    # logging.INFO 20
    # An indication that something unexpected happened, or that a problem might occur in the near future (e.g. ‘disk space low’). The software is still working as expected.
    # logging.WARNING 30
    # Due to a more serious problem, the software has not been able to perform some function.
    # logging.ERROR 40
    # A serious error, indicating that the program itself may be unable to continue running.
    # logging.CRITICAL 50

    # LULog.LoggerTOOLS.level = logging.NOTSET
    # LULog.LoggerTOOLS.level = logging.DEBUG
    # LULog.LoggerTOOLS.level = logging.INFO
    # LULog.LoggerTOOLS.level = logging.WARNING
    # LULog.LoggerTOOLS.level = logging.ERROR
    # LULog.LoggerTOOLS.level = logging.CRITICAL
    # LULog.LoggerTOOLS.level = logging.FATAL

    # LULog.LoggerTOOLS.level = logging.INFO
    # LULog.LoggerTOOLS.setLevel (logging.INFO)

    # LULog.LoggerTOOLS.debug ('DEBUG.')
    # LULog.LoggerTOOLS.info ('INFO.')
    # LULog.LoggerTOOLS.warning ('WARNING.')
    # LULog.LoggerTOOLS.error ('ERROR.')
    # LULog.LoggerTOOLS.critical ('CRITICAL.')
    # LULog.LoggerTOOLS.fatal ('FATAL.')
    # LULog.LoggerTOOLS.log (logging.WARNING, 'WARNING.')


    LULog.LoggerTOOLS.level = logging.INFO
    LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, FileNameSET)
    # LULog.LoggerAdd (LULog.LoggerAPPS, logging.INFO, FileNameSET)

    LUFile.FileDelete (FileNameSET)

    BEGIN ()

    LDirectory = Largs.Directory
    # LULog.LoggerAPPS_AddLevel (LULog.TEXT, f'Directory = {LDirectory}')
    if not LUFile.DirectoryExists(LDirectory):
        print ('LISTDIR: Directory', LDirectory, 'not exist...')
    else:
        LUFileUtils.__ListDir (LDirectory, GMask,
                           True, '', 'CONSOLE', 0, FuncDir, FuncFile)
    #endif

    END ()
    
    LULog.STOPLogging ()

#endfunction

#------------------------------------------
#
#------------------------------------------
#beginmodule
if __name__ == "__main__":
    main()
#endif

#endmodule
