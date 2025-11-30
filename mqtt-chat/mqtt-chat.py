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
FETCH_INTERVAL = 2  # sekunteina

# --- Käyttäjä ---
nickname = input("Anna nimimerkkisi: ").strip() or "Tuntematon"

# --- MQTT client setup ---
client = mqtt.Client(client_id=f"chat_{nickname}")
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

# --- Taustalanka REST API:sta haettaville viesteille ---
displayed_ids = set()

def fetch_loop():
    global displayed_ids
    while True:
        try:
            resp = requests.get(API_URL)
            resp.raise_for_status()
            messages = resp.json()
            for msg in messages:
                if msg["id"] not in displayed_ids:
                    print(f"{msg['nickname']}: {msg['message']}")
                    displayed_ids.add(msg["id"])
        except Exception as e:
            print(f"[Virhe haettaessa viestejä]: {e}")
        time.sleep(FETCH_INTERVAL)

thread = threading.Thread(target=fetch_loop, daemon=True)
thread.start()

# --- Pääloop viestien lähettämiseen MQTT:n kautta ---
print("Kirjoita viesti ja paina Enter lähetääksesi. Lopeta Ctrl+C.")

try:
    while True:
        msg = input()
        if msg.strip():
            payload = json.dumps({
                "nickname": nickname,
                "text": msg.strip(),
                "clientId": "python_chat"
            })
            client.publish(MQTT_TOPIC, payload)
except KeyboardInterrupt:
    print("\n[Lopetetaan chat...]")
    client.loop_stop()
    client.disconnect()
