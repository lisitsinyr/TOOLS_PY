"""LUDoc.py"""
# -*- coding: UTF-8 -*-
__annotations__ = """
------------------------------------------------------
 Copyright (c) 2023
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

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------

#------------------------------------------
# БИБЛИОТЕКИ LU
#------------------------------------------
import LULog

def PrintInfoObject (AObject):
#beginfunction
    s = f'{AObject}'
    #LULog_LoggerTOOLS_log(LULog.DEBUGTEXT, s)
    LULog.LoggerTOOLSAdd(LULog.DEBUGTEXT, s)
#endfunction

#------------------------------------------
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
