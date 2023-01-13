#=======================================================================================
# LUVersion.py
#=======================================================================================

#------------------------------------------
# БИБЛИОТЕКИ python
#------------------------------------------
import os
import win32api

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------
import datetime

#(*
#1 VERSIONINFO
#FILEVERSION 1, 0, 0, 1
#PRODUCTVERSION 1, 0, 0, 1
#FILEFLAGSMASK VS_FFI_FILEFLAGSMASK
#FILEFLAGS VS_FF_PRERELEASE
#FILEOS VOS__WINDOWS32
#FILETYPE VFT_APP
#{
# BLOCK "StringFileInfo"
# {
#  BLOCK "041904E3"
#  {
#   VALUE "CompanyName", "\023# &\021  $ ?> #;LO=>2A:>9 >1;.\000"
#   VALUE "FileDescription", "\000"
#   VALUE "FileVersion", "1.0.0.1\000"
#   VALUE "InternalName", "\000"
#   VALUE "LegalCopyright", "\000"
#   VALUE "LegalTrademarks", "\000"
#   VALUE "OriginalFilename", "\000"
#   VALUE "ProductName", "\000"
#   VALUE "ProductVersion", "1.0.0.0\000"
#   VALUE "Comments", "\000"
#  }
# }
# BLOCK "VarFileInfo"
# {
#  VALUE "Translation", 1049, 1251
# }
#}
#*)
#(*
#  PVSFixedFileInfo = ^TVSFixedFileInfo;
#  {$EXTERNALSYM tagVS_FIXEDFILEINFO}
#  tagVS_FIXEDFILEINFO = packed record
#    dwSignature: DWORD;        { e.g. $feef04bd }
#    dwStrucVersion: DWORD;     { e.g. $00000042 = "0.42" }
#    dwFileVersionMS: DWORD;    { e.g. $00030075 = "3.75" }
#    dwFileVersionLS: DWORD;    { e.g. $00000031 = "0.31" }
#    dwProductVersionMS: DWORD; { e.g. $00030010 = "3.10" }
#    dwProductVersionLS: DWORD; { e.g. $00000031 = "0.31" }
#    dwFileFlagsMask: DWORD;    { = $3F for version "0.42" }
#    dwFileFlags: DWORD;        { e.g. VFF_DEBUG | VFF_PRERELEASE }
#    dwFileOS: DWORD;           { e.g. VOS_DOS_WINDOWS16 }
#    dwFileType: DWORD;         { e.g. VFT_DRIVER }
#    dwFileSubtype: DWORD;      { e.g. VFT2_DRV_KEYBOARD }
#    dwFileDateMS: DWORD;       { e.g. 0 }
#    dwFileDateLS: DWORD;       { e.g. 0 }
#  end;
#*)
#type
#   PTransInfo = ^TTransInfo;
#   TTransInfo = packed record
#      dwLang1: WORD;
#      dwLang2: WORD;
#   end;
#
#type
#   TVersionInfo = class(TComponent)
#   private
#      FFileName : PChar;
#      FInfo: Pointer;
#      FInfoSize: DWORD;
#      FTmp: DWORD;
#      FFileInfo: PVSFixedFileInfo;
#      FFileInfoSize: DWORD;
#      FTransInfo: PTransInfo;
#      FTransInfoSize: DWORD;
#      FFileVersion: PChar;
#      FCompanyName: PChar;
#      FFileDescription: PChar;
#      FInternalName: PChar;
#      FLegalCopyright: PChar;
#      FLegalTrademarks: PChar;
#      FOriginalFilename: PChar;
#      FProductName: PChar;
#      FProductVersion: PChar;
#      FComments: PChar;
#      FFileDate: TDateTime;
#      function GetFileName: string;
#      procedure SetFileName(Value: string);
#      function GetLangCharSet: string;
#      function GetMajor1: Integer;
#      function GetMajor2: Integer;
#      function GetMinor1: Integer;
#      function GetMinor2: Integer;
#      function GetLang1: Integer;
#      function GetLang2: Integer;
#      function GetFileVersion: string;
#      function GetFileDate: string;
#      function GetCompanyName: string;
#      function GetFileDescription: string;
#      function GetInternalName: string;
#      function GetLegalCopyright: string;
#      function GetLegalTrademarks: string;
#      function GetOriginalFilename: string;
#      function GetProductName: string;
#      function GetProductVersion: string;
#      function GetComments: string;
#      property Lang1 : Integer read GetLang1;
#      property Lang2 : Integer read GetLang2;
#      property LangCharSet : string read GetLangCharSet;
#   public
#      constructor Create(AOwner: Tcomponent); override;
#      destructor Destroy; override;
#      property FileName : string read GetFileName write SetFileName;
#      property Major1 : Integer read GetMajor1;
#      property Major2 : Integer read GetMajor2;
#      property Minor1 : Integer read GetMinor1;
#      property Minor2 : Integer read GetMinor2;
#      property FileVersion : string read GetFileVersion;
#      property FileDate : string read GetFileDate;
#      property CompanyName : string read GetCompanyName;
#      property FileDescription : string read GetFileDescription;
#      property InternalName : string read GetInternalName;
#      property LegalCopyright : string read GetLegalCopyright;
#      property LegalTrademarks : string read GetLegalTrademarks;
#      property OriginalFilename : string read GetOriginalFilename;
#      property ProductName : string read GetProductName;
#      property ProductVersion : string read GetProductVersion;
#      property Comments : string read GetComments;
#   end;
#var
#   VersionInfo: TVersionInfo;


