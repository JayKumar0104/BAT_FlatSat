import math
import time
import os
import board
from datetime import datetime
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX as LSM6DS
from picamera2 import Picamera2

# ===== VARIABLES =====
THRESHOLD = 2.5        # shake sensitivity (m/s^2 above gravity)
g = 9.80665
delay = 1.5            # cooldown (seconds)
DEBUG = True

REPO_PATH = "/home/bayareatinkerers/BAT_FlatSat"
FOLDER_PATH = "Images"

# ===== Setup =====
os.makedirs(f"{REPO_PATH}/{FOLDER_PATH}", exist_ok=True)

i2c = board.I2C()
accel_gyro = LSM6DS(i2c)

picam2 = Picamera2()
picam2.configure(picam2.create_still_configuration())
picam2.start()
time.sleep(0.5)

# ===== Helper =====
def img_gen():
    return f"{REPO_PATH}/{FOLDER_PATH}/photo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"

# ===== Main Loop =====
def take_photo():
    print("FlatSat running — shake to trigger")
    last_print = 0

    while True:
        ax, ay, az = accel_gyro.acceleration
        a_mag = math.sqrt(ax**2 + ay**2 + az**2)
        mag_minus_g = abs(a_mag - g)

        if DEBUG and time.time() - last_print > 0.5:
            print(f"ax={ax:.2f} ay={ay:.2f} az={az:.2f} | mag={a_mag:.2f} | mag-g={mag_minus_g:.2f}")
            last_print = time.time()

        if mag_minus_g > THRESHOLD:
            print("SHAKE DETECTED")
            time.sleep(0.25)

            filename = img_gen()
            picam2.capture_file(filename)
            print("Saved:", filename)

            time.sleep(delay)

# ===== Start =====
if __name__ == "__main__":
    take_photo()
