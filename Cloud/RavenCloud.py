#!/usr/bin/python
#Scripted by Team Aparecium

import os
import RPi.GPIO as GPIO
import Adafruit_BMP.BMP085 as BMP085   # the pressure and temnperature sensor
import Adafruit_DHT as DHT11           # the DHT11 hunidty and temperature sensor
import smbus
import time
import requests  # HTTP
from time import sleep                 
 
#intitialization of the sensors
sensor = BMP085.BMP085()  # pressure and temperature
sensor2 = DHT11           # humidity and temperature
onewirepin = 24            # the pin for the one wire sensor
sensor1type = "BMP180"    # the type of sensor    
sensor2type = 11          # the type of sensor    


#BMP085 Sensor
sensor = BMP085.BMP085(mode=BMP085.BMP085_ULTRAHIGHRES)
 
#Cloud information(Thingspeak)
thingspeakurl = "https://api.thingspeak.com/update"   # url for sending updates to thingspeak
apikey = "REHOBWG80ORSBC8C"     # thingspeak api address for this channel 
TempField = "field1"            # temperature field
PressField = "field2"           # pressure field
 
# some debug info... here we print the BMP180 cal table
print "Calibration Coefficients read from sensor device "
print "-------------------------------------------------"
print "ac1 ", sensor.cal_AC1
print "ac2 ", sensor.cal_AC2
print "ac3 ", sensor.cal_AC3
print "ac4 ", sensor.cal_AC4 
print "ac5 ", sensor.cal_AC5
print "ac6 ", sensor.cal_AC6
print "b1  ", sensor.cal_B1
print "b2  ", sensor.cal_B2
print "mb  ", sensor.cal_MB
print "mc  ", sensor.cal_MC
print "md  ", sensor.cal_MD
print "--------------------------------------------------"
print " "
 
print "Initial data read to check sensors            "
print "-------------------------------------------------"
print "Time          ", time.ctime()
#print "Epoch Seconds ", time.time()
print " "
temperature = sensor.read_temperature()  # Note: fixed an error in the Adafruit module where it incorrectly divides by 10 
pressure = sensor.read_pressure()
altitude = sensor.read_altitude()
sealevelPressure = sensor.read_sealevel_pressure()
 
print "Data read from Sensor 1              "
print "---------------------------------------------------------"
print "Sensor type", sensor1type
print('Temp = {0:0.2f} *C'.format(sensor.read_temperature()))
print('Pressure = {0:0.2f} Pa'.format(sensor.read_pressure()))
print('Altitude = {0:0.2f} m'.format(sensor.read_altitude()))
print('Sealevel Pressure = {0:0.2f} Pa'.format(sensor.read_sealevel_pressure()))
print " "
 
print "Data read from Sensor 2              "
print "---------------------------------------------------------"
print "Sensor type", sensor2type
humidity2, temperature2 = DHT11.read_retry( sensor2type, onewirepin )
print 'Temperature= {0:0.1f} *C  Humidity= {1:0.1f} %'.format(temperature2,humidity2)
print " "
 
print "----------------------------------------------------------------------------------------------------------------------------------------"
print " Date/Time                   Point    Temp     Temp2   Pressure     Humidity     Altitude      Sealevel      Rain     Carbon     Status "
print "                               #       C         C        mbar          %           m        Pressure(Pa)            Monoxide     Code  "
print "----------------------------------------------------------------------------------------------------------------------------------------"
print " "
time.sleep(2)  # wait for the DHT sensor as it does not like to be accessed faster than every 2 seconds
# Now we enter the min code
 
try:           # wrapper to allow clean exit
    while True:

        #Rain Sensor
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(23, GPIO.IN)
        rain = GPIO.input(23)

        #Rain condition
        if (rain == 0):
            status1 = "Yes"
        else:
            status1 = "No"

            time.sleep(0.5)

        #CO sensor
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(18, GPIO.IN)
        co = GPIO.input(18)

        #Carbon Monoxide Condition
        if (co == 0):
            status2 = "Yes"
        else:
            status2 = "No"

        time.sleep(0.5)
 
        temperature = sensor.read_temperature()
        pressure = sensor.read_pressure()
        altitude = sensor.read_altitude()
        altitude = round(altitude,3)
        sealevelPressure = sensor.read_sealevel_pressure()
        humidity2, temperature2 = DHT11.read_retry( sensor2type, onewirepin )
        humidity2 = round(humidity2,3)
        temperature2 = round(temperature2,3)
       
        time.sleep(0.5)

         
 
        url = thingspeakurl
        payload = {'key' : apikey, 'field1' : temperature , 'field2' : pressure/ 100. , 'field3' : temperature2 ,
                   'field4' : humidity2 , 'field5' : altitude  , 'field6' : sealevelPressure , 'field7' : rain, 'field8' : co} # make the payload
     
        try :
            r = requests.get(url, params=payload)  # send to thingspeak
            print time.ctime(), "  ", r.text, "   ", temperature ,"   ", temperature2 ,"   ", pressure / 100.,"      ", humidity2, "      ",altitude,"      ",sealevelPressure,"      ",status1,"      ",status2,"      ",r.status_code
            #r.text will be the data point number
            #r.status code should be 200 if the page posted correctly
        except requests.exceptions as e :
            print e # some simple error trapping to avoid the program timing out
        except requests.exceptions.ConnectionError as e1 :
            print e1 # some simple error trapping if the connection is lost
     
        time.sleep(15) # thingspeak is set to ignore requests that come faster than every 15 seconds
 
except KeyboardInterrupt:
    time.sleep (0.1)
    print " "
    print "Exiting program due to Keyboard Interrupt"
    print " "
except:
    time.sleep (0.1)
    print " "
    print "An error occurred"
    print " "
 
# end
