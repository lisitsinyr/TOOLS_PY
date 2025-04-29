#!/usr/bin/env python
"""GetINI2.py"""
# -*- coding: UTF-8 -*-
__annotations__ = """
 =======================================================
 Copyright (c) 2024
 Author:
     Lisitsin Y.R.
 Project:
     SCRIPTS_PY
 Module:
     GetINI2.py
 =======================================================
"""

#------------------------------------------
# БИБЛИОТЕКИ python
#------------------------------------------
import os
import sys
import argparse
import logging
import shutil
import configparser

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------

#------------------------------------------
# БИБЛИОТЕКА LU
#------------------------------------------
import lyrpy.LUConst as LUConst
import lyrpy.LULog as LULog
import lyrpy.LUFile as LUFile
import lyrpy.LUParserARG as LUParserARG
import lyrpy.LUFileUtils as LUFileUtils


GINIFile = configparser.ConfigParser()
GIniFileName = ''
GSection = ''
GParameter = ''

def CheckParameter (ASection: str, AParameter: str):
    """CheckParameter"""
#beginfunction
    global GINIFile
    global GParameter
    LValue = GINIFile.get(ASection, AParameter, raw=False)
    # print (AParameter+'='+LValue)
    if GParameter != '':
        print (LValue)
    else:
        print ('%s[%s]="%s"' % (ASection, AParameter, LValue))
    #endif
#endfunction

def CheckSection (ASection: str):
    """CheckSection"""
#beginfunction
    global GINIFile

    print ("declare -A %s" % (ASection))

    LParameters = GINIFile.options(ASection)
    for i in range (0,len(LParameters)):
        LParameter = LParameters[i]
        CheckParameter (ASection, LParameter)
    #endfor
#endfunction

def CheckSections ():
    """CheckSections"""
#beginfunction
    global GINIFile
    LSections = GINIFile.sections()
    for i in range (0,len(LSections)):
        LSection = LSections[i]
        # CheckSection (LSection)
        print (LSection)
    #endfor
#endfunction

#------------------------------------------
def main ():
    """main"""
#beginfunction
    global GFileINI
    global GSection
    global GParameter

    # sys.argv[1] - <>.ini
    # sys.argv[2] - <Section>
    # sys.argv[3] - <parameter>

    # LUConst.SET_CONST(__file__)
    LUConst.SET_LIB(__file__)

    LULog.STARTLogging (LULog.TTypeSETUPLOG.tslINI, 'console', LUConst.GDirectoryLOG, LUConst.GFileNameLOG,
                        LUConst.GFileNameLOGjson)
    LULog.LoggerTOOLS.level = logging.INFO

    LArgParser = LUParserARG.TArgParser (description = 'Параметры', prefix_chars = '-/')
    LArg = LArgParser.ArgParser.add_argument ('FileINI', type = str, default = '', help = 'FileINI')
    LArg = LArgParser.ArgParser.add_argument ('Section', type = str, default = '', help = 'Section')
    LArg = LArgParser.ArgParser.add_argument ('Parameter', type = str, default = '', help = 'Parameter')
    Largs = LArgParser.ArgParser.parse_args ()
    GFileINI = Largs.FileINI
    LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, f'FileINI = {GFileINI}')
    GSection = Largs.Section
    LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, f'Section = {GSection}')
    GParameter = Largs.Parameter
    LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, f'Parameter = {GParameter}')

    N = not (len(sys.argv) in (2,4))
    # N = False
    if N:
        print ('GETINI: getini <ini_file> <Section> <parameter>')
    else:
        if not os.path.isfile (GFileINI):
            print ('GETINI: ini_file '+GFileINI+' not found...')
        else:
            GINIFile.read(GFileINI)
            if GParameter != '':
                CheckParameter (GSection, GParameter)
            else:
                if GSection != '':
                    CheckSection (GSection)
                else:
                    CheckSections ()
                #endif
            #endif
        #endif
    #endif
#endfunction

#------------------------------------------
#
#------------------------------------------
#beginmodule
if __name__ == "__main__":
    main()
#endif

#endmodule
