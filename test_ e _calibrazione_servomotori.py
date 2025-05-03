
import time
from adafruit_pca9685 import PCA9685
from board import SCL, SDA
import busio

# Imposta l'interfaccia I2C
i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c)
pca.frequency = 50  # Frequenza per servo SG90

# Funzione per convertire microsecondi in valori PWM (0-4095)
def us_to_pwm(us):
    pulse_length = 1000000 / pca.frequency / 4096  # in microsecondi
    return int(us / pulse_length)

# Test sequenziale iniziale su canali 0-3
print("== Test sequenziale: muovo i servo su canali 0-3 ==")
for channel in range(4):
    print(f"Servo {channel} -> posizione MIN")
    pca.channels[channel].duty_cycle = us_to_pwm(1000)
    time.sleep(0.5)
    print(f"Servo {channel} -> posizione MAX")
    pca.channels[channel].duty_cycle = us_to_pwm(2000)
    time.sleep(0.5)
    print(f"Servo {channel} -> posizione CENTRO")
    pca.channels[channel].duty_cycle = us_to_pwm(1500)
    time.sleep(0.5)

print("\n== Modalità calibrazione manuale ==")
print("Comandi disponibili:")
print("  [valore]+ : aumenta di valore microsecondi (es: 100+)")
print("  [valore]- : diminuisce di valore microsecondi (es: 100-)")
print("  [valore]x : posizione assoluta (es: 1500x)")
print("  s[num]    : cambia canale servo (es: s2 per usare canale 2)")
print("  exit      : per uscire")

servo_channel = 0
position_us = 1500

while True:
    cmd = input(f"[Servo {servo_channel} @ {position_us}us] > ").strip().lower()
    if cmd == "exit":
        break
    elif cmd.startswith("s") and cmd[1:].isdigit():
        servo_channel = int(cmd[1:])
        print(f"--> Canale cambiato a {servo_channel}")
    elif cmd.endswith("+") and cmd[:-1].isdigit():
        delta = int(cmd[:-1])
        position_us += delta
    elif cmd.endswith("-") and cmd[:-1].isdigit():
        delta = int(cmd[:-1])
        position_us -= delta
    elif cmd.endswith("x") and cmd[:-1].isdigit():
        position_us = int(cmd[:-1])
    else:
        print("Comando non valido.")
        continue

    pwm_val = us_to_pwm(position_us)
    pca.channels[servo_channel].duty_cycle = pwm_val
    print(f"--> Posizione aggiornata: {position_us}us -> PWM {pwm_val}")

# Al termine, fermiamo tutti i canali usati
for ch in range(4):
    pca.channels[ch].duty_cycle = 0

print("== Uscita == Servo fermati.")
