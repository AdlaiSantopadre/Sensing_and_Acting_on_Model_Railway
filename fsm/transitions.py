# Definizione delle transizioni tra stati come da grafo fsm_stati_con_deviazione_lr.png
from fsm.state import State
from fsm.states import states

# Convenzione: evento = nome nodo es. "nodo_1"

# Transizioni da S_4_4
states["S_4_4"].add_transition("nodo_1", states["S_1_4"])

# Da S_1_4
states["S_1_4"].add_transition("nodo_2", states["S_2_4"])
states["S_1_4"].add_transition("nodo_1", states["S_1_1"])

# Da S_2_4
states["S_2_4"].add_transition("nodo_1", states["S_2_1"])
states["S_2_4"].add_transition("nodo_3", states["S_3_4"])

# Da S_3_4
states["S_3_4"].add_transition("nodo_1", states["S_3_1"])  # warning
states["S_3_4"].add_transition("nodo_4", states["S_4_4"])  # halt

# Da S_1_1
states["S_1_1"].add_transition("nodo_2", states["S_2_1"])

# Da S_2_1
states["S_2_1"].add_transition("nodo_2", states["S_2_2"])
states["S_2_1"].add_transition("nodo_3", states["S_3_1"])

# Da S_3_1
states["S_3_1"].add_transition("nodo_3", states["S_3_2"])
states["S_3_1"].add_transition("nodo_4", states["S_4_1"])  # warning

# Da S_4_1
states["S_4_1"].add_transition("nodo_1", states["D_1_1"])  # deviazione

# Da D_1_1
states["D_1_1"].add_transition("nodo_2", states["D_1_2"])
states["D_1_1"].add_transition("nodo_5", states["D_2_1"])

# Da D_1_2
states["D_1_2"].add_transition("nodo_3", states["D_1_3"])
states["D_1_2"].add_transition("nodo_5", states["D_2_2"])

# Da D_1_3
states["D_1_3"].add_transition("nodo_4", states["D_1_4"])
states["D_1_3"].add_transition("nodo_5", states["D_2_3"])

# Da D_1_4
states["D_1_4"].add_transition("nodo_1", states["D_1_1_loop"])
states["D_1_4"].add_transition("nodo_5", states["D_2_4"])

# Da D_2_1 → D_2_2 → D_2_3 → D_2_4 (ciclo sul principale mentre V è deviato)
states["D_2_1"].add_transition("nodo_2", states["D_2_2"])
states["D_2_2"].add_transition("nodo_3", states["D_2_3"])
states["D_2_3"].add_transition("nodo_4", states["D_2_4"])

# Visualizza tabella transizioni
import pandas as pd
data = []
for s in states.values():
    for evt, next_s in s.transitions.items():
        data.append((s.name, evt, next_s.name))
df_transitions = pd.DataFrame(data, columns=["Stato Attuale", "Evento", "Stato Successivo"])
import ace_tools as tools; tools.display_dataframe_to_user(name="Tabella delle transizioni FSM", dataframe=df_transitions)
