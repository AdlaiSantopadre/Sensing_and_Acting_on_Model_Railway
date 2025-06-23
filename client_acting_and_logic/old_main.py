from mqtt_ack_handler import start_ack_handler
from mqtt_servomotore_new import start_acting_client
import threading

if __name__ == "__main__":
    print("[MAIN] Avvio sistema IoT client")

    t1 = threading.Thread(target=start_acting_client)
    t2 = threading.Thread(target=start_ack_handler)
    
    t1.start()
    t2.start()

    t1.join()
    t2.join()
