#!/usr/bin/python

# Proyecto Phenocam PUCV
#
# Descripcion  : Programa que permite obtener la lectura de un sensor DHT11
# Lenguaje     : Python
# Autor        : Sebastian Bruna <sebastian.bruna.s@mail.pucv.cl>
# Dependencias : Librerias:
# 					- Adafruit https://github.com/adafruit/Adafruit_Python_DHT
#					- time, datetime
#					- os
#					- ftplib
#
#--------------------------------IMPORT LIBRARIES-----------------------------------------------------------------------
import sys
import time
import Adafruit_DHT
import datetime
from ftplib import FTP
import os
import fileinput
 
#--------------------------------CONNECT FTP SERVER---------------------------------------------------------------------
ftp = FTP()
ftp.set_debuglevel(2)
ftp.connect('201.215.167.63', 21) 
ftp.login('pi','_4oYiEmqVUFl')
ftp.cwd('path to the T & H folder')

#--------------------------------PATH LOG FILE--------------------------------------------------------------------------
log_path = "/home/pi/log/iot/"
lastlist = []
localdir = "home\pi\log\iot"
file_name = ""
#--------------------------------CONF TYPE OF SENSOR--------------------------------------------------------------------
sensor = Adafruit_DHT.DHT11

#--------------------------------CONFIG GPIO 23 FOR DHT11 DATA----------------------------------------------------------
pin = 23

#--------------------------------WRITE THE LOG FILE WITH THE NAME yyyy-mm-dd_dht.log------------------------------------
def write_log(text):
	"""
	Function to write the actual temperature in C and humidity in %
	:param text: get in to the string to write
	:return: nothing
	"""
	log = open(log_path + file_name,"a")

	# EJ: 2019-09-10 11:00:00 Temperatura=22.0*  Humedad=60.0%
	line = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + text + "\n"
	log.write(line)
	log.close()

#--------------------------------SEND FILE------------------------------------------------------------------------------
def ftp_upload(localfile, remotefile):
	"""
	:param localfile: 
	:param remotefile: 
	:return: 
	"""""
	fp = open(localfile, 'rb')
	#ftp.storbinary('STOR myfile.txt'.encode('utf-8'), open('myfile.txt'))
	ftp.storbinary('STOR %s' % os.path.basename(localfile), fp, 1024)
	fp.close()
	print ("after upload " + localfile + " to " + remotefile)

#--------------------------------SEND IMG-------------------------------------------------------------------------------
def upload_img(file):
	"""
	:param file:
	:return:
	"""
	ftp_upload(localdir + "\\" + file, file)

#--------------------------------PROGRAM--------------------------------------------------------------------------------
try:	

	while True:

		humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)	#Read the humidity and temperature pin = GPIO 23

#Quede aca escribir el if si file_name es disntinto de la fecha de hoy
		if file_name == "":
			file_name = str(datetime.datetime.now().strftime("%Y-%m-%d") + "_dht.log")
		else:
			file_name = datetime.datetime.now().strftime("%Y-%m-%d") + "_dht.log"



		#IF WE CAN READ THE SENSOR, WRITE THE LOG FILE
		if humidity is not None and temperature is not None:
			write_log("DHT Sensor - temperature in ºC: %s" % str(temperature)) # write temperature
			write_log("DHT Sensor - humidity in %:  %s" % str(humidity))	   # write humidity
		else:
			write_log("Can't get data from the sensor") #write to the log file error in the sensor.

		# wait 10 seconds
		time.sleep(1)
# --------------------------------Check the hour------------------------------------------------------------------------
		if datetime.datetime.now().strftime("%H-%M-%S") == "15:30:00":

			for line in fileinput.input(localdir + file_name):
				lastlist.append(line.rstrip("\n"))

			currentlist = os.listdir(localdir)

			newfiles = list(set(currentlist) - set(lastlist))

			if len(newfiles) == 0:
				print "No files need to upload"
			else:
				for needupload in newfiles:
					print "uploading " + localdir + "\\" + needupload
					upload_img(needupload)
					with open(localdir + "\\list.txt", "a") as myfile:
					myfile.write(needupload + "\n")

			ftp.quit()


#WRITE ERROR TO LOG FILE 
except Exception as e:
	write_log(str(e))
