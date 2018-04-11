#!/usr/bin/env python
# Original code https://www.sunfounder.com/learn/sensor-kit-v2-0-for-raspberry-
#pi-b-plus/lesson-26-ds18b20-temperature-sensor-sensor-kit-v2-0-for-b-plus.html
#Edited by Clayton Byrer to show Farenheight displayed on LCD
#----------------------------------------------------------------
#    Note:
#        ds18b20's data pin must be connected to pin7.
#        replace the 28-XXXXXXXXX as yours.
#----------------------------------------------------------------
import os
import Adafruit_CharLCD as LCD
import socket
import time
ds18b20 = ''
lcd = LCD.Adafruit_CharLCDPlate()
SERVERIP = '10.0.0.43'
n = 0


def setup():
    global ds18b20
    for i in os.listdir('/sys/bus/w1/devices'):
        if i != 'w1_bus_master1':
            ds18b20 = i


def read():
#global ds18b20
    location = '/sys/bus/w1/devices/' + ds18b20 + '/w1_slave'
    tfile = open(location)
    text = tfile.read()
    tfile.close()
    secondline = text.split("\n")[1]
    temperaturedata = secondline.split(" ")[9]
    temperature = float(temperaturedata[2:])
    temperature = temperature / 1000
    farenheight = temperature * 1.8 + 32
    return farenheight


def loop():
    n = 0
    while True:
        if read() != None:
            print (("Current temp \n : %0.3f F" % read()))
            lcd.message("Current temp \n : %0.3f F" % read())
            # original code from Python in a Nutshell 2nd Ed. page 527
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((SERVERIP, 8881))
            print (("%d : Connected to server" % n,))
            data = "'Temp Sensor','n', 'Current temp \n : %0.3f F'" % read()
            sock.sendall(data)
            print ((" Sent:", data))
            sock.close()
            n += 1
            time.sleep(30)


def destroy():
    pass

if __name__ == '__main__':
    try:
        setup()
        loop()
    except KeyboardInterrupt:
        destroy()