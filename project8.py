#!/usr/bin/python
import serial  # type: ignore
import time

# serial1 = serial.Serial('/dev/ttyUSB0', 9600)
# serial2 = serial.Serial('/dev/ttyUSB1', 9600)
esp1_ser = serial.Serial('COM8', 9600)
#esp2_ser = serial.Serial('COM10', 9600)


i = 0
esp1_events = []
esp2_events = []

# Run for 30 seconds
while i < 30000:
    # Read serial data from ESP32 Things
    esp1_data = esp1_ser.readline().decode('utf-8').strip().split(' ')
    #esp2_data = esp2_ser.readline().decode('utf-8').strip().split(' ')

    if esp1_data[0] == "Event":
        # events[eventIndex]                  = (distance,     timestamp)
        #event_number = int(esp1_data[1] [1:-1])
        esp1_events.append(esp1_data[2])
    print(esp1_events)
    # if esp2_data[0] == "Event"
    #     esp2_events[esp2_data[2] [1:-1]] = (esp1_data[4], esp1_data[6])