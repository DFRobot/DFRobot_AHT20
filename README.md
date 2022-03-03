# DFRobot_AHT20

* [中文版](./README_CN.md)

This AHT20 temperature & humidity sensor employs digital output and I2C interface, through which users can read the measured temperature and humidity. Based on the AHT20 chip, it offers the following features:
1. Collect ambient temperature, unit Celsius (℃), range -40-85℃, resolution: 0.01, error: ±0.3-±1.6 ℃
2. Collect ambient relative humidity, unit: %RH, range 0-100%RH, resolution 0.024%RH, error: when the temprature is 25 ℃, error range is ±2-±5%RH
3. Use I2C interface, I2C address default to be 0x38
4. uA level sensor, the measured value is up to 200uA.
5. Power supply range 3.3-5V

![产品效果图](./resources/images/SEN0527.png) ![产品效果图](./resources/images/SEN0528.png)

## Product Link（[www.dfrobot.com](www.dfrobot.com)）
    SKU: SEN0527
    SKU: SEN0528

* [Summary](#summary)
* [Installation](#installation)
* [Methods](#methods)
* [Compatibility](#compatibility)
* [History](#history)
* [Credits](#credits)

## Summary
Provide AHT20 sensor with an Arduino library to obtain the temperature and humidity data measured by the sensor. This library boasts the following functions:
1. Get temperature data in Celsius;
2. Get temperature data in Fahrenheit, which is calculated from the data in Celsius;
3. Get humidity data;
4. Reset the sensor and restore its initial status

## Installation

There two methods: 
1. To use this library, first download the library file, paste it into the \Arduino\libraries directory, then open the examples folder and run the demo in the folder.
2. Search the DFRobot_AHT20 library from the Arduino Software Library Manager and download it.

## Methods

```C++

  /**
   * @fn DFRobot_AHT20
   * @brief DFRobot_AHT20 constructor
   * @param wire TwoWire class object reference
   * @return NONE
   */
  DFRobot_AHT20(TwoWire &wire = Wire);
  /**
   * @fn begin
   * @brief Initialize AHT20 sensor
   * @return Init status value
   * @retval  0    Init succeeded
   * @retval  1    _pWire is NULL, please check if the constructor DFRobot_AHT20 has correctly uploaded a TwoWire class object reference
   * @retval  2    Device is not found, please check if the connection is correct
   * @retval  3    If the sensor init fails, please check if there is any problem with the sensor, you can call the reset function and re-initialize after restoring the sensor
   */
  uint8_t begin();
  /**
   * @fn reset
   * @brief Sensor soft reset, restore the sensor to the initial status.
   * @return NONE
   */
  void reset();
  /**
   * @fn startMeasurementReady
   * @brief Start measurement and determine if it’s completed.
   * @param crcEn Whether to enable check during measurement
   * @n     false  Measure without check (by default)
   * @n     true   Measure with check
   * @return Whether the measurement is done
   * @retval true  If the measurement is completed, call a related function such as get* to obtain the measured data.
   * @retval false If the measurement failed, the obtained data is the data of last measurement or the initial value 0 if the related function such as get* is called at this time.
   */
  bool startMeasurementReady(bool crcEn = false);
  /**
   * @fn getTemperature_F
   * @brief Get ambient temperature, unit: Fahrenheit (F).
   * @return Temperature in F
   * @note  AHT20 can't directly get the temp in F, the temp in F is calculated according to the algorithm: F = C x 1.8 + 32
   * @n Users must call the startMeasurementReady function once before calling the function to start the measurement so as to get the real-time measured data,
   * @n otherwise what they obtained is the initial data or the data of last measurement.
   */
  float getTemperature_F();
  /**
   * @fn getTemperature_C
   * @brief Get ambient temperature, unit: Celsius (℃).
   * @return Temperature in ℃, it's normal data within the range of -40-85℃, otherwise it's wrong data
   * @note Users must call the startMeasurementReady function once before calling the function to start the measurement so as to get the real-time measured data,
   * @n otherwise what they obtained is the initial data or the data of last measurement.
   */
  float getTemperature_C();
  /**
   * @fn getHumidity_RH
   * @brief Get ambient relative humidity, unit: %RH.
   * @return Relative humidity, range 0-100
   * @note Users must call the startMeasurementReady function once before calling the function to start the measurement so as to get the real-time measured data,
   * @n otherwise what they obtained is the initial data or the data of last measurement
   */
  float getHumidity_RH();
```
## Compatibility

MCU                |  Work Well    | Work Wrong   | Untested    | Remarks
------------------ | :----------: | :----------: | :---------: | -----
Arduino Uno        |       √       |              |             | 
Mega2560           |      √       |              |             | 
Leonardo           |      √       |              |             | 
ESP32              |      √       |              |             | 
ESP8266            |      √       |              |             | 
micro:bit          |      √       |              |             | 
FireBeetle M0      |      √       |              |             | 

## History

- 2022/02/09 - Version 0.1 released.

## Credits

Written by Arya(xue.peng@dfrobot.com), 2022. (Welcome to our [website](https://www.dfrobot.com/))

