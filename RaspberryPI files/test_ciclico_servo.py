
import time
from adafruit_pca9685 import PCA9685
from board import SCL, SDA
import busio

def us_to_pwm(us, freq=50):
    pulse_length = 1000000 / freq / 4096
    return int(us / pulse_length)

# Inizializzazione I2C e PCA9685
i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c)
pca.frequency = 50

servo_channel = 0  # Cambia se vuoi testare altri canali

print("Test ciclico servo su canale 0:")
print("1000us -> 1500us -> 2000us con pause di 2 secondi")

while True:
    for us in [1000, 1500, 2000]:
        pwm_val = us_to_pwm(us)
        pca.channels[servo_channel].duty_cycle = pwm_val
        print(f"→ Posizione {us}us (PWM {pwm_val})")
        time.sleep(2)
