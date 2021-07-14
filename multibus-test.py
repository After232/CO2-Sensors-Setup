# import smbus2
# import time
# import datetime

# bus1 = smbus2.SMBus(1) # A
# bus5 = smbus2.SMBus(5) # B
# bus4 = smbus2.SMBus(4) # C

# address = 0x61

# bus1.write_i2c_block_data(address, )

import smbus2
from scd30_i2cx import SCD30

# Create object for each sensor
scd30A = SCD30(1)
scd30B = SCD30(5)
scd30C = SCD30(4)
print(scd30A.__dict__)
print('---')
print(scd30B.__dict__)
print('---')
print(scd30C.__dict__)