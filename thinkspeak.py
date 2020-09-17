import sys 
import RPi.GPIO as GPIO 
from time import sleep 
import urllib2
import serial
import string
import pynmea2
import os

from mpu6050 import mpu6050
acc_sensor = mpu6050(0x68)

myAPI = "L5ZVL7MASH3A6YGE"
def getSensorData(): 
   RH, T = 25, 50
   return (str(RH), str(T)) 
def main(): 
   print 'starting...' 
   baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI 
   while True:
       Accel_X = 0
       Accel_Y = 0
       while ((Accel_X < 5 ) and (-5 < Accel_Y) and (Accel_Y < 3)):
           acc_sensor_value = acc_sensor.get_accel_data()
           Accel_X          = acc_sensor_value['x']
           Accel_Y          = acc_sensor_value['y']
           print(str(Accel_X) + "      " + str(Accel_Y))
           sleep(0.5)
       
       port="/dev/ttyAMA0"
       ser=serial.Serial(port, baudrate=9600, timeout=0.5)
       dataout = pynmea2.NMEAStreamReader()
       newdata=ser.readline()

       lat = 0
       while((newdata[0:6] == "$GPRMC") and (lat == 0)):
           newmsg=pynmea2.parse(newdata)
           lat=newmsg.latitude
           lng=newmsg.longitude
           gps = "Latitude=" + str(lat) + "and Longitude=" + str(lng)
           print(gps)
           sleep(2)
           userid = 'high'
		
           try:
                   if(lat != 0):
                       f = urllib2.urlopen(baseURL + 
                                   "&field1=%s&field2=%s&field3=%s" % (lat,lng,userid)) 
                       print f.read() 
                       f.close() 
                       sleep(30)
                   else:
                    print 'location error'
           except: 
               print 'exiting.' 
               break
         
           port = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=1)
           port.write('AT'+'\r\n')
           port.write('AT+CMGS=1'+'\r\n')
           port.write('AT'+'\r\n')
         
# call main 
if __name__ == '__main__': 
   main()  
