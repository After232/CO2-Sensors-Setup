import smbus2
import time
import datetime
from scd30_i2cx import SCD30, SCD30B, SCD30C

bus1 = smbus2.SMBus(1)
bus3 = smbus2.SMBus(3) #Aditional 12c bus, configured in config.txt
bus4 = smbus2.SMBus(4) #Aditional 12c bus, configured in config.txt
address = 61

recordtime = datetime.datetime.now()

# CSV File Creation
fileNameA = ("CO2-sensor-A-readings-" + str(recordtime) + ".csv")
fileA = open(fileNameA, "a")
print("Created CSV file for Sensor A")
# fileNameB = ("CO2-sensor-B-readings-" + str(recordtime) + ".csv")
# fileB = open(fileNameB, "a")
# print("Created CSV file for Sensor B")
# fileNameC = ("CO2-sensor-C-readings-" + str(recordtime) + ".csv")
# fileC = open(fileNameC, "a")
# print("Created CSV file for Sensor C")

scd30A = SCD30()
scd30B = SCD30B()
scd30C = SCD30C()

measureTimeA = 2
measureTimeB = 15
measureTimeC = 15

scd30A.set_measurement_interval(measureTimeA)
scd30A.start_periodic_measurement()

print_labels = True
lineA = 0 # start at 0 because our header is not real data
time.sleep(2)

while True:
    if lineA == 0:
        print("Printing column headers")
        timestampA = "Time,"
        getDataA = "CO2 (ppm), Temp (C), Humidity (%),"
        lineA += 1
    else:
        timestampA = (str(datetime.datetime.now())[0:-7] + ",")
        if scd30A.get_data_ready():        
            m = scd30A.read_measurement()
            if m is not None:
                getDataA = (f"{m[0]:.2f}, {m[1]:.2f}, {m[2]:.2f}")
                print("Line " + str(lineA) + " of Sensor A: writing...")
                lineA += 1
            time.sleep(measureTimeA)
        else:
            continue
    loggedData = timestampA + getDataA
    print(loggedData)
    fileA = open(fileNameA, "a")
    fileA.write(loggedData + "\n")


