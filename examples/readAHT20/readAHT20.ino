/*!
 * @file readAHT20.ino
 * @brief AHT20 is used to read the temperature and humidity of the current environment. 
 *
 * @copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
 * @license     The MIT License (MIT)
 * @author [Arya](xue.peng@dfrobot.com)
 * @version  V1.0
 * @date  2022-02-08
 * @url https://github.com/DFRobot/DFRobot_AHT20
 */

#include "DFRobot_AHT20.h"

DFRobot_AHT20 aht20;

void setup(){
  Serial.begin(115200);

  while(!Serial){
    //Wait for USB serial port to connect. Needed for native USB port only
  }
  
  /**
   * @fn begin
   * @brief Initialize AHT20 sensor
   * @return Init status value
   * @n      0    Init succeeded
   * @n      1    _pWire is NULL, please check if the constructor DFRobot_AHT20 has correctly uploaded a TwoWire class object reference
   * @n      2    Device not found, please check if the connection is correct
   * @n      3    If the sensor init fails, please check if there is any problem with the sensor, you can call the reset function and re-initialize after restoring the sensor
   */
  uint8_t status;
  while((status = aht20.begin()) != 0){
    Serial.print("AHT20 sensor initialization failed. error status : ");
    Serial.println(status);
    delay(1000);
  }

}

void loop(){
  /**
   * @fn startMeasurementReady
   * @brief Start measurement and determine if it's completed.
   * @param crcEn Whether to enable check during measurement
   * @n     false  Measure without check (by default)
   * @n     true   Measure with check
   * @return Whether the measurement is done
   * @n     true  If the measurement is completed, call a related function such as get* to obtain the measured data.
   * @n     false If the measurement failed, the obtained data is the data of last measurement or the initial value 0 if the related function such as get* is called at this time.
   */
  if(aht20.startMeasurementReady(/* crcEn = */true)){
    Serial.print("temperature(-40~85 C): ");
    // Get temp in Celsius (℃), range -40-80℃
    Serial.print(aht20.getTemperature_C());
    Serial.print(" C, ");
    // Get temp in Fahrenheit (F)
    Serial.print(aht20.getTemperature_F());
    Serial.print(" F\t");
    Serial.print("humidity(0~100): ");
    // Get relative humidity (%RH), range 0-100℃
    Serial.print(aht20.getHumidity_RH());
    Serial.println(" %RH");
    delay(1000);
  }
}
