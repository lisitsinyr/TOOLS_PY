"""PATTERN_PY.py"""
# -*- coding: UTF-8 -*-
__annotations__ = """
 =======================================================
 Copyright (c) 2025
 Author:
     Lisitsin Y.R.
 Project:
     LISTDIR.py
 Module:
     PATTERN_PY.py
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

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------

#------------------------------------------
# БИБЛИОТЕКА lyrpy
#------------------------------------------
import lyrpy.LUDoc as LUDoc
import lyrpy.LULog as LULog
import lyrpy.LUConst as LUConst
import lyrpy.LUDoc as LUDoc
import lyrpy.LULog as LULog
import lyrpy.LUFile as LUFile
import lyrpy.LUParserARG as LUParserARG


def TEST_01 ():
    """TEST_"""
#beginfunction
    global GO1
    global AO1

    LUDoc.PrintInfoObject('-----TEST_01----')
    LUDoc.PrintInfoObject(TEST_01)
#endfunction

#------------------------------------------
def main ():
#beginfunction
    # LUConst.SET_CONST(__file__)
    LUConst.SET_LIB(__file__)

    LULog.STARTLogging (LULog.TTypeSETUPLOG.tslINI, 'console', LUConst.GDirectoryLOG, LUConst.GFileNameLOG,
                        LUConst.GFileNameLOGjson)
    LULog.LoggerTOOLS.level = logging.INFO

    LArgParser = LUParserARG.TArgParser (description = 'Параметры', prefix_chars = '-/')
    LArg = LArgParser.ArgParser.add_argument ('A1', type = str, default = 'A1_Default', help = 'A1')
    LArg = LArgParser.ArgParser.add_argument ('-O1', '--O1', type = str, default='O1_Default', help = 'O1')
    Largs = LArgParser.ArgParser.parse_args ()
    GO1 = Largs.O1
    LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, f'O1 = {GO1}')
    GA1 = Largs.A1
    LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, f'A1 = {GA1}')
   
    TEST_01 ()

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
    