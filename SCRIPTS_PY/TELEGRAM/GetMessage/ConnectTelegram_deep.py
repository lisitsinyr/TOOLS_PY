"""ConnectTelegram_deep.py"""
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
import os

#------------------------------------------
#
#------------------------------------------
from decouple import config
import asyncio

#------------------------------------------
# БИБЛИОТЕКА telethon
#------------------------------------------
from telethon import TelegramClient
from telethon import connection
import TelethonFakeTLS
import telethon.sync
import telethon.tl.types

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

# Данные из my.telegram.org
API_ID = Gapi_id  # Ваш API ID
API_HASH = Gapi_hash

# Gclient:telethon.sync.TelegramClient = None

#------------------------------------------
#
#------------------------------------------
def telegram_net ():
    """telegram_net"""
#beginfunction
    global Gclient
    SESSION_NAME = 'lyr60_TELEGRAM'
    Gclient = TelegramClient (
        SESSION_NAME, API_ID, API_HASH
    )
    Gclient.start (phone=Gphone, password=Gpassword)
    # # client.connect ()
    print (f'user_authorized={Gclient.is_user_authorized()}')
    me = Gclient.get_me ()
    print (f"Успешный вход! Ваш ID: {me.id}, Имя: {me.first_name}")

    return Gclient
#endfunction

#------------------------------------------
#
#------------------------------------------
def telegram_proxy ():
    """telegram_net"""
#beginfunction
    global Gclient
    # Параметры MTProto прокси
    # PROXY_IP = 'alo.acharbashi.info'
    # PROXY_PORT = 4515
    # PROXY_SECRET = 'eee9a4f23b1d768c04a8d7f39120ca5b6e626973636f7474692e79656b74616e65742e636f6d'

    # PROXY_IP = 'mtc4ljewnc4ymtmumjuz.he-de-24.mtproto.ru'
    # PROXY_PORT = 443
    # PROXY_SECRET = 'ee2111222233334444555566667777888865756331332e706c61796c6973742e7474766e772e6e6574'
    GPROXY_IP = config ('PROXY_IP')
    GPROXY_PORT = config ('PROXY_PORT')
    GPROXY_SECRET = config ('PROXY_SECRET')
    print (GPROXY_IP, GPROXY_PORT, GPROXY_SECRET)

    SESSION_NAME = 'lyr60_TELEGRAM_deepseek'
    _proxy = (GPROXY_IP, GPROXY_PORT, GPROXY_SECRET)
    _proxy = ('dedicated.love-internet.xyz', 4515, 'eee9a4f23b1d768c04a8d7f39120ca5b6e626973636f7474692e79656b74616e65742e636f6d')
    # proxy = ('alo.acharbashi.info', 4515, 'eee9a4f23b1d768c04a8d7f39120ca5b6e626973636f7474692e79656b74616e65742e636f6d')
    _connection = TelethonFakeTLS.ConnectionTcpMTProxyFakeTLS

    # -------------------------------------------------------------
    # Создаем клиента с поддержкой MTProto прокси
    #  2
    # 'my_session' — это имя файла сессии, в нем сохранятся данные входа
    # -------------------------------------------------------------
    # client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

    # Указываем прокси и специальный тип соединения для MTProxy
    Gclient = TelegramClient (
        SESSION_NAME, API_ID, API_HASH,
        # proxy=(GPROXY_IP, GPROXY_PORT, GPROXY_SECRET),
        # connection=connection.ConnectionTcpMTProxyRandomizedIntermediate
        connection=_connection,
        proxy=_proxy
    )

    # # Вариант 1: Abridged
    # client = TelegramClient(
    #     session_name, api_id, api_hash,
    #     proxy=(proxy_ip, proxy_port, secret),
    #     connection=connection.ConnectionTcpMTProxyAbridged
    # )
    #
    # # Вариант 2: Intermediate
    # client = TelegramClient(
    #     session_name, api_id, api_hash,
    #     proxy=(proxy_ip, proxy_port, secret),
    #     connection=connection.ConnectionTcpMTProxyIntermediate
    # )
    #
    # # Вариант 3: Randomized (если секрет с dd)
    # client = TelegramClient(
    #     session_name, api_id, api_hash,
    #     proxy=(proxy_ip, proxy_port, secret),
    #     connection=connection.ConnectionTcpMTProxyRandomizedIntermediate
    # )

    return Gclient

#endfunction

# -------------------------------------------------------------
#  1
# -------------------------------------------------------------
# Создаем клиента с поддержкой MTProto прокси
# client = TelegramClient(
#     SESSION_NAME,
#     API_ID,
#     API_HASH,
#     proxy=(PROXY_IP, PROXY_PORT, PROXY_SECRET),
#     connection=connection.ConnectionTcpMTProxyRandomizedIntermediate
# )
# async def main():
#     # await client.start(phone=phone, password=password)
#     await client.start()
#     print("✅ Подключено к Telegram через MTProto прокси!")
#     me = await client.get_me()
#     print(f"Аккаунт: {me.first_name}")

# Gclient = telegram_proxy ()
async def main ():
    print('main()')
    # Метод start() сам запустит процесс авторизации:
    # 1. Попросит номер телефона
    # 2. Попросит код из SMS или Telegram
    # 3. Попросит 2FA-пароль, если он включен

    await Gclient.start ()
    print("Успешное подключение через MTProxy!")

    # Проверяем, что мы вошли
    me = await Gclient.get_me ()
    print (f"Успешный вход! Ваш ID: {me.id}, Имя: {me.first_name}")

#------------------------------------------
#
#------------------------------------------
#beginmodule
if __name__ == "__main__":

    telegram_net()

    # Gclient = telegram_proxy ()

    # -------------------------------------------------------------
    #  1
    # -------------------------------------------------------------
    # with Gclient:
    #     Gclient.loop.run_until_complete (main ())

    # -------------------------------------------------------------
    #  2
    # -------------------------------------------------------------
    # asyncio.run (main ())

#endif

#endmodule







