# Bush cam script, using a PIR on GPIO24 and a LED flash on GPIO25
# F.R
# 2018

import os, time, sys
import picamera
import RPi.GPIO as GPIO
import serial
from fractions import Fraction

GPIO.setmode(GPIO.BCM)
GPIO.setup(25,GPIO.OUT,initial=0)
GPIO.setup(24,GPIO.IN)

def PrepFileSaveRetName():
  ftime = time.gmtime()
  save_dir = str(ftime.tm_year) + "-" + str(ftime.tm_mon).zfill(2) + "-" + str(ftime.tm_mday).zfill(2)
  if not os.path.isdir("./" + save_dir):
    os.mkdir("./" + save_dir)
  file_inc = 0
  save_file = str(ftime.tm_year) + str(ftime.tm_mon).zfill(2) + str(ftime.tm_mday).zfill(2) + "_" + str(ftime.tm_hour).zfill(2) + str(ftime.tm_min).zfill(2) + str(ftime.tm_sec).zfill(2) + "_" + str(file_inc).zfill(2) + ".jpg"
  while os.path.isfile("./" + save_dir + "/" + save_file):
    file_inc = file_inc + 1
    save_file = str(ftime.tm_year) + str(ftime.tm_mon).zfill(2) + str(ftime.tm_mday).zfill(2) + "_" + str(ftime.tm_hour).zfill(2) + str(ftime.tm_min).zfill(2) + str(ftime.tm_sec).zfill(2) + "_" + str(file_inc).zfill(2) + ".jpg"
  return "./" + save_dir + "/" + save_file 

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=0)

wifiDataCache = str('')

with picamera.PiCamera(framerate=4) as camera:
  while True:
    try: 
      if (GPIO.input(24) == 1):
        GPIO.output(25,1)
        #camera.iso = 1600
        camera.rotation = 180
        camera.flash_mode = 'off'
        camera.led = False
        camera.shutter_speed = 0
        newfile = PrepFileSaveRetName()
        print newfile
        camera.capture(newfile) 
        print camera.exposure_speed
        GPIO.output(25,0)
        if len(wifiDataCache) > 0:
          print wifiDataCache
          wifiDataCache = str()
        time.sleep(0.5)

      time.sleep(0.1)
      if ser.isOpen():
        while ser.inWaiting() > 0:
          for i in ser.readline():
            wifiDataCache += i
          
    except KeyboardInterrupt:
      print "Exiting"
      GPIO.cleanup()
      sys.exit()
	
GPIO.cleanup()
sys.exit()
