# La  Classe State gestisce nome, codice binario, transizioni e azioni collegate 
class State:
    def __init__(self, name: str, code: str):
        self.name = name                  # es. 'S_4_4'
        self.code = code                  # es. '00010001'
        self.transitions = {}             # dict: evento -> stato successivo
        self.actions = {}                 # dict: evento -> lista azioni da eseguire

    def add_transition(self, event: str, next_state: 'State', actions=None):
        if event in self.transitions:
            raise ValueError(f"Transizione duplicata per evento '{event}' nello stato '{self.name}'")
        self.transitions[event] = next_state
        self.actions[event] = actions if actions else []

    def __repr__(self):
        return f"State({self.name}, {self.code})"
