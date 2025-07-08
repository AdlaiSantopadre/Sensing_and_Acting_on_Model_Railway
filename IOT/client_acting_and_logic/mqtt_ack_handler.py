#gestione QoS di ricezione
import paho.mqtt.client as mqtt
import json
from config import BROKER, PORT, USERNAME, PASSWORD, CLIENT_IDS, TOPIC_ACK_IN, TOPIC_ACK_OUT, EVENT_MAP
from client_acting_and_logic.event_stack import enqueue_event # verra'  usato per FSM
from paho.mqtt.client import CallbackAPIVersion



# Stato per ogni client_id
sensor_state = {client_id: {"last": 1, "waiting_ack": False, "buffered": False} for client_id in CLIENT_IDS}

def on_connect(client, userdata, flags, rc):
    print(f"[ACK_HANDLER] Connesso al broker ({rc})")
    for topic in TOPIC_ACK_IN.values():
        client.subscribe(topic)
        print(f"[ACK_HANDLER] Subscribed to: {topic}")

def on_disconnect(client, userdata, rc):
    print(f"[ACK_HANDLER] Disconnesso dal broker. rc={rc}")

def on_message(client, userdata, msg):
    print(f"[ACK_HANDLER] Ricevuto: {msg.topic}: {msg.payload.decode()}")
    try:
        data = json.loads(msg.payload.decode())
        client_id = data.get("id")
        stato = data.get("stato")

        if client_id not in CLIENT_IDS:
            print(f"[ACK_HANDLER] ID non riconosciuto: {client_id}")
            return
        stato_prec = sensor_state[client_id]["last"]

        if stato == 0 and stato_prec == 1:
            # Fronte 1-0 (binario occupato): invio ack e genero evento logico
            sensor_state[client_id]["waiting_ack"] = True
            sensor_state[client_id]["last"] = 0

            # Invio ack MQTT
            client.publish(TOPIC_ACK_OUT[client_id], json.dumps({"ok": True}), qos=1)
            print(f"[ACK_HANDLER] TX ack su: {TOPIC_ACK_OUT[client_id]}")
        
            # Generazione evento logico (attraversamento)
            event = EVENT_MAP[client_id]
            enqueue_event(event)
            print(f"[ACK_HANDLER] Innescato evento logico: {event}")
        
        elif stato == 1 and stato_prec == 0:
            # Fronte 0-1, reset solo stato interno, nessun evento logico
            sensor_state[client_id]["waiting_ack"] = False
            sensor_state[client_id]["last"] = 1


    except Exception as e:
        print(f"[ACK_HANDLER] Errore: {e}")



def start_ack_handler():
    try:
        print("[ACK_HANDLER] Avvio handler MQTT ACK")
        client = mqtt.Client(client_id="ack_client", callback_api_version=CallbackAPIVersion.VERSION1)
        client.username_pw_set(USERNAME, PASSWORD)
        client.on_connect = on_connect
        client.on_message = on_message
        client.on_disconnect = on_disconnect

        print(f"[ACK_HANDLER] Connessione a {BROKER}:{PORT} come {USERNAME}")
        client.connect(BROKER, PORT, 60)

        print("[ACK_HANDLER] Inizio loop forever")
        client.loop_forever()
    except Exception as e:
        print(f"[ACK_HANDLER] Errore fatale: {e}")
