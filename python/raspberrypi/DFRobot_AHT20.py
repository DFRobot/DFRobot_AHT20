# -*- coding:utf-8 -*-
from __future__ import print_function


'''!
  @file DFRobot_AHT20.py
  @brief This AHT20 temperature & humidity sensor employs digital output and I2C interface, through which users can read the measured temperature and humidity. Based on the AHT20 chip, it offers the following features:
  @n 1. Collect ambient temperature, unit Celsius (℃), range -40-85℃, resolution: 0.01, error: ±0.3-±1.6℃
  @n 2. Collect ambient relative humidity, unit: %RH, range 0-100%RH, resolution 0.024%RH, error: when the temprature is 25℃, error range is ±2-±5%RH
  @n 3. Use I2C interface, I2C address is default to be 0x38
  @n 4. uA level sensor, the measuring current supply is less than 200uA
  @n 5. Power supply range 3.3-5V
  @copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
  @license     The MIT License (MIT)
  @author [Arya](xue.peng@dfrobot.com)
  @version  V1.0
  @date  2022-02-09
  @url https://github.com/DFRobot/DFRobot_AHT20
'''

import sys
import time
import smbus

class DFRobot_AHT20:
  ## Default I2C address of AHT20 sensor 
  AHT20_DEF_I2C_ADDR           = 0x38
  ## Init command
  CMD_INIT                     = 0xBE  
  ## The first parameter of init command: 0x08
  CMD_INIT_PARAMS_1ST          = 0x08  
  ## The second parameter of init command: 0x00
  CMD_INIT_PARAMS_2ND          = 0x00  
  ## Waiting time for init completion: 0.01s
  CMD_INIT_TIME                = 0.01    
  ## Trigger measurement command
  CMD_MEASUREMENT              = 0xAC  
  ## The first parameter of trigger measurement command: 0x33
  CMD_MEASUREMENT_PARAMS_1ST   = 0x33  
  ## The second parameter of trigger measurement command: 0x00
  CMD_MEASUREMENT_PARAMS_2ND   = 0x00  
  ## Measurement command completion time：0.08s
  CMD_MEASUREMENT_TIME         = 0.08   
  ## Return data length when the measurement command is without CRC check.
  CMD_MEASUREMENT_DATA_LEN     = 6     
  ## Return data length when the measurement command is with CRC check.
  CMD_MEASUREMENT_DATA_CRC_LEN = 7     
  ## Soft reset command
  CMD_SOFT_RESET               = 0xBA  
  ## Soft reset time: 0.02s
  CMD_SOFT_RESET_TIME          = 0.02   
  ## Get status word command
  CMD_STATUS                   = 0x71   

  _humidity = 0.0
  _temperature = 0.0
  
  def __init__(self):
    self._addr = self.AHT20_DEF_I2C_ADDR
    self._bus = smbus.SMBus(1)

  def begin(self):
    '''!
      @brief   Initialize AHT20 sensor
      @return  Return init status
      @retval True  Init succeeded
      @retval False Init failed
    '''
    if self._init() != True:
      return False
    return True
  
  def reset(self):
    '''!
      @brief   Sensor soft reset, restore the sensor to the initial status
      @return  NONE
    '''
    self._write_command(self.CMD_SOFT_RESET)
    time.sleep(self.CMD_SOFT_RESET_TIME)
  
  def start_measurement_ready(self, crc_en = False):
    '''!
      @brief   Start measurement and determine if it's completed.
      @param crc_en Whether to enable check during measurement
      @n     True  If the measurement is completed, call a related function such as get* to obtain the measured data.
      @n     False If the measurement failed, the obtained data is the data of last measurement or the initial value 0 if the related function such as get* is called at this time.
      @return  Whether the measurement is done
      @retval True  If the measurement is completed, call a related function such as get* to obtain the measured data.
      @retval False If the measurement failed, the obtained data is the data of last measurement or the initial value 0 if the related function such as get* is called at this time.
    '''
    recv_len = self.CMD_MEASUREMENT_DATA_LEN
    if self._ready() == False:
      print("Not cailibration.")
      return False
    if crc_en:
      recv_len = self.CMD_MEASUREMENT_DATA_CRC_LEN
    self._write_command_args(self.CMD_MEASUREMENT, self.CMD_MEASUREMENT_PARAMS_1ST, self.CMD_MEASUREMENT_PARAMS_2ND)
    time.sleep(self.CMD_MEASUREMENT_TIME)
    l_data = self._read_data(0x00, recv_len)
    #print(l_data)
    if l_data[0] & 0x80:
      print("AHT20 is busy!")
      return False
    if crc_en and self._check_crc8(l_data[6], l_data[:6]) == False:
      print("crc8 check failed.")
      return False
    temp = l_data[1]
    temp <<= 8
    temp |= l_data[2]
    temp <<= 4
    temp = temp | (l_data[3] >> 4)
    temp = (temp & 0xFFFFF) * 100.0
    self._humidity = temp / 0x100000

    temp = l_data[3] & 0x0F
    temp <<= 8
    temp |= l_data[4]
    temp <<= 8
    temp |= l_data[5]
    temp = (temp & 0xFFFFF) * 200.0
    self._temperature = temp / 0x100000 - 50
    return True


  def get_temperature_F(self):
    '''!
      @brief   Get ambient temperature, unit: Fahrenheit (F).
      @return  Temperature in F
      @note  AHT20 can't directly get the temp in F, the temp in F is calculated according to the algorithm: F = C x 1.8 + 32
      @n  Users must call the start_measurement_ready function once before calling the function to start the measurement so as to get the real-time measured data,
      @n  otherwise what they obtained is the initial data or the data of last measurement.
    '''
    return self._temperature * 1.8 + 32

  def get_temperature_C(self):
    '''!
      @brief   Get ambient temperature, unit: Celsius (℃).
      @return  Temperature in ℃, it's normal data within the range of -40-85℃, otherwise it's wrong data
      @note  Users must call the start_measurement_ready function once before calling the function to start the measurement so as to get the real-time measured data,
      @n  otherwise what they obtained is the initial data or the data of last measurement.
    '''
    return self._temperature
  
  def get_humidity_RH(self):
    '''!
      @brief   Get ambient relative humidity, unit: %RH.
      @return  Relative humidity, range 0-100
      @note  Users must call the start_measurement_ready function once before calling the function to start the measurement so as to get the real-time measured data,
      @n  otherwise what they obtained is the initial data or the data of last measurement.
    '''
    return self._humidity

  def _check_crc8(self, crc8, data):
    # CRC initial value: 0xFF
    # CRC8 check polynomial: CRC[7: 0] = X8 + X5 + X4 + 1  -  0x1 0011 0001 - 0x131
    crc = 0xFF
    pos = 0
    size = len(data)
    #print(data)
    while pos < size:
      i = 8
      #crc &= 0xFF
      crc ^= data[pos]
      while i > 0:
        if crc & 0x80:
          crc <<= 1
          crc ^= 0x31
        else:
          crc <<= 1
        i -= 1
      pos += 1
    crc &= 0xFF
    #print(crc)
    if crc8 == crc:
      return True
    return False

  def _ready(self):
    status = self._get_status_data()
    if status & 0x08:
      return True
    return False

  def _init(self):
    status = self._get_status_data()
    if status & 0x08:
      return True
    self._write_command_args(self.CMD_INIT, self.CMD_INIT_PARAMS_1ST, self.CMD_INIT_PARAMS_2ND)
    time.sleep(self.CMD_INIT_TIME)
    status = self._get_status_data()
    if status & 0x08:
      return True
    return False
  
  def _get_status_data(self):
    status = self._read_data(self.CMD_STATUS, 1)
    #print(status)
    if len(status):
      return status[0]
    else:
      return 0
  
  def _read_data(self, cmd, len):
    return self._read_bytes(cmd, len)
  
  def _write_command(self, cmd):
    self._bus.write_byte(self._addr, self.CMD_SOFT_RESET)
    time.sleep(self.CMD_SOFT_RESET_TIME)
  
  def _write_command_args(self, cmd, args1, args2):
    #
    l = [args1, args2]
    self._write_bytes(cmd, l)

  def _write_bytes(self, reg, buf):
    try:
      self._bus.write_i2c_block_data(self._addr, reg, buf)
      return len(buf)
    except:
      return 0

      

  def _read_bytes(self, reg, size):
    try:
      rslt = self._bus.read_i2c_block_data(self._addr, reg, size)
      return rslt
    except:
      return []
