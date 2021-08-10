import time
from scd30_i2cx import SCD30

# Create object for each sensor
scd30A = SCD30(1)

# Set measurement interval. Minimum is 2 seconds.
measureTimeA = 2

scd30A.set_measurement_interval(measureTimeA)
scd30A.forced_recalibration_reference(400)
scd30A.start_periodic_measurement()

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