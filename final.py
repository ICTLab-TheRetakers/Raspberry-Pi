#!/usr/bin/env python

import simplejson as json
import time
import grovepi
import math
import datetime;
import urllib.request, urllib.parse
import datetime;
import requests
# Connect the Grove Light Sensor to analog port A0
# SIG,NC,VCC,GND
light_sensor = 0
sound_sensor = 1
dhtsensor = 4

header_content = {'Content-type': 'application/json'} 

# Connect the LED to digital port D4
# SIG,NC,VCC,GND
led = 4

# Turn on LED once sensor exceeds threshold resistance
threshold = 10

grovepi.pinMode(sound_sensor,"INPUT")
grovepi.pinMode(light_sensor,"INPUT")
grovepi.pinMode(led,"OUTPUT")

threshold_value = 400
# temp_humidity_sensor_type
# Grove Base Kit comes with the blue sensor.
blue = 0    # The Blue colored sensor.
white = 1   # The White colored sensor.

while True:
    try:
        # Get sensor values
        lightsensor_value = grovepi.analogRead(light_sensor)
        soundsensor_value = grovepi.analogRead(sound_sensor)
        [temp,humidity] = grovepi.dht(dhtsensor,blue)  
        # Calculate resistance of sensor in K
        resistance = (float)(1023 - lightsensor_value) * 10 / lightsensor_value
        ts = datetime.datetime.now();
        if resistance > threshold:
            # Send HIGH to switch on LED
            grovepi.digitalWrite(led,1)
        else:
            # Send LOW to switch off LED
            grovepi.digitalWrite(led,0)
            
        
        if math.isnan(temp) == False and math.isnan(humidity) == False:
            print("temp = %.02f C humidity =%.02f%%"%(temp, humidity))
            
        LightData= json.dumps({'device_id':'1', 'created_on': ts.strftime("%Y-%m-%dT%H:%M:%S"), 'type': 'light', 'value': lightsensor_value});
        
        SoundData= json.dumps({'device_id':'1', 'created_on': ts.strftime("%Y-%m-%dT%H:%M:%S"), 'type': 'sound', 'value': int(soundsensor_value)});
        ##casting the humidity and temp values to an int
        TempData= json.dumps({'device_id':'1', 'created_on': ts.strftime("%Y-%m-%dT%H:%M:%S"), 'type': 'temp', 'value': int(temp)});
        HumidData= json.dumps({'device_id':'1', 'created_on': ts.strftime("%Y-%m-%dT%H:%M:%S"), 'type': 'humidity', 'value': int(humidity)});
        l = requests.post('http://145.24.222.238/api/readings/create', data = LightData, headers = header_content)
        s = requests.post('http://145.24.222.238/api/readings/create', data = SoundData, headers = header_content)
        t = requests.post('http://145.24.222.238/api/readings/create', data = TempData, headers = header_content)  
        h = requests.post('http://145.24.222.238/api/readings/create', data = HumidData, headers = header_content)

        print("sound_value = %d" %soundsensor_value)
        print("light_value = %d resistance = %.2f" %(lightsensor_value,  resistance))
        time.sleep(3)

    except IOError:
        print ("Error")

