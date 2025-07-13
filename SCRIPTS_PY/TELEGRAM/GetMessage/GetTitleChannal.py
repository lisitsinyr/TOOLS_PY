from telethon.sync import TelegramClient
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
import re
import asyncio

# Замените на свои данные
api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'
phone = 'YOUR_PHONE_NUMBER'

# profile
# Qwen3-235B-A22B
# Если ты хочешь получить название канала Telegram по ссылке на сообщение с помощью Python, это можно сделать с использованием библиотеки Telethon (асинхронная библиотека для работы с Telegram API).

# 🔗 Пример ссылки:
# Telegram-сообщение может выглядеть так:
# https://t.me/channelname/1234
# или
# https://t.me/c/123456789/1234


# Функция для парсинга ссылки
def parse_message_link (link):
    pattern = r'https?://t\.me/([a-zA-Z0-9\_]+|c/(\d+))/(\d+)'
    match = re.match (pattern, link)
    if not match:
        raise ValueError ("Invalid link")

    if match.group (1).startswith ('c/'):
        channel_id = int (match.group (2))
        msg_id = int (match.group (3))
        return {'channel_id': channel_id, 'msg_id': msg_id}
    else:
        username = match.group (1)
        msg_id = int (match.group (3))
        return {'username': username, 'msg_id': msg_id}


async def get_channel_name (link):
    async with TelegramClient ('session_name', api_id, api_hash) as client:
        await client.start (phone)

        parsed = parse_message_link (link)

        if 'username' in parsed:
            entity = await client.get_entity (parsed ['username'])
        elif 'channel_id' in parsed:
            entity = await client.get_entity (PeerChannel (parsed ['channel_id']))
        else:
            raise ValueError ("Could not resolve entity")

        print (f"Название канала: {entity.title}")
        return entity.title


# Пример использования:
if __name__ == '__main__':
    message_link = 'https://t.me/examplechannel/123 '
    asyncio.run (get_channel_name (message_link))
