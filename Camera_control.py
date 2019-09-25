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

import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO library
import time
import datetime
import smtplib, ssl

# --------------------------------GPIO CONFIG---------------------------------------------------------------------------
GPIO.setwarnings(False)  # Ignore warning for now
GPIO.setmode(GPIO.BCM)  # Use physical pin numbering
camera_pin = 17
GPIO.setup(17, GPIO.OUT, initial=GPIO.LOW)  # Set pin 17 to be an output pin and set initial value to low (off)
# --------------------------------DATE VAR------------------------------------------------------------------------------
date_now = ""
date_count = 0
check_hour_on = '17:15:00'
check_hour_off = '17:20:00'

# -create a secure connection with gmail SMTP server using SMTP_SSL() of smtplib to initiate a TLS-encrypted connecton--

port = 465  # For SSL
smtp_server = 'smtp.gmail.com'
sender_email = 'phenocam.pucv@gmail.com'
receiver_email = 'phenocam.pucv@gmail.com'
password = 'labgrs2019'
#body message to alert and error in the program ocurrs
message = """\
Subject: camera power on error.

This message is sent from phenocam control one."""
#body message to alert the camera its was turned on
message_power_on = """\
Subject: camera power on success.

This message is sent from phenocam control one."""
#body message to alert the camera its was turned off
message_power_off = """\
Subject: camera power off success.

This message is sent from phenocam control one."""
# --------------------------------send email alert to phenocam.pucv@gmail.com ------------------------------------------
def send_alert():
    """
    :return:
    Body: Create secure connection woth server and send email
    """
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
# --------------------------------send email power on OK to phenocam.pucv@gmail.com ------------------------------------
def send_ok_on():
    """
    :return:
    Body: Create secure connection with server and send email
    """
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message_power_on)
# --------------------------------send email power off OK to phenocam.pucv@gmail.com -----------------------------------
def send_ok_off():
    """

    :return:
    Body: Create a secure connection with server and send email
    """
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message_power_off)
# --------------------------------SET THE PIN 17 HIGH TO TURN ON THE CAMERA --------------------------------------------
def turn_on_device():
    """
    :return: None
    Body: Function to turn on the camera.
    """
    GPIO.output(camera_pin, GPIO.HIGH)  # Turn on


# --------------------------------SET THE PIN 17 OFF TO TURN ON THE CAMERA ---------------------------------------------
def turn_off_device():
    """
    :return: None
    Body: Function to turn off the camera.
    """
    GPIO.output(camera_pin, GPIO.LOW)  # Turn off

# --------------------------------DATE VAR------------------------------------------------------------------------------
def raise_email(e):
    send_alert()    # calls the email send function
    turn_off_device()   # calls the turn off device to power down the camera
    raise e # raise the corresponding error


# --------------------------------PROGRAM-------------------------------------------------------------------------------
try:

    while True:
# --------------------------------Check the hour------------------------------------------------------------------------
        # print("check the hour")
        if datetime.datetime.now().strftime('%H:%M:%S') == str(check_hour_on):
            #print(datetime.datetime.now().strftime('%H:%M:%S'))
            #print(check_hour_on)
            send_ok_on()
            while datetime.datetime.now().strftime('%H:%M:%S') != check_hour_off:
                #print("on")
                turn_on_device()
            send_ok_off()
        else:
            turn_off_device()
            #send_alert()

# --------------------------------Write error to log file --------------------------------------------------------------
except KeyboardInterrupt as e:
    raise_email(e)
except Exception as e:
    raise_email(e)
