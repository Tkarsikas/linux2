#!/usr/bin/env python3

import json
import time
import threading
import requests
import paho.mqtt.client as mqtt

# --- Konfiguraatio ---
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "chat/messages"
API_URL = "http://127.0.0.1:5001/api/messages?limit=50"
FETCH_INTERVAL = 3  # sekunteina

# --- Käyttäjä ---
nickname = input("Anna nimimerkkisi: ").strip() or "Tuntematon"

# --- Funktio viestien hakemiseen REST API:sta ---
def fetch_messages():
    try:
        resp = requests.get(API_URL)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"[Virhe haettaessa viestejä] {e}")
        return []

# --- Funktio viestien tulostukseen ---
displayed_ids = set()
def display_messages():
    global displayed_ids
    messages = fetch_messages()
    for msg in messages:
        if msg["id"] not in displayed_ids:
            print(f"{msg['nickname']}: {msg['message']}")
            displayed_ids.add(msg["id"])

# --- MQTT client setup ---
client = mqtt.Client(client_id="python_chat")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("[Yhdistetty MQTT-brokeriin]")
    else:
        print(f"[MQTT-yhteysvirhe, koodi: {rc}]")

client.on_connect = on_connect
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()  # pyörittää MQTT loopia rinnalla

# --- Taustalanka viestien hakemiseen ja näyttämiseen ---
def fetch_loop():
    while True:
        display_messages()
        time.sleep(FETCH_INTERVAL)

thread = threading.Thread(target=fetch_loop, daemon=True)
thread.start()

# --- Pääloop viestien lähettämiseen ---
print("Kirjoita viesti ja paina Enter lähetääksesi. Lopeta Ctrl+C.")
try:
    while True:
        msg = input()
        if msg.strip():
            payload = json.dumps({"nickname": nickname, "text": msg.strip(), "clientId": "python_client"})
            client.publish(MQTT_TOPIC, payload)
except KeyboardInterrupt:
    print("\n[Lopetetaan chat...]")
    client.loop_stop()
    client.disconnect()
    print("[Yhteys suljettu]")