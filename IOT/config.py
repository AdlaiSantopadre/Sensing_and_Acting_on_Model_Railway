# config.py
BROKER = "192.168.1.153"
PORT = 1883
USERNAME = "ack_client" 
PASSWORD ="esp2025"

#Client locali
CLIENT_ID = "supervisore_fsm"

# Lista dei nodi ESP8266 attivi
CLIENT_IDS = [f"Nodo0{i}" for i in range(1, 6)]  # Nodo01 ... Nodo05


TOPIC_ACK_IN = {cid: f"/binario/0{cid[-1]}" for cid in CLIENT_IDS}
TOPIC_ACK_OUT = {cid: f"ack/Nodo0{cid}" for cid in CLIENT_IDS}

# Mapping evento FSM (nome semantico)
EVENT_MAP = {cid: f"attraversamento_{cid[-1]}" for cid in CLIENT_IDS}

# Parametri logica interna (es: lunghezza storia stato per trigger evento)
SEQUENZA_TARGET = [1, 0, 1]
MAX_HISTORY = 5
