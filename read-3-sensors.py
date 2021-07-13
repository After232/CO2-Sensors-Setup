import smbus2
import time
import datetime
from scd30_i2cx import SCD30

# Create object for each sensor
scd30A = SCD30(1)
scd30B = SCD30(3)
scd30C = SCD30(4)

# Set measurement interval. Minimum is 2 seconds.
measureTimeA = 2
measureTimeB = 2
measureTimeC = 2

recordtime = datetime.datetime.now()

# CSV File Creation
fileNameA = ("CO2-sensor-A-readings-" + str(recordtime) + ".csv")
fileA = open(fileNameA, "a")
print("Created CSV file for Sensor A")
fileNameB = ("CO2-sensor-B-readings-" + str(recordtime) + ".csv")
fileB = open(fileNameB, "a")
print("Created CSV file for Sensor B")
fileNameC = ("CO2-sensor-C-readings-" + str(recordtime) + ".csv")
fileC = open(fileNameC, "a")
print("Created CSV file for Sensor C")

scd30A.set_measurement_interval(measureTimeA)
scd30A.start_periodic_measurement()
scd30B.set_measurement_interval(measureTimeB)
scd30B.start_periodic_measurement()
scd30C.set_measurement_interval(measureTimeC)
scd30C.start_periodic_measurement()

print_labels = True
lineA = 0 # start at 0 because our header is not real data
lineB = 0
lineC = 0
time.sleep(2)

# Start collection of data
while True:
    # Sensor A 
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
    loggedDataA = timestampA + getDataA
    print(loggedDataA)
    fileA = open(fileNameA, "a")
    fileA.write(loggedDataA + "\n")

    # Sensor B 
    if lineB == 0:
        print("Printing column headers")
        timestampB = "Time,"
        getDataB = "CO2 (ppm), Temp (C), Humidity (%),"
        lineB += 1
    else:
        timestampB = (str(datetime.datetime.now())[0:-7] + ",")
        if scd30B.get_data_ready():        
            n = scd30B.read_measurement()
            if n is not None:
                getDataB = (f"{m[0]:.2f}, {m[1]:.2f}, {m[2]:.2f}")
                print("Line " + str(lineB) + " of Sensor B: writing...")
                lineB += 1
            time.sleep(measureTimeB)
        else:
            continue
    loggedDataB = timestampB + getDataB
    print(loggedDataB)
    fileB = open(fileNameB, "a")
    fileB.write(loggedDataB + "\n")

    # Sensor C 
    if lineC == 0:
        print("Printing column headers")
        timestampC = "Time,"
        getDataC = "CO2 (ppm), Temp (C), Humidity (%),"
        lineC += 1
    else:
        timestampC = (str(datetime.datetime.now())[0:-7] + ",")
        if scd30C.get_data_ready():        
            n = scd30C.read_measurement()
            if n is not None:
                getDataC = (f"{m[0]:.2f}, {m[1]:.2f}, {m[2]:.2f}")
                print("Line " + str(lineC) + " of Sensor C: writing...")
                lineC += 1
            time.sleep(measureTimeC)
        else:
            continue
    loggedDataC = timestampC + getDataC
    print(loggedDataC)
    fileC = open(fileNameC, "a")
    fileC.write(loggedDataC + "\n")
