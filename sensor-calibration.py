import time
from scd30_i2cx import SCD30

# Create object for each sensor
scd30A = SCD30(1)
scd30B = SCD30(5)
scd30C = SCD30(4)

# Set measurement interval. Minimum is 2 seconds.
measureTimeA = 2
measureTimeB = 2
measureTimeC = 2

scd30A.set_measurement_interval(measureTimeA)
scd30A.start_periodic_measurement()
scd30A.set_auto_self_calibration(active=True) # Enables calibration mode
scd30B.set_measurement_interval(measureTimeB)
scd30B.start_periodic_measurement()
scd30B.set_auto_self_calibration(active=True)
scd30C.set_measurement_interval(measureTimeC)
scd30C.start_periodic_measurement()
scd30C.set_auto_self_calibration(active=True)

# Run calibration. Does not record measurements taken here.
while True:
    if scd30A.get_data_ready():
        measurementA = scd30A.read_measurement()
        if measurementA is not None:
            co2a, tempa, rha = measurementA
            print(f"Sensor A: CO2: {co2a:.2f}ppm, temp: {tempa:.2f}'C, rh: {rha:.2f}%")
        time.sleep(measureTimeA)
    else:
        continue

    if scd30B.get_data_ready():
        measurementB = scd30B.read_measurement()
        if measurementB is not None:
            co2b, tempb, rhb = measurementB
            print(f"Sensor B: CO2: {co2b:.2f}ppm, temp: {tempb:.2f}'C, rh: {rhb:.2f}%")
        time.sleep(measurementB)
    else:
        continue

    if scd30C.get_data_ready():
        measurementC = scd30C.read_measurement()
        if measurementC is not None:
            co2c, tempc, rhc = measurementC
            print(f"Sensor C: CO2: {co2c:.2f}ppm, temp: {tempc:.2f}'C, rh: {rhc:.2f}%")
        time.sleep(measurementC)
    else:
        continue


    