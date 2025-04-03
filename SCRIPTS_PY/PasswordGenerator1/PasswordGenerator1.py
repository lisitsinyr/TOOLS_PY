"""PasswordGenerator1.py"""
# -*- coding: UTF-8 -*-
__annotations__ = """
 =======================================================
 Copyright (c) 2025
 Author:
     Lisitsin Y.R.
 Project:
     SCRIPTS_PY
 Module:
     PasswordGenerator1.py
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
import psutil

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------
import random
import string
import tkinter as tk
import pyperclip

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

root = tk.Tk()
root.geometry('500x500')
root.title('PASSWORD GENERATOR')

letters = string.ascii_letters
digits = string.digits
special_chars = string.punctuation

alphabet = letters + digits + special_chars

pwd_length = ''
pwd = ''

#------------------------------------------
# create_pass ()
#------------------------------------------
def create_pass():
    """create_pass"""
#beginfunction
    global alphabet
    global pwd_length
    global pwd
    pwd_length = int(pass_length.get())
    pwd = ''
    for i in range(pwd_length):
        pwd += ''.join(random.choice(alphabet))
    text_result.config(text=pwd)
#endfunction

#------------------------------------------
# copy_pwd ()
#------------------------------------------
def copy_pwd():
    """copy_pwd"""
#beginfunction
    if pwd == '':
        lbl_alert.config(text='Create a password first')
    else:
        pyperclip.copy(pwd)
        lbl_alert.config(text='Succesfuly copied')
#endfunction

#------------------------------------------
def main ():
    """main"""
#beginfunction
    global text_result
    global pass_length
    global lbl_alert

    LUConst.SET_LIB(__file__)

    LULog.STARTLogging (LULog.TTypeSETUPLOG.tslINI, 'console', LUConst.GDirectoryLOG, LUConst.GFileNameLOG,
                        LUConst.GFileNameLOGjson)
    LULog.LoggerTOOLS.level = logging.INFO

    LPath = LUFile.ExtractFileDir(__file__)
    print(f'LPath: {LPath}')

    #--------------------------------------------------------------
    # 
    #--------------------------------------------------------------
    text_result = tk.Label(root, text='')
    text_result.pack()

    pass_length = tk.Entry(root)
    pass_length.pack()

    btn = tk.Button(root, text='Start', command=create_pass)
    btn.pack()

    btn_copy = tk.Button(root, text='Copy to clipboard', command=copy_pwd)
    btn_copy.pack()

    lbl_alert = tk.Label(root, text='')
    lbl_alert.pack()

    root.mainloop()
    
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
