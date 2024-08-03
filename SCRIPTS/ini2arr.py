#!/usr/bin/env python

"""ini2arr.py"""
# -*- coding: UTF-8 -*-
__annotations__ = """
 =======================================================
 Copyright (c) 2024
 Author:
     Lisitsin Y.R.
 Project:
     TOOLS_PY
 Module:
     ini2arr.py
 =======================================================
"""

#------------------------------------------
# БИБЛИОТЕКИ python
#------------------------------------------
import sys
import configparser

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------

#------------------------------------------
# БИБЛИОТЕКА LU
#------------------------------------------

config = configparser.ConfigParser()

#------------------------------------------
def CreateArr ():
#beginfunction
    for sec in config.sections():
        print ("declare -A %s" % (sec))
        for key, val in config.items(sec):
            print ('%s[%s]="%s"' % (sec, key, val))
        #endfor
    #endfor
#endfunction

#------------------------------------------
def main ():
#beginfunction
    LFileINI = sys.argv[1]
    config.read(LFileINI)

    # config.read(sys.stdin)

    CreateArr()

    # print ("test1")

#endfunction

#------------------------------------------
#
#------------------------------------------
#beginmodule
if __name__ == "__main__":
    main()
#endif

#endmodule
