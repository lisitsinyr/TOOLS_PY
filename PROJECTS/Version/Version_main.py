#=======================================================================================
# Version_main.py
#=======================================================================================

#------------------------------------------
# БИБЛИОТЕКИ python
#------------------------------------------
import sys

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------
import argparse


#------------------------------------------
# Разбор аргументов
#------------------------------------------
parser = argparse.ArgumentParser(description='Параметры')
parser.add_argument('-PYDir', type=str, nargs='?', default='', dest='PYDir', help='Библиотека')
parser.add_argument('-P1', type=str, nargs='?', default='', dest='P1', help='P1')
args = parser.parse_args()
print('-PYDir  = '+args.PYDir)
print('-P1 = ',args.P1)
#------------------------------------------
PYDir = 'D:\\PROJECTS_LYR\\CHECK_LIST\\05_DESKTOP\\02_Python\\PROJECTS_PY\\TOOLS_PY\\PY'
if args.PYDir != "":
    PYDir = args.PYDir
#endif
sys.path.append(PYDir)
print(PYDir)
print(sys.path)
#------------------------------------------
P1 = 'C:\\Program Files\\Far Manager\\Far.exe'
if args.P1 != '':
    P1 = args.P1
#endif
#------------------------------------------
print('P1 = ',P1)

#------------------------------------------
#БИБЛИОТЕКА LU
#------------------------------------------
import LUVersion
#------------------------------------------

#------------------------------------------
# main():
#------------------------------------------
def main():
#beginfunction
    if P1 != '':
        print (P1)
        VersionInfo = LUVersion.TVersionInfo()
        VersionInfo.FFileName = P1
        print('FileName         : {0} {1:d} {2:d} {3:d} {4:d}'.format(
            VersionInfo.FFileName, VersionInfo.GetMajor1,
            VersionInfo.GetMajor2, VersionInfo.GetMinor1, VersionInfo.GetMinor2
            ))
        print('FileVersion      : {0}'.format(VersionInfo.GetFileVersion))
        print('FileDate         : {0}'.format(VersionInfo.GetFileDate))
        print('CompanyName      : {0}'.format(VersionInfo.GetCompanyName))
        print('FileDescription  : {0}'.format(VersionInfo.GetFileDescription))
        print('InternalName     : {0}'.format(VersionInfo.GetInternalName))
        print('LegalCopyright   : {0}'.format(VersionInfo.GetLegalCopyright))
        print('LegalTrademarks  : {0}'.format(VersionInfo.GetLegalTrademarks))
        print('OriginalFilename : {0}'.format(VersionInfo.GetOriginalFilename))
        print('ProductName      : {0}'.format(VersionInfo.GetProductName))
        print('ProductVersion   : {0}'.format(VersionInfo.GetProductVersion))
        print('Comments         : {0}'.format(VersionInfo.GetComments))
        del VersionInfo
    else:
        print ('файл не задан')
#endif
#endfunction

#------------------------------------------
#
#------------------------------------------
#beginmodule
if __name__ == "__main__":
    main()
#endif

#endmodule
