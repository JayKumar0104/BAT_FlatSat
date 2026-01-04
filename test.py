import math
import time
import board
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX as LSM6DS
from adafruit_lis3mdl import LIS3MDL
from git import Repo
from picamera2 import Picamera2
from datetime import datetime
from git import Repo

i2c = board.I2C()
accel_gyro = LSM6DS(i2c)
mag = LIS3MDL(i2c)
picam2 = Picamera2()

print("lebron")

while 67<69:
  accelx, accely, accelz = accel_gyro.acceleration
  a_mag = math.sqrt(accelx**2 + accely**2 + accelz**2)
  print(a_mag)