class TVersionInfo:

    #--------------------------------------------------
    # static
    #--------------------------------------------------
    ruClassName = "TVersionInfo"
    
    #--------------------------------------------------
    # constructor
    #--------------------------------------------------
    def __init__(self):
        self.__FFileName = ''
        self.__FFileInfoSize = 0
        self.__FInfoSize = 0
        self.__FInfo = None
        self.__FFileInfo = None
        self.__FFileDate = 0
        self.__lang = ''
        self.__codepage = ''
        self.__FCompanyName = ''
        self.__FFileDescription = ''
        self.__FInternalName = ''
        self.__FLegalCopyright = ''
        self.__FLegalTrademarks = ''
        self.__FOriginalFilename = ''
        self.__FProductName = ''
        self.__FProductVersion = ''
        #self.__FFileDate = ''
        self.__FComments = ''
    #--------------------------------------------------
    # destructor
    #--------------------------------------------------
    def __del__(self):
        class_name = self.__class__.__name__  
        print('{} уничтожен'.format(class_name))
        pass

    #--------------------------------------------------
    # __FFileName
    #--------------------------------------------------
    # getter
    @property
    def GetFileName(self):
    #beginfunction
        return self.__FFileName
    #endfunction
    # setter
    @GetFileName.setter
    def GetFileName(self, Value: str):
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
        print (self.__FFileName)
        print (LFileTimeSource)
        print (self.__FFileDate)

        # Get the information
        #self.__FInfo = win32api.GetFileVersionInfo(self.__FFileName, 0, self.__FInfoSize, self.__FInfo)
        # backslash as parm returns dictionary of numeric info corresponding to VS_FIXEDFILEINFO struc
        self.__FInfo = win32api.GetFileVersionInfo (self.__FFileName, '\\')

        props ['FixedFileInfo'] = self.__FInfo
        print (props ['FixedFileInfo'])

        props ['FileVersion'] = "%d.%d.%d.%d" % (self.__FInfo ['FileVersionMS'] / 65536,
                                                 self.__FInfo ['FileVersionMS'] % 65536,
                                                 self.__FInfo ['FileVersionLS'] / 65536,
                                                 self.__FInfo ['FileVersionLS'] % 65536)
        print (props ['FileVersion'])

        # \VarFileInfo\Translation returns list of available (language, codepage)
        # pairs that can be used to retreive string info. We are using only the first pair.
        self.__lang, self.__codepage = win32api.GetFileVersionInfo (self.__FFileName, '\\VarFileInfo\\Translation') [0]
        print (self.__lang)
        print (self.__codepage)

        # any other must be of the form \StringfileInfo\%04X%04X\parm_name, middle
        # two are language/codepage pair returned from above

        strInfo = {}
        for propName in propNames:
            strInfoPath = u'\\StringFileInfo\\%04X%04X\\%s' % (self.__lang, self.__codepage, propName)
            ## print str_info
            strInfo [propName] = win32api.GetFileVersionInfo (self.__FFileName, strInfoPath)
            print (propName, strInfo [propName])

        props ['StringFileInfo'] = strInfo
        print (props ['StringFileInfo'])



        # Query the information for the version
        #VerQueryValue(FInfo, '\', Pointer(FFileInfo), FFileInfoSize)
        # Query
        #VerQueryValue(FInfo, '\VarFileInfo\Translation', pointer(FTransInfo), FTransInfoSize)
        # Query
        #VerQueryValue(FInfo, PChar('\StringFileInfo\'+LangCharSet+'\'+'FileVersion'), pointer(FFileVersion), FTmp);
        #VerQueryValue(FInfo, PChar('\StringFileInfo\'+LangCharSet+'\'+'CompanyName'), pointer(FCompanyName), FTmp);
        #VerQueryValue(FInfo, PChar('\StringFileInfo\'+LangCharSet+'\'+'FileDescription'), pointer(FFileDescription), FTmp);
        #VerQueryValue(FInfo, PChar('\StringFileInfo\'+LangCharSet+'\'+'InternalName'), pointer(FInternalName), FTmp);
        #VerQueryValue(FInfo, PChar('\StringFileInfo\'+LangCharSet+'\'+'LegalCopyright'), pointer(FLegalCopyright), FTmp);
        #VerQueryValue(FInfo, PChar('\StringFileInfo\'+LangCharSet+'\'+'LegalTrademarks'), pointer(FLegalTrademarks), FTmp);
        #VerQueryValue(FInfo, PChar('\StringFileInfo\'+LangCharSet+'\'+'OriginalFilename'), pointer(FOriginalFilename), FTmp);
        #VerQueryValue(FInfo, PChar('\StringFileInfo\'+LangCharSet+'\'+'ProductName'), pointer(FProductName), FTmp);
        #VerQueryValue(FInfo, PChar('\StringFileInfo\'+LangCharSet+'\'+'ProductVersion'), pointer(FProductVersion), FTmp);
        #VerQueryValue(FInfo, PChar('\StringFileInfo\'+LangCharSet+'\'+'Comments'), pointer(FComments), FTmp);
    #endfunction

    #--------------------------------------------------
    # 
    #--------------------------------------------------
    # getter
    @property
    def GetMajor1(self):
    #beginfunction
        LResult = 0
        #Result = self.__FFileInfo.dwFileVersionMS shr 16
        #LResult = self.__FInfo ['FileVersionMS'] / 65536
        return LResult
    #endfunction

    #--------------------------------------------------
    # 
    #--------------------------------------------------
    # getter
    @property
    def GetMajor2(self):
    #beginfunction
        LResult = 0
        #Result = self.__FFileInfo.dwFileVersionMS and $FFFF
        #LResult = self.__FInfo ['FileVersionMS'] % 65536
        return LResult
    #endfunction

    #--------------------------------------------------
    # 
    #--------------------------------------------------
    # getter
    @property
    def GetMinor1(self):
    #beginfunction
        LResult = 0
        #Result = self.__FFileInfo.dwFileVersionLS shr 16
        #LResult = self.__FInfo ['FileVersionLS'] / 65536
        return LResult
    #endfunction

    #--------------------------------------------------
    # 
    #--------------------------------------------------
    # getter
    @property
    def GetMinor2(self):
    #beginfunction
        LResult = 0
        #Result = self.__FFileInfo.dwFileVersionLS and $FFFF
        #LResult = self.__FInfo ['FileVersionLS'] % 65536
        return LResult
    #endfunction

    #--------------------------------------------------
    # 
    #--------------------------------------------------
    # getter
    @property
    def GetLang1(self):
    #beginfunction
        #Result = self.__FTransInfo.dwLang1
        LResult = ''
        return LResult
    #endfunction

    #--------------------------------------------------
    # 
    #--------------------------------------------------
    # getter
    @property
    def GetLang2(self):
    #beginfunction
        #Result = self.__FTransInfo.dwLang2
        LResult = ''
        return LResult
    #endfunction

    #--------------------------------------------------
    # 
    #--------------------------------------------------
    # getter
    @property
    def GetLangCharSet(self):
    #beginfunction
        #Result = IntToHex(Lang1,4)+IntToHex(Lang2,4)
        LResult = ''
        return LResult
    #endfunction

    #--------------------------------------------------
    # 
    #--------------------------------------------------
    # getter
    @property
    def GetFileVersion(self):
    #beginfunction
        #LResult = StrPas(self.__FFileVersion)
        LResult = ''
        return LResult
    #endfunction

    #--------------------------------------------------
    # 
    #--------------------------------------------------
    # getter
    @property
    def GetFileDate(self):
    #beginfunction
        LResult = self.__FFileDate
        return LResult
    #endfunction

    #--------------------------------------------------
    # 
    #--------------------------------------------------
    # getter
    @property
    def GetCompanyName(self):
    #beginfunction
        LResult = self.__FCompanyName
        return LResult
    #endfunction

    #--------------------------------------------------
    # 
    #--------------------------------------------------
    # getter
    @property
    def GetFileDescription(self):
    #beginfunction
        LResult = self.__FFileDescription
        return LResult
    #endfunction

    #--------------------------------------------------
    # 
    #--------------------------------------------------
    # getter
    @property
    def GetInternalName(self):
    #beginfunction
        LResult = self.__FInternalName
        return LResult
    #endfunction

    #--------------------------------------------------
    # 
    #--------------------------------------------------
    # getter
    @property
    def GetLegalCopyright(self):
    #beginfunction
        LResult = self.__FLegalCopyright
        return LResult
    #endfunction

    #--------------------------------------------------
    # 
    #--------------------------------------------------
    # getter
    @property
    def GetLegalTrademarks(self):
    #beginfunction
        LResult = self.__FLegalTrademarks
        return LResult
    #endfunction

    #--------------------------------------------------
    # 
    #--------------------------------------------------
    # getter
    @property
    def GetOriginalFilename(self):
    #beginfunction
        LResult = self.__FOriginalFilename
        return LResult
    #endfunction

    #--------------------------------------------------
    # 
    #--------------------------------------------------
    # getter
    @property
    def GetProductName(self):
    #beginfunction
        LResult = self.__FProductName
        return LResult
    #endfunction

    #--------------------------------------------------
    # 
    #--------------------------------------------------
    # getter
    @property
    def GetProductVersion(self):
    #beginfunction
        LResult = self.__FProductVersion
        return LResult
    #endfunction

    #--------------------------------------------------
    # 
    #--------------------------------------------------
    # getter
    @property
    def GetComments(self):
    #beginfunction
        LResult = self.__FComments
        return LResult
    #endfunction

#-------------------------------------------------------------------------------
# CreateVersion (AFileName: str): -> TVersionInfo
#-------------------------------------------------------------------------------
def CreateVersion (AFileName: str):
#beginfunction
   LResult = TVersionInfo ()
   LResult.__FFileName = AFileName
   return LResult
#endfunction

#------------------------------------------
#
#------------------------------------------
#beginmodule
if __name__ == "__main__":
    ...
#endif

#endmodule

