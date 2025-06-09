# event_stack.py
from collections import deque

# Stack FIFO per eventi da interpretare nella FSM
event_queue = deque()

def enqueue_event(event):
    event_queue.append(event)
    print(f"[STACK] Evento enqueued: {event}")

def pop_event():
    if event_queue:
        return event_queue.popleft()
    return None

def peek_stack():
    return list(event_queue)
