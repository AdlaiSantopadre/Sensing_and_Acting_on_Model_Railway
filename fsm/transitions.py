# Definizione delle transizioni tra stati come da grafo fsm_stati_con_deviazione_lr.png
from fsm.state import State
from fsm.states import states
import pandas as pd
# # Convenzione: evento = nome nodo es. "nodo_1"

transitions_data = [
    ("S_4_4", "nodo_1", "S_1_4", ["log:passaggio nodo_1"]),
    ("S_1_4", "nodo_2", "S_2_4", ["log:passaggio nodo_2"]),
    ("S_1_4", "nodo_1", "S_1_1", ["log:passaggio nodo_1"]),
    ("S_1_1", "nodo_2", "S_2_1", ["log:passaggio nodo_2"]),
    ("S_2_1", "nodo_3", "S_3_1", ["log:passaggio nodo_3"]),
    ("S_2_1", "nodo_2", "S_2_2", ["log:passaggio nodo_2"]),
    ("S_2_4", "nodo_3", "S_3_4", ["log:passaggio nodo_3"]),
    ("S_2_4", "nodo_1", "S_2_1", ["log:passaggio nodo_1"]),
    ("S_2_2", "nodo_3", "S_3_2", ["log:passaggio nodo_3"]),
    ("S_3_1", "nodo_4", "S_4_1", ["log:passaggio nodo_4", "set:warning=True"]),
    ("S_3_1", "nodo_3", "S_3_2", ["log:passaggio nodo_3"]),
    ("S_3_2", "nodo_3", "S_3_3", ["log:passaggio nodo_3"]),
    ("S_3_2", "nodo_4", "S_4_2", ["log:passaggio nodo_4"]),
    ("S_3_3", "nodo_4", "S_4_3", ["log:passaggio nodo_4"]),
    ("S_4_1", "nodo_2", "S_4_2", ["log:passaggio nodo_2"]),
    ("S_3_4", "nodo_1", "S_3_1", ["log:warning"]),
    ("S_3_4", "nodo_4", "S_4_4", ["halt"]),
    ("S_4_2", "nodo_3", "S_4_3", ["log:passaggio nodo_3"]),
    ("S_4_2", "nodo_1", "S_1_2", ["log:passaggio nodo_1"]),
    ("S_4_3", "nodo_1", "S_1_3", ["log:passaggio nodo_1"]),
    ("S_4_3", "nodo_4", "S_4_4", ["log:passaggio nodo_4"]),
    ("S_1_2", "nodo_3", "S_1_3", ["log:passaggio nodo_3"]),
    ("S_1_2", "nodo_2", "S_2_2", ["log:passaggio nodo_2"]),
    ("S_1_3", "nodo_4", "S_1_4", ["log:passaggio nodo_4"]),
    ("S_1_3", "nodo_3", "S_2_3", ["log:passaggio nodo_3"]),
    ("S_2_3", "nodo_4", "S_3_3", ["log:passaggio nodo_4"]),
    ("S_2_3", "nodo_3", "S_2_4", ["log:passaggio nodo_3"]),
    ("S_4_1", "nodo_1", "D_1_1", ["mqtt:binario/deviatoio01=1", "wait_ack", "set:deviato=True"]),
    ("S_4_2", "nodo_1", "D_1_2", ["mqtt:binario/deviatoio01=1", "wait_ack", "set:deviato=True"]),
    ("D_1_1", "nodo_2", "D_1_2", ["log:L su nodo 2"]),
    ("D_1_2", "nodo_3", "D_1_3", ["log:L su nodo 3"]),
    ("D_1_3", "nodo_4", "D_1_4", ["log:L su nodo 4"]),
    ("D_1_4", "nodo_1", "D_1_1", ["log:L su nodo 1"]),
    ("D_1_1", "nodo_5", "D_2_1", ["log:V deviato su nodo 5", "mqtt:binario/deviatoio01=0", "set:warning=False"]),
    ("D_1_2", "nodo_5", "D_2_2", ["log:V deviato su nodo 5", "mqtt:binario/deviatoio01=0", "set:warning=False"]),
    ("D_1_3", "nodo_5", "D_2_3", ["log:V deviato su nodo 5"]),
    ("D_1_4", "nodo_5", "D_2_4", ["log:V deviato su nodo 5"]),
    ("D_2_1", "nodo_2", "D_2_2", ["log:L su nodo 2"]),
    ("D_2_2", "nodo_3", "D_2_3", ["log:L su nodo 3"]),
    ("D_2_3", "nodo_4", "D_2_4", ["log:L su nodo 4"])
]


