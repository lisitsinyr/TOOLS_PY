"""ConnectTelegram.py"""
# -*- coding: UTF-8 -*-
__annotations__ = """
 =======================================================
 Copyright (c) 2026
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
import logging

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------
from decouple import config
import asyncio

#------------------------------------------
# БИБЛИОТЕКА telethon
#------------------------------------------
# import telethon
import telethon.sync
import telethon.tl.types
# from telethon.tl.types import Channel
from telethon import connection

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

# ------------------------------------------
# Авторизация в Telegram
# get_telethon_client (session_name, api_id, api_hash, phone, password) -> telethon.sync.TelegramClient:
# ------------------------------------------
def get_telethon_client (session_name, api_id, api_hash, phone, password) -> telethon.sync.TelegramClient:
    """get_telethon_client"""
# beginfunction
    LIB_name = 'LIB:telethon'
    LUTelegram.LIB_name = LIB_name

    # result = telethon.sync.TelegramClient(session_name, api_id, api_hash, system_version="4.16.30-vxNAME ")
    result = telethon.sync.TelegramClient(session_name, api_id, api_hash, system_version="4.43.1-vxNAME ")
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

    # try:
    #     result.start (phone=phone, password=password)
    #     result.run_until_disconnected ()
    # except Exception as e:
    #     print (f'Ошибка: {e}')

    result.start (phone=phone, password=password)
    result.connect ()
    print (f'{LIB_name}_user_authorized={result.is_user_authorized()}')

    return result
# endfunction

# ------------------------------------------
# Авторизация в Telegram
# get_telethon_client (session_name, api_id, api_hash, phone, password) -> telethon.sync.TelegramClient:
# ------------------------------------------
def get_telethon_client_PROXY (session_name, api_id, api_hash, phone, password) -> telethon.sync.TelegramClient:
    """get_telethon_client_PROXY"""
# beginfunction
    LIB_name = 'LIB:telethon'
    LUTelegram.LIB_name = LIB_name
    # proxy = (mtproto, 't.7.mazeram.com', 443, 'ee470cb2b8b29aeadfbdf8a2f7bee5ca3b62726f777365722e79616e6465782e636f6d')

    # Параметры MTProto прокси
    PROXY_IP = 'mtc4ljewnc4ymtmumjuz.he-de-24.mtproto.ru'
    PROXY_PORT = 443
    PROXY_SECRET = 'ee2111222233334444555566667777888865756331332e706c61796c6973742e7474766e772e6e6574'  # Например: 'ee1234567890abcdef'

    # Создаем клиента с поддержкой MTProto прокси
    client = telethon.TelegramClient (
        session_name, api_id, api_hash,
        proxy=(PROXY_IP, PROXY_PORT, PROXY_SECRET),
        connection = connection.ConnectionTcpMTProxyRandomizedIntermediate
    )

    # result = telethon.sync.TelegramClient (session_name, api_id, api_hash,
    #                                        # Use one of the available connection modes.
    #                                        # Normally, this one works with most proxies.
    #                                        connection=connection.ConnectionTcpMTProxyRandomizedIntermediate,
    #                                        # Then, pass the proxy details as a tuple:
    #                                        #     (host name, port, proxy secret)
    #                                        #
    #                                        # If the proxy has no secret, the secret must be:
    #                                        #     '00000000000000000000000000000000'
    # proxy=('t.7.mazeram.com', 443, 'ee470cb2b8b29aeadfbdf8a2f7bee5ca3b62726f777365722e79616e6465782e636f6d'))

    client.start ()

    # Проверяем, что мы вошли
    me = client.get_me ()
    print (f"Успешный вход! Ваш ID: {me.id}, Имя: {me.first_name}")

    # try:
    #     result.start (phone=phone, password=password)
    #     result.run_until_disconnected ()
    # except Exception as e:
    #     print (f'Ошибка: {e}')

    print("✅ Подключено к Telegram через MTProto прокси!")

    # client.connect ()

    print (f'{LIB_name}_user_authorized={client.is_user_authorized()}')

    # client.start (phone=phone, password=password)

    return client
# endfunction

# ------------------------------------------
# Получить the current User who is logged
# get_telethon_me (client:telethon.sync.TelegramClient) -> telethon.tl.types.User:
# ------------------------------------------
def get_telethon_me (client:telethon.sync.TelegramClient) -> telethon.tl.types.User:
    """get_telethon_me"""
# beginfunction
    result:telethon.tl.types.User = client.get_me ()

    # print (f'{LIB_name}_username={result.username}')
    # print (f'{LIB_name}_phone={result.phone}')

    # print (f'{LIB_name}_stringify={result.stringify()}')
    return result
# endfunction

# ----------------------------------------------
# func_telethon ():
# ----------------------------------------------
def func_telethon ():
    """func_telethon"""
#beginfunction
    LIB_name = 'LIB:telethon'
    # LUTelegram.LIB_name = LIB_name
    # print (f'{LIB_name:{'_'}<{60}}')
    LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, f'{LIB_name:{'_'}<{60}}')

    #-------------------------------------------
    # Авторизация в Telegram
    #-------------------------------------------
    # Имя сессии (может быть любым)
    session_name = 'lyr60_TELEGRAM'
    # print(session_name, Gapi_id, Gapi_hash, Gphone, Gpassword)

    # Tclient = get_telethon_client (session_name, Gapi_id, Gapi_hash, Gphone, Gpassword)
    Tclient = get_telethon_client_PROXY (session_name, Gapi_id, Gapi_hash, Gphone, Gpassword)

    print (f'{LIB_name}_session_name={session_name}')

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
    # me = get_telethon_me (Tclient)

    # Tclient.disconnect ()

    return 0
#endfunction

# ----------------------------------------------
# func_pyrogram ():
# ----------------------------------------------
def func_pyrogram ():
    """func_pyrogram"""
#beginfunction
    LIB_name = 'LIB:pyrogram'
    # LUTelegram.LIB_name = LIB_name

    # print (f'{LIB_name:{'_'}<{60}}')
    LULog.LoggerAdd (LULog.LoggerAPPS, LULog.TEXT, f'{LIB_name:{'_'}<{60}}')

    # -------------------------------------------
    # Авторизация в Telegram
    # -------------------------------------------
    # # Имя сессии (может быть любым)
    session_name = 'lyr60'
    # print (f'{LIB_name}_session_name={session_name}')
    Tclient: pyrogram.Client = LUTelegram.get_pyrogram_client (Gapi_id, Gapi_hash, Glogin, Gphone)

    # -------------------------------------------
    # Getting information about yourself
    # -------------------------------------------
    # me: pyrogram.User = LUTelegram.get_pyrogram_me (Tclient)
    # print (f"{me=}")

    Tclient.stop ()

    return 0
#endfunction

#------------------------------------------
#  main ():
#------------------------------------------
def main ():
    """main"""
#beginfunction
    global Gapi_id
    global Gapi_hash
    global Gphone
    global Glogin
    global Gpassword

    # tracemalloc.start ()

    LUConst.SET_LIB(__file__)

    LULog.STARTLogging (LULog.TTypeSETUPLOG.tslINI, 'console', '', '', '')
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

    func_telethon ()

    # error = -1
    # try:
    #     error = func_telethon ()
    # except Exception as e:
    #     print (f'Ошибка: {e}')
    # # endtry
    # if error > 0:
    #     # print(f'{error=}')
    #     LULog.LoggerAdd (LULog.LoggerAPPS, logging.ERROR, f'{error=}')

    # error = -1
    # try:
    #     error = func_pyrogram ()
    # except Exception as e:
    #     channel = None
    #     print (f'Ошибка: {e}')
    # # endtry
    # if error > 0:
    #     # print(f'{error=}')
    #     LULog.LoggerAdd (LULog.LoggerAPPS, logging.ERROR, f'{error=}')

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
