import time
import serial

ser = serial.Serial("/dev/ttyUSB0")
ser.setRTS(False)
time.sleep(0.5)
ser.setRTS(True)
time.sleep(0.5)
ser.setRTS(False)