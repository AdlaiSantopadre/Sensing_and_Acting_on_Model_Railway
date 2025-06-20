
from collections import deque
from datetime import datetime

# Coda FIFO per eventi da interpretare nella FSM
event_queue = deque()

def enqueue_event(event_name):
    """Accoda un evento con timestamp corrente"""
    event = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "event": event_name
    }
    event_queue.append(event)
    print(f"[STACK] Evento enqueued: {event}")

def pop_event():
    """Estrae l'evento più vecchio"""
    if event_queue:
        return event_queue.popleft()
    return None

def peek_stack():
    """Restituisce l'intera coda (non distruttivo)"""
    return list(event_queue)

