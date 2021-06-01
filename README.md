# SCD30 on Raspberry Pi
This is a guide to installing multiple Sensirion SCD30 air sensors onto a fresh Raspberry Pi 4.


## Contents:
* List of things to install via Terminal for setup
* Configuring additional buses
* Connecting Sensors to Breadboard and Raspi
* Python program to collect data


## List of things to install via Terminal for setup
Before you install anything, you need to set up the interfacing options on your Raspi. Go to the Raspberry Pi menu, under Preferences open Raspberry Pi Configuration and select Interfacing Options. Enable SSH, SPI, I2C and Serial. You can also enable VNC (for remote access) if you want. Restart your Raspi after enabling all of these.

Open a new Terminal window and enter all of the following lines of commands, in order and separately, to ensure that all the necessary packages are installed.

```
sudo apt-get update
sudo apt-get install -y python-smbus
sudo apt-get install -y i2c-tools
python -m pip install pyserial
python -m pip install scd30-i2c
python -m pip install smbus2
```
Restart the Raspi after all of this is done.

## Configuring additional buses
Because we're using multiple of the same I2C sensor, we need to create different addresses for each one to resolve conflicts. Otherwise, all three sensors will share the same address and you will have no idea which sensor is outputting the data.

First, open Terminal and enter:
```
sudo i2cdetect -l
```

You should only be seeing one item listed back, which should look something like this:
```
i2c-1	i2c       	bcm2835 (i2c@7e804000)          	I2C adapter
```

This is your main bus. If you run `sudo i2cdetect -y 1`, you will get a grid view of all the possible addresses in your bus. If nothing is connected to the GPIO pins, all addresses will show a `--` in them. Currently, all sensors get sent to this bus, so multiples of the same sensor will have the same address.

To add more buses, open a new Terminal window and enter:
```
cd /boot/
```
Then, enter:
```
sudo nano config.txt
```
This will open the config.txt file in Nano. Scroll down to the part which reads as follows:
```
dtparam=i2c_arm=on
#dtparam=i2s=on
dtparam=spi=on
```
Directly underneath, add these two lines:
```
dtoverlay=i2c-gpio,bus=4,i2c_gpio_delay_us=1,i2c_gpio_sda=23,i2c_gpio_scl=24
dtoverlay=i2c-gpio,bus=3,i2c_gpio_delay_us=1,i2c_gpio_sda=17,i2c_gpio_scl=27
```
Once done, press Control + X, then press Y, then press Enter. This will save and exit the config.txt.

Run `sudo i2cdetect -l` again. You should now see two extra I2C buses in the list. They will be named `i2c-3` and `i2c-4` respectively. These are the new buses that have just been added and they will allow you to have multiple of the same sensor without conflicting addresses.

## Connecting Sensors to Breadboard and Raspi
This part will only work if the above has been done properly. Below are the SCD30's pin guide and the Raspi pin guide. For the breadboard, you only really need the power rails (+) and (-). 

![SCD30 pin-out diagram](https://github.com/After232/co2-sensors-setup/blob/6d38d68f50b40f1db14479c7cd1ad5902f2c5f42/Images/SCD30-pinout-diagram.png)

The pins that matter to us on the SCD30 are VDD, GND, SCL, SDA and SEL. The rest can be left unconnected. As we have three sensors, we can give each of them a label (such as Sensor A, Sensor B and Sensor C) to help differentiate between them.

The pinout diagram for Raspi can be [found here](https://pinout.xyz/#).

Make sure that the Raspi is **turned off** before any connections are made. This is to prevent short-circuit issues. Once everything is clear, do the following connections in order:
1. Raspi pin 1 (3v3 power) to the anode (+) power rail of the breadboard.
2. Raspi pin 6 (ground) to the cathode (-) power rail of the breadboard, adjacent to the previous connection.
3. On Sensor A, connect VDD to the anode (+) power rail of the breadboard, parallel to the Raspi's 3v3 power connection.
4. On Sensor A, connect GND to the cathode (-) power rail of the breadboard, adjacent to the previous connection.
5. Repeat steps 3-4 for Sensor B and Sensor C.
6. Connect Raspi pin 3 (GPIO 2) to SDA on Sensor A.
7. Connect Raspi pin 5 (GPIO 3) to SCL on Sensor A.
8. Connect Raspi pin 6 (ground) to SEL on Sensor A.
6. Connect Raspi pin 11 (GPIO 17) to SDA on Sensor B.
7. Connect Raspi pin 13 (GPIO 27) to SCL on Sensor B.
8. Connect Raspi pin 14 (ground) to SEL on Sensor B.
6. Connect Raspi pin 16 (GPIO 23) to SDA on Sensor C.
7. Connect Raspi pin 18 (GPIO 24) to SCL on Sensor C.
8. Connect Raspi pin 20 (ground) to SEL on Sensor C.

![Breadboard connections](https://github.com/After232/co2-sensors-setup/blob/main/Images/Breadboard%20Connections.jpg)

Check that all the connections are correct. When you turn on your Raspi, open Terminal and enter `sudo i2cdetect -y 1`. This will check Sensor A's address, and you will see a grid of connections with most being labelled as `--`. The address that is not `--` is the address for the SCD30 sensor. Take note of this address for later.
The format for reading addresses is `columnxrow`, which means that if your address is in the column 1 and row 60 (displaying as address 61), your address is `1x60`.

**Troubleshooting:** Occasionally, there may be a case where every single address shows up (the entire grid has numbers and no `--`). This usually means that one of your SDA pins is incorrectly connected. Check your pinout connections again and run `sudo i2cdetect -y #` again with # being the bus where all addresses are being displayed.

In the event that *no* addresses are showing, check the sensor to see if it is periodically blinking. If the sensor is not blinking, there may be an issue with power. Check if your voltage and ground are connected correctly, and verify that nothing has short circuited. If the sensor is blinking and there are no visible addresses still, you may have either connected the pins wrongly or your SEL pin is not connected properly.

## Python Program to Collect Data
The final step is to use the program to collect data. Download the file `read-3-sensors.py` from this repository. Before running it, open the file in a text editor or IDE and change the address in line 10 (`address = 0x60`) to the one that is visible on your Raspi. Afterwards, save and exit the text editor/IDE.

Open a terminal window when all three sensors are plugged in and blinking. Use command line tools such as `ls` and `cd` to navigate to the directory of the python program. Run `python read-3-sensors.py` to initiate the program. This will start compiling the data collected from the three sensors into three separate^ CSV files. The files will show the exact time (according to the Raspi's configuration), the CO2 content in ppm, the temperature in °C and the relative humidity in %.

The program is made to run indefinitely until halted by user input. To end the program, click on the terminal window and press Control + C. This will finish exporting the CSVs. 



^The issue with compiling all three sensors' data in the same file is because, although they all record at 2 second intervals, their start times may be different, which can result in data becoming conflicted and outputting the wrong data to the wrong sensor's columns.
