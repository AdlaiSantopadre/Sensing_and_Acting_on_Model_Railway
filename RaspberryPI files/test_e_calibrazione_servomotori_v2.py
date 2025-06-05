# Attiva l'ambiente virtuale source ~/env/bin/activate
from adafruit_servokit import ServoKit
import time

# Inizializzazione del controller ServoKit per 16 canali
kit = ServoKit(channels=16)

def chiedi_intero(messaggio, minimo=0, massimo=15):
    while True:
        try:
            val = int(input(messaggio))
            if minimo is not None and val < minimo:
                print(f"Valore troppo basso. Minimo: {minimo}")
                continue
            if massimo is not None and val > massimo:
                print(f"Valore troppo alto. Massimo: {massimo}")
                continue
            return val
        except ValueError:
            print("Inserisci un numero intero valido.")

# Selezione del canale servo
servo_ch = chiedi_intero("Seleziona il canale servo (0-15): ", 0, 15)

# Impostazione gamma impulsi PWM
min_pulse = chiedi_intero("Inserisci min_pulse (us, es: 500): ", 400, 1000)
max_pulse = chiedi_intero("Inserisci max_pulse (us, es: 2400): ", 2000, 3000)

kit.servo[servo_ch].set_pulse_width_range(min_pulse=min_pulse, max_pulse=max_pulse)

# Calibrazione interattiva con angoli
print("\n== Modalità calibrazione manuale ==")
print("Inserisci un angolo tra 0 e 180 per muovere il servo.")
print("Digita 'fine' per terminare la calibrazione.")


while True:
    cmd = input(f"[Servo {servo_ch}] > Angolo (0-180) o 'fine': ").strip()
    if cmd.lower() == "fine":
        break
    try:
        angle = float(cmd)
        if 0 <= angle <= 180:
            kit.servo[servo_ch].angle = angle
        else:
            print("Angolo fuori intervallo.")
    except ValueError:
        print("Input non valido.")

# Test ciclico finale
print(f"\n== Avvio test ciclico su servo {servo_ch} ==")
for angolo in [0, 90, 180, 90]:
    print(f"→ Servo {servo_ch} a {angolo}°")
    kit.servo[servo_ch].angle = angolo
    time.sleep(2)

print("Test completato.")
