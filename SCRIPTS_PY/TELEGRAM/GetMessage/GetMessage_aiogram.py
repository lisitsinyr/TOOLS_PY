"""GetMessage_aiogram.py"""
# -*- coding: UTF-8 -*-
__annotations__ = """
 =======================================================
 Copyright (c) 2025
 Author:
     Lisitsin Y.R.
 Project:
     SCRIPTS_PY
 Module:
     GetMessage_aiogram.py
 =======================================================
"""

#------------------------------------------
# БИБЛИОТЕКИ python
#------------------------------------------
import os
import sys
import tracemalloc
from pathlib import Path
import argparse
import shutil
import textwrap

import logging

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------
import asyncio
from urllib.parse import urlparse
from decouple import config
import pyperclip
import requests
from pymsgbox import password
from pyrogram.raw.functions.help import GetDeepLinkInfo

#------------------------------------------
# БИБЛИОТЕКА aiogram
#------------------------------------------
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

#------------------------------------------
# БИБЛИОТЕКА lyrpy
#------------------------------------------
import lyrpy.LUConst as LUConst
# import lyrpy.LUDoc as LUDoc
import lyrpy.LULog as LULog
# import lyrpy.LUFile as LUFile
import lyrpy.LUParserARG as LUParserARG

#------------------------------------------
#
#------------------------------------------
Gdownload_path = r'G:\___РАЗБОР\YOUTUBE\TELEGRAM'

# ----------------------------------------------
# func_telethon ():
# ----------------------------------------------
def func_aiogram ():
    """func_aiogram"""
#beginfunction
    global Gsession_name
    global Gchannel
    global Gmessage_file

    global Gchannel_name

    print ('aiogram')

    #-------------------------------------------
    # Авторизация в Telegram
    #-------------------------------------------
    # Имя сессии (может быть любым)
    Gsession_name = 'lyr60_aiogram'
    print (Gsession_name)

    bot = Bot (token=GAPI_TOKEN)
    dp = Dispatcher (bot)

    # with TelegramClient (Gsession_name, Gapi_id, Gapi_hash) as Tclient:
    #     Tclient.start (phone=Gphone, password=Gpassword)
    #     b = Tclient.is_user_authorized()
    #     # print(b)
    #
    #     # -------------------------------------------
    #     # Getting information about yourself
    #     # -------------------------------------------
    #     # When you print something, you see a representation of it.
    #     # You can access all attributes of Telegram objects with
    #     # the dot operator. For example, to get the username:
    #     me = Tclient.get_me()
    #     # print (me.username)
    #     # print (me.phone)
    #     # "me" is a user object. You can pretty-print any Telegram object with the "stringify" method:
    #     # print(me.stringify())
    #
    #     # -------------------------------------------
    #     #
    #     # -------------------------------------------
    #     Gchannel = Tclient.get_entity (Gchannel_name_id)
    #     # print(f'{Gchannel.title=}')
    #     # print(f'{Gchannel.id=}')
    #
    #     # -------------------------------------------
    #     # Получаем сообщение
    #     # -------------------------------------------
    #     # message = Tclient.get_messages (Gchannel.title, ids=Gmessage_id)
    #     message = Tclient.get_messages (Gchannel.id, ids=Gmessage_id)
    #     print (message)
    #
    #     # -------------------------------------------
    #     #
    #     # -------------------------------------------
    #     Gmessage_file = Gchannel_name + '_' + str (Gmessage_id) + '_' + message.date.strftime ("%Y%m%d") + '.md'
    #     Gmessage_file = os.path.join (Gmessage_directory, Gmessage_file)
    #     # print (Gmessage_file)
    #     if Path (Gmessage_file).is_file ():
    #         os.remove (Gmessage_file)
    #
    #     # -------------------------------------------
    #     #
    #     # -------------------------------------------
    #     write_message_file ('Link: ' + Gmessage_url, Gmessage_file)
    #     write_message_file ('Дата: ' + str (message.date), Gmessage_file)
    #     write_message_file ('Title: ' + message.chat.title, Gmessage_file)
    #     # write_message_file ('username: ' + message.chat.username, Gmessage_file)
    #
    #     # -------------------------------------------
    #     # Выводим текст сообщения
    #     # -------------------------------------------
    #     if message.text:
    #         # print (message.date)
    #         # print (message.message)
    #         # print (message.text)
    #         write_message_file (message.text, Gmessage_file)
    #
    #     # -------------------------------------------
    #     # Если есть медиа (фото, видео, документ), скачиваем
    #     # -------------------------------------------
    #     if message.media:
    #         print (message.media)
    #         print (f'message.grouped_id={message.grouped_id}')
    #
    #         # if message.audio:
    #         #     print (message.audio)
    #
    #         if message.video:
    #             # print (message.video)
    #             try:
    #                 print (message.video.attributes [1].file_name)
    #                 # print (message.media.document.attributes [1].file_name)
    #                 # print (message.document.attributes [1].file_name)
    #             except:
    #                 pass
    #
    #             if not type (Gchannel_name_id) is str:
    #                 file_path = Tclient.download_media (message, Gmessage_directory)
    #                 print (f"message.video: {file_path}")
    #
    #         if message.photo:
    #             # print (message.photo[0])
    #             # print (message.photo)
    #             file_path = Tclient.download_media(message, Gmessage_directory)
    #             # print(f"message.photo: {file_path}")
    #
    #     else:
    #         print("В сообщении нет медиафайлов.")

