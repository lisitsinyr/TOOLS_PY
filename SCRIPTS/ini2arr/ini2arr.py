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

#------------------------------------------
def main ():
#beginfunction
    config = configparser.ConfigParser()

    # LFileINI = sys.argv[1]
    # print (LFileINI)
    # config.read(LFileINI)

    config.read(sys.stdin)

    for sec in config.sections():
        print ("declare -A %s" % (sec))
        for key, val in config.items(sec):
            print ('%s[%s]="%s"' % (sec, key, val))
        #endfor
    #endfor
#endfunction

#------------------------------------------
#
#------------------------------------------
#beginmodule
if __name__ == "__main__":
    main()
#endif

#endmodule
