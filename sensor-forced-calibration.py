import time
from scd30_i2cx import SCD30

# Create object for each sensor
scd30A = SCD30(1)

# Set measurement interval. Minimum is 2 seconds.
measureTimeA = 2

scd30A.set_measurement_interval(measureTimeA)
scd30A.forced_recalibration_reference()
scd30A.start_periodic_measurement()
scd30A.set_auto_self_calibration(active=True)