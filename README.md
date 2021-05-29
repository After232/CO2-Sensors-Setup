# SCD30 on Raspberry Pi

This is a guide to installing multiple Sensirion SCD30 air sensors onto a fresh Raspberry Pi 4.

## Interface

Check `pyton` 2

```
import cow
```



## Contents:
* Interface Configuration
* List of things to install via Terminal for setup
* Configuring additional buses
* VNC Server
* Python code
* Connecting Sensors to Breadboard and Raspi


## Interface Configuration


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

[SCD30 pin-out diagram specifications](https://www.sensirion.com/fileadmin/user_upload/customers/sensirion/Dokumente/9.5_CO2/Sensirion_CO2_Sensors_SCD30_Datasheet.pdf)
![SCD30 pin-out diagram](https://raw.githubusercontent.com/After232/co2-sensors-setup/main/Images/SCD30-pinout-diagram.png)




