import RPi.GPIO as GPIO
import time
import os
import subprocess

GPIO.setmode(GPIO.BCM)
#using GPIO number 4
GPIO.setup(4, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
#using GPIO number 3
GPIO.setup(3, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
#using GPIO number 2
GPIO.setup(2, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)


while True:
        if ( GPIO.input(4) == True):
                        subprocess.call("python /home/pi/Main/detector.py", shell=True)
                        time.sleep(0.2)
        if ( GPIO.input(3) == True):
                        subprocess.call("python /home/pi/Main/datasetCreator.py", shell=True)
                        time.sleep(0.2)
