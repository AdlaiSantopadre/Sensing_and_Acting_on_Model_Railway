#gestione QoS di ricezione
import paho.mqtt.client as mqtt
import json
import logging
from config import BROKER, PORT, TOPIC_ACK_IN, TOPIC_ACK_OUT, USERNAME, PASSWORD
from event_stack import enqueue_event  # verrà usato per FSM

# Configura logging
logging.basicConfig(level=logging.INFO, format='[ACK_HANDLER] %(message)s')
log = logging.getLogger("ACK_HANDLER")

def on_connect(client, userdata, flags, rc):
    log.info(f"Connesso al broker ({rc})")
    client.subscribe(TOPIC_ACK_IN)

def on_disconnect(client, userdata, rc):
    log.warning(f"Disconnesso dal broker. rc={rc}")

def on_message(client, userdata, msg):
    log.info(f"Ricevuto: {msg.topic}: {msg.payload.decode()}")
    try:
        data = json.loads(msg.payload.decode())
        if "id" in data and "stato" in data:
            enqueue_event(data)  # salva per FSM

            # QoS semantico: invia ack su occupato
            if data["stato"] == 0:
                ack_payload = json.dumps({"ok": True})
                client.publish(TOPIC_ACK_OUT, ack_payload, qos=1)
                log.info(f"TX ack ? {TOPIC_ACK_OUT}")
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

