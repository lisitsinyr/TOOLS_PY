#!/usr/bin/env python

"""SetINI.py"""
# -*- coding: UTF-8 -*-
__annotations__ = """
 =======================================================
 Copyright (c) 2024
 Author:
     Lisitsin Y.R.
 Project:
     TOOLS_PY
 Module:
     SetINI.py
 =======================================================
"""

#------------------------------------------
# БИБЛИОТЕКИ python
#------------------------------------------
import sys
import os
import configparser

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------

#------------------------------------------
# БИБЛИОТЕКА LU
#------------------------------------------

GINIFile = configparser.ConfigParser()
GIniFileName = ''
GSection = ''
GParameter = ''
GValue = ''

def CheckParameter (ASection: str, AParameter: str, AValue: str):
#beginfunction
    global GINIFile
    global GParameter
    global GValue = GINIFile.get(ASection, AParameter, raw=False)
    GValue = GINIFile.get(ASection, AParameter, raw=False)

    GINIFile.WriteString(GSection, GParameter, GValue);
#endfunction

#------------------------------------------
def main ():
#beginfunction
    # sys.argv[1] - <>.ini
    # sys.argv[2] - <Section>
    # sys.argv[3] - <parameter>
    # sys.argv[4] - <value>
    N = not (len(sys.argv) in (2,4))
    # N = False
    if N:
        print (''SETINI: setini <ini_file> <group> <parameter> <value>')
    else:
        GINIFileName = sys.argv[1]
        try:
            GSection = sys.argv[2]
        except IndexError as ERROR:
            GSection = ''
        #endtry
        try:
            GParameter = sys.argv[3]
        except IndexError as ERROR:
            GParameter = ''
        #endtry
        try:
            GValue = sys.argv[4]
        except IndexError as ERROR:
            GValue = ''
        #endtry

        if not os.path.isfile (GINIFileName):
            print ('SETINI: ini_file '+sys.argv[1]+' not found...')
        else:
            GINIFile.read(GINIFileName)
            if GParameter != '':
                CheckParameter (GSection, GParameter, GValue)
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
