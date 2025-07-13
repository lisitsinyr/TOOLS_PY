"""LUTelegram.py"""
# -*- coding: UTF-8 -*-
__annotations__ = """
 =======================================================
 Copyright (c) 2025
 Author:
     Lisitsin Y.R.
 Project:
     lyrpy
     
 Module:
     LUTelegram.py

 =======================================================
"""

from fontTools.misc.cython import returns
#------------------------------------------
# БИБЛИОТЕКИ python
#------------------------------------------

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------

#------------------------------------------
# БИБЛИОТЕКА telethon
#------------------------------------------
# import telethon
import telethon.sync
import telethon.tl.types

from telethon.sync import TelegramClient
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
import re
import asyncio

# from telethon.tl.functions.messages import GetDialogsRequest
# from telethon.tl.types import InputPeerEmpty
# from telethon.tl.types import User
# # класс, позволяющий нам подключаться к клиенту мессенджера и работать с ним;
# from telethon.sync import TelegramClient
# # PeerChannel - специальный тип, определяющий объекты типа «канал/чат»,
# # с помощью которого можно обратиться к нужному каналу для парсинга сообщений.
# from telethon.tl.types import Channel, PeerChannel, PeerChat, PeerUser, Message, User, MessageMediaPhoto, MessageMediaDocument
# # конструктор для работы с InputPeer, который передаётся в качестве аргумента в GetDialogsRequest;
# from telethon.tl.types import InputMessagesFilterPhotos
# # функция, позволяющая работать с сообщениями в чате;
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
# БИБЛИОТЕКИ LU
#------------------------------------------

LIB_name = ''

# ------------------------------------------
# Авторизация в Telegram
# get_telethon_client (session_name, api_id, api_hash, phone, password) -> telethon.sync.TelegramClient:
# ------------------------------------------
def get_telethon_client (session_name, api_id, api_hash, phone, password) -> telethon.sync.TelegramClient:
    """get_telethon_client"""
# beginfunction
    result = telethon.sync.TelegramClient(session_name, api_id, api_hash, system_version="4.16.30-vxNAME ")
    #   Вместо NAME используйте любое сочетание букв на английском КАПСОМ Пример: vxXYI, vxABC, vxMYNAME
    #   # (в папке с кодом нет файлика .session, клиент сам его создаст (в нашем случае 'my_session')
    #   # и будет с ним работать. Поэтому просто вставляем эти параметры в инициализацию и кайфуем:finger_up: )

    # Tclient = TelegramClient (Gsession_name, Gapi_id, Gapi_hash,
    #                           #         device_model = "iPhone 13 Pro Max",
    #                           #         app_version = "8.4",
    #                           #         lang_code = "en",
    #                           #         system_lang_code = "en-US")
    #                           system_version='4.16.30-vxABC')
    # Tclient.start (phone=Gphone, password=Gpassword)
    result.start (phone=phone, password=password)
    result.connect ()
    # print (f'{LIB_name}_user_authorized={result.is_user_authorized()}')
    return result
# endfunction

# ------------------------------------------
# Получить the current User who is logged
# get_telethon_me (client:telethon.sync.TelegramClient) -> telethon.tl.types.User:
# ------------------------------------------
def get_telethon_me (client:telethon.sync.TelegramClient) -> telethon.tl.types.User:
    """get_telethon_me"""
# beginfunction
    result:User = client.get_me ()

    # print (f'{LIB_name}_username={result.username}')
    # print (f'{LIB_name}_phone={result.phone}')

    # print (f'{LIB_name}_stringify={result.stringify()}')
    return result
# endfunction

# ------------------------------------------
# Получить channel
# get_telethon_channel (client:telethon.sync.TelegramClient, channel_name_id) -> telethon.tl.types.Channel:
# ------------------------------------------
def get_telethon_channel (client:telethon.sync.TelegramClient, channel_name_id) -> telethon.tl.types.Channel:
    """get_telethon_channel"""
# beginfunction
    result = client.get_entity (channel_name_id)
    # print (result)
    # print(f'{LIB_name}_Channel.title={result.title}')
    # print(f'{LIB_name}_Channel.id={result.id}')
    # print(f'{LIB_name}_Channel.username={result.id}')
    return result
# endfunction

# ------------------------------------------
# Получить message
# get_telethon_message (client:telethon.sync.TelegramClient, channel:telethon.tl.types.Channel, message_id) -> telethon.tl.types.Message:
# ------------------------------------------
def get_telethon_message (client:telethon.sync.TelegramClient, channel:telethon.tl.types.Channel, message_id) -> telethon.tl.types.Message:
    """get_telethon_message"""
