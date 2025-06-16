# Questo script di test permette di verificare manualmente il comportamento della FSM
# senza connessione MQTT. Utile per debug e sviluppo iniziale.

from fsm.fsm_engine_mqtt import FSMEngine
from fsm.states import states
from fsm.transitions import setup_transitions
setup_transitions()
# Inizializzazione FSM con stato iniziale
initial_state = states["S_4_4"]
fsm = FSMEngine(initial_state, mqtt_client=None)

print("[FSM-TEST] Stato iniziale:", fsm.get_state())

while True:
    evento = input("Inserisci evento (nodo_1 ... nodo_5 oppure 'exit'): ").strip()
    if evento == "exit":
        print("Uscita dal test interattivo.")
        break
    fsm.handle_event(evento)
    print("Stato attuale:", fsm.get_state())
    print("Warning attivo:", fsm.is_warning_active(), "| Deviato attivo:", fsm.is_deviation_active())