#endfunction

#----------------------------------------------
# write_message_file (content:str):
#----------------------------------------------
def write_message_file (content:str, filepath:str):
    """write_message_file"""
#beginfunction
    paragraphs = content.split ('\n')
    formatted_paragraphs = []

    for paragraph in paragraphs:
        substring = "https://"
        if substring in paragraph:
            # Подстрока найдена
            s = paragraph
        else:
            # Подстрока не найдена
            s = textwrap.fill (paragraph, width=Gwidth)
        # endif
        formatted_paragraphs.append (s)
    # endfor
    formatted_paragraphs.append ('\n')

    with open (filepath, 'a', encoding='utf-8') as file:
        file.write ('\n'.join (formatted_paragraphs))
    # endwith
#endfunction

#------------------------------------------
#  set_message ():
#------------------------------------------
def set_message (url):
    """set_message"""
#beginfunction
    global Gchannel_name
    global Gchannel_name_id
    global Gmessage_id
    global Gmessage_directory

    if url.path.split('/')[1] == 'c':
        Gchannel_name = url.path.split('/')[2]              # Получаем "9999999999999"
        # print(f'{Gchannel_name=}')
        Gchannel_name_id = int (Gchannel_name)              # Получаем 9999999999999
        # print(f'{Gchannel_name_id=}')
        Gmessage_id = int(url.path.split('/')[3])           # Получаем 9999
        # print(f'{Gmessage_id=}')
    else:
        Gchannel_name = url.path.split('/')[1]              # Получаем "xxxx" "9999999999999"
        # print(f'{Gchannel_name=}')
        Gchannel_name_id = Gchannel_name                    # Получаем "xxxx" "9999999999999"
        # print(f'{Gchannel_name_id=}')
        Gmessage_id = int(url.path.split('/')[2])           # Получаем 9999
        # print(f'{Gmessage_id=}')

    Gmessage_directory = os.path.join (GO2, Gchannel_name+'_'+str(Gmessage_id))
    # print(f'{Gmessage_directory=}')
    os.makedirs (Gmessage_directory, exist_ok=True)

#endfunction

#------------------------------------------
#  check_link ():
#------------------------------------------
def check_link (link:str):
    """check_link"""
#beginfunction
    global Glink
    # Разбираем ссылку
    parsed_url = urlparse (link)
    root = parsed_url.netloc
    if root == 't.me':
        Glink = link
        print (f'{link=}')
        # print (f'{parsed_url=}')
        set_message (parsed_url)

        # if GO3 == 'telethon':
        #     func_telethon ()
        # if GO3 == 'pyrogram':
        #     func_pyrogram ()
        # func_aiogram ()

        pyperclip.copy ('')

