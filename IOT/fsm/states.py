# Rieseguo dopo il reset
from dataclasses import dataclass

@dataclass
class State:
    name: str
    code: str
    transitions: dict = None
    actions: dict = None

    def __post_init__(self):
        self.transitions = self.transitions or {}
        self.actions = self.actions or {}

    def add_transition(self, event: str, next_state: 'State', actions=None):
        if event in self.transitions:
            raise ValueError(f"Transizione duplicata per evento '{event}' nello stato '{self.name}'")
        self.transitions[event] = next_state
        self.actions[event] = actions if actions else []

# Definizione degli stati
states = {
    "S_4_4": State("S_4_4", "00010001"),#
    "S_1_4": State("S_1_4", "10000001"),#
    "S_2_4": State("S_2_4", "01000001"),#
    "S_3_4": State("S_3_4", "00100001"),#
    "S_1_1": State("S_1_1", "00100010"),#
    "S_2_1": State("S_2_1", "01000010"),#
    "S_3_1": State("S_3_1", "00101000"),#
    "S_4_1": State("S_4_1", "00010010"),#
    "S_2_2": State("S_2_2", "01000100"),#
    "S_3_2": State("S_3_2", "00101000"),#
    "S_4_2": State("S_4_2", "00010100"),#
    "S_3_3": State("S_3_3", "00100010"),#
    "S_4_3": State("S_4_3", "00100010"),#
    "S_1_2": State("S_1_2", "00100100"),#
    "S_1_3": State("S_1_3", "00101000"),#
    
    
    "S_2_3": State("S_2_3", "01001000"),#
    

    # Stati di deviazione
    "D_1_1": State("D_1_1", "11100001"),#
    "D_1_2": State("D_1_2", "11100010"),#
    "D_1_3": State("D_1_3", "11100100"),#
    "D_1_4": State("D_1_4", "11101000"),#
    
    "D_2_1": State("D_2_1", "11110001"),#
    "D_2_2": State("D_2_2", "11110010"),#
    "D_2_3": State("D_2_3", "11110100"),#
    "D_2_4": State("D_2_4", "11111000"),#
}


