import telethon.sync
import TelethonFakeTLS

api_id = 29878842
api_hash = '2407467cce70aa3ebf856ca6e95e7e0c'

PHONE=+79063947656
LOGIN='lyr60'
password='DorodeseSaha73!'
API_TOKEN='7554938813:AAHZ2b6Kyaz9TCBj1KU6KVu5Wa8D_Bg6cAs'

session = 'lyr60_TELEGRAM'

proxy_ip = 'dedicated.love-internet.xyz'
proxy_port = 4515
# Удалите 'ee' из начала секрета
secret = 'e9a4f23b1d768c04a8d7f39120ca5b6e626973636f7474692e79656b74616e65742e636f6d'  # ee удалён

proxy = (proxy_ip, proxy_port, secret)
connection = TelethonFakeTLS.ConnectionTcpMTProxyFakeTLS

client = telethon.TelegramClient(
    session=session,
    api_id=api_id, 
    api_hash=api_hash,
    connection=connection,
    proxy=proxy
)