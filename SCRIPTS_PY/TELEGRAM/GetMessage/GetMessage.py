"""GetMessage.py"""
# -*- coding: UTF-8 -*-
__annotations__ = """
 =======================================================
 Copyright (c) 2025
 Author:
     Lisitsin Y.R.
 Project:
     SCRIPTS_PY
 Module:
     GetMessage.py
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
import collections

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
# БИБЛИОТЕКА telethon
#------------------------------------------
# import telethon
import telethon.sync
import telethon.tl.types

# # класс, позволяющий нам подключаться к клиенту мессенджера и работать с ним;
# from telethon.sync import TelegramClient
# # PeerChannel - специальный тип, определяющий объекты типа «канал/чат»,
# # с помощью которого можно обратиться к нужному каналу для парсинга сообщений.
# from telethon.tl.types import Channel, PeerChannel, PeerChat, PeerUser, Message, User, MessageMediaPhoto, MessageMediaDocument
# # конструктор для работы с InputPeer, который передаётся в качестве аргумента в GetDialogsRequest;
# from telethon.tl.types import InputPeerEmpty
# from telethon.tl.types import InputMessagesFilterPhotos
# # функция, позволяющая работать с сообщениями в чате;
# from telethon.tl.functions.messages import GetDialogsRequest
# # метод, позволяющий получить сообщения пользователей из чата и работать с ним;
# from telethon.tl.functions.messages import GetHistoryRequest
# from telethon import TelegramClient, events, sync
# import telethon.errors
# import telethon.client.messages as messages
#------------------------------------------
# БИБЛИОТЕКА pyrogram
#------------------------------------------
# from pyrogram import Client
import pyrogram

#------------------------------------------
# БИБЛИОТЕКА lyrpy
#------------------------------------------
import lyrpy.LUConst as LUConst
# import lyrpy.LUDoc as LUDoc
import lyrpy.LULog as LULog
# import lyrpy.LUFile as LUFile
import lyrpy.LUParserARG as LUParserARG
import lyrpy.LUTelegram as LUTelegram
# from lyrpy.LUTelegram import LIB_name

#------------------------------------------
#
#------------------------------------------
Gdownload_path = r'G:\___РАЗБОР\YOUTUBE\TELEGRAM'
Gwidth = 60


# ----------------------------------------------
# func_telethon ():
# ----------------------------------------------
def func_telethon ():
    """func_telethon"""
#beginfunction
    LIB_name = 'LIB:telethon'
    LUTelegram.LIB_name = LIB_name

    print (f'{LIB_name:{'_'}<{60}}')
    #-------------------------------------------
    # Авторизация в Telegram
    #-------------------------------------------
    # Имя сессии (может быть любым)
    session_name = 'lyr60_TELEGRAM'
    # print (f'{LIB_name}_session_name={session_name}')
    Tclient = LUTelegram.get_telethon_client (session_name, Gapi_id, Gapi_hash, Gphone, Gpassword)
    #-------------------------------------------
    #
    #-------------------------------------------
    # LUTelegram.get_telethon_mygroups (Tclient)
    # -------------------------------------------
    #
    # -------------------------------------------
    # LUTelegram.get_telethon_chats (Tclient)
    # -------------------------------------------
    # Getting information about yourself
    # -------------------------------------------
    me = LUTelegram.get_telethon_me (Tclient)
    # -------------------------------------------
    # channel
    # -------------------------------------------
    channel:telethon.tl.types.Channel = LUTelegram.get_telethon_channel (Tclient, Gchannel_name_id)
    # -------------------------------------------
    # Получаем сообщение
    # -------------------------------------------
    message:telethon.tl.types.Message = LUTelegram.get_telethon_message (Tclient, channel, Gmessage_id)
    # -------------------------------------------
    # message_file
    # -------------------------------------------
    message_file:str = Gchannel_name + '_' + str (Gmessage_id) + '_' + message.date.strftime ("%Y%m%d") + '.md'
    message_file = os.path.join (Gmessage_directory, message_file)
    # print (message_file)
    if Path (message_file).is_file ():
        os.remove (message_file)
    # -------------------------------------------
    #
    # -------------------------------------------
    write_message_file ('Link: ' + Gmessage_url, message_file)
    write_message_file ('Дата: ' + str (message.date), message_file)
    write_message_file ('Title: ' + message.chat.title, message_file)
    # -------------------------------------------
    # Выводим текст сообщения
    # -------------------------------------------
    if message.text:
        # write_message_file (message.message, message_file)
        write_message_file (message.text, message_file)
    # -------------------------------------------
    # Если есть медиа (фото, видео, документ)
    # -------------------------------------------
    if message.media:
        # print (message.media)
        grouped_id = message.grouped_id
        # print (f'{LIB_name}_message.grouped_id={grouped_id}')
        # if message.audio:
        #     print (message.audio)
        if message.video:
            # print (message.video)
            try:
                # print (message.video.attributes [1].file_name)
                # print (message.media.document.attributes [1].file_name)
                # print (message.document.attributes [1].file_name)
                pass
            except:
                pass
            if type (Gchannel_name_id) is int:
                file_path = Tclient.download_media (message, Gmessage_directory)
                print (f"{LIB_name}_message.video: {file_path}")
        if message.photo:
            # print (message.photo)
            file_path = Tclient.download_media(message, Gmessage_directory)
            print(f"{LIB_name}_message.photo: {file_path}")

            # Чтобы объединить сгруппированные фотографии по параметру grouped_id в Telethon,
            # можно использовать метод client.send_message с параметром file.
            # Этот метод позволяет отправить группу фотографий как одно сообщение,
            # если передать ему список файлов, соответствующих одному grouped_id

            # Словарь для хранения медиа
            # grouped_media = collections.defaultdict (list)
            # messages = Tclient.get_messages (Gchannel.id)
            # print(messages)
            # # Пройти по сообщениям
            # for message in messages:
            #     print (message)
            #     if isinstance (message.media,
            #                    (MessageMediaPhoto, MessageMediaDocument)):
            #         grouped_id = message.grouped_id or message.id
            #         print(grouped_id)
            #         # grouped_media [grouped_id].append (message)
            # # Сохранить медиа
            # for group_id, media_messages in grouped_media.items ():
            #     for msg in media_messages:
            #         Tclient.download_media (msg.media, Gmessage_directory)
    else:
        print (f"{LIB_name}_В сообщении нет медиафайлов.")

    Tclient.disconnect ()
#endfunction

# ----------------------------------------------
# get_telethon_mygroups ():
# ----------------------------------------------
def get_telethon_mygroups ():
    """get_telethon_mygroups"""
    # beginfunction
    LIB_name = 'LIB:telethon'
    LUTelegram.LIB_name = LIB_name

    print (f'{LIB_name:{'_'}<{60}}')
    # -------------------------------------------
    # Авторизация в Telegram
    # -------------------------------------------
    # Имя сессии (может быть любым)
    session_name = 'lyr60_TELEGRAM'
    print (f'{LIB_name}_session_name={session_name}')
    Tclient = LUTelegram.get_telethon_client (session_name, Gapi_id, Gapi_hash,
                                              Gphone, Gpassword)
    # -------------------------------------------
    #
    # -------------------------------------------
    # LUTelegram.get_telethon_mygroups (Tclient)
    # -------------------------------------------
    #
    # -------------------------------------------
    # LUTelegram.get_telethon_chats (Tclient)
    # -------------------------------------------
    # Getting information about yourself
    # -------------------------------------------
    me = LUTelegram.get_telethon_me (Tclient)

    LUTelegram.get_telethon_mygroups (Tclient)

    Tclient.disconnect ()
# endfunction

# ----------------------------------------------
# get_telethon_chats ():
# ----------------------------------------------
def get_telethon_chats ():
    """get_telethon_chats"""
    # beginfunction
    LIB_name = 'LIB:telethon'
    LUTelegram.LIB_name = LIB_name

    print (f'{LIB_name:{'_'}<{60}}')
    # -------------------------------------------
    # Авторизация в Telegram
    # -------------------------------------------
    # Имя сессии (может быть любым)
    session_name = 'lyr60_TELEGRAM'
    print (f'{LIB_name}_session_name={session_name}')
    Tclient = LUTelegram.get_telethon_client (session_name, Gapi_id, Gapi_hash,
                                              Gphone, Gpassword)
    # -------------------------------------------
    #
    # -------------------------------------------
    # LUTelegram.get_telethon_mygroups (Tclient)
    # -------------------------------------------
    #
    # -------------------------------------------
    # LUTelegram.get_telethon_chats (Tclient)
    # -------------------------------------------
    # Getting information about yourself
    # -------------------------------------------
    me = LUTelegram.get_telethon_me (Tclient)

    LUTelegram.get_telethon_chats (Tclient)

    Tclient.disconnect ()
# endfunction

# ----------------------------------------------
# get_telethon_groups ():
# ----------------------------------------------
def get_telethon_groups ():
    """get_telethon_groups"""
# beginfunction
    LIB_name = 'LIB:telethon'
    LUTelegram.LIB_name = LIB_name

    print (f'{LIB_name:{'_'}<{60}}')
    # -------------------------------------------
    # Авторизация в Telegram
    # -------------------------------------------
    # Имя сессии (может быть любым)
    session_name = 'lyr60_TELEGRAM'
    # print (f'{LIB_name}_session_name={session_name}')
    Tclient = LUTelegram.get_telethon_client (session_name, Gapi_id, Gapi_hash,
                                              Gphone, Gpassword)
    # -------------------------------------------
    #
    # -------------------------------------------
    # LUTelegram.get_telethon_mygroups (Tclient)
    # -------------------------------------------
    #
    # -------------------------------------------
    # LUTelegram.get_telethon_chats (Tclient)
    # -------------------------------------------
    # Getting information about yourself
    # -------------------------------------------
    me = LUTelegram.get_telethon_me (Tclient)

    # -------------------------------------------
    #
    # -------------------------------------------
    groups = LUTelegram.get_telethon_groups (Tclient)
    for group in groups:
        print (f"{LIB_name}_group={group}")

    Tclient.disconnect ()
# endfunction

# ----------------------------------------------
# get_telethon_users_group ():
# ----------------------------------------------
def get_telethon_users_group ():
    """get_telethon_users_group"""
# beginfunction
    LIB_name = 'LIB:telethon'
    LUTelegram.LIB_name = LIB_name

    print (f'{LIB_name:{'_'}<{60}}')
    # -------------------------------------------
    # Авторизация в Telegram
    # -------------------------------------------
    # Имя сессии (может быть любым)
    session_name = 'lyr60_TELEGRAM'
    # print (f'{LIB_name}_session_name={session_name}')
    Tclient = LUTelegram.get_telethon_client (session_name, Gapi_id, Gapi_hash,
                                              Gphone, Gpassword)
    # -------------------------------------------
    #
    # -------------------------------------------
    # LUTelegram.get_telethon_mygroups (Tclient)
    # -------------------------------------------
    #
    # -------------------------------------------
    # LUTelegram.get_telethon_chats (Tclient)
    # -------------------------------------------
    # Getting information about yourself
    # -------------------------------------------
    me = LUTelegram.get_telethon_me (Tclient)

    # -------------------------------------------
    #
    # -------------------------------------------
    groups = LUTelegram.get_telethon_groups (Tclient)

    # print (groups[0])
    # users = LUTelegram.get_telethon_users_group (Tclient, groups[0])
    # for user in users:
    #     print (f"{LIB_name}_user={user}")

    for group in groups:
        # print (f"{LIB_name}_group={group}")
        users = LUTelegram.get_telethon_users_group (Tclient, group)
        for user in users:
            print (f"{LIB_name}_user={user}")

    Tclient.disconnect ()
# endfunction

# ----------------------------------------------
# func_pyrogram ():
# ----------------------------------------------
def func_pyrogram ():
    """func_pyrogram"""
#beginfunction
    LIB_name = 'LIB:pyrogram'
    LUTelegram.LIB_name = LIB_name

    print (f'{LIB_name:{'_'}<{60}}')
    # #-------------------------------------------
    # # Авторизация в Telegram
    # #-------------------------------------------
    # bot = pyrogram.Client (name=Glogin, api_id=Gapi_id, api_hash=Gapi_hash, phone_number=Gphone)
    # print (f'{bot.name=}')
    # print (f'{bot.phone_number=}')
    # bot.start ()
    # # bot.run ()

    # print (f'Gchannel_name={Gchannel_name}')
    # print (f'Gmessage_id={Gmessage_id}')

    #-------------------------------------------
    # Авторизация в Telegram
    #-------------------------------------------
    # # Имя сессии (может быть любым)
    session_name = 'lyr60'
    # print (f'{LIB_name}_session_name={session_name}')
    Tclient:pyrogram.Client = LUTelegram.get_pyrogram_client (Gapi_id, Gapi_hash, Glogin, Gphone)
    # -------------------------------------------
    # Getting information about yourself
    # -------------------------------------------
    me:pyrogram.User = LUTelegram.get_pyrogram_me (Tclient)

    #-------------------------------------------
    # Получаем сообщение
    #-------------------------------------------
    message = None
    if type(Gchannel_name_id) is str:
        chat = Tclient.get_chat (Gchannel_name_id)
        # print(f'chat={chat}')
        # print(f'chat.description={chat.description}')

        # print(f'{LIB_name}_chat.title={chat.title}')
        # print(f'{LIB_name}_chat.username={chat.username}')

        message = Tclient.get_messages(chat.id, Gmessage_id)

    if not message is None:
        # print (message)

        # message_file = Gchannel_name + '_' + str (
        #     Gmessage_id) + '_' + message.date.strftime ("%Y%m%d") + '.md'
        # message_file = os.path.join (Gmessage_directory, message_file)
        # print (message_file)
        # if Path (message_file).is_file ():
        #     os.remove (message_file)
        
        # write_message_file ('Link: '+Gmessage_url, message_file)
        # write_message_file ('Дата: '+str(message.date), message_file)
        # write_message_file ('Title: '+message.chat.title, message_file)
        # write_message_file ('username: '+message.chat.username, message_file)
        
        # Выводим текст сообщения
        # if message.caption:
        #     # print (message.caption)
        #     write_message_file (message.caption, message_file)
        #

        # Выводим текст сообщения
        # if message.text:
        #     # print (message.text)
        #     write_message_file (message.text, message_file)
        #

        # if message.caption_entities:
        #     # print (message.caption_entities)
        #     for e in message.caption_entities:
        #         if e.type == pyrogram.enums.MessageEntityType.TEXT_LINK:
        #             # print (e.type)
        #             # print (e.url)
        #             write_message_file ('<'+e.url+'>', message_file)
        #

        if message.video:
            if type (Gchannel_name_id) is str:
                # print (message.video.file_name)
                # file_path = bot.download_media (message, download_path)
                file_media = os.path.join (Gmessage_directory, message.video.file_name)
                if Path (file_media).is_file ():
                    os.remove (file_media)
                file_path = Tclient.download_media (message, file_media)
                print(f"{LIB_name}_message.video: {file_path}")

        # if message.photo:
        #     # file_media = os.path.join (Gmessage_directory, message.photo.file_id)
        #     # if Path (file_media).is_file ():
        #     #     os.remove (file_media)
        #     # print ("file_id: " + str (message.photo.file_id))
        #     file_path = bot.download_media (message.photo)
        #     print(f"{LIB_name}_download_file: {file_path}")

    Tclient.stop ()

#endfunction

#----------------------------------------------
# write_message_file (content:str):
#----------------------------------------------
def write_message_file (content:str, filepath:str) -> None:
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
    return None
#endfunction

#------------------------------------------
#  set_message ():
#------------------------------------------
def set_message (url) -> None:
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
    return None
#endfunction

#------------------------------------------
#  check_link ():
#------------------------------------------
def check_link (link:str) -> None:
    """check_link"""
#beginfunction
    global GlinkT

    # Разбираем ссылку
    parsed_url = urlparse (link)
    root = parsed_url.netloc
    if root == 't.me':
        GlinkT = link
        print (f'{GlinkT=}')
        # print (f'{parsed_url=}')
        set_message (parsed_url)
        # if GO3 == 'telethon':
        #     func_telethon ()
        # if GO3 == 'pyrogram':
        #     func_pyrogram ()
        func_telethon ()
        func_pyrogram ()
        pyperclip.copy ('')
        print (f'Wait ...')
    return None
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

    global Gapi_id
    global Gapi_hash
    global Gphone
    global Glogin
    global Gpassword

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
    # INIT
    #----------------------------------------------
    os.makedirs (GO2, exist_ok=True)
    stop_file = os.path.join (GO2, 'stop')
    # print(stop_file)
    if Path (stop_file).is_file():
        os.remove (stop_file)
    pyperclip.copy ('')
    # ---------------------------------------------------------------
    # Ссылка на сообщение
    # ---------------------------------------------------------------
    Gmessage_url = GO1
    # Gmessage_url = "https://t.me/_канал_/_id_"
    # Gmessage_url = 'https://t.me/GardeZ66/13311'
    # Gmessage_url = 'https://t.me/GardeZ66/13285'
    # Gmessage_url = 'https://t.me/Selectel/5813'
    # Gmessage_url = 'https://t.me/+MnXPMuA95QdlMTYy/5765'
    # Gmessage_url = 'https://t.me/1471170142/7606'
    # ---------------------------------------------------------------

    # ----------------------------------------------
    # Данные API (получите на my.telegram.org)
    # ----------------------------------------------
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

    # get_telethon_mygroups ()
    # get_telethon_chats ()
    # get_telethon_groups ()
    # get_telethon_users_group ()

    if not Gmessage_url == '':
        check_link(Gmessage_url)
    else:
        print (f'Wait ...')
        while True and not Path (stop_file).is_file ():
            Gmessage_url = pyperclip.paste()
            check_link(Gmessage_url)
        #endwhile
    #endif
    if Path (stop_file).is_file():
        os.remove (stop_file)

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
