import time
import board
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX as LSM6DS
from adafruit_lis3mdl import LIS3MDL
from git import Repo
from picamera2 import Picamera2
import math
#VARIABLES
THRESHOLD = 10.5      #Any desired value from the accelerometer
REPO_PATH = "/home/bayareatinkerers/BAT_FlatSat"
FOLDER_PATH = "Images"
#imu and camera initialization
i2c = board.I2C()
accel_gyro = LSM6DS(i2c)
mag = LIS3MDL(i2c)
picam2 = Picamera2()
picam2.configure(picam2.create_still_configuration())
picam2.start()
def git_push():
    """
    This function is complete. Stages, commits, and pushes new images to your GitHub repo.
    """
    try:
        repo = Repo(REPO_PATH)
        origin = repo.remote('origin')
        print('added remote')
        origin.pull()
        print('pulled changes')
        repo.git.add(REPO_PATH + FOLDER_PATH)
        repo.index.commit('New Photo')
        print('made the commit')
        origin.push()
        print('pushed changes')
    except:
        print('Couldn\'t upload to git')
def img_gen(name):
    """
    This function is complete. Generates a new image name.
    Parameters:
        name (str): your name ex. MasonM
    """
    t = time.strftime("_%H%M%S")
    imgname = (f'{REPO_PATH}/{FOLDER_PATH}/{name}{t}.jpg')
    return imgname
def take_photo():
    while True:
        ax, ay, az = accel_gyro.acceleration
        a_mag = math.sqrt(ax**2 + ay**2 + az**2)
        if a_mag < THRESHOLD:
            print (ax, ay, az, a_mag)     
        elif a_mag > THRESHOLD:
           print("trigger detected")
           time.sleep(0.5)
           name = "BAT"
           filename = img_gen(name)
           picam2.capture_file(filename)
           print("Saved:", filename)
           time.sleep(0.5)
def main():
    take_photo()
if __name__ == '__main__':
    main()
