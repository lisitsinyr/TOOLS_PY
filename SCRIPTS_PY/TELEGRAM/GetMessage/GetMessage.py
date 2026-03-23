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
from pathlib import Path
import textwrap
import logging
import datetime
import re

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------
from urllib.parse import urlparse
from decouple import config
import pyperclip

#------------------------------------------
# БИБЛИОТЕКА telethon
#------------------------------------------
# import telethon
import telethon.sync
import telethon.tl.types
from telethon.tl.types import PeerChannel

#------------------------------------------
# БИБЛИОТЕКА pyrogram
#------------------------------------------
# from pyrogram import Client
import pyrogram

#------------------------------------------
# БИБЛИОТЕКА lyrpy
#------------------------------------------
import lyrpy.LUConst as LUConst
import lyrpy.LULog as LULog
import lyrpy.LUParserARG as LUParserARG
import lyrpy.LUTelegram as LUTelegram

#------------------------------------------
#
#------------------------------------------
GO1 = ''
GO2 = ''
GO3 = ''

Gapi_id = ''
Gapi_hash = ''
Gphone = ''
Glogin = ''
Gpassword = ''
Gmessage_url = ''
GlinkT = ''

Gchannel_name = ''
Gchannel_name_raw = ''
Gchannel_name_id = 0
Gmessage_id = 0
Gmessage_directory = ''

# Gdownload_path = r'G:\___РАЗБОР\YOUTUBE\TELEGRAM'
Gdownload_path = r'G:\___РАЗБОР\TELEGRAM'
Gwidth = 60

def sanitize_filename (filename, replacement = '_', platform = None):
    """
    Очищает строку, оставляя только допустимые символы для имени файла.

    :param filename: исходное имя файла
    :param replacement: символ для замены недопустимых символов
    :param platform: целевая платформа ('windows', 'linux', 'darwin' и т.д.), по умолчанию используется текущая ОС
    :return: корректное имя файла
    """
    if not platform:
        platform = os.name

    # Обрезаем до разумной длины (обычно максимум 255 байт)
    max_length = 255

    # Удаление начальных и конечные пробелы
    filename = filename.strip ()

    # Замена недопустимых символов
    if platform == 'nt':  # Windows
        invalid_chars = r'[<>:"/\\|?*\x00-\x1F]'
    else:  # Linux/macOS
        invalid_chars = r'[/\x00]'

    filename = re.sub (invalid_chars, replacement, filename)

    # Удаление лишних точек и подряд идущих заменителей
    filename = re.sub (r'(\.' + re.escape (replacement) + r')+', '.', filename)
    filename = re.sub (re.escape (replacement) + r'{2,}', replacement, filename)

    # Если имя стало пустым — вернуть дефолт
    if not filename:
        filename = f"unnamed_file{replacement}"

    return filename [:max_length]

# ----------------------------------------------
# get_telethon_mygroups ():
# ----------------------------------------------
def get_telethon_mygroups ():
    """get_telethon_mygroups"""
    # beginfunction
    LIB_name = 'LIB:telethon'
    LUTelegram.LIB_name = LIB_name

    # print (f'{LIB_name:{'_'}<{60}}')
    LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, f'{LIB_name:{'_'}<{60}}')
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
    # me = LUTelegram.get_telethon_me (Tclient)

    LUTelegram.get_telethon_mygroups (Tclient)

    Tclient.disconnect ()
# endfunction

# # ----------------------------------------------
# # get_telethon_chats ():
# # ----------------------------------------------
# def get_telethon_chats ():
#     """get_telethon_chats"""
#     # beginfunction
#     LIB_name = 'LIB:telethon'
#     LUTelegram.LIB_name = LIB_name
#
#     # print (f'{LIB_name:{'_'}<{60}}')
#     LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, f'{LIB_name:{'_'}<{60}}')
#     # -------------------------------------------
#     # Авторизация в Telegram
#     # -------------------------------------------
#     # Имя сессии (может быть любым)
#     session_name = 'lyr60_TELEGRAM'
#     print (f'{LIB_name}_session_name={session_name}')
#     Tclient = LUTelegram.get_telethon_client (session_name, Gapi_id, Gapi_hash,
#                                               Gphone, Gpassword)
#     # -------------------------------------------
#     #
#     # -------------------------------------------
#     # LUTelegram.get_telethon_mygroups (Tclient)
#     # -------------------------------------------
#     #
#     # -------------------------------------------
#     # LUTelegram.get_telethon_chats (Tclient)
#     # -------------------------------------------
#     # Getting information about yourself
#     # -------------------------------------------
#     me = LUTelegram.get_telethon_me (Tclient)
#
#     # LUTelegram.get_telethon_chats (Tclient)
#
#     Tclient.disconnect ()
# # endfunction

