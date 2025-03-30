"""ReadGmail.py"""
# -*- coding: UTF-8 -*-
__annotations__ = """
 =======================================================
 Copyright (c) 2025
 Author:
     Lisitsin Y.R.
 Project:
     SCRIPTS_PY
 Module:
     ReadGmail.py
 =======================================================
"""

#------------------------------------------
# БИБЛИОТЕКИ python
#------------------------------------------
import os

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------
import imaplib
import email
from dotenv import load_dotenv

#------------------------------------------
# БИБЛИОТЕКА lyrpy
#------------------------------------------

#------------------------------------------
def main ():
    """main"""
#beginfunction
    load_dotenv ()

    # Учетные данные
    # EMAIL = 'your_email@gmail.com'
    # PASSWORD = 'your_password'
    EMAIL = os.getenv("EMAIL")
    PASSWORD = os.getenv("PASSWORD")

    print(EMAIL) #AQAAAAAz55vbAAdBSHeydEoSe0fclxSSABT
    print(PASSWORD) #ramziv.com

    # Подключение к серверу Gmail через IMAP
    mail = imaplib.IMAP4_SSL('imap.gmail.com')

    # Вход в аккаунт
    mail.login(EMAIL, PASSWORD)

    # Выбор папки (например, INBOX)
    mail.select('inbox')

    # Поиск всех писем в выбранной папке
    result, data = mail.search(None, 'ALL')

    if result != 'OK':
        print("Ошибка при поиске писем.")
        exit()

    # Получение списка номеров писем
    email_ids = data[0].split()

    # Проход по каждому письму
    for email_id in email_ids:
        # Получение содержимого письма
        result, msg_data = mail.fetch(email_id, '(RFC822)')

        if result != 'OK':
            print(f"Ошибка при получении письма {email_id}.")
            continue

        # Парсинг письма
        msg = email.message_from_bytes(msg_data[0][1])

        # Получение информации о письме
        subject = email.header.decode_header(msg['Subject'])[0][0]
        from_ = email.utils.parseaddr(msg['From'])

        print(f'От: {from_}')
        print(f'Тема: {subject}')

        # Проверка на наличие текстового содержимого
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                if "attachment" not in content_disposition and content_type == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    print(f'Содержание: {body[:100]}...')  # вывод первых 100 символов
                    break
        else:
            body = msg.get_payload(decode=True).decode()
            print(f'Содержание: {body[:100]}...')  # вывод первых 100 символов

    # Закрытие соединения
    mail.logout()
#endfunction

#------------------------------------------
#
#------------------------------------------
#beginmodule
if __name__ == "__main__":
    main ()
#endif

#endmodule





























