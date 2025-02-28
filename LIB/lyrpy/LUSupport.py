"""LUSupport.py"""
# -*- coding: UTF-8 -*-
__annotations__ = """
 =======================================================
 Copyright (c) 2023-2024
 Author:
     Lisitsin Y.R.
 Project:
     LU_PY
     Python (LU)
 Module:
     LUSupport.py

 =======================================================
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

"""
function LoadDLL (NameDll: string; var HandleDLL: HModule): Boolean;
{ LoadDLL }
begin
    HandleDLL := LoadLibrary (PChar(NameDll));
    Result := (HandleDLL >= HINSTANCE_ERROR);
end;

function UnLoadDLL (HandleDLL: HModule): Boolean;
{ UnLoadDLL }
begin
    Result := FreeLibrary (HandleDLL);
end;

function GetFunc (HandleDLL: HModule; NameFunc: string; var AddFunc: Pointer): Boolean;
{ GetFunc }
begin
    try
        AddFunc := GetProcAddress (HandleDLL, PChar(NameFunc));
    except
        AddFunc := nil;
    end;
    Result := Assigned (AddFunc);
end;

function ErrorString (Error: DWORD): string;
{ ErrorString }
begin
    Result := SysErrorMessage (Error);
end;

function LastErrorString: string;
{ LastErrorString }
begin
    Result := ErrorString (GetLastError);
end;
"""

#-------------------------------------------------
# IsTerminal
# Возвращает True, если текущая консоль является терминалом
#-------------------------------------------------
def IsTerminal () -> bool:
    """IsTerminal"""
#beginfunction
    return sys.stdout.isatty ()
#endfunction

#-------------------------------------------------
# TupleToStr
# Возвращает кортеж в виде строки, состоящей из элементов ATuple
#-------------------------------------------------
def TupleToStr (ATuple:()) -> str:
    """TupleToStr"""
#beginfunction
    LResult = ''
    i = 0
    j = 0
    if type(ATuple) is tuple:
        for r in ATuple:
            i = i + 1
            if r != '':
                j = j + 1
                if j == 1:
                    LResult = LResult + r
                else:
                    LResult = LResult + ';' + r
                #endif
            #endif
        #endfor
    else:
        if len (ATuple) > 0:
            LResult = LResult + ATuple
        #endif
    #endif
    return LResult
#endfunction

#---------------------------------------------------------
# main
#---------------------------------------------------------
def main ():
#beginfunction
    ...
#endfunction

#---------------------------------------------------------
#
#---------------------------------------------------------
#beginmodule
if __name__ == "__main__":
    main()
#endif

#endmodule
