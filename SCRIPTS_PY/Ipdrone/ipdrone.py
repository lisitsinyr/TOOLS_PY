"""ipdrone.py"""
# -*- coding: UTF-8 -*-
__annotations__ = """
 =======================================================
 Copyright (c) 2025
 Author:
     Lisitsin Y.R.
 Project:
     SCRIPTS_PY
 Module:
     ipdrone.py
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
import speedtest
import pyspeedtest

import moviepy
# from moviepy.editor import VideoFileClip

import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

import argparse
import requests, json
import sys
from sys import argv
import os


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

#------------------------------------------
# 
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
    #arguments and parser
    # parser = argparse.ArgumentParser()
    # parser.add_argument ("-v", help= "target/host IP address", type=str, dest='target', required=True )
    # args = parser.parse_args()

    #colours used
    red = '\033[31m'
    yellow = '\033[93m'
    lgreen = '\033[92m'
    clear = '\033[0m'
    bold = '\033[01m'
    cyan = '\033[96m'

    #banner of script
    print (red+"""
    
    ██╗██████╗ ██████╗ ██████╗  ██████╗ ███╗   ██╗███████╗
    ██║██╔══██╗██╔══██╗██╔══██╗██╔═══██╗████╗  ██║██╔════╝
    ██║██████╔╝██║  ██║██████╔╝██║   ██║██╔██╗ ██║█████╗  
    ██║██╔═══╝ ██║  ██║██╔══██╗██║   ██║██║╚██╗██║██╔══╝  
    ██║██║     ██████╔╝██║  ██║╚██████╔╝██║ ╚████║███████╗
    ╚═╝╚═╝     ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝
                                                          v 1.0
    """+red)
    print (lgreen+bold+"         <===[[ coded by N17RO ]]===> \n"+clear)
    print (yellow+bold+"   <---(( search on youtube Noob Hackers ))--> \n"+clear)

    # ip = args.target
    ip = '192.168.1.1'

    api = "http://ip-api.com/json/"
    try:
        data = requests.get(api+ip).json()
        sys.stdout.flush()
        a = lgreen+bold+"[$]"
        b = cyan+bold+"[$]"
        print (a, "[Victim]:", data['query'])
        print(red+"<--------------->"+red)
        # print (b, "[ISP]:", data['isp'])
        print(red+"<--------------->"+red)
        # print (a, "[Organisation]:", data['org'])
        print(red+"<--------------->"+red)
        # print (b, "[City]:", data['city'])
        print(red+"<--------------->"+red)
        # print (a, "[Region]:", data['region'])
        print(red+"<--------------->"+red)
        # print (b, "[Longitude]:", data['lon'])
        print(red+"<--------------->"+red)
        # print (a, "[Latitude]:", data['lat'])
        print(red+"<--------------->"+red)
        # print (b, "[Time zone]:", data['timezone'])
        print(red+"<--------------->"+red)
        # print (a, "[Zip code]:", data['zip'])
        print (" "+yellow)

    except KeyboardInterrupt:
        print ('Terminating, Bye'+lgreen)
        sys.exit(0)
    except requests.exceptions.ConnectionError as e:
        print (red+"[~]"+" check your internet connection!"+clear)
    # sys.exit(1)

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
