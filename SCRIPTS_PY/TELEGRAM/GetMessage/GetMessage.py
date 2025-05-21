"""PATTERN3_PY.py"""
# -*- coding: UTF-8 -*-
__annotations__ = """
 =======================================================
 Copyright (c) 2025
 Author:
     Lisitsin Y.R.
 Project:
     PATTERN_PY
 Module:
     PATTERN3_PY.py
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

from telethon.sync import TelegramClient
# from telethon import TelegramClient

from telethon.tl.types import PeerChannel, PeerChat, PeerUser, Message
from telethon.tl.types import InputPeerEmpty
from telethon.tl.types import InputMessagesFilterPhotos

import telethon.errors
import telethon.client.messages as messages

# from telethon.tl.functions.messages import GetDialogsRequest
# from telethon import TelegramClient, events, sync

# from pyrogram import Client
import pyrogram

#------------------------------------------
# БИБЛИОТЕКА lyrpy
#------------------------------------------
import lyrpy.LUDoc as LUDoc
import lyrpy.LULog as LULog
import lyrpy.LUConst as LUConst
import lyrpy.LUDoc as LUDoc
import lyrpy.LULog as LULog
import lyrpy.LUFile as LUFile
import lyrpy.LUParserARG as LUParserARG

#------------------------------------------
#
#------------------------------------------
Gdownload_path = r'G:\___РАЗБОР\YOUTUBE\TELEGRAM'

#------------------------------------------
# get_telegraph_content (path):
#------------------------------------------
def get_telegraph_content (path):
    """get_telegraph_content"""
#beginfunction
    # LUDoc.PrintInfoObject('-----TEST_01----')
    # LUDoc.PrintInfoObject(get_telegraph_content)

    url = f"https://api.telegra.ph/getPage/ {path}?return_content=true"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data.get("ok"):
            content = data["result"]["content"]
            return "".join([item.get("#text", "") for item in content if "#text" in item])
    return None
#endfunction
# ----------------------------------------------
# Пример использования 01
# ----------------------------------------------
def func_01 ():
    """func_01"""
#beginfunction
    # path = "Пример-Страницы-01-01"
    # path = GA1
    # text = get_telegraph_content(path)
    # if text:
    #     print("Содержимое страницы:")
    #     print(text)
    # else:
    #     print("Не удалось загрузить страницу.")
    pass
#endfunction

# ----------------------------------------------
# Пример использования 02
# ----------------------------------------------
def func_02 ():
    """func_02"""
#beginfunction
    # ID чата/канала/пользователя, откуда читать сообщения
    chat_id = '@GardeZ66'  # или ID (число), или юзернейм (например, '@telegram')
    # Создаем клиент
    with TelegramClient (Gsession_name, Gapi_id, Gapi_hash) as client:
        # Получаем последние 10 сообщений из указанного чата
        for message in client.iter_messages (chat_id, limit=10):
            print (f"{message.sender_id}: {message.text}")
#endfunction

# ----------------------------------------------
# func_telethon ():
# ----------------------------------------------
def func_telethon ():
    """func_telethon"""
#beginfunction
    global Gsession_name
    global Gchannel
    global Gchannel_name

    print ('telethon')

    # Имя сессии (может быть любым)
    Gsession_name = 'lyr60_TELEGRAM'
    print (Gsession_name)

    #-------------------------------------------
    # Авторизация в Telegram
    #-------------------------------------------
    # client = TelegramClient('anon', api_id, api_hash, system_version="4.16.30-vxNAME ")
    # Вместо NAME используйте любое сочетание букв на английском КАПСОМ Пример: vxXYI, vxABC, vxMYNAME
    # # (в папке с кодом нет файлика .session, клиент сам его создаст (в нашем случае 'my_session')
    # # и будет с ним работать. Поэтому просто вставляем эти параметры в инициализацию и кайфуем:finger_up: )

    # Tclient = TelegramClient (Gsession_name, Gapi_id, Gapi_hash,
    #                           #         device_model = "iPhone 13 Pro Max",
    #                           #         app_version = "8.4",
    #                           #         lang_code = "en",
    #                           #         system_lang_code = "en-US")
    #                           system_version='4.16.30-vxABC')
    # Tclient.start (phone=Gphone, password=Gpassword)
    with TelegramClient (Gsession_name, Gapi_id, Gapi_hash) as Tclient:
        Tclient.start (phone=Gphone, password=Gpassword)
        b = Tclient.is_user_authorized()
        print(b)

        # Getting information about yourself
        # When you print something, you see a representation of it.
        # You can access all attributes of Telegram objects with
        # the dot operator. For example, to get the username:
        me = Tclient.get_me()
        print (me.username)
        print (me.phone)

        # "me" is a user object. You can pretty-print any Telegram object with the "stringify" method:
        # print(me.stringify())

        # Tclient.run_until_disconnected ()

        # @client.on (events.NewMessage (chats=-10 ** ** **** *2))
        # async def normal_handler (event):
        #     await client.send_message (-10 ** ** ** ** 3, event.message)

        Gchannel = Tclient.get_entity (Gchannel_name)
        # print(channel)

        # Получаем сообщение
        message = Tclient.get_messages (Gchannel_name, ids=Gmessage_id)
        print (message)

        Gmessage_file = Gchannel_name + '_' + str (Gmessage_id) + '_' + message.date.strftime ("%Y%m%d") + '.md'
        Gmessage_file = os.path.join (Gmessage_directory, Gmessage_file)
        print (Gmessage_file)

        if Path (Gmessage_file).is_file ():
            os.remove (Gmessage_file)

        write_message_file ('Link: ' + Gmessage_url, Gmessage_file)
        write_message_file ('Дата: ' + str (message.date), Gmessage_file)
        # write_message_file ('Дата: ' + message.date.strftime ("%Y%m%d"), Gmessage_file)
        write_message_file ('Title: ' + message.chat.title, Gmessage_file)
        write_message_file ('username: ' + message.chat.username, Gmessage_file)


        # Выводим текст сообщения
        if message.text:
            # print (message.date)
            # print (message.message)
            print (message.text)
            write_message_file (message.text, Gmessage_file)

        # Если есть медиа (фото, видео, документ), скачиваем
        if message.media:
            # print (message.media)
            if message.audio:
                print (message.audio)
            # if message.video:
            #     print (message.video)
            #     print (message.video.attributes [1].file_name)
            #     print (message.media.document.attributes [1].file_name)
            #     print (message.document.attributes [1].file_name)
            #     file_path = Tclient.download_media (message, Gmessage_directory)
            #     print (f"message.photo: {file_path}")
            if message.photo:
                # print (message.photo[0])
                # print (message.photo)
                file_path = Tclient.download_media(message, Gmessage_directory)
                print(f"message.photo: {file_path}")

        else:
            print("В сообщении нет медиафайлов.")

        # file_path = Tclient.download_file()
        # print(f"download_file: {file_path}")
        # Tclient.download_media(photos)
#endfunction

# ----------------------------------------------
# func_pyrogram ():
# ----------------------------------------------
def func_pyrogram ():
    """func_pyrogram"""
#beginfunction
    global Gsession_name
    global Gchannel
    global Gchannel_name

    print ('pyrogram')

    # Имя сессии (может быть любым)
    Gsession_name = 'lyr60'
    print(Gsession_name)

    bot = pyrogram.Client (name=Glogin, api_id=Gapi_id, api_hash=Gapi_hash,
                  phone_number=Gphone)
    bot.start ()
    # bot.run ()

    # Получаем сообщение
    message = bot.get_messages(Gchannel_name, Gmessage_id)
    # print (message)

    # Gmessage_file = Gchannel_name + '_' + str (
    #     Gmessage_id) + '_' + message.date.strftime ("%Y%m%d") + '.md'
    # Gmessage_file = os.path.join (Gmessage_directory, Gmessage_file)
    # print (Gmessage_file)
    # if Path (Gmessage_file).is_file ():
    #     os.remove (Gmessage_file)
    #
    # write_message_file ('Link: '+Gmessage_url, Gmessage_file)
    # write_message_file ('Дата: '+str(message.date), Gmessage_file)
    # write_message_file ('Title: '+message.chat.title, Gmessage_file)
    # write_message_file ('username: '+message.chat.username, Gmessage_file)
    #
    # # Выводим текст сообщения
    # if message.caption:
    #     # print (message.caption)
    #     write_message_file (message.caption, Gmessage_file)
    #
    # # Выводим текст сообщения
    # if message.text:
    #     # print (message.text)
    #     write_message_file (message.text, Gmessage_file)
    #
    # #
    # if message.caption_entities:
    #     # print (message.caption_entities)
    #     for e in message.caption_entities:
    #         if e.type == pyrogram.enums.MessageEntityType.TEXT_LINK:
    #             # print (e.type)
    #             # print (e.url)
    #             write_message_file ('<'+e.url+'>', Gmessage_file)
    #
    if message.video:
        # print (message.video.file_name)
        # file_path = bot.download_media (message, download_path)
        file_media = os.path.join (Gmessage_directory, message.video.file_name)
        if Path (file_media).is_file ():
            os.remove (file_media)
        file_path = bot.download_media (message, file_media)
        print(f"download_file: {file_path}")

    # if message.photo:
    #     # file_media = os.path.join (Gmessage_directory, message.photo.file_id)
    #     # if Path (file_media).is_file ():
    #     #     os.remove (file_media)
    #     # print ("file_id: " + str (message.photo.file_id))
    #     file_path = bot.download_media (message.photo)
    #     print(f"download_file: {file_path}")

    bot.stop ()
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
        # print(s)
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
    global Gmessage_id
    global Gmessage_directory
    global Gmessage_file

    # Разбираем ссылку
    # parsed_url = urlparse(url_path)
    # print(parsed_url)
    Gchannel_name = url.path.split('/')[1]  # Получаем "xxxx"
    # print(Gchannel_name)
    Gmessage_id = int(url.path.split('/')[2])  # Получаем "nnnn"
    # print(Gmessage_id)
    print(GO2)

    Gmessage_directory = os.path.join (GO2, Gchannel_name+'_'+str(Gmessage_id))
    print(Gmessage_directory)
    os.makedirs (Gmessage_directory, exist_ok=True)
    # Gmessage_file = os.path.join (Gmessage_directory, Gchannel_name+'_'+str(Gmessage_id)+'.md')
    # print(Gmessage_file)
#endfunction

#------------------------------------------
#  check_link ():
#------------------------------------------
def check_link (link:str):
    """check_link"""
#beginfunction
    parsed_url = urlparse (link)
    # print(parsed_url)

    root = parsed_url.netloc
    if root == 't.me':
        set_message (parsed_url)

        # if GO3 == 'telethon':
        #     func_telethon ()
        # if GO3 == 'pyrogram':
        #     func_pyrogram ()
        func_telethon ()
        func_pyrogram ()

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

    global Gwidth

    global Gmessage_url

    # tracemalloc.start ()

    LUConst.SET_LIB(__file__)

    LULog.STARTLogging (LULog.TTypeSETUPLOG.tslINI, 'console', LUConst.GDirectoryLOG, LUConst.GFileNameLOG,
                        LUConst.GFileNameLOGjson)
    LULog.LoggerTOOLS.level = logging.INFO

    #-------------------------------------------------
    # Отключить журнал 'telethon'
    #-------------------------------------------------
    logger = logging.getLogger('telethon.network.mtprotosender')
    logger.setLevel(logging.INFO)
    logger = logging.getLogger('telethon.extensions.messagepacker')
    logger.setLevel(logging.INFO)
    logger = logging.getLogger('telethon.network.mtprotostate')
    logger.setLevel(logging.INFO)

    LArgParser = LUParserARG.TArgParser (description = 'Параметры', prefix_chars = '-/')
    # LArg = LArgParser.ArgParser.add_argument ('A1', type = str, default = 'A1_Default', help = 'Link')
    LArg = LArgParser.ArgParser.add_argument ('-O1', '--O1', type = str, default='', help = 'Link')
    LArg = LArgParser.ArgParser.add_argument ('-O2', '--O2', type = str, default=Gdownload_path, help = 'Directory')
    LArg = LArgParser.ArgParser.add_argument ('-O3', '--O3', type = str, default='telethon', help = 'LIB')
    Largs = LArgParser.ArgParser.parse_args ()
    GO1 = Largs.O1
    print(f'{GO1=}')
    GO2 = Largs.O2
    print(f'{GO2=}')
    GO3 = Largs.O3
    print(f'{GO3=}')
    # GA1 = Largs.A1

    LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, f'GO1 = {GO1}')
    LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, f'GO2 = {GO2}')
    LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, f'GO3 = {GO3}')
    # LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, f'A1 = {GA1}')

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
    Gmessage_url = 'https://t.me/Selectel/5813'
    # ---------------------------------------------------------------

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
