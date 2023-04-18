"""LUConst.py"""
# -*- coding: UTF-8 -*-
__annotations__ = """
 =======================================================
 Copyright (c) 2023
 Author:
     Lisitsin Y.R.
 Project:
     LU_PY
     Python (LU)
 Module:
     LUConst.py

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
# БИБЛИОТЕКИ LU
#------------------------------------------
import LUStrUtils
import LULog

# GLULogger = logging.getLogger(__name__)
# GLULogger = LULog.CreateLoggerCONFIG (LULog.CDefaultFileLogCONFIG, __name__)
# GLULogger = LULog.CreateLoggerFILEINI (LULog.CDefaultFileLogINI, __name__)
GLULogger = LULog.CreateLoggerFILEINI (LULog.CDefaultFileLogINI, 'root')
# GLULogger = LULog.CreateLoggerBASIC (logging.DEBUG, 'LOG\\' + LULog.CDefaultFileLogFILEBASIC, __name__)

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def main ():
#beginfunction
    ...
#endfunction

#------------------------------------------
#
#------------------------------------------
#beginmodule
if __name__ == "__main__":
    main()
#endif

#endmodule
