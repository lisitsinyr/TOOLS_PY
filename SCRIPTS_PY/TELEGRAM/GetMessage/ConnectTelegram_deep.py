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
SESSION_NAME = 'lyr60_TELEGRAM_deepseek'

# Параметры MTProto прокси
# PROXY_IP = 'mtc4ljewnc4ymtmumjuz.he-de-24.mtproto.ru'
# PROXY_PORT = 443
# PROXY_SECRET = 'ee2111222233334444555566667777888865756331332e706c61796c6973742e7474766e772e6e6574'

# Параметры MTProto прокси
PROXY_IP = 'alo.acharbashi.info'
PROXY_PORT = 4515
PROXY_SECRET = 'eee9a4f23b1d768c04a8d7f39120ca5b6e626973636f7474692e79656b74616e65742e636f6d'

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

# -------------------------------------------------------------
#  2
# 'my_session' — это имя файла сессии, в нем сохранятся данные входа
# -------------------------------------------------------------
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
async def main ():
    # Метод start() сам запустит процесс авторизации:
    # 1. Попросит номер телефона
    # 2. Попросит код из SMS или Telegram
    # 3. Попросит 2FA-пароль, если он включен
    await client.start ()

    # Проверяем, что мы вошли
    me = await client.get_me ()
    print (f"Успешный вход! Ваш ID: {me.id}, Имя: {me.first_name}")

#------------------------------------------
#
#------------------------------------------
#beginmodule
if __name__ == "__main__":
    # Запуск

    # -------------------------------------------------------------
    #  1
    # -------------------------------------------------------------
    # with client:
    #     client.loop.run_until_complete(main())

    # -------------------------------------------------------------
    #  2
    # -------------------------------------------------------------
    asyncio.run (main ())

#endif

#endmodule







