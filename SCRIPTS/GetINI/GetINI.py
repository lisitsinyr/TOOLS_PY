"""GetINI.py"""
# -*- coding: UTF-8 -*-
__annotations__ = """
 =======================================================
 Copyright (c) 2024
 Author:
     Lisitsin Y.R.
 Project:
     TOOLS_PY
 Module:
     GetINI.py
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
#beginfunction
    # print(cfg.get('Section1', 'foo', raw=False))  # -> "Python is fun!"
    LValue = GINIFile.get(ASection, AParameter, raw=False)
    print (AParameter+'='+LValue)
#endfunction

def CheckSection (ASection: str):
#beginfunction
    LParameters = GINIFile.options(ASection)
    for i in range (0,len(LParameters)):
        LParameter = LParameters[i]
        CheckParameter (ASection, LParameter)
    #endfor
    pass
#endfunction

def CheckSections ():
#beginfunction
    LSections = GINIFile.sections()
    for i in range (0,len(LSections)):
        LSection = LSections[i]
        CheckSection (LSection)
    #endfor
    pass
#endfunction

#------------------------------------------
def main ():
#beginfunction
    # sys.argv[1] - <>.ini
    # sys.argv[2] - <Section>
    # sys.argv[3] - <parameter>
    N = not (len(sys.argv) in (2,4))
    N = False
    if N:
        print ('GETINI: getini <ini_file> <Section> <parameter>')
    else:
        # GINIFileName = sys.argv[1]
        # GSection = sys.argv[2]
        # GParameter = sys.argv[3]
        GINIFileName = 'ini2arr.ini'
        GSection = 'barfoo'
        GSection = ''

        GParameter = 'session'
        GParameter = ''

        if not os.path.isfile (GINIFileName):
            print ('GETINI: ini_file '+sys.argv[1]+' not found...')
        else:
            # GINIFile = configparser.ConfigParser()
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
