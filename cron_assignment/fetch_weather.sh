#!/bin/bash
# Polku virtuaaliympäristöön
VENV_DIR="venv"
# Luo virtuaaliympäristö, jos ei ole olemassa
#if [ ! -d "$VENV_DIR" ]; then
 #echo "Luodaan virtuaaliympäristö..."
 #python3 -m venv $VENV_DIR
# Aktivoi virtuaaliympäristö

 cd /home/ubuntu/lemp-app/
 source $VENV_DIR/bin/activate
 cd ~
# Asenna riippuvuudet requirements.txt-tiedostosta
if [ -f "requirements.txt" ]; then
 echo "Asennetaan riippuvuudet..."
 cd /home/ubuntu/cron_assignment/
 pip install --upgrade pip
 pip install -r requirements.txt
else
 echo "requirements.txt ei löytynyt!"
fi
# Suorita fetch_weather.py
if [ -f "fetch_weather.py" ]; then
 echo "Suoritetaan fetch_weather.py..."
 python fetch_weather.py
else
 echo "fetch_weather.py ei löytynyt!"
fi
echo "Valmis!"