# ----------------------------------------------
# get_telethon_groups ():
# ----------------------------------------------
def get_telethon_groups ():
    """get_telethon_groups"""
# beginfunction
    LIB_name = 'LIB:telethon'
    LUTelegram.LIB_name = LIB_name

    # print (f'{LIB_name:{'_'}<{60}}')
    LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, f'{LIB_name:{'_'}<{60}}')
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
    # me = LUTelegram.get_telethon_me (Tclient)

    # -------------------------------------------
    #
    # -------------------------------------------
    groups = LUTelegram.get_telethon_groups (Tclient)
    for group in groups:
        print (f"{LIB_name}_group={group}")
    #endfor
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

    # print (f'{LIB_name:{'_'}<{60}}')
    LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, f'{LIB_name:{'_'}<{60}}')
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
    # me = LUTelegram.get_telethon_me (Tclient)

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
        #endfor
    #endfor
    Tclient.disconnect ()
# endfunction

# ----------------------------------------------
# func_telethon ():
# ----------------------------------------------
def func_telethon ():
    """func_telethon"""
#beginfunction
    LIB_name = 'LIB:telethon'
    LUTelegram.LIB_name = LIB_name

    # print (f'{LIB_name:{'_'}<{60}}')
    LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, f'{LIB_name:{'_'}<{60}}')
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

    #-------------------------------------------
    #
    #-------------------------------------------
    # LUTelegram.get_telethon_chats (Tclient)

    #-------------------------------------------
    # Getting information about yourself
    #-------------------------------------------
    # me = LUTelegram.get_telethon_me (Tclient)

    #-------------------------------------------
    # channel
    #-------------------------------------------
    try:
        channel: telethon.tl.types.Channel = LUTelegram.get_telethon_channel (Tclient, Gchannel_name_raw)
    except:
        channel = None
    #endtry
    if not channel:
        try:
            channel: telethon.tl.types.Channel = LUTelegram.get_telethon_channel (Tclient, Gchannel_name_id)
        except:
            channel = None
        #endtry
    #endif

    # -------------------------------------------
    # Получаем сообщение
    # -------------------------------------------
    message:telethon.tl.types.Message = LUTelegram.get_telethon_message (Tclient, channel, Gmessage_id)
    if not message:
        Tclient.disconnect ()
        return 1
    #endif
    # -------------------------------------------
    # message_file
    # -------------------------------------------
    Gchannel_name_s = sanitize_filename (Gchannel_name, replacement = '_', platform = None)
    try:
        message_file:str = Gchannel_name_s + '_' + str (Gmessage_id) + '_' + message.date.strftime ("%Y%m%d") + '.md'
        message_file:str = os.path.join (Gmessage_directory, message_file)
        # print (message_file)
    except:
        print ('ERROR: message_file')
        message_file:str = 'message_file.md'
    #endtry
    if Path (message_file).is_file ():
        os.remove (message_file)
    #endif

    # -------------------------------------------
    #
    # -------------------------------------------
    write_message_file ('Link: ' + Gmessage_url, message_file)
    try:
        write_message_file ('Дата: ' + str (message.date), message_file)
    except:
        pass
    try:
        write_message_file ('Title: ' + message.chat.title, message_file)
    except:
        pass

    # -------------------------------------------
    # Выводим текст сообщения
    # -------------------------------------------
    if hasattr(message, 'text'):
        if message.text:
            # write_message_file (message.message, message_file)
            write_message_file (message.text, message_file)
    #endif

    # -------------------------------------------
    # Если есть медиа (фото, видео, документ)
    # -------------------------------------------
    if hasattr(message, 'media'):
        if message.media:
            # print (message.media)
            # grouped_id = message.grouped_id
            # print (f'{LIB_name}_message.grouped_id={grouped_id}')
            # if message.audio:
            #     print (message.audio)
            if message.video:
                # print (message.video)
                try:
                    # print (message.video.attributes [1].file_name)
                    # print (message.media.document.attributes [1].file_name)
                    # print (message.document.attributes [1].file_name)
                    if Gchannel_name_id is None:
                        LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, f'{LIB_name} Gchannel_name_id is None')
                    else:
                        LULog.LoggerAdd (LULog.LoggerAPPS,
                                         LULog.TEXT, f'{LIB_name} ЗАГРУЗКА ВИДЕО пропущена ...')
                        # file_path = Tclient.download_media (message, Gmessage_directory)
                        # print (f"{LIB_name}_message.video: {file_path}")
                        # LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, f"{LIB_name}_message.video: {file_path}")
                except:
                    # print (f"{LIB_name}_message.video: ERROR")
                    LULog.LoggerAdd (LULog.LoggerAPPS, logging.ERROR, f"{LIB_name}_message.video: ERROR")
                #endtry
            #endif

            if message.photo:
                # print (message.photo)
                try:
                    file_path = Tclient.download_media(message, Gmessage_directory)
                    LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT,
                                     f"{LIB_name} message.photo: {file_path}")
                except:
                    # print(f"{LIB_name}_message.photo: ERROR")
                    LULog.LoggerAdd (LULog.LoggerAPPS, logging.ERROR,
                                     f"{LIB_name} message.photo: ERROR")
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
            #endif

        else:
            # print (f"{LIB_name}_В сообщении нет медиафайлов.")
            LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT,
                             f"{LIB_name} В сообщении нет медиафайлов ...")
            # pass
        #endif

    Tclient.disconnect ()
    return 0
