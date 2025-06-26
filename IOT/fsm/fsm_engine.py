
from fsm.states import states


class FSMEngine:
    def __init__(self, start_state, mqtt_client):
        self.state = start_state               # Usa direttamente l'oggetto State
        self.mqtt_client = mqtt_client
        self.warning = False
        self.deviato = False
       

def handle_event(self, event_obj):
    """
    Gestisce un evento logico per la FSM.
    Accetta sia una stringa 'attraversamento_1' sia un dizionario con 'event' e 'timestamp'.
    """
    if isinstance(event_obj, dict):
        event = event_obj.get("event")
        ts = event_obj.get("timestamp", "N/D")
    else:
        event = event_obj
        ts = "N/D"
    print(f"[FSM] Evento ricevuto: {event} (timestamp: {ts})")
        
    if event in self.current_state.transitions:
            next_state = self.current_state.transitions[event]
            actions = self.current_state.actions.get(event, [])
            print(f"[Transizione] {self.current_state.name} --({event})--> {next_state.name}")
            self._execute_actions(actions)
            self.current_state = next_state
            print(f"[Stato Attuale] {self.current_state.name} ({self.current_state.code})")
    else:
            print(f"[FSM] Nessuna transizione definita per evento '{event}' nello stato {self.current_state.name}")
            print(f"Stato attuale: ({self.current_state.name}, {self.current_state.code})")
            print(f"Warning attivo: {self.warning} | Deviato attivo: {self.deviato}")

    def _execute_actions(self, actions):
        for action in actions:
            if action.startswith("log:"):
                print("[LOG]", action[4:])
            
            elif action.startswith("mqtt:"):
                try:
                    topic, payload = action[5:].split("=")
                    self.mqtt_client.publish(topic.strip(), payload.strip())
                    print(f"[MQTT] Pubblicato su {topic.strip()} ? {payload.strip()}")
                except Exception as e:
                    print(f"[FSM] Errore invio messaggio MQTT: {e}")
            elif action == "wait_ack":
                print("[ACK] Attesa ack... [simulato: ok]")
            elif action == "set:warning=True":
                self.warning = True
                print("[FLAG] Warning attivato")
            elif action == "set:warning=False":
                self.warning = False
                print("[FLAG] Warning disattivato")
            elif action == "set:deviato=True":
                self.deviato = True
                print("[FLAG] Percorso deviato attivo")
            elif action == "set:deviato=False":
                self.deviato = False
                print("[FLAG] Percorso deviato disattivato")
            elif action == "halt":
                print("[HALT] Sistema in stato di arresto! Alimentazione interrotta.")
            else:
                print(f"[AZIONE NON RICONOSCIUTA] {action}")

    def get_state(self):
        return self.current_state.name, self.current_state.code

    def is_warning_active(self):
        return self.warning

    def is_deviato_active(self):
        return self.deviato