# Definizione transizioni + azioni MQTT (mock topic/action)
def setup_transitions():
    states["S_4_4"].add_transition("nodo_1", states["S_1_4"], actions=["log:passaggio nodo_1"])
    states["S_1_4"].add_transition("nodo_2", states["S_2_4"], actions=["log:passaggio nodo_2"])
    states["S_1_4"].add_transition("nodo_1", states["S_1_1"], actions=["log:passaggio nodo_1"])
    states["S_1_1"].add_transition("nodo_2", states["S_2_1"], actions=["log:passaggio nodo_2"])
    states["S_2_1"].add_transition("nodo_3", states["S_3_1"], actions=["log:passaggio nodo_3"])
    states["S_2_1"].add_transition("nodo_2", states["S_2_2"], actions=["log:passaggio nodo_2"])
    states["S_2_2"].add_transition("nodo_3", states["S_3_2"], actions=["log:passaggio nodo_3"])
    states["S_3_1"].add_transition("nodo_4", states["S_4_1"], actions=["log:passaggio nodo_4", "set:warning=True"])
    states["S_3_1"].add_transition("nodo_2", states["S_3_2"], actions=["log:passaggio nodo_3"])
    states["S_3_2"].add_transition("nodo_3", states["S_3_3"], actions=["log:passaggio nodo_3"])
    states["S_3_2"].add_transition("nodo_4", states["S_4_2"], actions=["log:passaggio nodo_4"])
    states["S_3_3"].add_transition("nodo_4", states["S_4_3"], actions=["log:passaggio nodo_4"])
    states["S_4_1"].add_transition("nodo_2", states["S_4_2"], actions=["log:passaggio nodo_2"])
    states["S_3_4"].add_transition("nodo_1", states["S_3_1"], actions=["log:warning"])
    states["S_3_4"].add_transition("nodo_4", states["S_4_4"], actions=["halt"])
    states["S_4_2"].add_transition("nodo_3", states["S_4_3"], actions=["log:passaggio nodo_3"])
    # states["S_4_2"].add_transition("nodo_1", states["S_1_2"], actions=["log:passaggio nodo_1"])
    states["S_4_3"].add_transition("nodo_1", states["S_1_3"], actions=["log:passaggio nodo_1"])
    states["S_4_3"].add_transition("nodo_4", states["S_4_4"], actions=["log:passaggio nodo_4"])
    states["S_1_2"].add_transition("nodo_3", states["S_1_3"], actions=["log:passaggio nodo_3"])
    states["S_1_2"].add_transition("nodo_2", states["S_2_2"], actions=["log:passaggio nodo_2"])
    states["S_1_3"].add_transition("nodo_4", states["S_1_4"], actions=["log:passaggio nodo_4"])
    states["S_1_3"].add_transition("nodo_3", states["S_2_3"], actions=["log:passaggio nodo_3"])
    states["S_2_3"].add_transition("nodo_4", states["S_3_3"], actions=["log:passaggio nodo_4"])
    states["S_2_3"].add_transition("nodo_3", states["S_2_4"], actions=["log:passaggio nodo_3"])
    states["S_2_4"].add_transition("nodo_1", states["S_2_1"], actions=["log:passaggio nodo_1"])
    states["S_2_4"].add_transition("nodo_3", states["S_3_4"], actions=["log:passaggio nodo_3"]) 
    states["S_4_1"].add_transition("nodo_1", states["D_1_1"], actions=["mqtt:binario/deviatoio01=1", "wait_ack", "set:deviato=True"])
    states["S_4_2"].add_transition("nodo_1", states["D_1_2"], actions=["mqtt:binario/deviatoio01=1", "wait_ack", "set:deviato=True"]) #da rivedere actions
    states["D_1_1"].add_transition("nodo_2", states["D_1_2"], actions=["log:L su nodo 2"])
    states["D_1_2"].add_transition("nodo_3", states["D_1_3"], actions=["log:L su nodo 3"])
    states["D_1_3"].add_transition("nodo_4", states["D_1_4"], actions=["log:L su nodo 4"])
    states["D_1_4"].add_transition("nodo_1", states["D_1_1"], actions=["log:L su nodo 1"])
    states["D_1_1"].add_transition("nodo_5", states["D_2_1"], actions=["log:V deviato su nodo 5", "mqtt:binario/deviatoio01=0", "set:warning=False"])
    states["D_1_2"].add_transition("nodo_5", states["D_2_2"], actions=["log:V deviato su nodo 5", "mqtt:binario/deviatoio01=0", "set:warning=False"])
    states["D_1_3"].add_transition("nodo_5", states["D_2_3"], actions=["log:V deviato su nodo 5"])
    states["D_1_4"].add_transition("nodo_5", states["D_2_4"], actions=["log:V deviato su nodo 5"])
    states["D_2_1"].add_transition("nodo_2", states["D_2_2"], actions=["log:L su nodo 2"])
    states["D_2_2"].add_transition("nodo_3", states["D_2_3"], actions=["log:L su nodo 3"])
    states["D_2_3"].add_transition("nodo_4", states["D_2_4"], actions=["log:L su nodo 4"])

    states["D_2_4"].add_transition("nodo_1", states["D_2_1"], actions=["log:L su nodo 1"])


# Generazione tabella con azioni
def mostra_transizioni():
    data = []
    for state in states.values():
        for event, next_state in state.transitions.items():
            azioni = "; ".join(state.actions.get(event, []))
            data.append((state.name, event, next_state.name, azioni))

    df = pd.DataFrame(data, columns=["Stato Attuale", "Evento", "Stato Successivo", "Azioni MQTT / Log"])

    return df

