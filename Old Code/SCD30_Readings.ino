#include <Wire.h>
#include "SparkFun_SCD30_Arduino_Library.h"
//#include "SCD30.h"
//#include "Sensirion_GadgetBle_Lib.h"

//#define SDA_pin A4
//#define SCL_pin A5

SCD30 airSensor;

void setup()
{
  Serial.begin(115200);
  Serial.println("SCD30 Test");
  Wire.begin();
//  delay(100);
  if (airSensor.begin() == false)
  {
    Serial.println("Sensor undetected. Pausing.");
    while(1)
      ;
  }

  airSensor.setMeasurementInterval(2);
}

void loop() {
  if (airSensor.dataAvailable())
  {
    Serial.print("CO2(ppm):");
    Serial.print(airSensor.getCO2());
//
//    Serial.print(" Temperature(C):");
//    Serial.print(airSensor.getTemperature(), 2);
//
//    Serial.print(" Humidity(%):");
//    Serial.print(airSensor.getHumidity(), 2);

    Serial.println();
  }
//  else
//  {
//    Serial.println(".");
//  }
  delay(1);
}
