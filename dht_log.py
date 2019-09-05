#!/usr/bin/python

# Importa las librerias necesarias 
import time
import datetime
import Adafruit_DHT

# Log file
log_path = "/home/pi/log/iot/"

# Configuracion del tipo de sensor DHT
sensor = Adafruit_DHT.DHT11

# Configuracion del puerto GPIO al cual esta conectado (GPIO 23)
pin = 23

# Escribe un archivo log en log_path con el nombre en el formato yyyy-mm-dd_dht.log
def write_log(text):
	log = open(log_path + datetime.datetime.now().strftime("%Y-%m-%d") + "_dht.log","a")
	line = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + text + "\n"
	log.write(line)
	log.close()

# Intenta ejecutar las siguientes instrucciones, si falla va a la instruccion except
try:
	# Ciclo principal infinito
	while True:
		# Obtiene la humedad y la temperatura desde el sensor 
		humedad, temperatura = Adafruit_DHT.read_retry(sensor, pin)

		# Si obtiene una lectura del sensor la registra en el archivo log
		if humedad is not None and temperatura is not None:
			write_log("DHT Sensor - Temperatura: %s" % str(temperatura))
			write_log("DHT Sensor - Humedad:  %s" % str(humedad))
		else:
			write_log('Error al obtener la lectura del sensor')

		# Duerme 10 segundos
		time.sleep(1)

# Se ejecuta en caso de que falle alguna instruccion dentro del try
except Exception as e:
	write_log(str(e))
