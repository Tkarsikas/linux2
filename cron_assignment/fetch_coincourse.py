#!/home/ubuntu/lemp-app/venv/bin/python3
import requests
import mysql.connector
import secrets
from datetime import datetime
COIN = 'Ethereum'
URL = f'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=eur'
conn = mysql.connector.connect(host=secrets.host, user=secrets.user,
password=secrets.password, database=secrets.database)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS ethereum_data (id INT AUTO_INCREMENT PRIMARY KEY, coin VARCHAR(50), price FLOAT, timestamp DATETIME)''')
response = requests.get(URL)
data = response.json()
eth_price = data["ethereum"]["eur"]
timestamp = datetime.now()
cursor.execute('INSERT INTO ethereum_data (coin, price, timestamp) VALUES (%s, %s, %s)', (COIN, eth_price, timestamp))
conn.commit()
cursor.close()
conn.close()
print(f'Data tallennettu: {COIN} {eth_price}€')
