"""LUSupport.py"""
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
     LUSupport.py

 =======================================================
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
