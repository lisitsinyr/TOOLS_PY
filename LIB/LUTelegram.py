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

# from telethon.tl.types import User
# # класс, позволяющий нам подключаться к клиенту мессенджера и работать с ним;
# from telethon.sync import TelegramClient
# # PeerChannel - специальный тип, определяющий объекты типа «канал/чат»,
# # с помощью которого можно обратиться к нужному каналу для парсинга сообщений.
# from telethon.tl.types import Channel, PeerChannel, PeerChat, PeerUser, Message, User, MessageMediaPhoto, MessageMediaDocument
# # конструктор для работы с InputPeer, который передаётся в качестве аргумента в GetDialogsRequest;
# from telethon.tl.types import InputMessagesFilterPhotos
# # функция, позволяющая работать с сообщениями в чате;
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
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
# Авторизация в Telegram [telethon]
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
    print (f'{LIB_name}_user_authorized={result.is_user_authorized()}')
    return result
# endfunction

# ------------------------------------------
# Получить the current User who is logged
# ------------------------------------------
def get_telethon_me (client:telethon.sync.TelegramClient) -> telethon.tl.types.User:
    """get_telethon_client"""
# beginfunction
    result:User = client.get_me ()
    print (f'{LIB_name}_username={result.username}')
    print (f'{LIB_name}_phone={result.phone}')
    # print (f'{LIB_name}_stringify={result.stringify()}')
    return result
# endfunction

# ------------------------------------------
# Получить channel
# ------------------------------------------
def get_telethon_channel (client:telethon.sync.TelegramClient, channel_name_id) -> telethon.tl.types.Channel:
    """get_telethon_client"""
# beginfunction
    result = client.get_entity (channel_name_id)
    # print (result)
    print(f'{LIB_name}_Channel.title={result.title}')
    print(f'{LIB_name}_Channel.id={result.id}')
    print(f'{LIB_name}_Channel.username={result.id}')
    return result
# endfunction

# ------------------------------------------
# Получить message
# ------------------------------------------
def get_telethon_message (client:telethon.sync.TelegramClient, channel:telethon.tl.types.Channel, message_id) -> telethon.tl.types.Message:
    """get_telethon_client"""
# beginfunction
    result = client.get_messages (channel.id, ids=message_id)
    # print(f'{LIB_name}_Message={result}')
    return result
# endfunction

#------------------------------------------
# get_telethon_mygroups (client:TelegramClient):
#------------------------------------------
def get_telethon_mygroups (client:telethon.sync.TelegramClient):
    """get_mygroups"""
#beginfunction
    # Получение списка диалогов
    dialogs = client.get_dialogs()
    # Отображение списка групп
    for dialog in dialogs:
        if dialog.is_group:
            print(f"{LIB_name}_Группа: {dialog.title} (ID: {dialog.id})")
#endfunction

#------------------------------------------
# Получить список групп
#------------------------------------------
def get_telethon_chats (client:telethon.sync.TelegramClient):
    """get_chats"""
