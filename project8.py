#!/usr/bin/python
import serial # type: ignore
import time
import numpy as np
import matplotlib.pyplot as plt
import statistics

# serial1 = serial.Serial('/dev/ttyUSB0', 9600)
# serial2 = serial.Serial('/dev/ttyUSB1', 9600)
esp1_ser = serial.Serial('COM8', 9600)
esp2_ser = serial.Serial('COM10', 9600)


esp1_events = []
esp2_events = []
esp1_timeline = np.array([])
esp2_timeline = np.array([])
esp2_time_sync = np.array([])
sync_start_index = -1
esp1_distance = np.array([])
esp2_distance = np.array([])
offset_espToEsp = np.array([])
offset_times = np.array([])
event1_happened = False
event2_happened = False
delay1 = 0
delay2 = 0
hs1 = False
hs2 = False
i = 0


start_time = time.time() * 1000
handshake = "hello".encode('utf-8')
esp1_ser.write(handshake)
esp2_ser.write(handshake)
while not (hs1 and hs2):
    read1 = esp1_ser.readline().decode('utf-8').split(' ', 1)
    read2 = esp2_ser.readline().decode('utf-8').split(' ', 1)
    if read1[0] == "Timestamp":
        delay1 = (time.time() * 1000 - start_time) / 2
        hs1 = True
    if read2[0] == "Timestamp":
        delay2 = (time.time() * 1000 - start_time) / 2
        hs2 = True
    print("waiting for handshake")
print("Handshake complete\ndelay1: ", delay1, "\ndelay2: ", delay2)


while i < 2500:
    # ----- Read serial data from ESP32 Things -----
    esp1_data = esp1_ser.readline().decode('utf-8').strip().split(' ')
    esp2_data = esp2_ser.readline().decode('utf-8').strip().split(' ')

    # Record all timestamps
    esp1_timeline = np.append(esp1_timeline, int(esp1_data[-2]))
    esp2_timeline = np.append(esp2_timeline, int(esp2_data[-2]))

    # Record all distance for graph
    esp1_distance = np.append(esp1_distance, int(esp1_data[-1]))
    esp2_distance = np.append(esp2_distance, int(esp2_data[-1]))


    # ----- synchronize esp2 time -----
    if len(offset_espToEsp) > 1:
        if sync_start_index == -1:
            sync_start_index = len(esp1_timeline) - 1
        x = np.array(offset_times)
        y = np.array(offset_espToEsp)
        a, b = np.polyfit(x, y, 1)
        esp2_time_sync = np.append(esp2_time_sync, esp2_timeline[-1] * a + (sum(offset_espToEsp)/len(offset_espToEsp)) + esp2_timeline[-1])

    # ----- Get offset & log events-----
    
    # Array of timestamps for each event
    if esp1_data[0] == "Event":
        esp1_events.append(esp1_data[2])
        event2_happened = True
        print("event1")
    if esp2_data[0] == "Event": 
        esp2_events.append(esp2_data[2])
        event1_happened = True
        print("event2")

    # ----- calculate drift -----
    # Both events
    if event1_happened and event2_happened:
        # time of event 1 for esp1 - time of event 1 for esp2 = offset
        offset_espToEsp = np.append(offset_espToEsp, float(esp1_events[-1]) - float(esp2_events[-1]))
        # offset_espToEsp = np.append(offset_espToEsp, (float(esp1_timeline[len(esp1_timeline)-2]) - float(esp2_timeline[len(esp2_timeline)-2])) / 1000000.0)
        offset_times = np.append(offset_times, float(esp1_events[-1]))
        
        event1_happened = False
        event2_happened = False
    i = i + 1


# ----- Print graphs -----
# Esp-esp offset
x = np.array(offset_times)
y = np.array(offset_espToEsp)
plt.title("Esp-Esp Offset vs. Time", fontsize = 20)
plt.xlabel("ESP1 Timeline (us)")
plt.ylabel("Offset (us)")
#find line of best fit
a, b = np.polyfit(x, y, 1)
print("DRIFT: ", a)
#add points to plot
plt.scatter(x, y)
# add line of best fit to plot
plt.plot(x, a*x+b)
plt.show()



# synced esp2 time
x1 = np.linspace(min(esp2_timeline[0], esp1_timeline[0]), max(esp1_timeline[-1], esp2_timeline[-1]), len(esp2_time_sync))
y1 = np.array(esp2_time_sync)
y2 = np.array(esp1_timeline[sync_start_index:])
y3 = np.array(esp2_timeline[sync_start_index:])
plt.plot(x1, y1, color='b', label = "Synced ESP2 Time")
plt.plot(x1, y2, color='g', label = "ESP1 Time") 
plt.plot(x1, y3, color='r', label = "ESP2 Time")
plt.title("Comparing Raw and Synchronized Timestamps", fontsize = 20)
plt.xlabel("Time (us)")
plt.ylabel("Time (us)")
# plt.ylabel("microseconds")
plt.legend()
plt.show()

# esp1 distance events
x = np.array(esp1_timeline)
y = np.array(esp1_distance)
plt.title("Esp1 Event Detection", fontsize = 20)
plt.xlabel("Esp1 Time (us)")
plt.ylabel("Distance (cm)")
plt.plot(x, y, label = "Distance Reported")
plt.plot(x, [15] * len(x), color='r', linestyle='--', label = "Event Threshold ")
plt.legend()
plt.show()

# esp2 distance events
x = np.array(esp2_timeline)
y = np.array(esp2_distance)
plt.title("ESP2 Event Detection", fontsize = 20)
plt.xlabel("ESP2 Time (us)")
plt.ylabel("Distance (cm)")
plt.plot(x, y, label = "Distance Reported")
plt.plot(x, [15] * len(x), color='r', linestyle='--', label = "Event Threshold")
plt.legend()
plt.show()
