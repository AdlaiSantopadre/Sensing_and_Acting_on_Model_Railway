import time
import paho.mqtt.client as mqtt
from adafruit_servokit import ServoKit
import RPi.GPIO as GPIO


# === Configurazione ===
CLIENT_ID_DEVIATOIO1 = "deviatoio01"
TOPIC_COMMAND = "deviatoio/01"
TOPIC_ACK = "ack/deviatoio/01"
mqtt_client.username_pw_set("deviatoio01", "esp2025")

ANGLE_DEVIAZIONE = 70
ANGLE_RIPRISTINO = 98
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
    print(f"[{CLIENT_ID_DEVIATOIO1}] Servo inizializzato a {ANGLE_RIPRISTINO} sul canale {SERVO_CHANNEL}")
except Exception as e:
    print(f"[{CLIENT_ID_DEVIATOIO1}] ERRORE inizializzazione servomotore: {e}")
    kit = None

# === Funzione per attivare relÃ¨ di emergenza ===
def attiva_emergenza():
    GPIO.output(RELE_GPIO_PIN, GPIO.HIGH)
    print(f"[{CLIENT_ID_DEVIATOIO1}] EMERGENZA: attivato rele` su GPIO{RELE_GPIO_PIN}")

# === Callback MQTT ===
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[{CLIENT_ID_DEVIATOIO1}] Connesso al broker MQTT.")
        client.subscribe(TOPIC_COMMAND)
        print(f"[{CLIENT_ID_DEVIATOIO1}] Ascolto su topic: {TOPIC_COMMAND}")
    else:
        print(f"[{CLIENT_ID_DEVIATOIO1}] ERRORE connessione MQTT: codice {rc}")


def on_message(client, userdata, msg):
    payload = msg.payload.decode().strip().lower()
    print(f"[{CLIENT_ID_DEVIATOIO1}] Ricevuto comando: {payload}")

    if not kit:
        print(f"[{CLIENT_ID_DEVIATOIO1}] ERRORE: Servomotore non disponibile.")
        attiva_emergenza()
        return

    try:
        if payload == "on":
            kit.servo[SERVO_CHANNEL].angle = ANGLE_DEVIAZIONE
            print(f"[{CLIENT_ID_DEVIATOIO1}] Servo impostato a {ANGLE_DEVIAZIONE}")
            client.publish(TOPIC_ACK, "ok: deviato")
        elif payload == "off":
            kit.servo[SERVO_CHANNEL].angle = ANGLE_RIPRISTINO
            print(f"[{CLIENT_ID_DEVIATOIO1}] Servo impostato a {ANGLE_RIPRISTINO}")
            client.publish(TOPIC_ACK, "ok: non_deviato")
        else:
            print(f"[{CLIENT_ID_DEVIATOIO1}] ERRORE: comando non valido: '{payload}'")
    except Exception as e:
        print(f"[{CLIENT_ID_DEVIATOIO1}] ERRORE movimento servo: {e}")
        attiva_emergenza()

# === Avvio client MQTT ===
def start_acting_servomotori(broker_address="192.168.1.153", broker_port=1883):
    client = mqtt.Client(CLIENT_ID_DEVIATOIO1)
    client.on_connect = on_connect
    client.on_message = on_message
    try:
        client.connect(broker_address, broker_port, keepalive=60)
        client.loop_start()
        print(f"[{CLIENT_ID_DEVIATOIO1}] Client MQTT acting avviato.")
    except Exception as e:
        print(f"[{CLIENT_ID_DEVIATOIO1}] ERRORE connessione al broker: {e}")
