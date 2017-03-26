import RPi.GPIO as GPIO
import time
import os
import subprocess

GPIO.setmode(GPIO.BCM)
#using GPIO number 4
GPIO.setup(4, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

while True:
        input_state = GPIO.input(4)
        if input_state == True:
                subprocess.call("python /home/pi/Main/detector.py", shell=True)
                time.sleep(0.2)
                
                
