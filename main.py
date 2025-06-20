import threading
from client_acting_and_logic.mqtt_ack_handler import start_ack_handler
from client_acting_and_logic.mqtt_servomotore import start_acting_client
from fsm.fsm_engine_mqtt import FSMEngine
from fsm.states import states
from fsm.transitions import setup_transitions
# Ensure event_stack.py exists in the same directory or update the import path accordingly
from client_acting_and_logic.event_stack import pop_event
import time

# Inizializza FSM
setup_transitions()
fsm = FSMEngine(initial_state=states["S_4_4"], mqtt_client=None)

def fsm_event_loop():
    print("[FSM_LOOP] Avvio ciclo di polling eventi")
    while True:
        event = pop_event()
        if event:
            try:
                event_id = event.get("id")  # es: "Nodo01"
                if event_id:
                    x = event_id[-1]  # prende il numero finale: 1..5
                    evento_fsm = f"attraversamento_{x}"
                    fsm.handle_event(evento_fsm)
            except Exception as e:
                print("[FSM_LOOP] Errore nella gestione evento:", e)
        time.sleep(0.1)

if __name__ == "__main__":
    print("[MAIN] Avvio sistema IoT client con FSM")

    t1 = threading.Thread(target=start_acting_client)
    t2 = threading.Thread(target=start_ack_handler)
    t3 = threading.Thread(target=fsm_event_loop)

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()