#beginfunction
    chats = []
    last_date = None
    size_chats = 200
    groups = []

    #-----------------------------------------------
    # Напишем запрос для получения списка групп
    #-----------------------------------------------
    # offset_date и offset_peer мы передаём с пустыми значениями.
    # Обычно они используются для фильтрации полученных данных, но здесь мы
    # хотим получить весь список. Лимит по количеству элементов в ответе задаём 200,
    # передавая в параметр limit переменную size_chats.
    result = client (GetDialogsRequest (
        offset_date=last_date,
        offset_id=0,
        offset_peer=InputPeerEmpty (),
        limit=size_chats,
        hash=0
    ))
    chats.extend (result.chats)

    #-----------------------------------------------
    #
    #-----------------------------------------------
    for chat in chats:
        try:
            print (int(chat.megagroup), chat.title)
            if chat.megagroup == True:
                groups.append (chat)
        except:
            continue
    # понять, канал или чат, можно проверяя у диалога параметр "dialog.entity.megagroup
    for dialog in client.iter_dialogs ():
        if 'Channel' in str (type (dialog.entity)):  # откидываем юзеров
            if dialog.entity.megagroup:
                print (dialog.entity.id, '//', dialog.entity.username,
                       ' - ', dialog.name, ' is CHAT')
            else:
                print (dialog.entity.id, '//', dialog.entity.username,
                       ' - ', dialog.name, ' is CHANNEL')

    # #-----------------------------------------------
    # #
    # #-----------------------------------------------
    # print('Выберите номер группы из перечня:')
    # i=0
    # for g in groups:
    #    print(str(i) + '- ' + g.title)
    #    i+=1
    # #-----------------------------------------------
    # # Теперь дадим пользователю возможность выбрать нужную группу из списка для последующего парсинга:
    # #-----------------------------------------------
    # g_index = input("Введите нужную цифру: ")
    # target_group=groups[int(g_index)]

    # #-----------------------------------------------
    # #
    # #-----------------------------------------------
    # target_group=groups[0]
    # print ('Узнаём пользователей...')
    # all_participants = []
    # all_participants = Tclient.get_participants (target_group)
    #
    # print ('Сохраняем данные в файл...')
    # # with open ("members.csv", "w", encoding='UTF-8') as f:
    #     # writer = csv.writer (f, delimiter=",", lineterminator="\n")
    #     # writer.writerow (['username', 'name', 'group'])
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
    #         # writer.writerow ([username, name, target_group.title])
    # print ('Парсинг участников группы успешно выполнен.')

    # #-----------------------------------------------
    # #
    # #-----------------------------------------------
    # all_messages = []
    # offset_id = 0
    # limit = 100
    # total_messages = 0
    # total_count_limit = 0
    # while True:
    #     history = Tclient (GetHistoryRequest (
    #         peer=target_group,
    #         offset_id=offset_id,
    #         offset_date=None,
    #         add_offset=0,
    #         limit=limit,
    #         max_id=0,
    #         min_id=0,
    #         hash=0
    #     ))
    #
    #     if not history.messages:
    #         break
    #
    #     messages = history.messages
    #
    #     for message in messages:
    #         # all_messages.append (message.to_dict ())
    #         all_messages.append (message.message)
    #
    #     offset_id = messages [len (messages) - 1].id
    #
    #     if total_count_limit != 0 and total_messages >= total_count_limit:
    #         break
    #
    #     for message in all_messages:
    #         print (message)
    #
    #     # print ("Сохраняем данные в файл...")  # Cообщение для пользователя о том, что начался парсинг сообщений.
    #     # with open ("chats.csv", "w", encoding="UTF-8") as f:
    #     #     writer = csv.writer (f, delimiter=",", lineterminator="\n")
    #     #     writer.writerow (["message"])
    #     #     for message in all_messages:
    #     #         writer.writerow ([message])
    #     # print ("Парсинг сообщений группы успешно выполнен.")  # Сообщение об удачном парсинге чата.

#endfunction

# ----------------------------------------------
# Получаем последние 10 сообщений из указанного чата
# ----------------------------------------------
def get_telethon_chat (client:telethon.sync.TelegramClient, chat_id):
    """func_02"""
#beginfunction
    # ID чата/канала/пользователя, откуда читать сообщения
    # chat_id = '@GardeZ66'  # или ID (число), или юзернейм (например, '@telegram')
    for message in client.iter_messages (chat_id, limit=10):
        print (f"{LIB_name}_message.sender_id:{message.sender_id}: {message.text}")
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
    print (f'{LIB_name}_is_connected={result.is_connected}')
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
    print (f'{LIB_name}_username={result.username}')
    print (f'{LIB_name}_phone_number={result.phone_number}')
    # print (f'pyrogram:stringify={result.stringify()}')
    return result
# endfunction

#---------------------------------------------------------
# main
#---------------------------------------------------------
def main ():
#beginfunction
    ...
#endfunction

#---------------------------------------------------------
#
#---------------------------------------------------------
#beginmodule
if __name__ == "__main__":
    main()
#endif

#endmodule