#endfunction


#------------------------------------------
#  main ():
#------------------------------------------
def main ():
    """main"""
#beginfunction
    global GO1
    global GO2
    global GO3

    global Glogin
    global Gapi_id
    global Gapi_hash
    global Gphone
    global Gpassword
    global GAPI_TOKEN

    global Gwidth

    global Gmessage_url

    # tracemalloc.start ()

    LUConst.SET_LIB(__file__)

    LULog.STARTLogging (LULog.TTypeSETUPLOG.tslINI, 'console', '',
                        '', '')
    LULog.LoggerAPPS.level = logging.INFO

    #-------------------------------------------------
    # Отключить журнал 'telethon'
    #-------------------------------------------------
    logger = logging.getLogger('telethon.network.mtprotosender')
    logger.setLevel(logging.ERROR)
    logger = logging.getLogger('telethon.extensions.messagepacker')
    logger.setLevel(logging.ERROR)
    logger = logging.getLogger('telethon.network.mtprotostate')
    logger.setLevel(logging.ERROR)
    logger = logging.getLogger('telethon.client.telegrambaseclient')
    logger.setLevel(logging.ERROR)

    LArgParser = LUParserARG.TArgParser (description = 'Параметры', prefix_chars = '-/')
    LArg = LArgParser.ArgParser.add_argument ('-O1', '--O1', type = str, default='', help = 'Link')
    LArg = LArgParser.ArgParser.add_argument ('-O2', '--O2', type = str, default=Gdownload_path, help = 'Directory')
    LArg = LArgParser.ArgParser.add_argument ('-O3', '--O3', type = str, default='telethon', help = 'LIB')
    Largs = LArgParser.ArgParser.parse_args ()
    GO1 = Largs.O1
    # print(f'{GO1=}')
    GO2 = Largs.O2
    # print(f'{GO2=}')
    GO3 = Largs.O3
    # print(f'{GO3=}')

    LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, f'GO1 = {GO1}')
    LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, f'GO2 = {GO2}')
    LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, f'GO3 = {GO3}')

    #----------------------------------------------
    # Данные API (получите на my.telegram.org)
    #----------------------------------------------
    Gapi_id = config ('API_ID')
    # print(Gapi_id)
    Gapi_hash = config ('API_HASH')
    # print(Gapi_hash)
    Gphone = config ('PHONE')
    # print(Gphone)
    Glogin = config ('LOGIN')
    # print(Glogin)
    Gpassword = config ('password')
    # print(Gpassword)

    GAPI_TOKEN = config ('API_TOKEN')
    # print(GAPI_TOKEN)

    #----------------------------------------------
    # INIT
    #----------------------------------------------
    os.makedirs (GO2, exist_ok=True)
    Gwidth = 60
    stop_file = os.path.join (GO2, 'stop')
    print(stop_file)
    if Path (stop_file).is_file():
        os.remove (stop_file)
    pyperclip.copy ('')
    # ---------------------------------------------------------------
    # Ссылка на сообщение
    # message_url = "https://t.me/_канал_/_id_"
    # ---------------------------------------------------------------
    Gmessage_url = GO1
    # Gmessage_url = 'https://t.me/GardeZ66/13311'
    # Gmessage_url = 'https://t.me/GardeZ66/13285'
    # Gmessage_url = 'https://t.me/Selectel/5813'
    # Gmessage_url = 'https://t.me/+MnXPMuA95QdlMTYy/5765'
    # Gmessage_url = 'https://t.me/1471170142/7606'
    # ---------------------------------------------------------------

    # get_mygroups ()

    # get_chats ()

    if not Gmessage_url == '':
        check_link(Gmessage_url)
    else:
        while True and not Path (stop_file).is_file ():
            Gmessage_url = pyperclip.paste()
            check_link(Gmessage_url)
        #endwhile
    #endif

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
