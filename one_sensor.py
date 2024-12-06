#!/usr/bin/python

import serial
import time

serial = serial.Serial('COM5', 9600)

start_time = time.time() * 1000
handshake = "hello".encode('utf-8')
serial.write(handshake)
delay = 0
timestamp = 0
while True:
    read = serial.readline().decode('utf-8').split(' ', 1)
    if read[0] == "Timestamp":
        delay = (time.time() * 1000 - start_time) / 2
        timestamp = int(read[1])
        break
    print("waiting for handshake")

print("handshake complete\ndelay: ", delay, "\ntimestamp: ", timestamp)