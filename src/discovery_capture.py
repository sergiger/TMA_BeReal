import os
import time

while True:
    os.system("adb shell input swipe 750 1500 300 300")
    time.sleep(2.5)