import streamlit as st
import json
import requests
import paho.mqtt.publish as publish
from streamlit_autorefresh import st_autorefresh

# --- Konfiguraatio ---
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "chat/messages"
API_URL = "http://127.0.0.1:5001/api/messages?limit=100"

# --- Streamlit-sivun asetukset ---
st.set_page_config(page_title="MQTT Chat", layout="wide")
st.title("MQTT Chat")

# --- Autorefresh (3s välein) ---
st_autorefresh(interval=3000, key="refresh")

# --- Hae viestit REST API:sta ---
def fetch_messages():
    try:
        resp = requests.get(API_URL)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.error(f"Virhe haettaessa viestejä: {e}")
        return []

messages = fetch_messages()

# --- Näytä chat-viestit ---
st.subheader("Chat-historia")
chat_container = st.empty()

if messages:
    for msg in reversed(messages):  # Näytä vanhimmat ensin
        chat_container.markdown(f"**{msg['nickname']}**: {msg['message']}")
else:
    chat_container.info("Ei viestejä näytettäväksi.")

# --- Lähetä uusi viesti ---
st.subheader("Lähetä viesti")
nickname = st.text_input("Nimimerkki", key="nickname_input")
message = st.text_input("Viesti", key="message_input")
send_button = st.button("Lähetä")

if send_button:
    if not nickname.strip() or not message.strip():
        st.warning("Täytä sekä nimimerkki että viesti!")
    else:
        payload = json.dumps({
            "nickname": nickname.strip(),
            "text": message.strip(),
            "clientId": "web"
        })
        try:
            publish.single(MQTT_TOPIC, payload, hostname=MQTT_BROKER, port=MQTT_PORT)
            st.success("Viesti lähetetty!")
        except Exception as e:
            st.error(f"Virhe viestiä lähetettäessä: {e}")