# beginfunction
    try:
        result = client.get_messages (channel.id, ids=message_id)
        # print(f'{LIB_name}_Message={result}')
    except:
        result = None

    return result
# endfunction

#------------------------------------------
# Получить мои группы
# get_telethon_mygroups (client:TelegramClient):
#------------------------------------------
def get_telethon_mygroups (client:telethon.sync.TelegramClient):
    """get_telethon_mygroups"""
#beginfunction
    # Получение списка диалогов
    dialogs = client.get_dialogs()
    # Отображение списка групп
    for dialog in dialogs:
        if dialog.is_group:
            print(f"{LIB_name}_Группа: {dialog.title} (ID: {dialog.id})")
#endfunction

#------------------------------------------
# Получить список groups
#------------------------------------------
def get_telethon_groups (client:telethon.sync.TelegramClient) -> list:
    """get_telethon_groups"""
#beginfunction
    chats = []
    last_date = None
    size_chats = 200
    groups = []

    # -----------------------------------------------
    # Напишем запрос для получения списка групп
    # -----------------------------------------------
    # offset_date и offset_peer мы передаём с пустыми значениями.
    # Обычно они используются для фильтрации полученных данных, но здесь мы
    # хотим получить весь список. Лимит по количеству элементов в ответе задаём 200,
    # передавая в параметр limit переменную size_chats.
    result = client (telethon.tl.functions.messages.GetDialogsRequest (
        offset_date=last_date,
        offset_id=0,
        offset_peer=telethon.tl.types.InputPeerEmpty (),
        limit=size_chats,
        hash=0
    ))
    chats.extend (result.chats)

    # -----------------------------------------------
    #
    # -----------------------------------------------
    for chat in chats:
        try:
            # print (int(chat.megagroup), chat.title)

            # Megagroup в библиотеке Telethon — это свойство объекта Channel,
            # которое указывает, является ли он мегагруппой (большой группой).
            # Мегагруппы — это каналы, для которых значение свойства channel.megagroup равно True.
            # В официальных приложениях Telegram такие группы называются «супергруппами»

            if chat.megagroup == True:
                groups.append (chat)
        except:
            continue
    return groups

#endfunction

#------------------------------------------
# Получить список groups
#------------------------------------------
def get_telethon_groups (client:telethon.sync.TelegramClient) -> list:
    """get_telethon_groups"""
#beginfunction
    chats = []
    last_date = None
    size_chats = 200
    groups = []

    # -----------------------------------------------
    # Напишем запрос для получения списка групп
    # -----------------------------------------------
    # offset_date и offset_peer мы передаём с пустыми значениями.
    # Обычно они используются для фильтрации полученных данных, но здесь мы
    # хотим получить весь список. Лимит по количеству элементов в ответе задаём 200,
    # передавая в параметр limit переменную size_chats.
    result = client (telethon.tl.functions.messages.GetDialogsRequest (
        offset_date=last_date,
        offset_id=0,
        offset_peer=telethon.tl.types.InputPeerEmpty (),
        limit=size_chats,
        hash=0
    ))
    chats.extend (result.chats)
    # -----------------------------------------------
    #
    # -----------------------------------------------
    for chat in chats:
        try:
            # print (int(chat.megagroup), chat.title)
            # Megagroup в библиотеке Telethon — это свойство объекта Channel,
            # которое указывает, является ли он мегагруппой (большой группой).
            # Мегагруппы — это каналы, для которых значение свойства channel.megagroup равно True.
            # В официальных приложениях Telegram такие группы называются «супергруппами»
            if chat.megagroup == True:
                groups.append (chat)
            else:
                # groups.append (chat)
                pass
        except:
            continue
    return groups
#endfunction

#------------------------------------------
# Получить список users group
#------------------------------------------
def get_telethon_users_group (client:telethon.sync.TelegramClient, group) -> list:
    """get_telethon_users_group"""
#beginfunction
    #-----------------------------------------------
    # Узнаём пользователей...
    #-----------------------------------------------
    all_participants = []
    try:
        all_participants = client.get_participants (group, limit=100000)
        # print (group)
        # for user in all_participants:
        #     if user.username:
        #         username = user.username
        #     else:
        #         username = ""
        #     if user.first_name:
        #         first_name = user.first_name
        #     else:
        #         first_name = ""
        #     if user.last_name:
        #         last_name = user.last_name
        #     else:
        #         last_name = ""
        #     name = (first_name + ' ' + last_name).strip ()
        #     print(f'{username=}, {name=}, {target_group.title=}')
    except:
        pass
    return all_participants
#endfunction

#------------------------------------------
# Получить список CHATs
#------------------------------------------
def get_telethon_CHATs (client:telethon.sync.TelegramClient):
    """get_telethon_CHATs"""
