
import time
import paho.mqtt.client as mqtt
from adafruit_servokit import ServoKit
import RPi.GPIO as GPIO
from logutil import logInfo, logError

# === Configurazione ===
CLIENT_ID = "deviatoio01"
TOPIC_COMMAND = "deviatoio/01"
TOPIC_ACK = "ack/deviatoio/01"

ANGLE_DEVIAZIONE = 105
ANGLE_RIPRISTINO = 75
SERVO_CHANNEL = 0

# === GPIO Rele' ===
RELE_GPIO_PIN = 6
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELE_GPIO_PIN, GPIO.OUT)
GPIO.output(RELE_GPIO_PIN, GPIO.LOW)  # non attivo

# === Inizializzazione servo ===
try:
    kit = ServoKit(channels=16)
    kit.servo[SERVO_CHANNEL].set_pulse_width_range(min_pulse=500, max_pulse=2400)
    kit.servo[SERVO_CHANNEL].angle = ANGLE_RIPRISTINO
    logInfo(CLIENT_ID, f"Servo inizializzato a {ANGLE_RIPRISTINO}° sul canale {SERVO_CHANNEL}")
except Exception as e:
    logError(CLIENT_ID, f"Errore inizializzazione servomotore: {e}")
    kit = None

# === Funzione per attivare relè di emergenza ===
def attiva_emergenza():
    GPIO.output(RELE_GPIO_PIN, GPIO.HIGH)
    logError(CLIENT_ID, "EMERGENZA: attivato relè su GPIO6")

# === Callback MQTT ===
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logInfo(CLIENT_ID, "Connesso al broker MQTT.")
        client.subscribe(TOPIC_COMMAND)
        logInfo(CLIENT_ID, f"Ascolto su topic: {TOPIC_COMMAND}")
    else:
        logError(CLIENT_ID, f"Connessione MQTT fallita: codice {rc}")

def on_message(client, userdata, msg):
    payload = msg.payload.decode().strip().lower()
    logInfo(CLIENT_ID, f"Ricevuto comando: {payload}")

    if not kit:
        logError(CLIENT_ID, "Servomotore non disponibile.")
        attiva_emergenza()
        return

    try:
        if payload == "on":
            kit.servo[SERVO_CHANNEL].angle = ANGLE_DEVIAZIONE
            logInfo(CLIENT_ID, f"Servo impostato a {ANGLE_DEVIAZIONE}°")
            client.publish(TOPIC_ACK, "ok: deviato")
        elif payload == "off":
            kit.servo[SERVO_CHANNEL].angle = ANGLE_RIPRISTINO
            logInfo(CLIENT_ID, f"Servo impostato a {ANGLE_RIPRISTINO}°")
            client.publish(TOPIC_ACK, "ok: non_deviato")
        else:
            logError(CLIENT_ID, f"Comando non valido: {payload}")
    except Exception as e:
        logError(CLIENT_ID, f"Errore movimento servo: {e}")
        attiva_emergenza()

# === Avvio client MQTT ===
def start_acting_servomotori(broker_address="localhost", broker_port=1883):
    client = mqtt.Client(CLIENT_ID)
    client.on_connect = on_connect
    client.on_message = on_message
    try:
        client.connect(broker_address, broker_port, keepalive=60)
        client.loop_start()
        logInfo(CLIENT_ID, "Client MQTT acting avviato.")
    except Exception as e:
        logError(CLIENT_ID, f"Errore connessione al broker: {e}")
