# DFRobot_AHT20

- [English Version](./README.md)

AHT20是一款测量温湿度的温湿度传感器，采用数字输出，I2C接口，用户可通过I2C接口读取测量的温度和湿度。DFRobot采用AHT20芯片设计的此款温湿度传感器具有以下特点:
1. 采集环境温度，单位：摄氏度（℃)，范围-40 ~ 85℃，分辨率：0.01，误差：±0.3 ~ ±1.6 ℃
2. 采集环境相对湿度，单位：%RH,范围0~100%RH，分辨率0.024%RH，误差：25℃时，误差范围±2 ~ ±5%RH
3. 采用I2C接口，默认I2C地址为0x38
4. uA级传感器，实测最大不超过200uA。
5. 供电范围3.3~5V。

![产品效果图](../../resources/images/SEN0527.png) ![产品效果图](../../resources/images/SEN0528.png)


## 产品链接（[www.dfrobot.com](www.dfrobot.com)）
    SKU: SEN0527
    SKU: SEN0528 

## 目录

  * [概述](#概述)
  * [库安装](#库安装)
  * [方法](#方法)
  * [兼容性](#兼容性)
  * [历史](#历史)
  * [创作者](#创作者)

## 概述

提供一个python库给AHT20传感器，以获取该传感器测量的温度和湿度数据，此库具有以下功能：
1. 获取摄氏度温度数据；
2. 获取华摄氏度温度数据，此数据通过摄氏度温度数据计算而来；
3. 获取湿度数据。
4. 复位传感器，恢复其初始状态

## 库安装
1. 下载库至树莓派，要使用这个库，首先要将库下载到Raspberry Pi，命令下载方法如下:<br>
```python
sudo git clone https://github.com/DFRobot/DFRobot_AHT20
```
2. 打开并运行例程，要执行一个例程demo_x.py，请在命令行中输入python demo_x.py。例如，要执行 demo_read_aht20.py例程，你需要输入:<br>

```python
python demo_read_aht20.py 
或 
python2 demo_read_aht20.py 
或 
python3 demo_read_aht20.py
```

## 方法

```python
  '''!
    @brief   AHT20传感器初始化
    @return  返回初始化状态
    @retval True  初始化成功
    @retval False 初始化失败
  '''
  def begin(self):

  '''!
    @brief   传感器软复位，将传感器恢复到初始状态。
    @return  NONE
  '''
  def reset(self):
    
  '''!
    @brief   启动测量，并判断测量数据是否完成。
    @param crc_en 测量时是否使能校验检测
    @n     True  此次测量完成，可调用get*等相关函数，获取测量的数据
    @n     False 此次测量失败，如果此时调用get*等相关函数，获取的数据是上一次测量的数据，或初始值0
    @return  测量数据是否完成
    @retval True  此次测量完成，可调用get*等相关函数，获取测量的数据
    @retval False 此次测量失败，如果此时调用get*等相关函数，获取的数据是上一次测量的数据，或初始值0
  '''
  def start_measurement_ready(self, crc_en = False):
    
  '''!
    @brief   获取环境温度，单位：华摄氏度（F）。
    @return  华摄氏度温度
    @note  AHT20不可直接获取华摄氏度温度，这里的华摄氏度温度是根据算法计算出来的： F = C x 1.8 + 32
    @n  用户调用此函数，必须先调用一次start_measurement_ready函数，来启动测量，才能获取到实时的测量数据，
    @n  否则将获取到初始数据或上一次测量数据
  '''
  def get_temperature_F(self):

  '''!
    @brief   获取环境温度，单位：摄氏度（℃）。
    @return  摄氏度温度，范围-40 ~ 85℃为正常数据，否则为错误数据
    @note  用户调用此函数，必须先调用一次start_measurement_ready函数，来启动测量，才能获取到实时的测量数据，
    @n  否则将获取到初始数据或上一次测量数据
  '''
  def get_temperature_C(self):
    
  '''!
    @brief   获取环境相对湿度，单位：%RH。
    @return  相对湿度，范围0~100
    @note  用户调用此函数，必须先调用一次start_measurement_ready函数，来启动测量，才能获取到实时的测量数据，
    @n  否则将获取到初始数据或上一次测量数据
  '''
  def get_humidity_RH(self):
```

## 兼容性

| 主板         | 通过 | 未通过 | 未测试 | 备注 |
| ------------ | :--: | :----: | :----: | :--: |
| RaspberryPi2 |      |        |   √    |      |
| RaspberryPi3 |      |        |   √    |      |
| RaspberryPi4 |  √   |        |        |      |

* Python 版本

| Python  | 通过 | 未通过 | 未测试 | 备注 |
| ------- | :--: | :----: | :----: | ---- |
| Python2 |  √   |        |        |      |
| Python3 |  √   |        |        |      |

## 历史

- 2022/02/09 - 1.0.0 版本

## 创作者

Written by Arya(xue.peng@dfrobot.com), 2022. (Welcome to our [website](https://www.dfrobot.com/))






