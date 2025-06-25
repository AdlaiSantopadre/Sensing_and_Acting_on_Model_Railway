#gestione QoS di ricezione
import paho.mqtt.client as mqtt
import json
import logging
from config import BROKER, PORT, USERNAME, PASSWORD, CLIENT_IDS, TOPIC_ACK_IN, TOPIC_ACK_OUT, EVENT_MAP
from client_acting_and_logic.event_stack import enqueue_event # verrÃ  usato per FSM

# Configura logging
logging.basicConfig(level=logging.INFO, format='[ACK_HANDLER] %(message)s')
log = logging.getLogger("ACK_HANDLER")

# Stato per ogni client_id
sensor_state = {client_id: {"last": 1, "waiting_ack": False, "buffered": False} for client_id in CLIENT_IDS}

def on_connect(client, userdata, flags, rc):
    log.info(f"Connesso al broker ({rc})")
    for topic in TOPIC_ACK_IN.values():
        client.subscribe(topic)
        log.info(f"Subscribed to: {topic}")

def on_disconnect(client, userdata, rc):
    log.warning(f"Disconnesso dal broker. rc={rc}")

def on_message(client, userdata, msg):
    log.info(f"Ricevuto: {msg.topic}: {msg.payload.decode()}")
    try:
        data = json.loads(msg.payload.decode())
        client_id = data.get("id")
        stato = data.get("stato")

        if client_id not in CLIENT_IDS:
            log.warning(f"ID non riconosciuto: {client_id}")
            return
        stato_prec = sensor_state[client_id]["last"]

        if stato == 0 and stato_prec == 1:
            # Fronte 1â0 (binario occupato): invio ack e genero evento logico
            sensor_state[client_id]["waiting_ack"] = True
            sensor_state[client_id]["last"] = 0

            # Invio ack MQTT
            client.publish(TOPIC_ACK_OUT[client_id], json.dumps({"ok": True}), qos=1)
            log.info(f"TX ack su: {TOPIC_ACK_OUT[client_id]}")
            # Generazione evento logico (attraversamento)
            event = EVENT_MAP[client_id]
            enqueue_event(event)
            log.info(f"Innescato evento logico: {event}")
        
        elif stato == 1 and stato_prec == 0:
            # Fronte 0â1, reset solo stato interno, nessun evento logico
            sensor_state[client_id]["waiting_ack"] = False
            sensor_state[client_id]["last"] = 1


    except Exception as e:
        log.error(f"Errore: {e}")



def start_ack_handler():
    try:
        log.info("Avvio handler MQTT ACK")
        client = mqtt.Client(client_id="ack_client_handler")
        client.username_pw_set(USERNAME, PASSWORD)
        client.on_connect = on_connect
        client.on_message = on_message
        client.on_disconnect = on_disconnect

        log.info(f"Connessione a {BROKER}:{PORT} come {USERNAME}")
        client.connect(BROKER, PORT, 60)

        log.info("Inizio loop forever")
        client.loop_forever()
    except Exception as e:
        log.critical(f"Errore fatale: {e}")
