#!/bin/bash
# Polku virtuaaliympäristöön
VENV_DIR="venv"
# Luo virtuaaliympäristö, jos ei ole olemassa
if [ ! -d "$VENV_DIR" ]; then
 echo "Luodaan virtuaaliympäristö..."
 python3 -m venv $VENV_DIR
fi
# Aktivoi virtuaaliympäristö
source $VENV_DIR/bin/activate
# Asenna riippuvuudet requirements.txt-tiedostosta
if [ -f "requirements.txt" ]; then
 echo "Asennetaan riippuvuudet..."
 pip install --upgrade pip
 pip install -r requirements.txt
else
 echo "requirements.txt ei löytynyt!"
fi
# Suorita fetch_weather.py
if [ -f "fetch_coincourse.py" ]; then
 echo "Suoritetaan coincourse.py..."
 python fetch_coincourse.py
else
 echo "fetch_coincourse.py ei löytynyt!"
fi
echo "Valmis!"