# ローカルにセンサデータを保存し、読み込む
import serial
import datetime
import numpy as np
from time import time
import csv
import pprint
import time
import sys
import keyboard

try:
    from msvcrt import getch
except ImportError:
    def getch():
        import sys
        import tty
        import termios
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

class HMDSerialRead():

    def __init__(self, comnum, rate):
        self.com = comnum
        self.ser = serial.Serial(comnum, rate)
        self.values = [0 for i in range(20)]   
    
    def UpdateSensorData(self):
        # When micro computer receives the "b", it sends back the sensor data.
        # This system receive the 24 bytes which include the sensor data and start stop character
        
        # self.ser.write(b"b")
        byteBuffer = self.ser.read_until(terminator="Z".encode("utf-8"))
        SensorList = byteBuffer
      
        # print("SensorList = ", SensorList)
        # print(byteBuffer)
        if(len(SensorList) == 27):
            # print(SensorList[0])
            self.values[0] = (((SensorList[1]) & 0xff) << 2) + (((SensorList[21]) & 0xc0) >> 6)	    
            self.values[1] = (((SensorList[2]) & 0xff) << 2) + (((SensorList[21]) & 0x30) >> 4)
            self.values[2] = (((SensorList[3]) & 0xff) << 2) + (((SensorList[21]) & 0x0c) >> 2)
            self.values[3] = (((SensorList[4]) & 0xff) << 2) + ((SensorList[21]) & 0x03)
            self.values[4] = (((SensorList[5]) & 0xff) << 2) + (((SensorList[22]) & 0xc0) >> 6)	
            self.values[5] = (((SensorList[6]) & 0xff) << 2) + (((SensorList[22]) & 0x30) >> 4)
            self.values[6] = (((SensorList[7]) & 0xff) << 2) + (((SensorList[22]) & 0x0c) >> 2)
            self.values[7] = (((SensorList[8]) & 0xff) << 2) + ((SensorList[22]) & 0x03)
            self.values[8] = (((SensorList[9]) & 0xff) << 2) + (((SensorList[23]) & 0xc0) >> 6)
            self.values[9] = (((SensorList[10]) & 0xff) << 2) + (((SensorList[23]) & 0x30) >> 4)
            self.values[10] = (((SensorList[11]) & 0xff) << 2) + (((SensorList[23]) & 0x0c) >> 2)
            self.values[11] = (((SensorList[12]) & 0xff) << 2) + ((SensorList[23]) & 0x03)
            self.values[12] = (((SensorList[13]) & 0xff) << 2) + (((SensorList[24]) & 0xc0) >> 6)
            self.values[13] = (((SensorList[14]) & 0xff) << 2) + (((SensorList[24]) & 0x30) >> 4)
            self.values[14] = (((SensorList[15]) & 0xff) << 2) + (((SensorList[24])& 0x0c) >> 2)
            self.values[15] = (((SensorList[16]) & 0xff) << 2) + ((SensorList[24]) & 0x03)
            self.values[16] = (((SensorList[17]) & 0xff) << 2) + (((SensorList[25]) & 0xc0) >> 6)
            self.values[17] = (((SensorList[18]) & 0xff) << 2) + (((SensorList[25]) & 0x30) >> 4)
            self.values[18] = (((SensorList[19]) & 0xff) << 2) + (((SensorList[25]) & 0x0c) >> 2)
            self.values[19] = (((SensorList[20]) & 0xff) << 2) + ((SensorList[25]) & 0x03)
            # print(self.values)

        else:
            print("sensor data error")

    def getSensorData(self):
        self.UpdateSensorData()
        return self.values 

class SensorData:
    def __init__(self):
        self.commandType = -1
        self.strength = 0
        self.sensorValues = []
    
    def setSensorValues(self, sensorValues):
        self.sensorValues = sensorValues
    
    def getSensorValues(self):
        return self.sensorValues

# Arduinoを繋げたCOMポートを開く 
# * ポート名は環境に合わせて適宜変えること
ser = HMDSerialRead("/dev/tty.usbserial-DN03ZVUJ", 57600) # e2mask left
ser2 = HMDSerialRead("/dev/tty.usbserial-DN040KE7", 57600) # e2mask right

# ser = HMDSerialRead("/dev/tty.usbserial-DN0404LS", 57600)

sensorData = SensorData()
sensorData2 = SensorData()
# print("getSensorData = ", ser.getSensorData())
sensorDataList = []
# output = csv.writer("leaningData.csv")
print("Please enter a learning number")
print("{0:ニュートラル 1:喜び 2:怒り　3:驚き　4:悲しみ} ")
key = int(input())

while True:        
    ser.UpdateSensorData()
    ser2.UpdateSensorData()
    sensorData.setSensorValues(ser.getSensorData())
    sensorData2.setSensorValues(ser.getSensorData())
    sensorDataList = sensorData.getSensorValues()+sensorData2.getSensorValues()

    with open('./learningData.csv',"a") as f:
        writer = csv.writer(f)
        writer.writerow([key]+sensorDataList)

    print(sensorData.getSensorValues()+sensorData2.getSensorValues())
    # print(sensorData.getSensorValues()) # e2mask left
    # print(sensorData2.getSensorValues()) # e2mask right