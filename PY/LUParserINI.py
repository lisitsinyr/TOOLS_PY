"""LUParserINI.py"""
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
     LUParserINI.py

 =======================================================
"""

#------------------------------------------
# БИБЛИОТЕКИ python
#------------------------------------------
import configparser
import logging

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------

#------------------------------------------
# БИБЛИОТЕКА LU
#------------------------------------------
# from LULog import LULogger
import LULog
import LUConst
import LUFile
import LUos
import LUStrDecode

class TINIFile (configparser.ConfigParser):
    """TINIFile"""
    luClassName = 'TINIFile'

    #--------------------------------------------------
    # constructor
    #--------------------------------------------------
    """
    class configparser.ConfigParser (
        defaults=None,
        dict_type=dict,
        allow_no_value=False,
        delimiters=('=', ':'),
        comment_prefixes=('#', ';'),
        inline_comment_prefixes=None,
        strict=True,
        empty_lines_in_values=True,
        default_section=configparser.DEFAULTSECT,
        interpolation=BasicInterpolation(),
        converters={}
        )
    """
    @staticmethod
    def __GetINIFileName (AFileName: str) -> str:
    #beginfunction
        P = LUFile.ExtractFileDir (AFileName)
        F = LUFile.ExtractFileName (AFileName)
        E = LUFile.ExtractFileExt (AFileName)
        if E == '':
            F = F + '.ini'
        #endif
        if P == '':
            LWinDir = LUos.GetEnvVar (LUos.cWINDIR)
            APath = LUos.GetCurrentDir () + ';' + LWinDir
            LResult = LUFile.FileSearch (F, APath)
            if LResult == '':
                LResult = LUFile.IncludeTrailingBackslash (LWinDir) + F
            #endif
        else:
            LResult = LUFile.ExpandFileName (AFileName)
        #endif
        return LResult
    #endfunction

    def __init__ (self, **kwargs):      # allow_no_value=True
        """Constructor"""
    #beginfunction
        super ().__init__ (**kwargs)
        self.__FSectionName: str = ''
        self.__FOptionName: str = ''
        self.__FOptionValue: str = ''
        self.__FChangedFileINI: bool = False
        self.__FFileNameINI: str = ''
    #endfunction

    #--------------------------------------------------
    # destructor
    #--------------------------------------------------
    def __del__ (self):
        """destructor"""
    #beginfunction
        LClassName = self.__class__.__name__
        s = '{} уничтожен'.format (LClassName)
        # LULog.LoggerTOOLS.log (LULog.DEBUGTEXT, s)
        print (s)
    #endfunction

    #--------------------------------------------------
    # @property ConfigParser
    #--------------------------------------------------
    # getter
    @property
    def ConfigParser(self) -> configparser.ConfigParser:
    #beginfunction
        return self
    #endfunction

    #--------------------------------------------------
    # @property Sections
    #--------------------------------------------------
    # getter
    @property
    def Sections(self):
    #beginfunction
        return self.sections()
    #endfunction

    #--------------------------------------------------
    # @property Options
    #--------------------------------------------------
    # getter
    @property
    def Options(self):
    #beginfunction
        return self.options(self.SectionName)
    #endfunction

    #--------------------------------------------------
    # @property SectionName
    #--------------------------------------------------
    # getter
    @property
    def SectionName(self):
    #beginfunction
        return self.__FSectionName
    #endfunction
    # setter
    @SectionName.setter
    def SectionName (self, AValue: str):
    #beginfunction
        self.__FSectionName = AValue
    #endfunction

    #--------------------------------------------------
    # @property OptionName
    #--------------------------------------------------
    # getter
    @property
    def OptionName(self):
    #beginfunction
        return self.__FOptionName
    #endfunction
    # setter
    @OptionName.setter
    def OptionName (self, AValue: str):
    #beginfunction
        self.__FOptionName = AValue
    #endfunction

    #--------------------------------------------------
    # @property OptionValue
    #--------------------------------------------------
    # getter
    @property
    def OptionValue(self):
    #beginfunction
        self.__FOptionValue = self.get(self.SectionName, self.OptionName)
        return self.__FOptionValue
    #endfunction
    # setter
    @OptionValue.setter
    def OptionValue (self, AValue: str):
    #beginfunction
        self.__FOptionValue = AValue
        self.set(self.SectionName, self.OptionName, AValue)
    #endfunction

    #--------------------------------------------------
    # @property FileNameINI
    #--------------------------------------------------
    # getter
    @property
    def FileNameINI(self):
    #beginfunction
        return self.__FFileNameINI
    #endfunction
    # setter
    @FileNameINI.setter
    def FileNameINI (self, AValue: str):
    #beginfunction
        LFullFileName = self.__GetINIFileName (AValue)
        if not LUFile.FileExists (LFullFileName):
            LFullFileName = LUFile.ExpandFileName (LUFile.ExtractFileName(AValue))
            LUFile.CreateTextFile (LFullFileName, '', LUStrDecode.cCP1251)
        self.__FFileNameINI = LFullFileName
        self.__OpenFileINI ()
        self.ChangedFileINI = False
    #endfunction

    #--------------------------------------------------
    # @property ChangedFileINI
    #--------------------------------------------------
    # getter
    @property
    def ChangedFileINI(self):
    #beginfunction
        return self.__FChangedFileINI
    #endfunction
    # setter
    @ChangedFileINI.setter
    def ChangedFileINI (self, AValue: bool):
    #beginfunction
        self.__FChangedFileINI = AValue
    #endfunction

    def __OpenFileINI (self):
        """__OpenFileINI"""
    #beginfunction
        self.read (self.FileNameINI)
    #endfunction

    def IsSection (self, ASectionName: str) -> bool:
        """IsSection"""
    #beginfunction
        return self.has_section(ASectionName)
    #endfunction

    def IsOption (self, ASectionName: str, AOption: str) -> bool:
        """IsOption"""
    #beginfunction
        return self.has_option(ASectionName, AOption)
    #endfunction

    def UpdateFileINI (self):
        """UpdateFileINI"""
    #beginfunction
        if self.ChangedFileINI:
            with open (self.FileNameINI, 'w', encoding = LUStrDecode.cCP1251) as LFileINI:
                self.write (LFileINI)
            #endwith
            self.__OpenFileINI ()
        #endif
    #endfunction

    def GetOption (self, ASectionName: str, AOptionName: str, AValueDefault: str) -> str:
        """GetOption"""
    #beginfunction
        try:
            return self.get(ASectionName, AOptionName)
        except configparser.NoSectionError as ERROR:
            return AValueDefault
    #endfunction

    def SetOption (self, ASectionName: str, AOptionName: str, AValue: str):
        """SetOption"""
    #beginfunction
        try:
            if not self.has_section(ASectionName):
                self.add_section (ASectionName)
            #endif
            self.set(ASectionName, AOptionName, AValue)
            self.ChangedFileINI = True
            self.UpdateFileINI ()
        except:
            self.ChangedFileINI = False
    #endfunction

    def DeleteSection (self, ASectionName: str):
        """DeleteSection"""
    #beginfunction
        if self.IsSection (ASectionName):
            self.remove_section(ASectionName)
            self.UpdateFileINI ()
        #endif
        self.ChangedFileINI = True
    #endfunction

    def DeleteOption (self, ASectionName: str, AOptionName: str):
        """DeleteOption"""
    #beginfunction
        if self.IsOption (ASectionName, AOptionName):
            self.remove_option(ASectionName, AOptionName)
            self.UpdateFileINI ()
        #endif
        self.ChangedFileINI = True
    #endfunction

#endclass

def CreateTINIFile () -> TINIFile:
    """CreateTINIFile"""
#beginfunction
    return TINIFile ()
#endfunction

GINIFile = CreateTINIFile ()

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
