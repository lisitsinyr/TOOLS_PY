"""DirectoryRename.py"""
# -*- coding: UTF-8 -*-
__annotations__ = """
 =======================================================
 Copyright (c) 2025
 Author:
     Lisitsin Y.R.
 Project:
     SCRIPTS_PY
 Module:
     DirectoryRename.py
 =======================================================
"""

#------------------------------------------
# БИБЛИОТЕКИ python
#------------------------------------------
import os
import sys
import argparse
import time
from pathlib import Path
import psutil

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------

#------------------------------------------
# БИБЛИОТЕКА lyrpy
#------------------------------------------
import lyrpy.LUos as LUos
import lyrpy.LUDoc as LUDoc
import lyrpy.LULog as LULog
import lyrpy.LUConst as LUConst
import lyrpy.LUDoc as LUDoc
import lyrpy.LULog as LULog
import lyrpy.LUFile as LUFile
import lyrpy.LUParserARG as LUParserARG

def find_directory(directory_name, search_path):
    """find_directory"""
    """
    Функция для поиска каталога по имени в указанной директории.
    :param directory_name: Имя искомого каталога.
    :param search_path: Путь, где будет производиться поиск.
    :return: Список путей к найденным каталогам.
    """
#beginfunction
    found_directories = []
    for root, dirs, files in os.walk(search_path):
        if directory_name in dirs:
            s = os.path.join(root, directory_name)
            sys.stdout.write (s)
            sys.stdout.flush ()
            # time.sleep (1)
            sys.stdout.write ('\r')
            # found_directories.append(os.path.join(root, directory_name))
            found_directories.append(root)
    return found_directories
#endfunction

#------------------------------------------
def main ():
    """main"""
#beginfunction
    LUConst.SET_LIB(__file__)

    LULog.STARTLogging (LULog.TTypeSETUPLOG.tslINI, 'console', LUConst.GDirectoryLOG, LUConst.GFileNameLOG,
                        LUConst.GFileNameLOGjson)
    LULog.LoggerTOOLS.level = logging.INFO

    # Путь, где будет производиться поиск (например, корневой каталог C:)
    Lsearch_path = r"D:\PROJECTS_LYR\CHECK_LIST\DESKTOP\Python\PROJECTS_PY"
    # Имя искомого каталога
    Ldirectory_name = "INFO"
    Ldirectory_name_new = ".INFO"

    # s = f'sys.argv = {sys.argv}'
    # print(s)

    LArgParser = argparse.ArgumentParser (description='Параметры', prefix_chars='-/')
    LArgParser.add_argument ('search_path', type = str, default='..', help = 'search_path')
    LArgParser.add_argument ('directory_name', type = str, default='', help = 'directory_name')
    LArgParser.add_argument ('directory_name_new', type = str, default='', help = 'directory__new')
    Largs = LArgParser.parse_args ()
    Lsearch_path = Largs.search_path
    # print(f'Lsearch_path:{Lsearch_path}')
    Ldirectory_name = Largs.directory_name
    # print(f'Ldirectory_name:{Ldirectory_name}')
    Ldirectory_name_new = Largs.directory_name_new
    # print(f'Ldirectory_name_new:{Ldirectory_name_new}')


    Lfound_directories = find_directory (Ldirectory_name, Lsearch_path)
    if found_directories:
        print (f"Найдены следующие каталоги с именем '{Ldirectory_name}':")
        for dir_path in Lfound_directories:
            # Старое имя каталога
            Lold_name = Path (os.path.join (dir_path, Ldirectory_name))
            # Новое имя каталога
            Lnew_name = Path (os.path.join (dir_path, Ldirectory_name_new))
            if not Lnew_name.exists ():
                # os.rename (Lold_name, Lnew_name)
                print (Lold_name)
                print (Lnew_name)
                Lold_name.rename (Lnew_name)
            else:
                print ("Каталог с таким именем уже существует.")
    else:
        print (f"Каталог с именем '{Ldirectory_name}' не найден.")

    LULog.STOPLogging ()
#endfunction

# ------------------------------------------
#
# ------------------------------------------
# beginmodule
if __name__ == "__main__":
    print (psutil.cpu_stats())
    main ()
# endif
# endmodule
