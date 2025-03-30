"""DirectorySync.py"""
# -*- coding: UTF-8 -*-
__annotations__ = """
 =======================================================
 Copyright (c) 2025
 Author:
     Lisitsin Y.R.
 Project:
     SCRIPTS_PY
 Module:
     DirectorySync.py
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
import filecmp

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------
from tqdm import tqdm

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

#------------------------------------------
# func_pass ()
#------------------------------------------
def func_pass():
    """func_pass"""
#beginfunction
    pass
#endfunction

#-----------------------------------------------------------
# check_directories(src_dir, dst_dir)
#-----------------------------------------------------------
def check_directories(src_dir, dst_dir):
    """func_pass"""
    # Function to check if the source and destination directories exist
#beginfunction
    # Check if the source directory exists
    if not os.path.exists(src_dir):
        print(f"\nSource directory '{src_dir}' does not exist.")
        return False
    #endif

    # Create the destination directory if it does not exist
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
        print(f"\nDestination directory '{dst_dir}' created.")
    #endif
    return True
#endfunction

#-----------------------------------------------------------
# sync_directories(src_dir, dst_dir, delete=False)
#-----------------------------------------------------------
def sync_directories(src_dir, dst_dir, delete=False):
    """sync_directories"""
    # Function to synchronize files between two directories
    # Get a list of all files and directories in the source directory
#beginfunction
    files_to_sync = []
    for root, dirs, files in os.walk(src_dir):
        for directory in dirs:
            files_to_sync.append(os.path.join(root, directory))
        #endfor
        for file in files:
            files_to_sync.append(os.path.join(root, file))
        #endfor
    #endfor

    # Iterate over each file in the source directory with a progress bar
    with tqdm(total=len(files_to_sync), desc="Syncing files", unit="file") as pbar:
        # Iterate over each file in the source directory
        for source_path in files_to_sync:
            # Get the corresponding path in the replica directory
            replica_path = os.path.join(dst_dir, os.path.relpath(source_path, src_dir))

            # Check if path is a directory and create it in the replica directory if it does not exist
            if os.path.isdir(source_path):
                if not os.path.exists(replica_path):
                    os.makedirs(replica_path)
                #endif
            #endif

            # Copy all files from the source directory to the replica directory
            else:
                # Check if the file exists in the replica directory and if it is different from the source file
                if not os.path.exists(replica_path) or not filecmp.cmp(source_path, replica_path, shallow=False):
                    # Set the description of the progress bar and print the file being copied
                    pbar.set_description(f"Processing '{source_path}'")
                    print(f"\nCopying {source_path} to {replica_path}")

                    # Copy the file from the source directory to the replica directory
                    shutil.copy2(source_path, replica_path)
                # endif
            #endif
            # Update the progress bar
            pbar.update(1)
    #endwith

    #-----------------------------------------------------------
    # Шаг 3, Удалить лишние файлы
    # Clean up files in the destination directory that are not in the source directory, if delete flag is set
    #-----------------------------------------------------------
    if delete:
        # Get a list of all files in the destination directory
        files_to_delete = []
        for root, dirs, files in os.walk(dst_dir):
            for directory in dirs:
                files_to_delete.append(os.path.join(root, directory))
            #endfor
            for file in files:
                files_to_delete.append(os.path.join(root, file))
            #endfor
        #endfor

        # Iterate over each file in the destination directory with a progress bar
        with tqdm(total=len(files_to_delete), desc="Deleting files", unit="file") as pbar:
            # Iterate over each file in the destination directory
            for replica_path in files_to_delete:
                # Check if the file exists in the source directory
                source_path = os.path.join(src_dir, os.path.relpath(replica_path, dst_dir))
                if not os.path.exists(source_path):
                    # Set the description of the progress bar
                    pbar.set_description(f"Processing '{replica_path}'")
                    print(f"\nDeleting {replica_path}")

                    # Check if the path is a directory and remove it
                    if os.path.isdir(replica_path):
                        shutil.rmtree(replica_path)
                    else:
                        # Remove the file from the destination directory
                        os.remove(replica_path)
                    #endif
                # endif

                # Update the progress bar
                pbar.update(1)
            #endfor
        #endwith
#endfunction

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

    source_directory = r'D:\WORK\EXAMPLES_PY'
    destination_directory = r'G:\WORK\EXAMPLES_PY'

    #--------------------------------------------------------------
    # Шаг 1. Проверить и подготовить каталоги
    # Check the source and destination directories
    #--------------------------------------------------------------
    if not check_directories(source_directory, destination_directory):
        exit(1)

    #--------------------------------------------------------------
    # Шаг 2. Синхронизировать файлы между каталогами
    # Synchronize the directories
    #--------------------------------------------------------------
    sync_directories(source_directory, destination_directory)
    print("\nSynchronization complete.")
    
    LULog.STOPLogging ()
#endfunction

#------------------------------------------
#
#------------------------------------------
#beginmodule
if __name__ == "__main__":
    main ()
# endif

# endmodule
