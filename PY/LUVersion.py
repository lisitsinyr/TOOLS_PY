"""LUVersion.py"""
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
     LUVersion.py

 =======================================================
"""
#------------------------------------------
# БИБЛИОТЕКИ python
#------------------------------------------
import os
import win32api

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------
import datetime

#------------------------------------------
# БИБЛИОТЕКА LU
#------------------------------------------
import LULog
import LUConst

class TVersionInfo:
    """TVersionInfo"""
    luClassName = "TVersionInfo"
    
    #--------------------------------------------------
    # constructor
    #--------------------------------------------------
    def __init__(self):
        self.__FFileName = ''
        self.__FInfo = None
        self.__FFileDate = 0
        self.__FFileVersion = ''
        self.__FFileInfoSize = 0
        self.__FInfoSize = 0
        self.__FFileInfo = None
        self.__FCompanyName = ''
        self.__FFileDescription = ''
        self.__FInternalName = ''
        self.__FLegalTrademarks = ''
        self.__FLegalCopyright = ''
        self.__FProductName = ''
        self.__FOriginalFilename = ''
        self.__FProductVersion = ''
        self.__FComments = ''

        self.__lang = ''
        self.__codepage = ''

        self.__FTmp = None
        self.__FTransInfo = None
        self.__FTransInfoSize = 0

    #--------------------------------------------------
    # destructor
    #--------------------------------------------------
    def __del__(self):
    #beginfunction
        LClassName = self.__class__.__name__
        s = '{} уничтожен'.format (LClassName)
        # LUConst.LULogger.log (LULog.DEBUGTEXT, s)
        print (s)
    #endfunction

    #--------------------------------------------------
    # @property FileName
    #--------------------------------------------------
    # getter
    @property
    def FileName(self):
    #beginfunction
        return self.__FFileName
    #endfunction
    # setter
    @FileName.setter
    def FileName(self, Value: str):
        propNames = ('Comments', 'InternalName', 'ProductName',
                     'CompanyName', 'LegalCopyright', 'ProductVersion',
                     'FileDescription', 'LegalTrademarks', 'PrivateBuild',
                     'FileVersion', 'OriginalFilename', 'SpecialBuild')

        props = {'FixedFileInfo': None, 'StringFileInfo': None, 'FileVersion': None}
    #beginfunction
        if Value == '':
            return
        self.__FFileName = Value
        # Get the size of the FileVersionInformatioin
        if self.__FInfoSize > 0:
            pass
        #self.__FInfoSize = win32api.GetFileVersionInfoSize(self.__FFileName.encode(), None)
        # If InfoSize = 0, then the file may not exist, or
        # it may not have file version information in it.
        #if self.__FInfoSize == 0:
        #    raise Exception.Create("Can''t get file version information for "+self.__FFileName)

        #file modification
        #self.__FFileDate = FileDateToDateTime(FileAge(Value))
        LFileTimeSource = os.path.getmtime(self.__FFileName)
        #convert timestamp into DateTime object
        self.__FFileDate = datetime.datetime.fromtimestamp(LFileTimeSource)

        # Get the information
        #self.__FInfo = win32api.GetFileVersionInfo(self.__FFileName, 0, self.__FInfoSize, self.__FInfo)
        # backslash as parm returns dictionary of numeric info corresponding to VS_FIXEDFILEINFO struc
        self.__FInfo = win32api.GetFileVersionInfo (self.__FFileName, '\\')
        props ['FixedFileInfo'] = self.__FInfo
        props ['FileVersion'] = "%d.%d.%d.%d" % (self.__FInfo ['FileVersionMS'] / 65536,
                                                 self.__FInfo ['FileVersionMS'] % 65536,
                                                 self.__FInfo ['FileVersionLS'] / 65536,
                                                 self.__FInfo ['FileVersionLS'] % 65536)
        self.__FFileVersion = props ['FileVersion']

        # \VarFileInfo\Translation returns list of available (language, codepage)
        # pairs that can be used to retreive string info. We are using only the first pair.
        self.__lang, self.__codepage = win32api.GetFileVersionInfo (self.__FFileName, '\\VarFileInfo\\Translation') [0]
        #print ('__lang = ',self.__lang)
        #print ('__codepage = ', self.__codepage)

        # any other must be of the form \StringfileInfo\%04X%04X\parm_name, middle
        # two are language/codepage pair returned from above
        strInfo = {}
        for propName in propNames:
            strInfoPath = u'\\StringFileInfo\\%04X%04X\\%s' % (self.__lang, self.__codepage, propName)
            ## print str_info
            strInfo [propName] = win32api.GetFileVersionInfo (self.__FFileName, strInfoPath)
        props ['StringFileInfo'] = strInfo
        self.__FCompanyName = strInfo ['CompanyName']
        self.__FFileDescription = strInfo ['FileDescription']
        self.__FInternalName = strInfo ['InternalName']
        self.__FLegalCopyright = strInfo ['LegalCopyright']
        self.__FLegalTrademarks = strInfo ['LegalTrademarks']
        self.__FOriginalFilename = strInfo ['OriginalFilename']
        self.__FProductName = strInfo ['ProductName']
        self.__FProductVersion = strInfo ['ProductVersion']
        self.__FComments = strInfo ['Comments']
    #endfunction

    #--------------------------------------------------
    # @property Major1
    #--------------------------------------------------
    # getter
    @property
    def Major1(self):
    #beginfunction
        LResult = int(self.__FInfo ['FileVersionMS'] / 65536)
        return LResult
    #endfunction

    #--------------------------------------------------
    # @property Major2
    #--------------------------------------------------
    # getter
    @property
    def Major2(self):
    #beginfunction
        LResult = int(self.__FInfo ['FileVersionMS'] % 65536)
        return LResult
    #endfunction

    #--------------------------------------------------
    # @property Minor1
    #--------------------------------------------------
    # getter
    @property
    def Minor1(self):
    #beginfunction
        LResult = int(self.__FInfo ['FileVersionLS'] / 65536)
        return LResult
    #endfunction

    #--------------------------------------------------
    # @property Minor2
    #--------------------------------------------------
    # getter
    @property
    def Minor2(self):
    #beginfunction
        LResult = int(self.__FInfo ['FileVersionLS'] % 65536)
        return LResult
    #endfunction

    #--------------------------------------------------
    # @property Lang1
    #--------------------------------------------------
    # getter
    @property
    def Lang1(self):
    #beginfunction
        #Result = self.__FTransInfo.dwLang1
        LResult = ''
        return LResult
    #endfunction

    #--------------------------------------------------
    # @property Lang2
    #--------------------------------------------------
    # getter
    @property
    def Lang2(self):
    #beginfunction
        #Result = self.__FTransInfo.dwLang2
        LResult = ''
        return LResult
    #endfunction

    #--------------------------------------------------
    # @property LangCharSet
    #--------------------------------------------------
    # getter
    @property
    def LangCharSet(self):
    #beginfunction
        #Result = IntToHex(Lang1,4)+IntToHex(Lang2,4)
        LResult = ''
        return LResult
    #endfunction

    #--------------------------------------------------
    # @property FileVersion
    #--------------------------------------------------
    # getter
    @property
    def FileVersion(self):
    #beginfunction
        LResult = self.__FFileVersion
        return LResult
    #endfunction

    #--------------------------------------------------
    # @property FileDate
    #--------------------------------------------------
    # getter
    @property
    def FileDate(self):
    #beginfunction
        LResult = self.__FFileDate
        return LResult
    #endfunction

    #--------------------------------------------------
    # @property CompanyName
    #--------------------------------------------------
    # getter
    @property
    def CompanyName(self):
    #beginfunction
        LResult = self.__FCompanyName
        return LResult
    #endfunction

    #--------------------------------------------------
    # @property FileDescription
    #--------------------------------------------------
    # getter
    @property
    def FileDescription(self):
    #beginfunction
        LResult = self.__FFileDescription
        return LResult
    #endfunction

    #--------------------------------------------------
    # @property InternalName
    #--------------------------------------------------
    # getter
    @property
    def InternalName(self):
    #beginfunction
        LResult = self.__FInternalName
        return LResult
    #endfunction

    #--------------------------------------------------
    # @property LegalCopyright
    #--------------------------------------------------
    # getter
    @property
    def LegalCopyright(self):
    #beginfunction
        LResult = self.__FLegalCopyright
        return LResult
    #endfunction

    #--------------------------------------------------
    # @property LegalTrademarks
    #--------------------------------------------------
    # getter
    @property
    def LegalTrademarks(self):
    #beginfunction
        LResult = self.__FLegalTrademarks
        return LResult
    #endfunction

    #--------------------------------------------------
    # @property OriginalFilename
    #--------------------------------------------------
    # getter
    @property
    def OriginalFilename(self):
    #beginfunction
        LResult = self.__FOriginalFilename
        return LResult
    #endfunction

    #--------------------------------------------------
    # @property ProductName
    #--------------------------------------------------
    # getter
    @property
    def ProductName(self):
    #beginfunction
        LResult = self.__FProductName
        return LResult
    #endfunction

    #--------------------------------------------------
    # @property ProductVersion
    #--------------------------------------------------
    # getter
    @property
    def ProductVersion(self):
    #beginfunction
        LResult = self.__FProductVersion
        return LResult
    #endfunction

    #--------------------------------------------------
    # @property Comments
    #--------------------------------------------------
    # getter
    @property
    def Comments(self):
    #beginfunction
        LResult = self.__FComments
        return LResult
    #endfunction
#endclass

#-------------------------------------------------------------------------------
# CreateVersion (AFileName: str): -> TVersionInfo
#-------------------------------------------------------------------------------
def CreateVersion (AFileName: str) -> TVersionInfo:
    """CreateVersion"""
#beginfunction
    LResult:TVersionInfo = TVersionInfo ()
    LResult.__FFileName = AFileName
    return LResult
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
