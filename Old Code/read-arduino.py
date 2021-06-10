# This code exists for reading SCD30 data from an Arduino.
# It is only used for one sensor and requires an Arduino Uno. 
# This is not applicable to the Raspberry Pi version at all.
# It only exists for reference.

import serial
import datetime 

arduino_port = "/dev/cu.usbmodem14101" # serial port
baud = 9600
recordtime = datetime.datetime.now()
fileName = ("CO2-sensor-readings-" + str(recordtime) + ".csv")
ser = serial.Serial(arduino_port, baud)
print("Connected to Arduino port: " + arduino_port)
file = open(fileName, "a")
print("Created CSV file")

samples = 10
print_labels = True
line = 0 # start at 0 because our header is not real data
while line <= samples:
    # incoming = ser.read(9999)
    # if len(incoming) > 0
    if print_labels:
        if line == 0:
            print("Printing column headers")
            line += 1
        else:
            print("Line " + str(line) + ": writing...")
            line += 1
    # This section displays the data to the terminal
    getData = str(ser.readline())
    # print(getData)
    if line <= 1:
        file = open(fileName, "a") 
        file.write(getData[2:][:-5] + "\n")
        continue
    else:
        timestamp = (str(datetime.datetime.now()) + ",")
    loggedData = timestamp + getData[2:][:-5]
    print(loggedData)

    # This section adds data to the CSV file
    file = open(fileName, "a") 
    file.write(loggedData + "\n")

# # This section displays the data to the terminal
# getData = str(ser.readline())
# loggedData = getData[0:][:-2]
# print(data)

# # This section adds data to the CSV file
# file = open(fileName, "a") 
# file.write(loggedData + "\\n")

print("Logging complete")
file.close()