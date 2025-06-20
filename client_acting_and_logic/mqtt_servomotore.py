# def start_acting_client():
#	print("Da implementare")
	
import time
import paho.mqtt.client as mqtt
from adafruit_servokit import ServoKit
from logutil import logInfo, logError

# Configurazioni servo e MQTT
CLIENT_ID = "deviatoio01"
MQTT_TOPIC_CMD = "deviatoio/01"
MQTT_TOPIC_ACK = "ack/deviatoio/01"

ANGLE_DEVIAZIONE = 105
ANGLE_RIPRISTINO = 75
SERVO_CHANNEL = 0

# Inizializzazione servomotore
try:
    kit = ServoKit(channels=16)
    kit.servo[SERVO_CHANNEL].angle = ANGLE_RIPRISTINO
    logInfo(CLIENT_ID, f"Servo inizializzato su canale {SERVO_CHANNEL} con angolo {ANGLE_RIPRISTINO}")
except Exception as e:
    logError(CLIENT_ID, f"Errore inizializzazione servomotore: {e}")
    kit = None

# Callback alla ricezione di un messaggio MQTT
def on_message(client, userdata, msg):
    payload = msg.payload.decode("utf-8").strip()
    logInfo(CLIENT_ID, f"Ricevuto comando MQTT: {payload}")

    if kit is None:
        logError(CLIENT_ID, "Servomotore non inizializzato, comando ignorato.")
        return

    try:
        if payload == "on":
            kit.servo[SERVO_CHANNEL].angle = ANGLE_DEVIAZIONE
            logInfo(CLIENT_ID, f"Deviazione attivata (angolo {ANGLE_DEVIAZIONE})")
            client.publish(MQTT_TOPIC_ACK, "ok: deviato")

        elif payload == "off":
            kit.servo[SERVO_CHANNEL].angle = ANGLE_RIPRISTINO
            logInfo(CLIENT_ID, f"Deviazione disattivata (angolo {ANGLE_RIPRISTINO})")
            client.publish(MQTT_TOPIC_ACK, "ok: non_deviato")

        else:
            logError(CLIENT_ID, f"Comando sconosciuto: {payload}")

    except Exception as e:
        logError(CLIENT_ID, f"Errore esecuzione comando: {e}")

# Avvio del client MQTT
def start_acting_client():
    client = mqtt.Client(CLIENT_ID)
    client.on_message = on_message

    try:
        client.connect("localhost", 1883, 60)
        client.subscribe(MQTT_TOPIC_CMD)
        logInfo(CLIENT_ID, f"Connesso a MQTT broker e sottoscritto a {MQTT_TOPIC_CMD}")
        client.loop_forever()

    except Exception as e:
        logError(CLIENT_ID, f"Errore connessione MQTT: {e}")
