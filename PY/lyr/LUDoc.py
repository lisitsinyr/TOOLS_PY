"""LUDoc.py"""
# -*- coding: UTF-8 -*-
__annotations__ = """
------------------------------------------------------
 Copyright (c) 2023-2024
 Author:
     Lisitsin Y.R.
 Project:
     LU_PY
     Python (LU)
 Module:
     LUDoc.py

------------------------------------------------------
"""

#------------------------------------------
# БИБЛИОТЕКИ python
#------------------------------------------
import sys

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------

#------------------------------------------
# БИБЛИОТЕКИ LU
#------------------------------------------
import lyr.LULog as LULog

#---------------------------------------------------------------
# PrintInfoObject
#---------------------------------------------------------------
def PrintInfoObject (AObject):
#beginfunction
    # print (sys._getframe (0).f_code.co_name, '...')
    # print (inspect.currentframe().f_code.co_name, '...')
    # print (inspect.stack () [0] [3], '...')
    # print (traceback.extract_stack () [-1].name, '...')
    s = f'{AObject}'
    #LULog_LoggerTOOLS_log(LULog.DEBUGTEXT, s)
    LULog.LoggerTOOLS_AddLevel(LULog.DEBUGTEXT, s)
#endfunction

#---------------------------------------------------------------
# main
#---------------------------------------------------------------
def main ():
#beginfunction
    print('main LUDoc.py...')
#endfunction

#------------------------------------------
#
#------------------------------------------
#beginmodule
if __name__ == "__main__":
    main()
#endif

#endmodule
