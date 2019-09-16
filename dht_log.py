#!/usr/bin/python

#--------------------------------IMPORT LIBRARIES--------------------------------
import sys
import time
import Adafruit_DHT
import datetime

#--------------------------------PATH LOG FILE--------------------------------
log_path = "/home/pi/log/iot/"

#--------------------------------CONF TYPE OF SENSOR--------------------------------
sensor = Adafruit_DHT.DHT11

#--------------------------------CONFIG GPIO 23 FOR DHT11 DATA--------------------------------
pin = 23

#--------------------------------WRITE THE LOG FILE WITH THE NAME yyyy-mm-dd_dht.log--------------------------------
def write_log(text):
	log = open(log_path + datetime.datetime.now().strftime("%Y-%m-%d") + "_dht.log","a")
	line = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + text + "\n"
	log.write(line)
	log.close()
#--------------------------------PROGRAM--------------------------------
try:	

	while True:

		humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

		#IF WE CAN READ THE SENSOR, WRITE THE LOG FILE
		if humidity is not None and temperature is not None:
			write_log("DHT Sensor - temperature in ºC: %s" % str(temperature))
			write_log("DHT Sensor - humidity in %:  %s" % str(humidity))
		else:
			write_log("Can't get data from the sensor")

		#DELAY
		time.sleep(1)

#WRITE ERROR TO LOG FILE 
except Exception as e:
	write_log(str(e))
