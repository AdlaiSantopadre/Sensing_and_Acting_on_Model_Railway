# Definizione delle transizioni tra stati come da grafo fsm_stati_con_deviazione_lr.png
from fsm.state import State
from fsm.states import states
#import pandas as pd
# # Convenzione: evento = nome attraversamento es. "attraversamento_1"

transitions_data = [
    ("S_4_4", "attraversamento_1", "S_1_4", ["log:convoglio in attraversamento_1"]),
    ("S_1_4", "attraversamento_2", "S_2_4", ["log:convoglio in attraversamento_2"]),
    ("S_1_4", "attraversamento_1", "S_1_1", ["log:convoglio in attraversamento_1"]),
    ("S_1_1", "attraversamento_2", "S_2_1", ["log:convoglio in attraversamento_2"]),
    ("S_2_1", "attraversamento_3", "S_3_1", ["log:convoglio in attraversamento_3"]),
    ("S_2_1", "attraversamento_2", "S_2_2", ["log:convoglio in attraversamento_2"]),
    ("S_2_4", "attraversamento_3", "S_3_4", ["log:convoglio in attraversamento_3"]),
    ("S_2_4", "attraversamento_1", "S_2_1", ["log:convoglio in attraversamento_1"]),
    ("S_2_2", "attraversamento_3", "S_3_2", ["log:convoglio in attraversamento_3"]),
    ("S_3_1", "attraversamento_4", "S_4_1", ["log:convoglio in attraversamento_4", "set:warning=True"]),
    ("S_3_1", "attraversamento_3", "S_3_2", ["log:convoglio in attraversamento_3"]),
    ("S_3_2", "attraversamento_3", "S_3_3", ["log:convoglio in attraversamento_3"]),
    ("S_3_2", "attraversamento_4", "S_4_2", ["log:convoglio in attraversamento_4"]),
    ("S_3_3", "attraversamento_4", "S_4_3", ["log:convoglio in attraversamento_4"]),
    ("S_4_1", "attraversamento_2", "S_4_2", ["log:convoglio in attraversamento_2"]),
    ("S_3_4", "attraversamento_1", "S_3_1", ["log:warning"]),
    ("S_3_4", "attraversamento_4", "S_4_4", ["halt"]),
    ("S_4_2", "attraversamento_3", "S_4_3", ["log:convoglio in attraversamento_3"]),
    ("S_4_2", "attraversamento_1", "S_1_2", ["log:convoglio in attraversamento_1"]),
    ("S_4_3", "attraversamento_1", "S_1_3", ["log:convoglio in attraversamento_1"]),
    ("S_4_3", "attraversamento_4", "S_4_4", ["log:convoglio in attraversamento_4"]),
    ("S_1_2", "attraversamento_3", "S_1_3", ["log:convoglio in attraversamento_3"]),
    ("S_1_2", "attraversamento_2", "S_2_2", ["log:convoglio in attraversamento_2"]),
    ("S_1_3", "attraversamento_4", "S_1_4", ["log:convoglio in attraversamento_4"]),
    ("S_1_3", "attraversamento_3", "S_2_3", ["log:convoglio in attraversamento_3"]),
    ("S_2_3", "attraversamento_4", "S_3_3", ["log:convoglio in attraversamento_4"]),
    ("S_2_3", "attraversamento_3", "S_2_4", ["log:convoglio in attraversamento_3"]),
    ("S_4_1", "attraversamento_1", "D_1_1", ["mqtt:binario/deviatoio01=1", "wait_ack", "set:deviato=True"]),
    ("S_4_2", "attraversamento_1", "D_1_2", ["mqtt:binario/deviatoio01=1", "wait_ack", "set:deviato=True"]),
    ("D_1_1", "attraversamento_2", "D_1_2", ["log:L su attraversamento 2"]),
    ("D_1_2", "attraversamento_3", "D_1_3", ["log:L su attraversamento 3"]),
    ("D_1_3", "attraversamento_4", "D_1_4", ["log:L su attraversamento 4"]),
    ("D_1_4", "attraversamento_1", "D_1_1", ["log:L su attraversamento 1"]),
    ("D_1_1", "attraversamento_5", "D_2_1", ["log:V deviato su attraversamento 5", "mqtt:binario/deviatoio01=0", "set:warning=False"]),
    ("D_1_2", "attraversamento_5", "D_2_2", ["log:V deviato su attraversamento 5", "mqtt:binario/deviatoio01=0", "set:warning=False"]),
    ("D_1_3", "attraversamento_5", "D_2_3", ["log:V deviato su attraversamento 5"]),
    ("D_1_4", "attraversamento_5", "D_2_4", ["log:V deviato su attraversamento 5"]),
    ("D_2_1", "attraversamento_2", "D_2_2", ["log:L su attraversamento 2"]),
    ("D_2_2", "attraversamento_3", "D_2_3", ["log:L su attraversamento 3"]),
    ("D_2_3", "attraversamento_4", "D_2_4", ["log:L su attraversamento 4"])
]