#beginfunction
    # понять, канал или чат, можно проверяя у диалога параметр "dialog.entity.megagroup
    for dialog in client.iter_dialogs ():
        if 'Channel' in str (type (dialog.entity)):  # откидываем юзеров
            if dialog.entity.megagroup:
                print (dialog.entity.id, '//', dialog.entity.username,
                       ' - ', dialog.name, ' is CHAT')
#endfunction

#------------------------------------------
# Получить список CHANNELs
#------------------------------------------
def get_telethon_CHANNELs (client:telethon.sync.TelegramClient):
    """get_telethon_CHANNELs"""
#beginfunction
    # понять, канал или чат, можно проверяя у диалога параметр "dialog.entity.megagroup
    for dialog in client.iter_dialogs ():
        if 'Channel' in str (type (dialog.entity)):  # откидываем юзеров
            if not dialog.entity.megagroup:
                print (dialog.entity.id, '//', dialog.entity.username,
                       ' - ', dialog.name, ' is CHANNEL')
#endfunction

# ----------------------------------------------
# Получаем последние 10 сообщений из указанного чата
# ----------------------------------------------
def get_telethon_chat (client:telethon.sync.TelegramClient, chat_id):
    """get_telethon_chat"""
#beginfunction
    # ID чата/канала/пользователя, откуда читать сообщения
    # chat_id = '@GardeZ66'  # или ID (число), или юзернейм (например, '@telegram')
    for message in client.iter_messages (chat_id, limit=10):
        print (f"{LIB_name}_message.sender_id:{message.sender_id}: {message.text}")
#endfunction



# ----------------------------------------------
# Функция для парсинга ссылки
# ----------------------------------------------
def parse_message_link (link):
    """parse_message_link"""
#beginfunction
    pattern = r'https?://t\.me/([a-zA-Z0-9\_]+|c/(\d+))/(\d+)/(\d+)'
    match = re.match (pattern, link)
    if not match:
        raise ValueError ("Invalid link")

    # print(f'{match.group (1)=}')
    # print(f'{match.group (2)=}')
    # print(f'{match.group (3)=}')
    # print(f'{match.group (4)=}')

    if match.group (1).startswith ('c'):
        channel_id = int (match.group (3))
        msg_id = int (match.group (3))
        return {'channel_id': channel_id, 'msg_id': msg_id}
    else:
        username = match.group (1)
        msg_id = int (match.group (3))
        return {'username': username, 'msg_id': msg_id}
#endfunction

# ----------------------------------------------
# async def get_channel_name (link, TelegramClient):
# ----------------------------------------------
def get_channel_name (link, session_name, api_id, api_hash, phone):
    """get_channel_name"""
#beginfunction
    with TelegramClient (session_name, api_id, api_hash) as client:
        client.start (phone)
        # print (f'{link=}')
        parsed = parse_message_link (link)
        print (f'{parsed=}')

        if 'username' in parsed:
            entity = client.get_entity (parsed ['username'])
            # entity = client.get_entity (parsed ['msg_id'])
        elif 'channel_id' in parsed:
            entity = client.get_entity (PeerChannel (parsed ['channel_id']))
        else:
            raise ValueError ("Could not resolve entity")
        print (f"Название канала: {entity.title}")

    # client.disconnect ()

    return entity.title
#endfunction








# ------------------------------------------
# Авторизация в Telegram [pyrogram]
# ------------------------------------------
def get_pyrogram_client (api_id, api_hash, login, phone) -> pyrogram.Client:
    """get_pyrogram_client"""
# beginfunction
    result = pyrogram.Client (login, api_id=api_id, api_hash=api_hash, phone_number=phone)
    result.start ()
    # result.connect ()
    # print (f'{LIB_name}_is_connected={result.is_connected}')

    # print(Tclient.export_session_string())
    # print(result.workdir)

    # result.run ()
    return result
# endfunction

# ------------------------------------------
# Метод client.get_me() в библиотеке Pyrogram возвращает объект pyrogram.User
# с информацией о текущем зарегистрированном пользователе или боте.
# ------------------------------------------
def get_pyrogram_me (client:pyrogram.Client) -> pyrogram.types.User:
    """get_pyrogram_me"""
# beginfunction
    result = client.get_me()
    # print (f'{LIB_name}_username={result.username}')
    # print (f'{LIB_name}_phone_number={result.phone_number}')
    # print (f'pyrogram:stringify={result.stringify()}')
    return result
# endfunction

#---------------------------------------------------------
# main
#---------------------------------------------------------
def main ():
#beginfunction
    pass
#endfunction

#---------------------------------------------------------
#
#---------------------------------------------------------
#beginmodule
if __name__ == "__main__":
    main()
#endif

#endmodule
