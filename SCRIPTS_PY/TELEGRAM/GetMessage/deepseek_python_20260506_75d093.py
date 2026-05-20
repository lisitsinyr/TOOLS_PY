from telethon import TelegramClient, connection

api_id = 29878842  # Ваш API ID с my.telegram.org
api_hash = '2407467cce70aa3ebf856ca6e95e7e0c'
session_name = 'lyr60_TELEGRAM'

# Данные MTProxy
# proxy_ip = 'mtc4ljewnc4yntiuodk.he-de-01.mtproto.icu'
# proxy_port = 443
# secret = '21112222333344445555666677778888636c6f756463646e2d6672612d30312e63646e2e79616e6465782e6e6574'  # ee удалён

proxy_ip = 'alo.acharbashi.info'
proxy_port = 4515
# ee удалён
secret = 'e9a4f23b1d768c04a8d7f39120ca5b6e626973636f7474692e79656b74616e65742e636f6d'

_connection1 = connection.ConnectionTcpMTProxyRandomizedIntermediate
_connection2 = connection.ConnectionTcpMTProxyAbridged
_connection3 = connection.ConnectionTcpMTProxyIntermediate

# Указываем прокси и специальный тип соединения для MTProxy
client = TelegramClient(
    session_name,
    api_id,
    api_hash,
    proxy=(proxy_ip, proxy_port, secret),
    connection=_connection1
)

async def main():
    await client.start()
    print("Успешное подключение через MTProxy!")
    me = await client.get_me()
    print(f"Авторизован как: {me.first_name}")

with client:
    client.loop.run_until_complete(main())