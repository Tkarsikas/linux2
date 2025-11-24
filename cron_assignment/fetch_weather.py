#!/usr/bin/env python3
import requests
import mysql.connector, secrets
from datetime import datetime
API_KEY = secrets.API_KEY
CITY = 'Helsinki'
URL = f'https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric'
conn = mysql.connector.connect(host=secrets.host, user=secrets.user,
password=secrets.password, database=secrets.database)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS weather_data (id INT AUTO_INCREMENT PRIMARY KEY, city VARCHAR(50), temperature FLOAT, description VARCHAR(100), timestamp DATETIME)''')
response = requests.get(URL)
data = response.json()
temp = data['main']['temp']
desc = data['weather'][0]['description']
timestamp = datetime.now()
cursor.execute('INSERT INTO weather_data (city, temperature, description,timestamp) VALUES (%s, %s, %s, %s)', (CITY, temp, desc, timestamp))
conn.commit()
cursor.close()
conn.close()
print(f'Data tallennettu: {CITY} {temp}°C {desc}')
