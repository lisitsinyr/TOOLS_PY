"""EmailAutomation.py"""
# -*- coding: UTF-8 -*-
__annotations__ = """
 =======================================================
 Copyright (c) 2025
 Author:
     Lisitsin Y.R.
 Project:
     SCRIPTS_PY
 Module:
     EmailAutomation.py
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
# read_excel(file_name):
#------------------------------------------
def read_excel(file_name):
    """read_excel"""
#beginfunction
    print (file_name)
    data = pd.read_excel(file_name, engine='openpyxl')
    return data
#endfunction

#------------------------------------------
# send_email(receiver_address, sender_address, sender_pass, subject, body):
#------------------------------------------
def send_email(receiver_address, sender_address, sender_pass, subject, body):
    """send_email"""
#beginfunction
    msg = MIMEMultipart()
    msg['From'] = sender_address
    msg['To'] = receiver_address
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    # Use the appropriate SMTP server
    # For Gmail
    server = smtplib.SMTP('smtp.gmail.com', 587)
    # For Office 365
    # server = smtplib.SMTP('smtp.office365.com', 587)
    # For iCloud
    # server = smtplib.SMTP('smtp.mail.me.com', 587)

    server.starttls()
    server.login(sender_address, sender_pass)

    text = msg.as_string()
    server.sendmail(sender_address, receiver_address, text)
    server.quit()
#endfunction

#------------------------------------------
# automate_emails(data_frame, sender_address, sender_pass, subject):
#------------------------------------------
def automate_emails(data_frame, sender_address, sender_pass, subject):
    """automate_emails"""
#beginfunction
    for index, row in data_frame.iterrows():
        send_email(row['email'], sender_address, sender_pass, subject, f"Hello {row['name']},\n{row['message']}")
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
    Lemailsend = r'D:\PROJECTS_LYR\CHECK_LIST\DESKTOP\Python\PROJECTS_PY\SCRIPTS_PY\SRC\00.TEST\EmailAutomation\emailsend.xlsx'
    data_frame = read_excel(Lemailsend)

    # Replace 'your-email@gmail.com' and 'your-password' with your own credentials. Pass the app password as the third parameter.

    load_dotenv ()

    EMAIL = os.getenv("EMAIL")
    PASSWORD = os.getenv("PASSWORD")

    automate_emails(data_frame, EMAIL, PASSWORD, 'TEST')

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
