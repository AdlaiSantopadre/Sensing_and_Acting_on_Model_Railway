# fsm_engine.py
import time
import paho.mqtt.client as mqtt
from fsm.states import states
from fsm.state import State

class FSMEngine:
    def __init__(self, initial_state: State, mqtt_client: mqtt.Client):
        self.state = initial_state
        self.mqtt_client = mqtt_client
        self.warning = False
        self.deviato = False

    def handle_event(self, event: str):
        if event in self.state.transitions:
            next_state = self.state.transitions[event]
            actions = self.state.actions.get(event, [])

            print(f"[FSM] Evento ricevuto: {event} → Transizione {self.state.name} ➜ {next_state.name}")
            self.execute_actions(actions)

            self.state = next_state
        else:
            print(f"[FSM] Nessuna transizione definita per evento '{event}' nello stato {self.state.name}")

    def execute_actions(self, actions):
        for action in actions:
            if action.startswith("log:"):
                print(f"[LOG] {action[4:]}")
            elif action.startswith("mqtt:"):
                topic, payload = action[5:].split("=")
                self.mqtt_client.publish(topic.strip(), payload.strip())
                print(f"[MQTT] Pubblicato su {topic.strip()} → {payload.strip()}")
            elif action == "wait_ack":
                print("[FSM] Attesa ACK (simulata)...")
                time.sleep(0.5)  # sostituire con attesa reale in produzione
            elif action == "halt":
                print("[FSM] HALT: Condizione critica! Interruzione...")
                raise SystemExit("Sistema arrestato per sicurezza.")
            elif action.startswith("set:"):
                var, val = action[4:].split("=")
                setattr(self, var.strip(), eval(val.strip()))
                print(f"[FSM] Stato interno aggiornato: {var.strip()} = {getattr(self, var.strip())}")

    def get_state(self):
        return self.state.name, self.state.code

    def is_warning_active(self):
        return self.warning

    def is_deviation_active(self):
        return self.deviato
