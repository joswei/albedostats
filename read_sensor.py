#!/usr/bin/env python

# Source code adapted from http://www.perrygeo.com/
#        raspberry-pi-real-time-sensor-plots-with-websocketd.html
# To run, use command $ sudo python read_sensor.py
 
# import RPi.GPIO as GPIO, time, os      
import time, os
import datetime
import pytz
from sys import stdout
import serial
import random

# Establish serial connection
# TODO: find port name for Arduino. (for now, /dev/ttyACM0 is used)
# source of help: https://raspberrypi.stackexchange.com/questions/
#                 12246/why-does-usb-port-enumeration-change
# ser = serial.Serial('/dev/ttyACM0', 9600)
ser = False
 
DEBUG = 1
 
def readSensorValue ():
    # Read from Serial, and use strip() to remove \r\n, then convert to float
    if (ser):
        reading = float(ser.readline().strip())
        return reading

    else:
        return -1
 
def bars(x, scale=0.01):
    return "#" * int(scale * x)    

def stopAudio():
    os.system('pkill mpg123 &')
    return

def playAudio(trackNumber):
    stopAudio()
    if (trackNumber == 1):
        os.system('mpg123 -q audio/windchimes.mp3 &')
    elif (trackNumber == 2):
        os.system('mpg123 -q audio/water-dripping.mp3 &')
    else:
        os.system('mpg123 -q audio/river.mp3 &')
    return

def adjustAudio(reading, trackNumber):
    if (reading > 0.65):
        newTrackNumber = 1
        # cold, high albedo
    elif ((reading <= 0.65) & (reading > 0.1)):
        newTrackNumber = 2
        # water dripping when albedo moderate
    else:
        newTrackNumber = 3
        # do default for low albedo

    if (newTrackNumber == trackNumber):
        return trackNumber
    else:
        playAudio(newTrackNumber)
        time.sleep(1)
        return newTrackNumber
   
def to_unix_timestamp(ts):
    """
    Get the unix timestamp (seconds from Unix epoch) 
    from a datetime object
    """
    start = datetime.datetime(year=1970, month=1, day=1)
    diff = ts - start
    return diff.total_seconds()


if __name__ == "__main__":

    trackNumber = 1
    while True:                                     
         reading = readSensorValue()
         reading = round(reading, 2)
         if (reading == -1):
             reading = random.random()
             reading = round(reading, 2)
         n = datetime.datetime.now()
         timestamp = to_unix_timestamp(n)
         print("{},{}".format(timestamp, reading))
         # Flush the output to stdout after every reading to make sure 
         # output isn't buffered
         time.sleep(0.5)
         stdout.flush()
#         trackNumber = adjustAudio(reading, trackNumber)