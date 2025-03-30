import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Учетные данные
# EMAIL = 'your_email@gmail.com'
# PASSWORD = 'your_password'
EMAIL = 'lisitsinyr@gmail.com'
PASSWORD = '****************'

# Создание сообщения
msg = MIMEMultipart()
msg['From'] = EMAIL
msg['To'] = TO_EMAIL
msg['Subject'] = 'Тестовое письмо'

# Текст письма
body = "Это тестовое письмо."
msg.attach(MIMEText(body, 'plain'))

# Подключение к серверу Gmail через SMTP
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()

# Вход в аккаунт
server.login(EMAIL, PASSWORD)

# Отправка письма
text = msg.as_string()
server.sendmail(EMAIL, TO_EMAIL, text)

# Закрытие соединения
server.quit()
