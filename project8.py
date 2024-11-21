#!/usr/bin/python

import serial
import time

serial1 = serial.Serial('/dev/ttyUSB0', 9600)
serial2 = serial.Serial('/dev/ttyUSB1', 9600)
# serial1 = serial.Serial('COM8', 9600)
# serial2 = serial.Serial('COM10', 9600)


i = 0
threshold = 10
timeline1 = []
timeline2 = []
drift1 = []
drift2 = []
relativeDrift = []
event1 = False
event2 = False
events = []
eventIndex = 0
offset1 = 0
offset2 = 0

# Run for 30 seconds
while i < 30000:
    # Read serial data from ESP32 Things
    piTime = round(time.time() * 1000)
    esp32Thing1 = serial1.readline()
    esp32Thing2 = serial2.readline()
    data1 = esp32Thing1.decode('utf-8').split(' ', 1).append(piTime)
    data2 = esp32Thing2.decode('utf-8').split(' ', 1).append(piTime)
    #   timestamp(esp32)[0], distance[1], timestamp(pi)[2]
    
    # Save serial from each
    timeline1.append(data1)
    timeline2.append(data2)
    
    # wait until there is a previous timestamp to reference
    if i > 0:

        # Even happens on sensor 1
        if timeline1[i-1][1] > threshold & timeline1[i][1] < threshold:
            event1 = True
            eventIndex = eventIndex + 1

            if (event2):
            # Both see event
                events[eventIndex].append(data1)
                eventIndex = eventIndex + 1
            else:
                events.append(data1)
            
        # Even happens on sensor 2
        if timeline2[i-1][1] > threshold & timeline2[i][1] < threshold:
            event2 = True
            eventIndex = eventIndex + 1

            # Both see event
            if (event1):
                events[eventIndex].append(data2)
                
                eventIndex = eventIndex + 1
            else:
                events.append(data2)
                

            
        # Drift calculation
        drift1.append(timeline1[i][0] - timeline1[i-1][0] - 1)
        drift2.append(timeline2[i][0] - timeline2[i-1][0] - 1)
        relativeDrift.append(drift1 - drift2)

        # delay calcualation ?
        

    # serial output
    print(data1[0] + " " + data1[1])
    print(data2[0] + " " + data2[1])

    
    i = i + 1
    time.delay(0.01)