# Definizione transizioni + azioni MQTT (mock topic/action)
def setup_transitions():
    states["S_4_4"].add_transition("attraversamento_1", states["S_1_4"], actions=["log:convoglio in attraversamento_1"])
    states["S_1_4"].add_transition("attraversamento_2", states["S_2_4"], actions=["log:convoglio in attraversamento_2"])
    states["S_1_4"].add_transition("attraversamento_1", states["S_1_1"], actions=["log:convoglio in attraversamento_1"])
    states["S_1_1"].add_transition("attraversamento_2", states["S_2_1"], actions=["log:convoglio in attraversamento_2"])
    states["S_2_1"].add_transition("attraversamento_3", states["S_3_1"], actions=["log:convoglio in attraversamento_3"])
    states["S_2_1"].add_transition("attraversamento_2", states["S_2_2"], actions=["log:convoglio in attraversamento_2"])
    states["S_2_2"].add_transition("attraversamento_3", states["S_3_2"], actions=["log:convoglio in attraversamento_3"])
    states["S_3_1"].add_transition("attraversamento_4", states["S_4_1"], actions=["log:convoglio in attraversamento_4", "set:warning=True"])
    states["S_3_1"].add_transition("attraversamento_2", states["S_3_2"], actions=["log:convoglio in attraversamento_3"])
    states["S_3_2"].add_transition("attraversamento_3", states["S_3_3"], actions=["log:convoglio in attraversamento_3"])
    states["S_3_2"].add_transition("attraversamento_4", states["S_4_2"], actions=["log:convoglio in attraversamento_4"])
    states["S_3_3"].add_transition("attraversamento_4", states["S_4_3"], actions=["log:convoglio in attraversamento_4"])
    states["S_4_1"].add_transition("attraversamento_2", states["S_4_2"], actions=["log:convoglio in attraversamento_2"])
    states["S_3_4"].add_transition("attraversamento_1", states["S_3_1"], actions=["log:warning"])
    states["S_3_4"].add_transition("attraversamento_4", states["S_4_4"], actions=["halt"])
    states["S_4_2"].add_transition("attraversamento_3", states["S_4_3"], actions=["log:convoglio in attraversamento_3"])
    # states["S_4_2"].add_transition("attraversamento_1", states["S_1_2"], actions=["log:convoglio in attraversamento_1"])
    states["S_4_3"].add_transition("attraversamento_1", states["S_1_3"], actions=["log:convoglio in attraversamento_1"])
    states["S_4_3"].add_transition("attraversamento_4", states["S_4_4"], actions=["log:convoglio in attraversamento_4"])
    states["S_1_2"].add_transition("attraversamento_3", states["S_1_3"], actions=["log:convoglio in attraversamento_3"])
    states["S_1_2"].add_transition("attraversamento_2", states["S_2_2"], actions=["log:convoglio in attraversamento_2"])
    states["S_1_3"].add_transition("attraversamento_4", states["S_1_4"], actions=["log:convoglio in attraversamento_4"])
    states["S_1_3"].add_transition("attraversamento_3", states["S_2_3"], actions=["log:convoglio in attraversamento_3"])
    states["S_2_3"].add_transition("attraversamento_4", states["S_3_3"], actions=["log:convoglio in attraversamento_4"])
    states["S_2_3"].add_transition("attraversamento_3", states["S_2_4"], actions=["log:convoglio in attraversamento_3"])
    states["S_2_4"].add_transition("attraversamento_1", states["S_2_1"], actions=["log:convoglio in attraversamento_1"])
    states["S_2_4"].add_transition("attraversamento_3", states["S_3_4"], actions=["log:convoglio in attraversamento_3"]) 
    states["S_4_1"].add_transition("attraversamento_1", states["D_1_1"], actions=["mqtt:binario/deviatoio01=1", "wait_ack", "set:deviato=True"])
    states["S_4_2"].add_transition("attraversamento_1", states["D_1_2"], actions=["mqtt:binario/deviatoio01=1", "wait_ack", "set:deviato=True"]) #da rivedere actions
    states["D_1_1"].add_transition("attraversamento_2", states["D_1_2"], actions=["log:L su attraversamento 2"])
    states["D_1_2"].add_transition("attraversamento_3", states["D_1_3"], actions=["log:L su attraversamento 3"])
    states["D_1_3"].add_transition("attraversamento_4", states["D_1_4"], actions=["log:L su attraversamento 4"])
    states["D_1_4"].add_transition("attraversamento_1", states["D_1_1"], actions=["log:L su attraversamento 1"])
    states["D_1_1"].add_transition("attraversamento_5", states["D_2_1"], actions=["log:V deviato su attraversamento 5", "mqtt:binario/deviatoio01=0", "set:warning=False"])
    states["D_1_2"].add_transition("attraversamento_5", states["D_2_2"], actions=["log:V deviato su attraversamento 5", "mqtt:binario/deviatoio01=0", "set:warning=False"])
    states["D_1_3"].add_transition("attraversamento_5", states["D_2_3"], actions=["log:V deviato su attraversamento 5"])
    states["D_1_4"].add_transition("attraversamento_5", states["D_2_4"], actions=["log:V deviato su attraversamento 5"])
    states["D_2_1"].add_transition("attraversamento_2", states["D_2_2"], actions=["log:L su attraversamento 2"])
    states["D_2_2"].add_transition("attraversamento_3", states["D_2_3"], actions=["log:L su attraversamento 3"])
    states["D_2_3"].add_transition("attraversamento_4", states["D_2_4"], actions=["log:L su attraversamento 4"])

    states["D_2_4"].add_transition("attraversamento_1", states["D_2_1"], actions=["log:L su attraversamento 1"])


# Generazione tabella con azioni
# def mostra_transizioni():
    # data = []
    # for state in states.values():
        # for event, next_state in state.transitions.items():
            # azioni = "; ".join(state.actions.get(event, []))
            # data.append((state.name, event, next_state.name, azioni))

    # df = pd.DataFrame(data, columns=["Stato Attuale", "Evento", "Stato Successivo", "Azioni MQTT / Log"])

    # return df
#

