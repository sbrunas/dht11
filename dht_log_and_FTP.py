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
# --------------------------------IMPORT LIBRARIES----------------------------------------------------------------------
import sys
import time
import Adafruit_DHT
import datetime
from ftplib import FTP
import os
import fileinput
import smtplib, ssl

# -create a secure connection with gmail SMTP server using SMTP_SSL() of smtplib to initiate a TLS-encrypted connecton--

port = 465  # For SSL
smtp_server = 'smtp.gmail.com'
sender_email = 'phenocam.pucv@gmail.com'
receiver_email = 'phenocam.pucv@gmail.com'
password = 'labgrs2019'

# body message to alert if the file was send
message_fileSend = """\
Subject: dht11 log send ok.

This message is sent from phenocam control one."""
# body message to alert if we can't read the sensor
message_sensor_error = """\
Subject: camera power on success.

This message is sent from phenocam control one."""
# body message to alert if we can't send the file
message_fileSend_error = """\
Subject: error in sending the file via FTP.

This message is sent from phenocam control one."""

# body message to alert general error
message_error = """\
Subject: general error.

This message is sent from phenocam control one."""


# --------------------------------send email read dht11 error to phenocam.pucv@gmail.com -------------------------------
def sensor_read_error():
    """
    :return:
    Body: Create secure connection woth server and send email
    """
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message_sensor_error)


# --------------------------------send email if the file was sent, to phenocam.pucv@gmail.com --------------------------
def fileSend_ok():
    """
    :return:
    Body: Create secure connection with server and send email
    """
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message_fileSend)


# --------------------------------send email if the file was sent, to phenocam.pucv@gmail.com --------------------------
def fileSend_error(e):
    """
    :return:
    Body: Create secure connection with server and send email
    """
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message_fileSend_error)
    raise e


def general_error(e):
    """
    :return:
    Body: Create secure connection with server and send email
    """
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message_error)
    raise e


# --------------------------------CONNECT FTP SERVER--------------------------------------------------------------------
ftp = FTP()
ftp.set_debuglevel(2)
ftp.connect('201.215.167.63', 21)
ftp.login('pi', '_4oYiEmqVUFl')
ftp.cwd("/home/pi/nextcloud/data/__groupfolders/1/log")

# --------------------------------PATH LOG FILE-------------------------------------------------------------------------
log_path = "/home/pi/log/iot/"
server_path = "/home/pi/nextcloud/data/__groupfolders/1/log"
lastlist = []
file_name = ""
# --------------------------------DATE VAR------------------------------------------------------------------------------
date_now = ""
date_count = 0
hour_now = datetime.datetime.now().strftime('%M')
half_an_hour_zero = '00'
half_an_hour = '30'
check_hour = '50'  # hour to send the file via FTP
# --------------------------------CONF TYPE OF SENSOR-------------------------------------------------------------------
sensor = Adafruit_DHT.DHT11

# --------------------------------CONFIG GPIO 23 FOR DHT11 DATA---------------------------------------------------------
pin = 23


# --------------------------------WRITE THE LOG FILE WITH THE NAME yyyy-mm-dd_dht.log-----------------------------------
def write_log(text, fName):
    """
    Function to write the actual temperature in C and humidity in %
    :param text: get in to the string to write
    :return: nothing

    """
    log = open(log_path + fName, "a")  # Open /home/pi/log/iot/ with file_name

    # EJ: 2019-09-10 11:00:00 Temperatura=22.0*  Humedad=60.0%
    line = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + text + "\n"
    log.write(line)
    log.close()


# --------------------------------SEND FILE-----------------------------------------------------------------------------
def ftp_upload(localfile, remotefile):
    """
    :param localfile:
    :param remotefile:
    :return: print "after upload + localfile to remotefile"
    This function take the path + file_name and open in "fp" and uppload the file via FTP
    Finally close the FTP connection

    """
    fp = open(localfile, 'rb')  # r+ is for read & write, rb read binary file

    # ftp.storbinary('STOR myfile.txt'.encode('utf-8'), open('myfile.txt'))
    ftp.storbinary('STOR %s' % os.path.basename(localfile), fp, 1024)
    fp.close()
    print("after upload " + localfile + " to " + remotefile)


# --------------------------------SEND IMG------------------------------------------------------------------------------
def upload_file(file):
    """
    :param file: name of the current file to be upload
    :return: None
    This function call the ftp_upload function and concat the local path + name of the current file to be upload.

    """
    ftp_upload(log_path + file, file)


# --------------------------------PROGRAM-------------------------------------------------------------------------------
try:

    while True:

        # print("check the date and the file name")
        # ----------------------------Check the date and the file name----------------------------------------------------------
        if date_now != str(datetime.datetime.now().strftime('%Y-%m-%d')):

            date_now = str(datetime.datetime.now().strftime('%Y-%m-%d'))  # save the actual day
            file_name = date_now + '_dht.txt'  # save the actual file name
            date_count += 1  # add one to the day count

        else:

            date_now = str(datetime.datetime.now().strftime('%Y-%m-%d'))
            file_name = date_now + '_dht.txt'

        # ------------------------Check if we can read the sensor, write the log file ------------------------------------------
        if (datetime.datetime.now().strftime('%S') == half_an_hour_zero) or (
                datetime.datetime.now().strftime('%S') == half_an_hour):
            print("getting temperature and humidity")
            humidity, temperature = Adafruit_DHT.read_retry(sensor,
                                                            pin)  # Read the humidity and temperature pin = GPIO 23
            print("check if we can read the sensor")
            if humidity is not None and temperature is not None:
                write_log("DHT Sensor - temperature is: %s" % str(temperature), file_name)  # write temperature
                write_log("DHT Sensor - humidity is :  %s" % str(humidity), file_name)  # write humidity
            else:
                write_log("Can't get data from the sensor", file_name)  # write to the log file error in the sensor.
                sensor_read_error()

        # --------------------------------Check the hour------------------------------------------------------------------------
        # print("check the hour")
        if datetime.datetime.now().strftime('%S') == check_hour:
            print("Sending files")
            for line in fileinput.input(log_path + file_name):
                lastlist.append(line.rstrip("\n"))  # append the current text to "lastlist"

            currentlist = os.listdir(log_path)  # save the current files in the directory tu current list

            newfiles = list(set(currentlist) - set(lastlist))
            #try:
            if len(newfiles) == 0:
                print("No files need to upload")
            else:
                for needupload in newfiles:
                    print("uploading " + log_path + file_name + needupload)
                    upload_file(needupload)
                    with open(log_path + file_name, "a") as myfile:
                        myfile.write(needupload + "\n")
                    fileSend_ok()
            #except Exception as e:
            #   fileSend_error(e)
                ftp.quit()

# --------------------------------Write error to log file --------------------------------------------------------------
except Exception as e:
    write_log(str(e), file_name)
    general_error(str(e))

except KeyboardInterrupt as e:
    general_error(str(e))
