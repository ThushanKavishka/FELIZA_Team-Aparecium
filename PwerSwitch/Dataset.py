import RPi.GPIO as GPIO
import time
import os
import subprocess

GPIO.setmode(GPIO.BCM)
#using GPIO number 10
GPIO.setup(10, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

while True:
        if GPIO.input(10)==1:
                subprocess.call("python /home/pi/Main/datasetCreator.py", shell=True)
                time.sleep(0.2)
