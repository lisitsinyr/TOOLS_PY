from telethon import TelegramClient

# Ваши данные для авторизации
api_id = 1234567  # замените на ваш api_id
api_hash = 'ваш_api_hash'  # замените на ваш api_hash
client = TelegramClient('session_name', api_id, api_hash)

async def download_photos_from_message(chat_entity, message_id):
    # Получаем сообщение по ID
    message = await client.get_messages(chat_entity, ids=message_id)

    if message and message.media and hasattr(message.media, 'photo'):
        print("Сообщение содержит фото. Скачиваем...")
        # Если это список медиафайлов (например, альбом)
        if hasattr(message, 'grouped_id') and message.grouped_id:
            # Получаем всю группу медиа
            messages = await client.get_messages(chat_entity, min_id=message_id - 1, max_id=message_id + 1)
            for msg in messages:
                if msg.media and hasattr(msg.media, 'photo'):
                    await msg.download_media(file=f'photo_{msg.id}.jpg')
                    print(f"Фото {msg.id} скачано")
        else:
            # Это одиночное фото
            await message.download_media(file=f'photo_{message.id}.jpg')
            print(f"Фото {message.id} скачано")
    else:
        print("Сообщение не содержит фото.")

async def main():
    # Можно использовать username, id или ссылку
    chat_entity = 'username_or_id'  # например, 'testchannel123'
    message_id = 12345              # ID сообщения, которое содержит фото

    await download_photos_from_message(chat_entity, message_id)

with client:
    client.loop.run_until_complete(main())
