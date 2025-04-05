"""CryptoTEXT1.py"""
# -*- coding: UTF-8 -*-
__annotations__ = """
 =======================================================
 Copyright (c) 2025
 Author:
     Lisitsin Y.R.
 Project:
     SCRIPTS_PY
 Module:
     CryptoTEXT1.py
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
    # get the plaintext
    # plain_text = sys.argv[1]
    plain_text = 'Тестовое сообщение'

    # The key length must be 16 (AES-128), 24 (AES-192), or 32 (AES-256) Bytes.
    key = b'this is a 16 key'

    # Generate a non-repeatable key vector with a length
    # equal to the size of the AES block
    iv = Random.new().read(AES.block_size)

    # Use key and iv to initialize AES object, use MODE_CFB mode
    mycipher = AES.new(key, AES.MODE_CFB, iv)

    # Add iv (key vector) to the beginning of the encrypted ciphertext
    # and transmit it together
    ciphertext = iv + mycipher.encrypt(plain_text.encode())

    # To decrypt, use key and iv to generate a new AES object
    mydecrypt = AES.new(key, AES.MODE_CFB, ciphertext[:16])

    # Use the newly generated AES object to decrypt the encrypted ciphertext
    decrypttext = mydecrypt.decrypt(ciphertext[16:])

    # output
    file_out = open("encrypted.bin", "wb")
    file_out.write(ciphertext[16:])
    file_out.close()

    print("The key k is: ", key)
    print("iv is: ", b2a_hex(ciphertext)[:16])
    print("The encrypted data is: ", b2a_hex(ciphertext)[16:])
    print("The decrypted data is: ", decrypttext.decode())

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