#endfunction

# ----------------------------------------------
# func_pyrogram ():
# ----------------------------------------------
def func_pyrogram ():
    """func_pyrogram"""
#beginfunction
    LIB_name = 'LIB:pyrogram'
    LUTelegram.LIB_name = LIB_name

    # print (f'{LIB_name:{'_'}<{60}}')
    LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, f'{LIB_name:{'_'}<{60}}')

    #-------------------------------------------
    # Авторизация в Telegram
    #-------------------------------------------
    # # Имя сессии (может быть любым)
    # session_name = 'lyr60'
    # print (f'{LIB_name}_session_name={session_name}')
    Tclient: pyrogram.Client = LUTelegram.get_pyrogram_client (Gapi_id, Gapi_hash, Glogin, Gphone)

    # -------------------------------------------
    # Getting information about yourself
    # -------------------------------------------
    # me: pyrogram.User = LUTelegram.get_pyrogram_me (Tclient)
    # print (f"{me=}")

    #-------------------------------------------
    # Получаем сообщение
    #-------------------------------------------
    print (f"{Gchannel_name_raw=}")
    print (f"{Gchannel_name_id=}")
    try:
        chat = Tclient.get_chat (Gchannel_name_raw)
        # print(f'chat={chat}')
        # print(f'chat.description={chat.description}')
        # print(f'{LIB_name}_chat.title={chat.title}')
        # print(f'{LIB_name}_chat.username={chat.username}')
    except:
        chat = None
        # LULog.LoggerAdd (LULog.LoggerAPPS, logging.ERROR, f"{Gchannel_name_raw=}")
    #endtry
    if not chat is None:
        try:
            chat = Tclient.get_chat (Gchannel_name_id)
        except:
            chat = None
            # LULog.LoggerAdd (LULog.LoggerAPPS, logging.ERROR, f"{Gchannel_name_id=}")
        #endtry

    try:
        message = Tclient.get_messages (chat.id, Gmessage_id)
    except:
        message = None

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

        # today = datetime.datetime.utcnow()
        today = datetime.datetime.now (datetime.UTC)
        if message.video:
            # print (message.video)
            if Gchannel_name_id is None:
                if message.video.file_name is None:
                    file_media = 'video_'+f'{today:%Y-%m-%d_%H-%M-%S}'+'.mp4'
                    file_media_path = os.path.join (Gmessage_directory, file_media)

                    # print (file_media_path)

                    if Path (file_media_path).is_file ():
                        os.remove (file_media_path)
                    #endif
                    LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, f'ЗАГРУЗКА ВИДЕО {file_media_path} ...')

                    LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT,
                                     f'ЗАГРУЗКА ВИДЕО '
                                     f'{file_media_path} пропущена ...')
                    # file_media_path = Tclient.download_media (message, file_media_path)

                    # print (f"{LIB_name}_message.video: {file_media_path}")
                    LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, file_media_path)
                else:
                    file_media_path = os.path.join (Gmessage_directory, message.video.file_name)

                    # print (file_media_path)

                    if Path (file_media_path).is_file ():
                        os.remove (file_media_path)
                    #endif
                    LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, f'ЗАГРУЗКА ВИДЕО {message.video.file_name} ...')
                    try:
                        LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT,
                                         f'ЗАГРУЗКА ВИДЕО '
                                         f'{file_media_path} пропущена ...')
                        # file_media_path = Tclient.download_media (message, file_media_path)

                        # print(f"{LIB_name}_message.video: {file_media_path}")
                        LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, f'{file_media_path}')
                    except:
                        # print (f"{LIB_name}_message.video: ERROR")
                        LULog.LoggerAdd (LULog.LoggerAPPS, logging.ERROR, f"{LIB_name}_message.video: ERROR")
                    #endtry
                #endif
            #endif
        else:
            # print (f"{LIB_name}_В сообщении нет видеофайлов")
            LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT,
                             f"{LIB_name} В сообщении нет видеофайлов ...")
            # pass
        #endif

        # if message.photo:
        #     # file_media = os.path.join (Gmessage_directory, message.photo.file_id)
        #     # if Path (file_media).is_file ():
        #     #     os.remove (file_media)
        #     # print ("file_id: " + str (message.photo.file_id))
        #     file_path = bot.download_media (message.photo)
        #     print(f"{LIB_name}_download_file: {file_path}")
    else:
        Tclient.stop ()
        return 0

    Tclient.stop ()
    return 0
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
        #endif
        formatted_paragraphs.append (s)
    # endfor
    formatted_paragraphs.append ('\n')

    with open (filepath, 'a', encoding='utf-8') as file:
        file.write ('\n'.join (formatted_paragraphs))
    #endwith
    return None
