"""LUDict.py"""
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
     LUDict.py

 =======================================================
"""

#------------------------------------------
# БИБЛИОТЕКИ python
#------------------------------------------
import sys
import logging

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------
import json

#------------------------------------------
# БИБЛИОТЕКИ LU
#------------------------------------------
...

"""
    data = {}
    data ['people'] = []
    data ['people'].append ({
        'name': 'Scott',
        'website': 'pythonist.ru',
        'from': 'Nebraska'
    })
    data ['people'].append ({
        'name': 'Larry',
        'website': 'pythonist.ru',
        'from': 'Michigan'
    })
    data ['people'].append ({
        'name': 'Tim',
        'website': 'pythonist.ru',
        'from': 'Alabama'
    })
"""

#---------------------------------------------------------------
# PrintDict
#---------------------------------------------------------------
def PrintDict (ADict: dict):
    """PrintDict"""
#beginfunction

    # LResult = AARGS.get (AARGName).get (AARGValue)

    for key, value in ADict.items():
        # print(key, value)
        try:
            print("key:\t" + key)
            # ADict (value)
        except AttributeError:
            print("value:\t" + str(value))
        #endtry
    #endfor
#endfunction

#---------------------------------------------------------------
# SaveDictJSON
#---------------------------------------------------------------
def SaveDictJSON (ADict, AFileName):
    """SaveDictJSON"""
#beginfunction
    with open (AFileName, 'w') as LFileDictJSON:
        json.dump (ADict, LFileDictJSON)
    #endwith
#endfunction

#---------------------------------------------------------------
# SaveDictSTR
#---------------------------------------------------------------
def SaveDictSTR (ADict, AFileName):
    """SaveDictSTR"""
#beginfunction
    LDict = json.dumps (ADict, ensure_ascii = False, indent = 4)
    # Save a reference to the original standard output
    original_stdout = sys.stdout
    with open (AFileName, 'w') as LFileDictSTR:
        # Change the standard output to the file we created.
        sys.stdout = LFileDictSTR
        print (LDict)
    #endwith
    # Reset the standard output to its original value
    sys.stdout = original_stdout
#endfunction

#---------------------------------------------------------------
#
#---------------------------------------------------------------
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
