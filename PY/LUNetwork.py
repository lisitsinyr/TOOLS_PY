"""LUNetwork.py"""
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
     LUNetwork.py

 =======================================================
"""

#------------------------------------------
# БИБЛИОТЕКИ python
#------------------------------------------
import platform

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
function GetLocalIP: string;
var
    WSAData: TWSAData;
    Host: PHostEnt;
    Buf: array [0 .. 127] of Char;
begin
    if WSAStartup ($101, WSAData) = 0 then
    begin
        if GetHostName (@Buf, 128) = 0 then
        begin
            Host := GetHostByName (@Buf);
            if Host <> nil then
            begin
                Result := iNet_ntoa (PInAddr(Host^.h_addr_list^)^);
            end;
        end;
        WSACleanUP;
    end;
end;
"""

"""
(*
 Пример получения имени пользователя и домена под которым работает
 текущий поток или процесс

 Использовать функцию можно так :
   chDomain:=50;
   chUser :=50;
   GetCurrentUserAndDomain(User,chuser,Domain,chDomain)
 Если вам необходимо получить только имя пользователя - используйте GetUserName
 Данный пример можно использовать и для определения - запущен ли процесс
 системой или пользователем.  Учетной записи Localsystem соответствует
 имя пользователя - SYSTEM и домен NT AUTORITY (лучше проверить на практике)
*)

function GetCurrentUserAndDomain (szUser: PChar; var chUser: DWORD;
    szDomain: PChar; var chDomain: DWORD): Boolean;
var
    hToken: THandle;
    cbBuf: Cardinal;
    ptiUser: PTOKEN_USER;
    snu: SID_NAME_USE;
begin
    Result := False;
   { Получаем маркер доступа текущего потока нашего процесса }
    if not OpenThreadToken (GetCurrentThread(), TOKEN_QUERY, True, hToken) then
    begin
        if GetLastError () <> ERROR_NO_TOKEN then
            Exit;
      { В случее ошибки - получаем маркер доступа нашего процесса. }
        if not OpenProcessToken (GetCurrentProcess(), TOKEN_QUERY, hToken) then
            Exit;
    end;

   { Вывываем GetTokenInformation для получения размера буфера }
    if not GetTokenInformation (hToken, TokenUser, nil, 0, cbBuf) then
        if GetLastError () <> ERROR_INSUFFICIENT_BUFFER then
        begin
            CloseHandle (hToken);
            Exit;
        end;

    if cbBuf = 0 then
        Exit;

   { Выделяем память под буфер }
    GetMem (ptiUser, cbBuf);

   { В случае удачного вызова получим указатель на TOKEN_USER }
    if GetTokenInformation (hToken, TokenUser, ptiUser, cbBuf, cbBuf) then
    begin
      { Ищем имя пользователя и его домен по его SID }
        if LookupAccountSid (nil, ptiUser.User.Sid, szUser, chUser, szDomain,
            chDomain, snu) then
            Result := True;
    end;

   { Освобождаем ресурсы }
    CloseHandle (hToken);
    FreeMem (ptiUser);
end;
"""

"""
function DivideUserName_02 (S: string; var Domain: string;
    var Username: string): Boolean;
var
    i: Integer;
begin
    i := Pos ('\', S);
    if i <> 0 then
    begin
        Domain := Copy (S, 1, i - 1);
        Username := Copy (S, i + 1, Maxint);
        Result := True;
    end else begin
        i := Pos ('@', S);
        if i <> 0 then
        begin
            Username := Copy (S, 1, i - 1);
            Domain := Copy (S, i + 1, Maxint);
         // result := true;
        end else begin
            Domain := '';
            Username := S;
        end;
        Result := False;
    end;
end;
"""

"""
function GetCompName_02: string;
var
    sz: DWORD;
begin
    SetLength (Result, MAX_COMPUTERNAME_LENGTH);
    sz := MAX_COMPUTERNAME_LENGTH + 1;
    GetComputerName (PChar(Result), sz);
    SetLength (Result, sz);
end;
"""

"""
function Error (Res: DWORD): string;
var
    // FErrorBufPtr: Pointer;
    // FNameBufPtr: Pointer;
    FErrorString: string;

    function CheckNetError (Res: DWORD): string;
    var
        S: string;
      // Error: EWin32Error;
    begin
        S := '';
        if (Res <> NERR_Success){ and (Res <> ERROR_MORE_DATA) } then
        begin
            S := SysAndNetErrorMessage (Res);
            S := Format ('Net Error code: %d.'#10'"%s"', [Res, S]);
        end;
        Result := S;
    end;

begin
    FErrorString := CheckNetError (Res);
end;
"""

"""
function GetUserSID_02 (Domain, Username: string; var Sid: PSID;
    var sidType: SID_NAME_USE): Boolean; overload;
var
    pdomain: PChar;
    Size: DWORD;
    refDomainLen: DWORD;
    S: string;
begin
    if Domain <> '' then
        pdomain := PChar (Domain)
    else
        pdomain := nil;
    Size := 4096;
    refDomainLen := 0;
   // result := LookupAccountName(pdomain, pchar(userName), nil, size, nil,refDomainLen,sidType);
    S := Error (GetLastError);
    GetMem (Sid, Size);
    SetLength (Domain, refDomainLen);
    Result := LookupAccountName (pdomain, PChar(Username), Sid, Size,
        @Domain[1], refDomainLen, sidType);
end;
"""

"""
function GetUserSID_02 (Domain, Username: string; var Sid: PSID)
    : Boolean; overload;
var
    ignoreSidType: SID_NAME_USE;
begin
    Result := GetUserSID_02 (Domain, Username, Sid, ignoreSidType);
end;
"""

"""
function GetUserSID_02 (Username: string; var Sid: PSID;
    var sidType: SID_NAME_USE): Boolean; overload;
var
    Domain: string;
begin
    DivideUserName_02 (Username, Domain, Username);
    Result := GetUserSID_02 (Domain, Username, Sid, sidType);
end;
"""

"""
function GetUserSID_02 (Username: string; var Sid: PSID): Boolean; overload;
var
    ignoreSidType: SID_NAME_USE;
begin
    Result := GetUserSID_02 (Username, Sid, ignoreSidType);
end;
"""

"""
function GetUserName_02 (Sid: PSID; out Username: string): Boolean;
var
    Name: string;
    nameLen: DWORD;
    Domain: string;
    domainLen: DWORD;
    sidType: SID_NAME_USE;
begin
    nameLen := 1024;
    SetLength (name, nameLen);
    domainLen := 1024;
    SetLength (Domain, domainLen);
    Result := LookupAccountSid (nil, Sid, @name[1], nameLen, @Domain[1],
        domainLen, sidType);
    if Result then
    begin
        SetLength (name, nameLen);
        SetLength (Domain, domainLen);
        Username := Domain + '\' + name;
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
