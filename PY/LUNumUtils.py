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
     LUNumUtils.py

 =======================================================
"""

#------------------------------------------
# БИБЛИОТЕКИ python
#------------------------------------------

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------
if platform.system() == 'Windows':
    import win32api
    import win32con
#endif

#------------------------------------------
# БИБЛИОТЕКИ LU
#------------------------------------------

"""
function Dec2Hex (N: Longint; A: Byte): string;
begin
    Result := IntToHex (N, A);
end;

function D2H (N: Longint; A: Byte): string;
begin
    Result := IntToHex (N, A);
end;

function Hex2Dec (const S: string): Longint;
var
    HexStr: string;
begin
    if Pos ('$', S) = 0 then
        HexStr := '$' + S
    else
        HexStr := S;
    Result := StrToIntDef (HexStr, 0);
end;

function H2D (const S: string): Longint;
begin
    Result := Hex2Dec (S);
end;

function Dec2Numb (N: Longint; A, B: Byte): string;
var
    C: Integer;
{$IFDEF RX_D4}
    Number: Cardinal;
{$ELSE}
    Number: Longint;
{$ENDIF}
begin
    if N = 0 then
        Result := '0'
    else
    begin
{$IFDEF RX_D4}
        Number := Cardinal (N);
{$ELSE}
        Number := N;
{$ENDIF}
        Result := '';
        while Number > 0 do
        begin
            C := Number mod B;
            if C > 9 then
                C := C + 55
            else
                C := C + 48;
            Result := Chr (C) + Result;
            Number := Number div B;
        end;
    end;
    if Result <> '' then
        Result := AddChar ('0', Result, A);
end;

function Numb2Dec (S: string; B: Byte): Longint;
var
    I, P: Longint;
begin
    I := Length (S);
    Result := 0;
    S := UpperCase (S);
    P := 1;
    while (I >= 1) do
    begin
        if S[I] > '@' then
            Result := Result + (Ord(S[I]) - 55) * P
        else
            Result := Result + (Ord(S[I]) - 48) * P;
        Dec (I);
        P := P * B;
    end;
end;

function RomanToInt (const S: string): Longint;
const
    RomanChars = ['C', 'D', 'I', 'L', 'M', 'V', 'X'];
    RomanValues: array ['C' .. 'X'] of Word = (100, 500, 0, 0, 0, 0, 1, 0, 0,
        50, 1000, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 10);
var
    Index, Next: Char;
    I: Integer;
    Negative: Boolean;
begin
    Result := 0;
    I := 0;
    Negative := (Length(S) > 0) and (S[1] = '-');
    if Negative then
        Inc (I);
    while (I < Length(S)) do
    begin
        Inc (I);
        index := UpCase (S[I]);
        if index in RomanChars then
        begin
            if Succ (I) <= Length (S) then
                Next := UpCase (S[I + 1])
            else
                Next := #0;
            if (Next in RomanChars) and (RomanValues[index] < RomanValues[Next])
            then
            begin
                Inc (Result, RomanValues[Next]);
                Dec (Result, RomanValues[index]);
                Inc (I);
            end
            else
                Inc (Result, RomanValues[index]);
        end else begin
            Result := 0;
            Exit;
        end;
    end;
    if Negative then
        Result := - Result;
end;

function IntToRoman (Value: Longint): string;
label A500,
    A400,
    A100,
    A90,
    A50,
    A40,
    A10,
    A9,
    A5,
    A4,
    A1;
begin
    Result := '';
{$IFNDEF WIN32}
    if (Value > MaxInt * 2) then
        Exit;
{$ENDIF}
    while Value >= 1000 do
    begin
        Dec (Value, 1000);
        Result := Result + 'M';
    end;
    if Value < 900 then
        goto A500
    else
    begin
        Dec (Value, 900);
        Result := Result + 'CM';
    end;
    goto A90;
A400:
    if Value < 400 then
        goto A100
    else
    begin
        Dec (Value, 400);
        Result := Result + 'CD';
    end;
    goto A90;
A500:
    if Value < 500 then
        goto A400
    else
    begin
        Dec (Value, 500);
        Result := Result + 'D';
    end;
A100:
    while Value >= 100 do
    begin
        Dec (Value, 100);
        Result := Result + 'C';
    end;
A90:
    if Value < 90 then
        goto A50
    else
    begin
        Dec (Value, 90);
        Result := Result + 'XC';
    end;
    goto A9;
A40:
    if Value < 40 then
        goto A10
    else
    begin
        Dec (Value, 40);
        Result := Result + 'XL';
    end;
    goto A9;
A50:
    if Value < 50 then
        goto A40
    else
    begin
        Dec (Value, 50);
        Result := Result + 'L';
    end;
A10:
    while Value >= 10 do
    begin
        Dec (Value, 10);
        Result := Result + 'X';
    end;
A9:
    if Value < 9 then
        goto A5
    else
    begin
        Result := Result + 'IX';
    end;
    Exit;
A4:
    if Value < 4 then
        goto A1
    else
    begin
        Result := Result + 'IV';
    end;
    Exit;
A5:
    if Value < 5 then
        goto A4
    else
    begin
        Dec (Value, 5);
        Result := Result + 'V';
    end;
    goto A1;
A1:
    while Value >= 1 do
    begin
        Dec (Value);
        Result := Result + 'I';
    end;
end;

function IntToBin (Value: Longint; Digits, Spaces: Integer): string;
begin
    Result := '';
    if Digits > 32 then
        Digits := 32;
    while Digits > 0 do
    begin
        if (Digits mod Spaces) = 0 then
            Result := Result + ' ';
        Dec (Digits);
        Result := Result + IntToStr ((Value shr Digits) and 1);
    end;
end;

"""

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
