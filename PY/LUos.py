"""LUos.py"""
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
     LUos.py

 =======================================================
"""
#------------------------------------------
# БИБЛИОТЕКИ python
#------------------------------------------
import os
import sys
import enum
import platform
import ctypes
import datetime
import logging

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------
import psutil

#------------------------------------------
# БИБЛИОТЕКИ LU
#------------------------------------------
# from LULog import LoggerTOOLS
import LULog
import LUConst
import LUParserREG
import LUDateTime

cHOME = 'HOME'
cWINDIR = 'windir'
cTEST = 'TEST'

@enum.unique
class TProductType(enum.Enum):
    """TFoldersConst"""
    W95 = 'Windows 95'
    W98 = 'Windows 98'
    WNT1 = 'Windows NT Workstation'
    WNT2 = 'Windows NT Server'
    WNT3 = 'Windows NT Domain Controller'
    W20001 = 'Windows 2000 Professional'
    W20002 = 'Windows 2000 Server'
    W20003 = 'Windows 2000 Domain Controller'
    WXP1 = 'Windows XP Home Edition'
    WXP2 = 'Windows XP Home Edition Tablet PC'
    WXP3 = 'Windows XP Professional'
    WXP4 = 'Windows XP Professional Tablet PC'
    W20031 = 'Windows Server 2003'
    W20032 = 'Windows Server 2003 Domain Controller'
    W7 = 'Windows 6.1 / 1'
    W8 = 'Windows 6.2 / 1'
    WXX = 'W95 or W98'
    WXXXX = 'W2000 or WXP or W2003'
#endclass

cSection = 'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'

class TFoldersConst(enum.Enum):
    """TFoldersConst"""
    cuDesktop     = 'Desktop'
    cuStartMenu   = 'Start Menu'
    cuFavorites   = 'Favorites'
    cuPrograms    = 'Programs'
    cuStartup     = 'Startup' 
    cuMyDocuments = 'Personal'

    lmDesktop     = 'Desktop'
    lmStartMenu   = 'Start Menu'
    lmFavorites   = 'Favorites'
    lmPrograms    = 'Programs'
    lmStartup     = 'Startup' 
#endclass

class TFolders (object):
    """TFolders"""
    luClassName = 'TFolders'
    __annotations__ ="""
    """
    #--------------------------------------------------
    # constructor
    #--------------------------------------------------
    def __init__ (self, **kwargs):
        """ Constructor """
    #beginfunction
        super ().__init__ (**kwargs)
        self.__FRegParser = LUParserREG.TREGParser()
        ...
    #endfunction

    #--------------------------------------------------
    # destructor
    #--------------------------------------------------
    def __del__ (self):
        """ destructor """
    #beginfunction
        LClassName = self.__class__.__name__
        s = '{} уничтожен'.format(LClassName)
        LULog.LoggerTOOLS.log (LULog.DEBUGTEXT, s)
    #endfunction

    #--------------------------------------------------
    # @property cuDesktop
    #--------------------------------------------------
    # getter
    @property
    def cuDesktop(self):
    #beginfunction
        return self.GetFolderCU (TFoldersConst.cuDesktop.value)
    #endfunction
    # setter
    @cuDesktop.setter
    def cuDesktop (self, AValue: str):
    #beginfunction
        self.SetFolderCU (TFoldersConst.cuDesktop.value, AValue)
    #endfunction

    #--------------------------------------------------
    # @property lmDesktop
    #--------------------------------------------------
    # getter
    @property
    def lmDesktop(self):
    #beginfunction
        return self.GetFolderCU (TFoldersConst.cuDesktop.value)
    #endfunction
    # setter
    @lmDesktop.setter
    def lmDesktop (self, AValue: str):
    #beginfunction
        self.SetFolderCU (TFoldersConst.cuDesktop.value, AValue)
    #endfunction
    #--------------------------------------------------
    # @property cuStartMenu
    #--------------------------------------------------
    # getter
    @property
    def cuStartMenu(self):
    #beginfunction
        return self.GetFolderCU (TFoldersConst.cuStartMenu.value)
    #endfunction
    # setter
    @cuStartMenu.setter
    def cuStartMenu (self, AValue: str):
    #beginfunction
        self.SetFolderCU (TFoldersConst.cuStartMenu.value, AValue)
    #endfunction

    #--------------------------------------------------
    # @property lmStartMenu
    #--------------------------------------------------
    # getter
    @property
    def lmStartMenu(self):
    #beginfunction
        return self.GetFolderCU (TFoldersConst.cuStartMenu.value)
    #endfunction
    # setter
    @lmStartMenu.setter
    def lmStartMenu (self, AValue: str):
    #beginfunction
        self.SetFolderCU (TFoldersConst.cuStartMenu.value, AValue)
    #endfunction

    #--------------------------------------------------
    # @property cuFavorites
    #--------------------------------------------------
    # getter
    @property
    def cuFavorites(self):
    #beginfunction
        return self.GetFolderCU (TFoldersConst.cuFavorites.value)
    #endfunction
    # setter
    @cuFavorites.setter
    def cuFavorites (self, AValue: str):
    #beginfunction
        self.SetFolderCU (TFoldersConst.cuFavorites.value, AValue)
    #endfunction

    #--------------------------------------------------
    # @property lmFavorites
    #--------------------------------------------------
    # getter
    @property
    def lmFavorites(self):
    #beginfunction
        return self.GetFolderCU (TFoldersConst.cuFavorites.value)
    #endfunction
    # setter
    @lmFavorites.setter
    def lmFavorites (self, AValue: str):
    #beginfunction
        self.SetFolderCU (TFoldersConst.cuFavorites.value, AValue)
    #endfunction

    #--------------------------------------------------
    # @property cuPrograms
    #--------------------------------------------------
    # getter
    @property
    def cuPrograms(self):
    #beginfunction
        return self.GetFolderCU (TFoldersConst.cuPrograms.value)
    #endfunction
    # setter
    @cuPrograms.setter
    def cuPrograms (self, AValue: str):
    #beginfunction
        self.SetFolderCU (TFoldersConst.cuPrograms.value, AValue)
    #endfunction

    #--------------------------------------------------
    # @property lmPrograms
    #--------------------------------------------------
    # getter
    @property
    def lmPrograms(self):
    #beginfunction
        return self.GetFolderCU (TFoldersConst.cuPrograms.value)
    #endfunction
    # setter
    @lmPrograms.setter
    def lmPrograms (self, AValue: str):
    #beginfunction
        self.SetFolderCU (TFoldersConst.cuPrograms.value, AValue)
    #endfunction

    #--------------------------------------------------
    # @property cuStartup
    #--------------------------------------------------
    # getter
    @property
    def cuStartup(self):
    #beginfunction
        return self.GetFolderCU (TFoldersConst.cuStartup.value)
    #endfunction
    # setter
    @cuStartup.setter
    def cuStartup (self, AValue: str):
    #beginfunction
        self.SetFolderCU (TFoldersConst.cuStartup.value, AValue)
    #endfunction

    #--------------------------------------------------
    # @property lmStartup
    #--------------------------------------------------
    # getter
    @property
    def lmStartup(self):
    #beginfunction
        return self.GetFolderCU (TFoldersConst.cuStartup.value)
    #endfunction
    # setter
    @lmStartup.setter
    def lmStartup (self, AValue: str):
    #beginfunction
        self.SetFolderCU (TFoldersConst.cuStartup.value, AValue)
    #endfunction

    #--------------------------------------------------
    # @property cuMyDocuments
    #--------------------------------------------------
    # getter
    @property
    def cuMyDocuments(self):
    #beginfunction
        return self.GetFolderCU (TFoldersConst.cuMyDocuments.value)
    #endfunction
    # setter
    @cuMyDocuments.setter
    def cuMyDocuments (self, AValue: str):
    #beginfunction
        self.SetFolderCU (TFoldersConst.cuMyDocuments.value, AValue)
    #endfunction

    #--------------------------------------------------------------------------------
    # GetFolderCU (AFolderName: str) -> str:
    #--------------------------------------------------------------------------------
    def GetFolderCU (self, AFolderName: str) -> str:
    #beginfunction
        LKeyName = AFolderName
        LFolderValue, LType = self.__FRegParser.GetKeyReg (LUParserREG.THKEYConst.cHKCU, cSection, LKeyName)
        return LFolderValue
    #endfunction

    #--------------------------------------------------------------------------------
    # SetFolderCU (AFolderName: str, AValue: str)
    #--------------------------------------------------------------------------------
    def SetFolderCU (self, AFolderName: str, AValue: str):
    #beginfunction
        LKeyName = AFolderName
        self.__FRegParser.SetValueReg (LUParserREG.THKEYConst.cHKCU, cSection,
                                       LKeyName, LUParserREG.TValueTypes.vtEXPAND_SZ, AValue)
    #endfunction

    #--------------------------------------------------------------------------------
    # GetFolderLM (AFolderName: str) -> str:
    #--------------------------------------------------------------------------------
    def GetFolderLM (self, AFolderName: str) -> str:
    #beginfunction
        LKeyName = AFolderName
        LFolderValue, LType = self.__FRegParser.GetKeyReg(LUParserREG.THKEYConst.cHKLM, cSection, LKeyName)
        return LFolderValue
    #endfunction

    #--------------------------------------------------------------------------------
    # SetFolderLM (AFolderName: str, AValue: str)
    #--------------------------------------------------------------------------------
    def SetFolderLM (self, AFolderName: str, AValue: str):
    #beginfunction
        LKeyName = AFolderName
        self.__FRegParser.SetValueReg (LUParserREG.THKEYConst.cHKLM, cSection,
                                LKeyName, LUParserREG.TValueTypes.vtEXPAND_SZ, AValue)
    #endfunction
#endclass

class TOSInfo (object):
    """TOSInfo"""
    luClassName = 'TOSInfo'
    __annotations__ ="""
    """
    #--------------------------------------------------
    # constructor
    #--------------------------------------------------
    def __init__ (self, **kwargs):
        """ Constructor """
    #beginfunction
        super ().__init__ (**kwargs)
        ...
    #endfunction

    #--------------------------------------------------
    # destructor
    #--------------------------------------------------
    def __del__ (self):
        """ destructor """
    #beginfunction
        LClassName = self.__class__.__name__
        s = '{} уничтожен'.format(LClassName)
        LUConst.LULogger.log (LULog.DEBUGTEXT, s)
    #endfunction

    # Return the number of CPUs in the system. Returns None if undetermined.
    #--------------------------------------------------
    # @property CPUs
    #--------------------------------------------------
    # getter
    @property
    def CPUs (self):
    #beginfunction
        return os.cpu_count()
    #endfunction

    # Returns the machine type
    #--------------------------------------------------
    # @property machine
    #--------------------------------------------------
    # getter
    @property
    def machine (self):
    #beginfunction
        return platform.machine()
    #endfunction

    # Returns the computer’s network name
    #--------------------------------------------------
    # @property node
    #--------------------------------------------------
    # getter
    @property
    def node (self):
    #beginfunction
        return platform.node()
    #endfunction

    # Returns a namedtuple() containing six attributes: system, node, release, version, machine, and processor
    #--------------------------------------------------
    # @property uname
    #--------------------------------------------------
    # getter
    @property
    def uname (self):
    #beginfunction
        return platform.uname ()
    #endfunction

    # Returns the (real) processor name, e.g. 'amdk6'.
    #--------------------------------------------------
    # @property processor
    #--------------------------------------------------
    # getter
    @property
    def processor (self):
    #beginfunction
        return platform.processor ()
    #endfunction

    # Returns the system’s release
    #--------------------------------------------------
    # @property release
    #--------------------------------------------------
    # getter
    @property
    def release (self):
    #beginfunction
        return platform.release ()
    #endfunction

    # Returns the system/OS name, such as 'Linux', 'Darwin', 'Java', 'Windows'
    #--------------------------------------------------
    # @property release
    #--------------------------------------------------
    # getter
    @property
    def system (self):
    #beginfunction
        return platform.system ()
    #endfunction

    # Returns the system’s release version
    #--------------------------------------------------
    # @property version
    #--------------------------------------------------
    # getter
    @property
    def version (self):
    #beginfunction
        return platform.version ()
    #endfunction

    #Returns (system, release, version) aliased to common marketing names
    #platform.system_alias(system, release, version)

    # Get additional version information from the Windows Registry and return a tuple (release, version, csd, ptype) referring to OS release
    #--------------------------------------------------
    # @property win32_ver
    #--------------------------------------------------
    # getter
    @property
    def win32_ver (self):
    #beginfunction
        return platform.win32_ver()
    #endfunction

    # Returns a string representing the current Windows edition, or None if the value cannot be determined. Possible values include but are not limited to 'Enterprise', 'IoTUAP', 'ServerStandard', and 'nanoserver'.
    #--------------------------------------------------
    # @property win32_edition
    #--------------------------------------------------
    @property
    def win32_edition (self):
    #beginfunction
        return platform.win32_edition ()
    #endfunction

    #---------------------------------------------
    # Python
    #---------------------------------------------
    # Returns a tuple (buildno, builddate) stating the Python build number and date as strings.
    #--------------------------------------------------
    # @property python_build
    #--------------------------------------------------
    @property
    def python_build (self):
    #beginfunction
        return platform.python_build ()
    #endfunction

    # Returns a string identifying the compiler used for compiling Python.
    #--------------------------------------------------
    # @property python_compiler
    #--------------------------------------------------
    @property
    def python_compiler (self):
    #beginfunction
        return platform.python_compiler ()
    #endfunction

    # Returns a string identifying the Python implementation SCM branch.
    #--------------------------------------------------
    # @property python_branch
    #--------------------------------------------------
    @property
    def python_branch (self):
    #beginfunction
        return platform.python_branch ()
    #endfunction

    # Returns a string identifying the Python implementation
    #--------------------------------------------------
    # @property python_implementation
    #--------------------------------------------------
    @property
    def python_implementation (self):
    #beginfunction
        return platform.python_implementation ()
    #endfunction

    # Returns a string identifying the Python implementation SCM revision.
    #--------------------------------------------------
    # @property python_revision
    #--------------------------------------------------
    @property
    def python_revision (self):
    #beginfunction
        return platform.python_revision ()
    #endfunction

    # Returns the Python version
    #--------------------------------------------------
    # @property python_version
    #--------------------------------------------------
    @property
    def python_version (self):
    #beginfunction
        return platform.python_version ()
    #endfunction

    # Python sys.version
    #--------------------------------------------------
    # @property version_sys
    #--------------------------------------------------
    @property
    def version_sys (self):
    #beginfunction
        return sys.version
    #endfunction

    # Returns the Python version as tuple (major, minor, patchlevel) of strings.
    #--------------------------------------------------
    # @property python_version_tuple
    #--------------------------------------------------
    @property
    def python_version_tuple (self):
    #beginfunction
        return platform.python_version_tuple ()
    #endfunction

    #--------------------------------------------------
    # @property UserID
    #--------------------------------------------------
    @property
    def UserID (self):
    #beginfunction
        return os.getlogin ()
    #endfunction

    @staticmethod
    def Info_psutil ():
        """Info_psutil"""
    #beginfunction
        """CPU"""
        # Return system CPU times as a named tuple
        psutil.cpu_times(percpu=False)
        # Return the number of logical CPUs in the system
        psutil.cpu_count (logical = True)

        """Memory"""
        # Return statistics about system memory usage as a named tuple including the following fields, expressed in bytes
        psutil.virtual_memory ()

        """Disks"""
        # Return all mounted disk partitions as a list of named tuples including device, mount point and filesystem type
        psutil.disk_partitions (all = False)
        # Return disk usage statistics about the partition which contains the given path as a named tuple including total, used and free space
        # psutil.disk_usage (path)

        """Network"""
        # Return the addresses associated to each NIC (network interface card) installed on the system as a dictionary whose keys are the NIC names and value is a list of named tuples for each address assigned to the NIC
        psutil.net_if_addrs()

        """Other system info"""
        psutil.users ()

        """Processes"""

        """Windows services"""
    #endfunction
#endclass

#------------------------------------------
# GetCurrentDir () -> str:
#------------------------------------------
def GetCurrentDir () -> str:
    """GetCurrentDir"""
#beginfunction
    return os.getcwd ()
#endfunction

#------------------------------------------
# APPWorkDir () -> str:
#------------------------------------------
def APPWorkDir () -> str:
    """APPWorkDir"""
#beginfunction
    return os.getcwd ()
#endfunction

#------------------------------------------
# GetEnvVar
#------------------------------------------
def GetEnvVar (AEnvVar: str) -> str:
    """GetEnvVar"""
#beginfunction
    s = ''
    try:
        s = os.environ [AEnvVar]
    # except KeyError as Key:
    # print (Key)
    except:
        ...
    finally:
        ...
    return s
#endfunction

#------------------------------------------
# SetEnvVar
#------------------------------------------
def SetEnvVar (AEnvVar: str, AValue: str):
    """SetEnvVar"""
#beginfunction
    os.environ[AEnvVar] = AValue
#endfunction

def get_data (EXTENDED_NAME_FORMAT: int):
#beginfunction
    GetUserNameEx = ctypes.windll.secur32.GetUserNameExW
    data = EXTENDED_NAME_FORMAT
    size = ctypes.pointer (ctypes.c_ulong (0))
    GetUserNameEx (data, None, size)
    nameBuffer = ctypes.create_unicode_buffer (size.contents.value)
    GetUserNameEx (data, nameBuffer, size)
    return nameBuffer.value
#endfunction

def get_display_name ():
#beginfunction
    GetUserNameEx = ctypes.windll.secur32.GetUserNameExW
    NameDisplay = 3
    size = ctypes.pointer (ctypes.c_ulong (0))
    GetUserNameEx (NameDisplay, None, size)
    nameBuffer = ctypes.create_unicode_buffer (size.contents.value)
    GetUserNameEx (NameDisplay, nameBuffer, size)
    return nameBuffer.value
#endfunction

def Print_get_data ():
#beginfunction
    print ("NameUnknown            : ", get_data (0))
    print ("NameFullyQualifiedDN   : ", get_data (1))
    print ("NameSamCompatible      : ", get_data (2))
    print ("NameDisplay            : ", get_data (3))
    print ("NameUniqueId           : ", get_data (6))
    print ("NameCanonical          : ", get_data (7))
    print ("NameUserPrincipal      : ", get_data (8))
    print ("NameCanonicalEx        : ", get_data (9))
    print ("NameServicePrincipal   : ", get_data (10))
    print ("NameDnsDomain          : ", get_data (12))
#endfunction

#------------------------------------------------------
# PrintGeneralTitle ($LLog, $LFile)
#------------------------------------------------------
def PrintGeneralTitle ():
#beginfunction
    LTOSInfo = TOSInfo()
    print ('===========================================')
    print ('Текущее время = ' + LUDateTime.DateTimeStr (True, datetime.datetime.now(), LUDateTime.cFormatDateTimeLog05))
    print ('UserID        = ' + LTOSInfo.UserID)
    # print ('FullName      = ' + @FullName+' ('+@Comment+')')
    print ('PCUser        = ' + LTOSInfo.node)
    print ('CPUs          = ' + str(LTOSInfo.CPUs))
    # print (LTOSInfo.uname)
    # print ('CPU           = ' + @CPU+' '+@MHz)
    print ('HostName      = ' + LTOSInfo.node)
    print ('OS            = ' + LTOSInfo.uname.system+' '+ '('+LTOSInfo.uname.version+')')
    # print ('CompName      = ' + @WKSTA)
    # print ('===========================================')
    # print ('DomainPC      = ' + @Domain)
    # print ('DomainUser    = ' + @LDomain)
    # print ('LServer       = ' + @LServer)
    print ('===========================================')
#endfunction

#------------------------------------------
def main ():
#beginfunction
    # PrintGeneralTitle ()
    # Print_get_data ()
    # get_display_name ()
    ...
#endfunction

#------------------------------------------
#
#------------------------------------------
#beginmodule
if __name__ == '__main__':
    main()
#endif

#endmodule
