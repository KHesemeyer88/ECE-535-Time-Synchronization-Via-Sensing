#!/usr/bin/python
import serial # type: ignore
import time
import numpy as np
import matplotlib.pyplot as plt

# serial1 = serial.Serial('/dev/ttyUSB0', 9600)
# serial2 = serial.Serial('/dev/ttyUSB1', 9600)
esp1_ser = serial.Serial('COM8', 9600)
esp2_ser = serial.Serial('COM10', 9600)


esp1_events = []
esp2_events = []
esp1_timeline = np.array([])
esp2_timeline = np.array([])
offset_espToEsp = np.array([])
event1_happened = False
event2_happened = False
start_time = time.time() * 1000
handshake = "hello".encode('utf-8')
esp1_ser.write(handshake)
esp2_ser.write(handshake)
delay1 = 0
delay2 = 0
timestamp1 = 0
timestamp2 = 0
offset = 0
hs1 = False
hs2 = False
while not (hs1 and hs2):
    read1 = esp1_ser.readline().decode('utf-8').split(' ', 1)
    read2 = esp2_ser.readline().decode('utf-8').split(' ', 1)
    if read1[0] == "Timestamp":
        delay1 = (time.time() * 1000 - start_time) / 2
        timestamp1 = int(read1[1])
        hs1 = True
    if read2[0] == "Timestamp":
        delay2 = (time.time() * 1000 - start_time) / 2
        timestamp2 = int(read2[1])
        hs2 = True
    print("waiting for handshake")

print("Handshake complete\ndelay1: ", delay1, "\ndelay2: ", delay2)


# Run for 30 seconds
while True:
    # ----- Read serial data from ESP32 Things -----
    esp1_data = esp1_ser.readline().decode('utf-8').strip().split(' ')
    esp2_data = esp2_ser.readline().decode('utf-8').strip().split(' ')
    esp1_timeline = np.append(esp1_timeline, int(esp1_data[len(esp1_data) - 2]))
    esp2_timeline = np.append(esp2_timeline, int(esp2_data[len(esp2_data) - 2]))
 
    # ----- synchronize -----
    
    # plot synhronized times against un synchronized times
    

    # ----- Get offset & log events-----
    offset_espToEsp = np.append(offset_espToEsp, (esp1_timeline[int(len(esp1_timeline)-1)]) - int(esp2_timeline[int(len(esp2_timeline)-1)]))

    if esp1_data[0] == "Event":
        esp1_events.append(esp1_data[2])
        event2_happened = True
        print("event1")
    if esp2_data[0] == "Event": 
        esp2_events.append(esp2_data[2])
        event1_happened = True
        print("event2")


    # ----- calculate drift -----
    if event1_happened and event2_happened:
        #define data
        x = np.array(esp1_timeline)
        y = np.array(offset_espToEsp)

        #find line of best fit
        a, b = np.polyfit(x, y, 1)

        #add points to plot
        plt.scatter(x, y)

        #add line of best fit to plot
        plt.plot(x, a*x+b)
        plt.show()

        event1_happened = False
        event2_happened = False
