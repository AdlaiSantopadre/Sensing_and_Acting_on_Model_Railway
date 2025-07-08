#gestione QoS di ricezione
import paho.mqtt.client as mqtt
import json
import logging
from config import BROKER, PORT, USERNAME, PASSWORD, CLIENT_IDS, TOPIC_ACK_IN, TOPIC_ACK_OUT, EVENT_MAP
from client_acting_and_logic.event_stack import enqueue_event  # verrà usato per FSM

# Configura logging
logging.basicConfig(level=logging.INFO, format='[ACK_HANDLER] %(message)s')
log = logging.getLogger("ACK_HANDLER")

# Stato per ogni client_id
sensor_state = {
    client_id: {
        "last": 1,
        "waiting_ack": False,
        "ready_for_event": False
    } for client_id in CLIENT_IDS
}

def on_connect(client, userdata, flags, rc):
    log.info(f"Connesso al broker ({rc})")
    for topic in TOPIC_ACK_IN.values():
        client.subscribe(topic)
        log.info(f"Subscribed to: {topic}")

def on_disconnect(client, userdata, rc):
    log.warning(f"Disconnesso dal broker. rc={rc}")

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
        waiting_ack = sensor_state[client_id]["waiting_ack"]
        ready_for_event = sensor_state[client_id]["ready_for_event"]

        if stato == 0 and stato_prec == 1 and not waiting_ack:
            # Primo fronte 1→0 → invio ack
            sensor_state[client_id]["waiting_ack"] = True
            sensor_state[client_id]["last"] = 0
            print(f"[ACK_HANDLER] TX ack su: {TOPIC_ACK_OUT[client_id]}")
            client.publish(TOPIC_ACK_OUT[client_id], json.dumps({"ok": True}), qos=1)

        elif stato == 1 and stato_prec == 0 and waiting_ack:
            # Primo fronte 0→1 → genera evento
            sensor_state[client_id]["waiting_ack"] = False
            sensor_state[client_id]["last"] = 1
            event = EVENT_MAP[client_id]
            enqueue_event(event)
            print(f"[STACK] Evento enqueued: {{'timestamp': 'AUTO', 'event': '{event}'}}")
            print(f"[ACK_HANDLER] Innescato evento logico: {event}")

        elif stato == 0 and stato_prec == 0:
            # Rimbalzo multiplo su 0 ignorato
            print(f"[ACK_HANDLER] Stato 0 duplicato ignorato per {client_id}")

        elif stato == 1 and stato_prec == 1:
            # Rimbalzo multiplo su 1 ignorato
            print(f"[ACK_HANDLER] Stato 1 duplicato ignorato per {client_id}")

        else:
            # Aggiorna solo stato interno
            sensor_state[client_id]["last"] = stato

    except Exception as e:
        print(f"[ACK_HANDLER] Errore: {e}")

def start_ack_handler():
    try:
        print("[ACK_HANDLER] Avvio handler MQTT ACK")
        client = mqtt.Client(client_id="ack_client_handler")
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
