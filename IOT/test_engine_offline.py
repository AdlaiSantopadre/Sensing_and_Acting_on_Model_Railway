from fsm.fsm_engine import FSMEngine
from fsm.states import states
from fsm.transitions import setup_transitions
fsm = FSMEngine()

event_sequence = [
    "nodo_1",  # S_4_4 → S_1_4
    "nodo_2",  # S_1_4 → S_2_4
    "nodo_3",  # S_2_4 → S_3_4
    "nodo_1",  # S_3_4 → S_3_1 + WARNING
    "nodo_4",  # S_3_1 → S_4_1 + set warning
    "nodo_1",  # S_4_1 → D_1_1 + deviazione
    "nodo_5",  # D_1_1 → D_2_1 + reset warning
    "nodo_2",  # D_2_1 → D_2_2
    "nodo_3",  # D_2_2 → D_2_3
    "nodo_4",  # D_2_3 → D_2_4
]

for e in event_sequence:
    print(f"\n>> Evento: {e}")
    fsm.handle_event(e)