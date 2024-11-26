#!/usr/bin/python

import serial
import time

serial1 = serial.Serial('/dev/ttyUSB0', 9600)
serial2 = serial.Serial('/dev/ttyUSB1', 9600)
# serial1 = serial.Serial('COM8', 9600)
# serial2 = serial.Serial('COM10', 9600)


i = 0
threshold = 10
raw_timeline1 = []
raw_timeline2 = []
sync_timeline1 = []
sync_timeline2 = []
drift1 = []
drift2 = []
relativeDrift = []
event1 = False
event2 = False
events = []
eventIndex = 0
offset1 = 0
offset2 = 0


# delay calcualation
    #1. esp32 things waits
    #2. raspberry pi timestamps(1), then sends handshake
    #3. esp32 recives handshake, timestamps(2)
    #4. timestamps(3) ,esp32 sends acknowledgement 
    #5. raspberryy pi receives ack, timestamps(4)
    #6. 

# Handshake
start_time = time.time() * 1000
handshake = b'\x01'
serial1.write(handshake)
serial2.write(handshake)
hs1 = False
hs2 = False
delay1 = 0
delay2 = 0
while hs1 == False | hs2 == False:
    if serial1.readline().decode('utf-8').split(' ', 1)[0] == "Timestamp":
        delay1 = (time.time() * 1000 - start_time) / 2
        hs1 = True
    if serial2.readline().decode('utf-8').split(' ', 1)[0] == "Timestamp":
        delay2 = (time.time() * 1000 - start_time) / 2
        hs2 = True

# Run for 30 seconds
while i < 30000:
    # Read serial data from ESP32 Things
    piTime = round(time.time() * 1000)
    esp32Thing1 = serial1.readline()
    esp32Thing2 = serial2.readline()
    data1 = esp32Thing1.decode('utf-8').split(' ', 1).append(piTime)
    data2 = esp32Thing2.decode('utf-8').split(' ', 1).append(piTime)
    #   timestamp(esp32)[0], distance[1], timestamp(pi)[2]

    
    # Save raw serial from each
    raw_timeline1.append(data1)
    raw_timeline2.append(data2)

    # Apply offsets
    data1[0] = data1[0] - offset1
    data2[0] = data2[0] - offset2
    
    # Save synchronized serial from each
    sync_timeline1.append(data1)
    sync_timeline2.append(data2)
    
    # wait until there is a previous timestamp to reference
    if i > 0:

        # Even happens on sensor 1
        if raw_timeline1[i-1][1] > threshold & raw_timeline1[i][1] < threshold:
            event1 = True
            eventIndex = eventIndex + 1

            if (event2):
                # Both see event
                events[eventIndex].append(raw_timeline1[i][0])
                eventIndex = eventIndex + 1
                event1 = False
                event2 = False
                offset1 = events[eventIndex][3] - events[eventIndex][0]
                offset2 = 0
            else:
                events.append(data1)
            
        # Even happens on sensor 2
        if raw_timeline2[i-1][1] > threshold & raw_timeline2[i][1] < threshold:
            event2 = True
            eventIndex = eventIndex + 1

            if (event1):
                # Both see event
                events[eventIndex].append(raw_timeline2[i][0])
                eventIndex = eventIndex + 1
                event1= False
                event2= False
                offset1 = 0
                offset2 = events[eventIndex][3] - events[eventIndex][0]
            else:
                events.append(data2)
                

            
        # Drift calculation
        drift1.append(raw_timeline1[i][0] - raw_timeline1[i-1][0] - 1)
        drift2.append(raw_timeline2[i][0] - raw_timeline2[i-1][0] - 1)
        relativeDrift.append(drift1 - drift2)

       
    # serial output
    print(data1[0] + " " + data1[1])
    print(data2[0] + " " + data2[1])

    
    i = i + 1
    time.delay(0.01)