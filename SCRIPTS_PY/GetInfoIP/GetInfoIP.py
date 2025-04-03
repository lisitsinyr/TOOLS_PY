"""GetInfoIP.py"""
# -*- coding: UTF-8 -*-
__annotations__ = """
 =======================================================
 Copyright (c) 2025
 Author:
     Lisitsin Y.R.
 Project:
     SCRIPTS_PY
 Module:
     GetInfoIP.py
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
import time

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------
import random
import string
import tkinter as tk
import pyperclip
import requests # Импортируем библиотеку requests для выполнения HTTP- запросов
import urllib.request as urllib2
import json

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
# get_public_ip()
#------------------------------------------
def get_public_ip() -> str:
    """get_public_ip"""
#beginfunction
    try:
        # Делаем GET-запрос к сервису іpify, который возвращает публичный ІР-адрес в формате JSON
        response = requests.get('https://api.ipify.org?format=json')
        # Извлекаем IP-адрес из JSON-ответа
        ip = response.json().get('ip')
        return ip # Возвращаем ІР-адрес
    except requests. RequestException:
        # В случае возникновения исключения (например, проблем с сетью) возвращаем соответствующее сообщение
        return "Не удалось получить ІР-адрес"
#endfunction

#------------------------------------------
# get_info_ip (Aip) -> None:
#------------------------------------------
def get_info_ip (Aip) -> None:
    """get_public_ip"""
#beginfunction
    while True:
        #ip = input("What is your target IP: ")
        url = "http://ip-api.com/json/"
        response = urllib2.urlopen (url + Aip)
        data = response.read()
        values = json.loads(data)

        print("IP: " + values["query"])
        print("City: " + values["city"])
        print("ISP: " + values["isp"])
        print("Country: " + values["country"])
        print("Region: " + values["region"])
        print("Timezone: " + values["timezone"])

        break
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
    get_info_ip (get_public_ip())
    
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
