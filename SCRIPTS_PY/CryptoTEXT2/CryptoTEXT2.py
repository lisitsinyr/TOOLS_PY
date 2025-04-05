"""CryptoTEXT2.py"""
# -*- coding: UTF-8 -*-
__annotations__ = """
 =======================================================
 Copyright (c) 2025
 Author:
     Lisitsin Y.R.
 Project:
     SCRIPTS_PY
 Module:
     CryptoTEXT2.py
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

#------------------------------------------
# generate_key():
#------------------------------------------
def generate_key():
    """process"""
    """Генерирует и сохраняет ключ шифрования в файл."""
#beginfunction
    key = Fernet.generate_key()
    Lsecret_key = r'D:\PROJECTS_LYR\CHECK_LIST\DESKTOP\Python\PROJECTS_PY\SCRIPTS_PY\SRC\00.TEST\CryptoTEXT2\secret.key'
    with open(Lsecret_key, "wb") as key_file:
        key_file.write(key)
    print("Ключ успешно сгенерирован и сохранен в файл 'secret.key'.")

#------------------------------------------
# load_key():
#------------------------------------------
def load_key():
    """process"""
    """Загружает ключ шифрования из файла."""
#beginfunction
    Lsecret_key = r'D:\PROJECTS_LYR\CHECK_LIST\DESKTOP\Python\PROJECTS_PY\SCRIPTS_PY\SRC\00.TEST\CryptoTEXT2\secret.key'
    try:
        with open(Lsecret_key, "rb") as key_file:
            return key_file.read()
    except FileNotFoundError:
        print("Ключ не найден. Сначала создайте его.")
        return None

#------------------------------------------
# encrypt_message(message, key):
#------------------------------------------
def encrypt_message(message, key):
    """process"""
    """Шифрует сообщение с использованием ключа."""
#beginfunction
    fernet = Fernet(key)
    return fernet.encrypt(message.encode()).decode()

#------------------------------------------
# decrypt_message(encrypted_message, key):
#------------------------------------------
def decrypt_message(encrypted_message, key):
    """process"""
    """Расшифровывает сообщение с использованием ключа."""
#beginfunction
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_message.encode()).decode()

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
    print("Программа: Шифрование и дешифрование текста")
    while True:
        print("\nМеню:")
        print("1. Создать ключ шифрования")
        print("2. Зашифровать сообщение")
        print("3. Расшифровать сообщение")
        print("4. Выйти")
        choice = input("Выберите действие (1-4): ").strip()

        if choice == "1":
            generate_key()
        elif choice in ["2", "3"]:
            key = load_key()
            if key:
                if choice == "2":
                    message = input("Введите сообщение для шифрования: ").strip()
                    encrypted = encrypt_message(message, key)
                    print(f"Зашифрованное сообщение: {encrypted}")
                elif choice == "3":
                    encrypted_message = input("Введите сообщение для расшифровки: ").strip()
                    try:
                        decrypted = decrypt_message(encrypted_message, key)
                        print(f"Расшифрованное сообщение: {decrypted}")
                    except Exception:
                        print("Не удалось расшифровать сообщение. Проверьте ключ и ввод.")
        elif choice == "4":
            print("Выход из программы. До свидания!")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

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
