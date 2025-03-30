"""seedir_py.py"""
# -*- coding: UTF-8 -*-
__annotations__ = """
 =======================================================
 Copyright (c) 2025
 Author:
     Lisitsin Y.R.
 Project:
     SCRIPTS_PY
 Module:
     seedir_py.py
 =======================================================
"""

#------------------------------------------
# БИБЛИОТЕКИ python
#------------------------------------------
import os
import sys
import argparse
import logging
import shutil

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------
import seedir as sd
import pandas as pd

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

data = []

#------------------------------------------
# func_pass ()
#------------------------------------------
def func_pass():
    """func_pass"""
#beginfunction
    pass
#endfunction

#------------------------------------------
# func_os_walk ()
#------------------------------------------
def func_os_walk(start_path):
    """func_os_walk"""
#beginfunction
    for root, dirs, files in os.walk(start_path):
        level = root.replace(start_path, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
    #endfor
#endfunction


#------------------------------------------
# list_files_folders ()
#------------------------------------------
def list_files_folders(start_path):
    """func_os_walk"""
#beginfunction
    for root, dirs, files in os.walk(start_path):
        level = root.replace(start_path, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print(f'{indent}{os.path.basename(root)}/')
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print(f'{subindent}{f}')
    #endfor
#endfunction

def build_tree(root, level):
    folder = os.path.basename(root)
    parent = os.path.dirname(root)
    parent_folder = parent.split('/')[-1]
    # print(level, folder, parent_folder)
    return [level, folder, parent_folder]

def list_folders(start_path):
    for root, dirs, files in os.walk(start_path):
        level = root.replace(start_path, '').count(os.sep)
        indent = ' ' * 4 * (level)
        subindent = ' ' * 4 * (level + 1)
        data.append(build_tree(root, level))

#------------------------------------------
def main ():
    """main"""
#beginfunction
    LUConst.SET_LIB(__file__)

    LULog.STARTLogging (LULog.TTypeSETUPLOG.tslINI, 'console', LUConst.GDirectoryLOG, LUConst.GFileNameLOG,
                        LUConst.GFileNameLOGjson)
    LULog.LoggerTOOLS.level = logging.INFO

    LPath = LUFile.ExtractFileDir(__file__)
    print(f'LPath: {LPath}')

    path = r'D:\WORK'

    # sd.seedir(path=path, style='lines',  exclude_folders='.git')    

    # func_os_walk (path)

    # sd.seedir(path=path, style='lines', itemlimit=10, depthlimit=2, exclude_folders='.git')

    # sd.seedir(path=path, style='emoji',  exclude_folders='Packages')

    # list_files_folders (path)


    list_folders(path)          

    df = pd.DataFrame(data)
    df.columns = ['level', 'name', 'parent']
    df.to_csv(r'D:\PROJECTS_LYR\CHECK_LIST\DESKTOP\Python\PROJECTS_PY\SCRIPTS_PY\SRC\00.TEST\SeeDir\seedir_py\test.csv', index=False)
    df.to_json (r'D:\PROJECTS_LYR\CHECK_LIST\DESKTOP\Python\PROJECTS_PY\SCRIPTS_PY\SRC\00.TEST\SeeDir\seedir_py\test.json')

    LULog.STOPLogging ()
#endfunction

#------------------------------------------
#
#------------------------------------------
#beginmodule
if __name__ == "__main__":
    main()
#endif

#endmodule


