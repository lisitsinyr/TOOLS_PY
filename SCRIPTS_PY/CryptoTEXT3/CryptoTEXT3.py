"""CryptoTEXT3.py"""
# -*- coding: UTF-8 -*-
__annotations__ = """
 =======================================================
 Copyright (c) 2025
 Author:
     Lisitsin Y.R.
 Project:
     SCRIPTS_PY
 Module:
     CryptoTEXT3.py
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

import random
from tkinter import *
from tkinter import messagebox
import pyperclip

import os
import shutil
from datetime import datetime

from Crypto.Cipher import AES
from Crypto import Random
from binascii import b2a_hex
import sys

from cryptography.fernet import Fernet

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
# process () -> None:
#------------------------------------------
def process () -> None:
    """process"""
#beginfunction
    pass
#endfunction

class Encrypt:
    def __init__(self):
        self.send = ""
        self.res = []

    # Sender encrypts the data
    def sender(self):
        self.send = input("Enter the data: ")
        self.res = [ord(i) + 2 for i in self.send]
        print("Encrypted data:", "".join(chr(i) for i in self.res))

class Decrypt (Encrypt):
    # Receiver decrypts the data
    def receiver(self):
        decrypted_data = "".join(chr(i - 2) for i in self.res)
        print("Decrypted data: ", decrypted_data)

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
    # Usage
    obj = Decrypt()
    obj.sender()
    obj.receiver()

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