#endfunction

# ----------------------------------------------
#
# ----------------------------------------------
def get_channel_name_ (channel_id) -> str:
    """get_channel_name_"""
#beginfunction
    #-------------------------------------------
    # Авторизация в Telegram
    #-------------------------------------------
    # Имя сессии (может быть любым)
    session_name = 'lyr60_TELEGRAM'
    Tclient = LUTelegram.get_telethon_client (session_name, Gapi_id, Gapi_hash, Gphone, Gpassword)
    entity = Tclient.get_entity (PeerChannel (channel_id))
    Tclient.disconnect ()

    return entity.title
#endfunction

#------------------------------------------
#  set_message ():
#------------------------------------------
def set_message (url) -> None:
    """set_message"""
#beginfunction
    global Gchannel_name
    global Gchannel_name_raw
    global Gchannel_name_id
    global Gmessage_id
    global Gmessage_directory

    if url.path.split('/')[1] == 'c':
        Gmessage_id = int(url.path.split('/')[3])           # Получаем 9999
        # print(f'{Gmessage_id=}')
        Gchannel_name_id = int(url.path.split('/')[2])      # Получаем 9999999999999
        print(f'{Gchannel_name_id=}')
        # Gchannel_name = LUTelegram.get_channel_name (GlinkT,'lyr60_TELEGRAM', Gapi_id, Gapi_hash, Gphone)
        Gchannel_name_raw = get_channel_name_ (Gchannel_name_id)
    else:
        Gmessage_id = int(url.path.split('/')[2])           # Получаем 9999
        # print(f'{Gmessage_id=}')
        Gchannel_name_id = None
        Gchannel_name_raw = url.path.split('/')[1]              # Получаем "xx...xx"
    # print (f'{Gchannel_name_raw=}')

    Gchannel_name = sanitize_filename (Gchannel_name_raw, replacement = '_', platform = None)
    # print(Gchannel_name)

    # s = re.sub (r'[^a-zA-Z0-9]', '', Gchannel_name)
    # Gchannel_name_s = sanitize_filename (Gchannel_name_raw, replacement = '_', platform = None)

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
        # print (f'{GlinkT=}')
        # print (f'{parsed_url=}')
        LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, f'{GlinkT}')
        set_message (parsed_url)
        error = func_telethon ()
        if error > 0:
            # print(f'{error=}')
            LULog.LoggerAdd (LULog.LoggerAPPS, logging.ERROR, f'{error=}')
        error = func_pyrogram ()
        if error > 0:
            # print(f'{error=}')
            LULog.LoggerAdd (LULog.LoggerAPPS, logging.ERROR, f'{error=}')
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
    # LULog.LoggerAPPS.level = logging.INFO
    LULog.LoggerAPPS.level = 0


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
    logger = logging.getLogger('telethon.client.downloads')
    logger.setLevel(logging.ERROR)

    LArgParser = LUParserARG.TArgParser (description = 'Параметры', prefix_chars = '-/')
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
    # 🔗 Пример ссылки:
    # Telegram-сообщение может выглядеть так:
    # https://t.me/channelname/1234
    # или
    # https://t.me/c/123456789/1234
    # ---------------------------------------------------------------
    # Gmessage_url = 'https://t.me/GardeZ66/13311'
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
    
    print (f'Wait ...')
    while True and not Path (stop_file).is_file ():
        Gmessage_url = pyperclip.paste()
        check_link(Gmessage_url)
    #endwhile

    if Path (stop_file).is_file():
        os.remove (stop_file)

    LULog.STOPLogging ()
#endfunction

#------------------------------------------
#
#------------------------------------------
#beginmodule
if __name__ == "__main__":
    # today = datetime.datetime.utcnow()
    # today = datetime.datetime.now (datetime.UTC)
    # file_media = 'video_' + f'{today:%Y-%m-%d_%H-%M-%S}' + '.mp4'
    # print (file_media)

    main()
#endif

#endmodule
