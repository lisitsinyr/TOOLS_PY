"""CryptoTEXT4.py"""
# -*- coding: UTF-8 -*-
__annotations__ = """
 =======================================================
 Copyright (c) 2025
 Author:
     Lisitsin Y.R.
 Project:
     SCRIPTS_PY
 Module:
     CryptoTEXT4.py
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

KEY_FILE = "secret.key"

#------------------------------------------
# func_pass ()
#------------------------------------------
def func_pass():
    """func_pass"""
#beginfunction
    pass
#endfunction

#-----------------------------------------------------------
# generate_key()
#-----------------------------------------------------------
def generate_key():
    """generate_key"""
    # Генерирует и сохраняет ключ шифрования в файл
#beginfunction
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)
    return key
#endfunction

#-----------------------------------------------------------
# load_key()
#-----------------------------------------------------------
def load_key():
    """load_key"""
    # Загружает ключ шифрования из файла или генерирует новый, если файл отсутствует
#beginfunction
    if not os.path.exists(KEY_FILE):
        print(f"Файл с ключом '{KEY_FILE} не найден. Генерация нового ключа...")
        return generate_key()
    with open(KEY_FILE, "rb") as key_file:
        return key_file.read()
#endfunction

def encrypt_message(message, key):
    """encrypt_message"""
    # Шифрует сообщение с использованием ключа. 
#beginfunction
    fernet = Fernet(key)
    return fernet.encrypt(message.encode()).decode()

def decrypt_message(encrypted_message, key):
    """decrypt_message"""
    # Расшифровывает сообщение с использованием ключа. 
#beginfunction
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_message.encode()). decode()

def encrypt_decrypt_test():
    """encrypt_decrypt_test"""
#beginfunction
    key = generate_key()
    message = "Hello, World!"
    encrypted = encrypt_message(message, key)
    decrypted = decrypt_message(encrypted, key)
    assert message == decrypted, "Test failed: расшифрованное сообщение не совпадает с исходным" 
    print("Тест успешен: шифрование и дешифрование работают корректно")

#------------------------------------------
def main ():
    """main"""
#beginfunction
    LUConst.SET_LIB(__file__)

    LULog.STARTLogging (LULog.TTypeSETUPLOG.tslINI, 'console', LUConst.GDirectoryLOG, LUConst.GFileNameLOG,
                        LUConst.GFileNameLOGjson)
    LULog.LoggerTOOLS.level = logging.INFO

    LPath = LUFile.ExtractFileDir(__file__)
    print (f'LPath: {LPath}')

    #--------------------------------------------------------------
    # 
    #--------------------------------------------------------------
    key = load_key()
    message = "Тестовое сообщение"
    encrypted = encrypt_message(message, key)
    decrypted = decrypt_message(encrypted, key)
    
    print (f"Исходное сообщени: {message}")
    print (f"Зашифрованное сообщение: {encrypted}")
    print (f"Расшифрованное сообщение: {decrypted}")

    LULog.STOPLogging ()
#endfunction

#------------------------------------------
#
#------------------------------------------
#beginmodule
if __name__ == "__main__":
    encrypt_decrypt_test()
    main ()
# endif

# endmodule
