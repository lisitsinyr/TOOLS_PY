"""LUParserREG.py"""
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
     LUParserREG.py

 =======================================================
"""

#------------------------------------------
# БИБЛИОТЕКИ python
#------------------------------------------
import winreg
import enum

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------

#------------------------------------------
# БИБЛИОТЕКА LU
#------------------------------------------

#----------------------------------------------------------
# HKEY_* Constants
#----------------------------------------------------------
"""
winreg.HKEY_CLASSES_ROOT
Registry entries subordinate to this key define types (or classes) of documents and the properties associated with those types. Shell and COM applications use the information stored under this key.
---------------------
winreg.HKEY_CURRENT_USER
Registry entries subordinate to this key define the preferences of the current user. These preferences include the settings of environment variables, data about program groups, colors, printers, network connections, and application preferences.
---------------------
winreg.HKEY_LOCAL_MACHINE
Registry entries subordinate to this key define the physical state of the computer, including data about the bus type, system memory, and installed hardware and software.
---------------------
winreg.HKEY_USERS
Registry entries subordinate to this key define the default user configuration for new users on the local computer and the user configuration for the current user.
---------------------
winreg.HKEY_PERFORMANCE_DATA
Registry entries subordinate to this key allow you to access performance data. The data is not actually stored in the registry; the registry functions cause the system to collect the data from its source.
---------------------
winreg.HKEY_CURRENT_CONFIG
Contains information about the current hardware profile of the local computer system.
---------------------
winreg.HKEY_DYN_DATA
This key is not used in versions of Windows after 98.
---------------------
"""
@enum.unique
class THKEYConst(enum.Enum):
    """THKEYConst"""
    cHKCR = winreg.HKEY_CLASSES_ROOT
    cHKCU = winreg.HKEY_CURRENT_USER
    cHKLM = winreg.HKEY_LOCAL_MACHINE
    cHKU = winreg.HKEY_USERS
    cHKPD = winreg.HKEY_PERFORMANCE_DATA
    cHKCC = winreg.HKEY_CURRENT_CONFIG
    cHKDD = winreg.HKEY_DYN_DATA
#endclass

#---------------------------------------------------------
# Access Rights
#---------------------------------------------------------
"""
winreg.KEY_ALL_ACCESS
Combines the STANDARD_RIGHTS_REQUIRED, KEY_QUERY_VALUE, KEY_SET_VALUE, KEY_CREATE_SUB_KEY, KEY_ENUMERATE_SUB_KEYS, KEY_NOTIFY, and KEY_CREATE_LINK access rights.
---------------------
winreg.KEY_WRITE
Combines the STANDARD_RIGHTS_WRITE, KEY_SET_VALUE, and KEY_CREATE_SUB_KEY access rights.
---------------------
winreg.KEY_READ
Combines the STANDARD_RIGHTS_READ, KEY_QUERY_VALUE, KEY_ENUMERATE_SUB_KEYS, and KEY_NOTIFY values.
---------------------
winreg.KEY_EXECUTE
Equivalent to KEY_READ.
---------------------
winreg.KEY_QUERY_VALUE
Required to query the values of a registry key.
---------------------
winreg.KEY_SET_VALUE
Required to create, delete, or set a registry value.
---------------------
winreg.KEY_CREATE_SUB_KEY
Required to create a subkey of a registry key.
---------------------
winreg.KEY_ENUMERATE_SUB_KEYS
Required to enumerate the subkeys of a registry key.
---------------------
winreg.KEY_NOTIFY
Required to request change notifications for a registry key or for subkeys of a registry key.
---------------------
winreg.KEY_CREATE_LINK
Reserved for system use.
---------------------
"""
# @enum.unique
class TKEYAccess(enum.Enum):
    """TKEYAccess"""
    kaALL_ACCESS = winreg.KEY_ALL_ACCESS
    kaWRITE = winreg.KEY_WRITE
    kaREAD = winreg.KEY_READ
    kaEXECUTE = winreg.KEY_EXECUTE
    kaQUERY_VALUE = winreg.KEY_QUERY_VALUE
    kaSET_VALUE = winreg.KEY_SET_VALUE
    kaCREATE_SUB_KEY = winreg.KEY_CREATE_SUB_KEY
    kaENUMERATE_SUB_KEYS = winreg.KEY_ENUMERATE_SUB_KEYS
    kaKEY_NOTIFY = winreg.KEY_NOTIFY
    kaKEY_CREATE_LINK = winreg.KEY_CREATE_LINK
#endclass

#---------------------------------------------------------
# Value Types¶
# ---------------------------------------------------------
"""
winreg.REG_BINARY
Binary data in any form.
---------------------
winreg.REG_DWORD
32-bit number.
---------------------
winreg.REG_DWORD_LITTLE_ENDIAN
A 32-bit number in little-endian format. Equivalent to REG_DWORD.
---------------------
winreg.REG_DWORD_BIG_ENDIAN
A 32-bit number in big-endian format.
---------------------
winreg.REG_EXPAND_SZ
Null-terminated string containing references to environment variables (%PATH%).
---------------------
winreg.REG_LINK
A Unicode symbolic link.
---------------------
winreg.REG_MULTI_SZ
A sequence of null-terminated strings, terminated by two null characters. (Python handles this termination automatically.)
---------------------
winreg.REG_NONE
No defined value type.
---------------------
"""
# @enum.unique
class TValueTypes(enum.Enum):
    """TValueTypes"""
    vtBINARY = winreg.REG_BINARY
    vtDWORD = winreg.REG_DWORD
    vtDWORD_LITTLE_ENDIAN = winreg.REG_DWORD_LITTLE_ENDIAN
    vtDWORD_BIG_ENDIAN = winreg.REG_DWORD_BIG_ENDIAN
    vtEXPAND_SZ = winreg.REG_EXPAND_SZ
    vtLINK = winreg.REG_LINK
    vtMULTI_SZ = winreg.REG_MULTI_SZ
    vtNONE = winreg.REG_NONE
#endclass

#-------------------------------------------------------------------------------
# General Reestr Keys
#-------------------------------------------------------------------------------
RootKeyHKLM = winreg.HKEY_LOCAL_MACHINE
RootKeyHKCU = winreg.HKEY_CURRENT_USER

cHKLMSCCS    = r'HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet'
cHKLMSMWCV   = r'HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion'
cHKLMSMWNTCV = r'HKEY_LOCAL_MACHINE\Software\Microsoft\Windows NT\CurrentVersion'
cHKCUSMWCV   = r'HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion'
cHKCUSMWNTCV = r'HKEY_CURRENT_USER\Software\Microsoft\Windows NT\CurrentVersion'

class TREGParser (object):
    """TREGParser"""
    luClassName = 'TREGParser'
    __annotations__ =\
    """
    TREGParser - Работа с реестром windows
    
    aReg = _winreg.ConnectRegistry(None,_winreg.HKEY_LOCAL_MACHINE)
    
    """
    #--------------------------------------------------
    # constructor
    #--------------------------------------------------
    def __init__ (self, **kwargs):
        """ Constructor """
    #beginfunction
        super ().__init__ (**kwargs)
        self.__Fhkey = 0
        ...
    #endfunction

    #--------------------------------------------------
    # destructor
    #--------------------------------------------------
    def __del__ (self):
        """ destructor """
    #beginfunction
        LClassName = self.__class__.__name__
        s = '{} уничтожен'.format (LClassName)
        # LULog.LoggerTOOLS_AddLevel (LULog.DEBUGTEXT, s)
        #print (s)
    #endfunction

    #--------------------------------------------------
    # @property hkey
    #--------------------------------------------------
    # getter
    @property
    def hkey(self):
    #beginfunction
        return self.__Fhkey
    #endfunction
    # setter
    @hkey.setter
    def hkey (self, AValue: int):
    #beginfunction
        self.__Fhkey = AValue
    #endfunction

    def CreateKeyReg (self, AHKEY: THKEYConst, ASection: str) -> bool:
        """CreateKeyReg"""
    #beginfunction
        # winreg.CreateKey (key, sub_key)
        #   Создает или открывает указанный ключ, возвращая объект дескриптора
        # winreg.CreateKeyEx(key, sub_key, reserved=0, access=KEY_WRITE)
        #   Создает или открывает указанный ключ, возвращая объект дескриптора
        self.hkey = None
        try:
            self.hkey = winreg.CreateKeyEx (AHKEY.value, ASection, 0, TKEYAccess.kaALL_ACCESS.value)
            self.CloseKeyReg (self.hkey)
        except FileNotFoundError as ERROR:
            ...
        finally:
            return not self.hkey is None
    #endfunction

    @staticmethod
    def DeleteKeyReg (AHKEY: THKEYConst, ASection: str):
        """DeleteKeyReg"""
    #beginfunction
        # winreg.DeleteKey (key, sub_key)
        #   Удаляет указанный ключ.
        # winreg.DeleteKeyEx (key, sub_key, access = KEY_WOW64_64KEY, reserved = 0)
        #   Удаляет указанный ключ.
        LResult = False
        try:
            winreg.DeleteKey (AHKEY.value, ASection)
            LResult = True
        except FileNotFoundError as ERROR:
            ...
        finally:
            return LResult
    #endfunction

    def OpenKeyReg (self, AHKEY: THKEYConst, ASection: str):
        """OpenKeyReg"""
    #beginfunction
        #+winreg.OpenKey (key, sub_key, reserved = 0, access = KEY_READ)
        #   Открывает указанный ключ, возвращая объект дескриптора .
        #+winreg.OpenKeyEx (key, sub_key, reserved = 0, access = KEY_READ)
        #   Открывает указанный ключ, возвращая объект дескриптора .
        self.hkey = None
        try:
            self.hkey = winreg.OpenKeyEx (AHKEY.value, ASection, 0, TKEYAccess.kaALL_ACCESS.value)
        except FileNotFoundError as ERROR:
            ...
        finally:
            return self.hkey
    #endfunction

    @staticmethod
    def CloseKeyReg (Ahkey):
        """CloseKeyReg"""
    #beginfunction
        # winreg.CloseKey(hkey)
        # Закрывает ранее открытый раздел реестра. HKEY аргумент указывает, ранее открытый ключ.
        # Если hkey не закрыт с помощью этого метода (или через hkey.Close() ), он закрывается,
        # когда объект hkey уничтожается Python.
        LResult = False
        if Ahkey:
            winreg.CloseKey (Ahkey)
            LResult = True
        return LResult
    #endfunction

    def EnumKeyReg (self, AHKEY: THKEYConst, ASection: str) -> []:
        """EnumKeyReg"""
    #beginfunction
        # winreg.EnumKey (key, index)
        #   Нумеровывает подклавиши открытого ключа реестра,возвращая строку.
        LInfo = self.QueryInfoKeyReg (AHKEY, ASection)
        LList = []
        if len(LInfo) > 0:
            self.hkey = self.OpenKeyReg (AHKEY, ASection)
            # LWork = EnumKey (self.hkey, 0)
            for i in range (LInfo[0],LInfo[1]):
                try:
                    LWork = winreg.EnumKey (self.hkey, i)
                except OSError as ERROR:
                    LWork = ERROR.strerror
                    #LUErrors.LUFileError_FileNotExist as ERROR
                    ...
                finally:
                    ...
                LList.append(LWork)
            self.CloseKeyReg (self.hkey)
        return LList
    #endfunction

    def EnumValueReg (self, AHKEY: THKEYConst, ASection: str) -> []:
        """EnumValueReg"""
    #beginfunction
        #+winreg.EnumValue (key, index)
        #   Перечисляет значения открытого ключа реестра,возвращая кортеж.
        LInfo = self.QueryInfoKeyReg (AHKEY, ASection)
        LList = []
        if len(LInfo) > 0:
            self.hkey = self.OpenKeyReg (AHKEY, ASection)
            for i in range (LInfo[0],LInfo[1]):
                LList.append(winreg.EnumValue (self.hkey, i))
                # LKeyName, LValue, LFormat = EnumValue (self.hkey, i)
            self.CloseKeyReg (self.hkey)
        return LList
    #endfunction

    def SaveKeyReg (self, AHKEY: THKEYConst, ASection: str, AFileName: str):
        """SaveKeyReg"""
    #beginfunction
        # winreg.SaveKey (key, file_name)
        #   Сохраняет указанный ключ и все его подклавиши в указанный файл.
        self.hkey = self.OpenKeyReg (AHKEY, ASection)
        if not self.hkey is None:
            winreg.SaveKey (self.hkey, AFileName)
            self.CloseKeyReg(self.hkey)
    #endfunction

    def LoadKeyReg (self, AHKEY: THKEYConst, ASection: str, AFileName: str):
        """LoadKeyReg"""
    #beginfunction
        # winreg.LoadKey(key, sub_key, file_name)
        #   Создает под-ключ под указанным ключом и сохраняет регистрационную информацию из указанного файла в этот под-ключ.
        self.hkey = self.OpenKeyReg (AHKEY, ASection)
        if not self.hkey is None:
            winreg.LoadKey (self.hkey, ASection, AFileName)
            self.CloseKeyReg(self.hkey)
    #endfunction

    def QueryValueReg (self, AHKEY: THKEYConst, ASection: str, AOption: str) -> ():
        """QueryValueReg"""
    #beginfunction
        #+winreg.QueryValue (key, sub_key)
        #   Возвращает безымянное значение для ключа,в виде строки.
        #+winreg.QueryValueEx (key, value_name)
        #   Результат-кортеж из 2 пунктов:
        #   0 - Значение элемента реестра.
        #   1 - Целое число, указывающее тип реестра для этого значения
        LResult = ''
        self.hkey = self.OpenKeyReg (AHKEY, ASection)
        if not self.hkey is None:
            if len(AOption) > 0:
                LResult = winreg.QueryValueEx (self.hkey, AOption)
            else:
                LResult = winreg.QueryValue (self.hkey, None)
            self.CloseKeyReg(self.hkey)
        return LResult
    #endfunction

    def QueryInfoKeyReg (self, AHKEY: THKEYConst, ASection: str) -> ():
        """QueryInfoKeyReg"""
    #beginfunction
        #+winreg.QueryInfoKey (key)
        #   Результат-кортеж из 3 пунктов:
        LResult = ()
        self.hkey = self.OpenKeyReg (AHKEY, ASection)
        if not self.hkey is None:
            LResult = winreg.QueryInfoKey (self.hkey)
            self.CloseKeyReg(self.hkey)
        return LResult
    #endfunction

    def DeleteValueReg (self, AHKEY: THKEYConst, ASection: str, AOption: str) -> bool:
        """SetValueReg"""
    #beginfunction
        # winreg.DeleteValue (key, value)
        #   Удаляет именованное значение из ключа реестра.
        LResult = False
        self.hkey = self.OpenKeyReg (AHKEY, ASection)
        if not self.hkey is None:
            winreg.DeleteValue (self.hkey, AOption)
            self.CloseKeyReg(self.hkey)
            LResult = True
        return LResult
    #endfunction

    def SetValueReg (self, AHKEY: THKEYConst, ASection: str, AOption: str, AFormat: TValueTypes, Value: str):
        """SetValueReg"""
    #beginfunction
        # winreg.SetValue (key, sub_key, type, value)
        #   Сопоставляет стоимость с указанным ключом.
        # winreg.SetValueEx (key, value_name, reserved, type, value)¶
        #   Хранит данные в поле значений открытого ключа реестра.
        LResult = False
        self.hkey = self.OpenKeyReg (AHKEY, ASection)
        if not self.hkey is None:
            winreg.SetValueEx (self.hkey, AOption, 0, AFormat.value, Value)
            self.CloseKeyReg(self.hkey)
            LResult = True
        return LResult
    #endfunction

    def GetKeyReg (self, AHKEY: THKEYConst, ASection: str, AOption: str):
        """GetKeyReg"""
    #beginfunction
        return self.QueryValueReg (AHKEY, ASection, AOption)
    #endfunction

    def GetOptionsReg (self, AHKEY: THKEYConst, ASection: str) -> ():
        """QueryInfoKeyReg"""
    #beginfunction
        #+winreg.QueryInfoKey (key)
        #   Результат-кортеж из 3 пунктов:
        LListKeyValue = self.EnumValueReg (AHKEY, ASection)
        LList = []
        for key in LListKeyValue:
            LList.append(key[0])
        return LList
    #endfunction

    def IsSection (self, AHKEY: THKEYConst, ASection: str) -> bool:
    #beginfunction
        LResult = False
        self.hkey = self.OpenKeyReg (AHKEY, ASection)
        if not self.hkey is None:
            LResult =  True
        return LResult
    #endfunction

    def IsOption (self, AHKEY: THKEYConst, ASection: str, AOption: str) -> bool:
    #beginfunction
        LResult = False
        self.hkey = self.OpenKeyReg (AHKEY, ASection)
        if not self.hkey is None:
            LList = self.GetOptionsReg (AHKEY, ASection)
            if len (LList) > 0 and AOption in LList:
                LResult = True
            #endif
        #endif
        return LResult
    #endfunction
#endclass

def SaveRegToFile_regedit (AFileName: str, AHKEY: THKEYConst, ASection: str):
    """SaveRegToFile"""
#beginfunction
    # LWorkDir = LUFile.ExtractFileDir (AFileName)
    LProgramName = 'regedit.exe'
    LParamStr = ''
    match AHKEY:
        case THKEYConst.cHKLM:
            s = 'HKEY_LOCAL_MACHINE'
            LParamStr = '/ea'+' '+AFileName+' '+s+'\\'+ASection
        case THKEYConst.cHKCU:
            s = 'HKEY_CURRENT_USER'
            LParamStr = '/ea'+' '+AFileName+' "'+s+'\\'+ASection+'"'
    #endmatch
    if len (LParamStr) > 0:
        #print (LParamStr)
        # Lregedit = subprocess.Popen ('C:\\Windows\\System32\\regedit.exe', LParamStr)
        # Lregedit = subprocess.Popen ('regedit.exe', LParamStr)
        # Lregedit = subprocess.Popen ('regedit.exe')
        # os.system (command)
        # os.startfile ('regedit.exe', LParamStr)
        # os.startfile ('regedit.exe')
        ...
    #endif
#endfunction

#---------------------------------------------------------
# CreateTREGParser
#---------------------------------------------------------
def CreateTREGParser () -> TREGParser:
    """CreateTREGParser"""
#beginfunction
    return TREGParser ()
#endfunction

GREGParser = CreateTREGParser ()

#---------------------------------------------------------
# main
#---------------------------------------------------------
def main ():
#beginfunction
    # print (tuple(THKEYConst))
    # print (tuple(TKEYAccess))
    # print (tuple(TValueTypes))
    ...
#endfunction

#---------------------------------------------------------
#
#---------------------------------------------------------
#beginmodule
if __name__ == '__main__':
    main()
#endif

#endmodule
