#!/usr/bin/env python
"""GetINI1.py"""
# -*- coding: UTF-8 -*-
__annotations__ = """
=======================================================
Copyright (c) 2024
Author:
    Lisitsin Y.R.
Project:
    SCRIPTS_PY
Module:
    GetINI1.py
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

def CheckParameter (ASection: str, AParameter: str):
    """CheckParameter"""
#beginfunction
    global GINIFile
    global GParameter
    try:
        LValue = GINIFile.get(ASection, AParameter, raw=False)
    except:
        LValue = ''
    #endtry

    # print (AParameter+'='+LValue)

    print ('%s=%s' % (AParameter, LValue))

    #if GParameter != '':
        # print (LValue)
    #    print ('%s=%s' % (AParameter, LValue))
    #else:
    #    print ('%s[%s]="%s"' % (ASection, AParameter, LValue))
    #endif
#endfunction

def CheckSection (ASection: str):
    """CheckSection"""
#beginfunction
    global GINIFile

    # print ("declare -A %s" % (ASection))

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
    # sys.argv[1] - <>.ini
    # sys.argv[2] - <Section>
    # sys.argv[3] - <parameter>
    global GSection
    global GParameter

    try:
        GINIFileName = sys.argv[1]
    except IndexError as ERROR:
        GINIFileName = ''
    #endtry
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

    if not os.path.isfile (GINIFileName):
        print ('GETINI1: ini_file '+GINIFileName+' not found...')
    else:
        GINIFile.read(GINIFileName)
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
#endfunction

#------------------------------------------
#
#------------------------------------------
#beginmodule
if __name__ == "__main__":
    main()
#endif

#endmodule
