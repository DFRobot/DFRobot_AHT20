# -*- coding:utf-8 -*-
from __future__ import print_function


'''!
  @file demo_read_aht20.py
  @brief AHT20 is used to read the temperature and humidity of the current environment.  
  @copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
  @license     The MIT License (MIT)
  @author [Arya](xue.peng@dfrobot.com)
  @version  V1.0
  @date  2022-02-09
  @url https://github.com/DFRobot/DFRobot_AHT20
'''

import sys
import os
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from DFRobot_AHT20 import *

aht20 = DFRobot_AHT20()

if __name__ == "__main__":
  print("Initialization AHT20 Sensor...", end=" ")
  '''!
    @brief   Initialize AHT20 sensor
    @return  Init status value
    @retval True  Init succeeded
    @retval False Init failed
  '''
  while aht20.begin() != True:
    print("failed, please check if the connection is correct?")
    time.sleep(1)
    print("Initialization AHT20 Sensor...", end=" ")
  print("done")
  aht20.reset()

  while True:
    '''!
      @brief   Start measurement and determine if it's completed.
      @param crc_en Whether to enable check during measurement
      @n     True  If the measurement is completed, call a related function such as get* to obtain the measured data.
      @n     False If the measurement failed, the obtained data is the data of last measurement or the initial value 0 if the related function such as get* is called at this time.
      @return  Whether the measurement is done
      @retval True  If the measurement is completed, call a related function such as get* to obtain the measured data.
      @retval False If the measurement failed, the obtained data is the data of last measurement or the initial value 0 if the related function such as get* is called at this time.
    '''
    if aht20.start_measurement_ready(crc_en = True):
      # Get temp in Celsius (℃), range -40-80℃
      temperature_c = aht20.get_temperature_C()
      # Get temp in Fahrenheit (F)
      temperature_f = aht20.get_temperature_F()
      # Get relative humidity (%RH), range 0-100℃
      humidity      = aht20.get_humidity_RH()
      print("temperature(-40~85 C): %.2f C, %.2f F    humidity(0~100 %%RH): %.2f %%RH"%(temperature_c, temperature_f, humidity))
      time.sleep(1)

