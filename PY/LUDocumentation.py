"""LUDocumentation.py"""
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
     LUDocumentation.py

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
from LUDateTime import *

def PrintInfoObject (AObject):
#beginfunction
    print (f'{DateTimeStr(True,Now(),cFormatDateTimeLog01, True)} {AObject}')

    # print (f'Class={AObject.__class__}')
    # print (f'Name={AObject.__name__}')

    # print (f'Doc={AObject.__doc__}')
    # print (f'Annotations=({AObject.__annotations__})')
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
