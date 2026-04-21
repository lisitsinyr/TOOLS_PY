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
# БИБЛИОТЕКА telethon
#------------------------------------------
from telethon import TelegramClient
from telethon import connection

# Данные из my.telegram.org
API_ID = 29878842  # Ваш API ID
API_HASH = '2407467cce70aa3ebf856ca6e95e7e0c'
SESSION_NAME = 'lyr60_TELEGRAM_deep'

# Параметры MTProto прокси
PROXY_IP = 'he.de.ndkumtiumtmunja.mtproto.ru'
PROXY_PORT = 443
PROXY_SECRET = 'ee2111222233334444555566667777888865756331312e706c61796c6973742e7474766e772e6e6574'  # Например: 'ee1234567890abcdef'

# Создаем клиента с поддержкой MTProto прокси
client = TelegramClient(
    SESSION_NAME,
    API_ID,
    API_HASH,
    proxy=(PROXY_IP, PROXY_PORT, PROXY_SECRET),
    connection=connection.ConnectionTcpMTProxyRandomizedIntermediate
)


async def main():
    # await client.start(phone=phone, password=password)
    await client.start()
    print("✅ Подключено к Telegram через MTProto прокси!")
    me = await client.get_me()
    print(f"Аккаунт: {me.first_name}")

#------------------------------------------
#
#------------------------------------------
#beginmodule
if __name__ == "__main__":
    # Запуск
    with client:
        client.loop.run_until_complete(main())
#endif

#endmodule







