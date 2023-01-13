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
#print(PYDir)
#print(sys.path)
#------------------------------------------
P1 = 'C:\\Program Files\\Far Manager\\Far.exe'
if args.P1 != '':
    P1 = args.P1
#endif
#------------------------------------------

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
        VersionInfo = LUVersion.TVersionInfo()
        VersionInfo.FileName = P1
        print('FileName         : {0}'.format(VersionInfo.FileName))
        print('FileVersion      : {0}'.format(VersionInfo.FileVersion))
        print('FileDate         : {0}'.format(VersionInfo.FileDate))
        print('CompanyName      : {0}'.format(VersionInfo.CompanyName))
        print('FileDescription  : {0}'.format(VersionInfo.FileDescription))
        print('InternalName     : {0}'.format(VersionInfo.InternalName))
        print('LegalCopyright   : {0}'.format(VersionInfo.LegalCopyright))
        print('LegalTrademarks  : {0}'.format(VersionInfo.LegalTrademarks))
        print('OriginalFilename : {0}'.format(VersionInfo.OriginalFilename))
        print('ProductName      : {0}'.format(VersionInfo.ProductName))
        print('ProductVersion   : {0}'.format(VersionInfo.ProductVersion))
        print('Comments         : {0}'.format(VersionInfo.Comments))
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
