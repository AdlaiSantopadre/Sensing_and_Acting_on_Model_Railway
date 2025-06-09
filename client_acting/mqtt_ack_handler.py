#gestione QoS di ricezione
import paho.mqtt.client as mqtt
import json
from config import BROKER, PORT, TOPIC_ACK_IN, TOPIC_ACK_OUT,USERNAME, PASSWORD
from event_stack import enqueue_event  # verrà usato per FSM

def on_connect(client, userdata, flags, rc):
    print(f"[ACK_HANDLER] Connesso al broker ({rc})")
    client.subscribe(TOPIC_ACK_IN)

def on_message(client, userdata, msg):
    print(f"[ACK_HANDLER] Ricevuto: {msg.topic}: {msg.payload.decode()}")
    try:
        data = json.loads(msg.payload.decode())
        if "id" in data and "stato" in data:
            enqueue_event(data)  # salva per FSM

            # QoS semantico: invia ack su occupato
            if data["stato"] == 0:
                client.publish(TOPIC_ACK_OUT, json.dumps({"ok": True}), qos=1)
                print(f"[ACK_HANDLER] TX ack → {TOPIC_ACK_OUT}")
    except Exception as e:
        print(f"[ACK_HANDLER] Errore: {e}")

def start_ack_handler():
    client = mqtt.Client()
    client.username_pw_set(USERNAME, PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT, 60)
    client.loop_forever()
