#!usr/bin/env python
# -*- coding: utf-8 -*-

import paho.mqtt.client as paho
import os
import socket
import ssl
import json
import time
from time import sleep
from pprint import pprint
import globalConfig
import csv

# These variables are all set to be empty.
csvDir = devDir = deviceId = awshost = certPath = keyPath = caPath = " "

# connflag is used later, within the MQTT loop.
connflag = "false"
awsport = 8883

# This function takes a series of readings and prepares them to be published through MQTT.
def buildJSONStrAWS(s1,s2,tstamp,lat=54.6004142, lon=-5.930640):

	# These dictionaries are used below to nest the JSON correctly.
	message = {}
	state = {}
	reported = {}
	latest = {}
	location = {}

	# Here, the values for each sensor are set to the values passed in.
	sensors = {}
	sensors ['PM_2.5'] = s2
	sensors ['PM_10'] = s1

	# Same for location.
	location['lat'] = lat
	location['lon'] = lon
	
	# The current time is calculated and then used.
	location['timestamp'] = int(tstamp) * 1000

	# This is the actual nesting of the data to resemble the JSON format Concert will be expecting.
	latest['sensors'] = sensors
	latest['timestamp'] = int(tstamp) * 1000
	reported['latest'] = latest
	reported['location'] = location
	state['reported'] = reported
	message['state'] = state

	return json.dumps(message)


# This function checks to see if the CSV file and correct certificates for writing to the device exist.
def getDeviceDetails(devId):

	global csvDir, devDir, deviceId, awshost, certPath, keyPath, caPath

	# Get the current working directory and append the CSV folder name.
	csvDir = os.getcwd() + globalConfig.csvFileDir

	# If it does not exist, inform the user and exit.
	if not os.path.isdir(csvDir):
		print("Directory {} holding CSV files does not exist\n".format(csvDir))
		return 0

	# If the folder containing the certificates for the device does not exist, inform the user and exit.
	devDir = os.getcwd() + "/" + devId
	if not os.path.isdir(devDir):
		print("Directory {} holding dev files does not exist\n".format(devDir))
		return 0

	# If the file containing the device ID does not exist, inform the user and exit.
	if not os.path.isfile(devDir + "/" + "deviceId"):
		print("File {0} does not exist in directory {1}\n".format(deviceId, devDir))
		return 0

	# Otherwise, open the file containing the device ID and read the ID into memory.
	f = open(devDir + "/" + "deviceId", 'r')
	deviceId = f.read()
	f.close()

	# If the file containing the awshost for the device does not exist, inform the user and exit.
	if not os.path.isfile(devDir + "/" + "awshost"):
		print("File {0} does not exist in directory {1}\n".format(deviceId, devDir))
		return 0

	# Otherwise, open the file containing the awshost and read it into memory.
	f = open(devDir + "/" + "awshost", 'r')
	awshost = f.read()
	f.close()

	# Check for the certificates for the device. If they do not exist, inform the user and exit.
	certPath = devDir + "/" + devId + ".cert.pem"
	print("CertPath : {0}".format(certPath))
	if not os.path.isfile(certPath):
		print("certPath file {0} does not exist in directory {1}\n".format(certPath, devDir))
		return 0

	keyPath = devDir + "/" + devId + ".private.key"

	if not os.path.isfile(keyPath):
		print("keyPath file {0} does not exist in directory {1}\n".format(keyPath, devDir))
		return 0

	caPath = "root-CA.crt"

	# Exit successfully.
	return 1


def on_connect(client, userdata, flags, rc):
	global connflag
	connflag = True
	if rc == 0:
		print("Connection status: successful")
	elif rc == 1:
		print("Connection status: Connection refused")


def main():
	mqttc = paho.Client()
	mqttc.on_connect = on_connect

	#curdir = os.getcwd()

	if not os.path.isfile(globalConfig.RegDevicesFile):
		print("File {0} does not exist in directory {1}\n".format(globalConfig.RegDevicesFile, csvDir))
		return 0

	try:
		regIn = open(globalConfig.RegDevicesFile, 'r')
		readReg = csv.reader(regIn, delimiter=',')
		for row in readReg:
			if getDeviceDetails(row[1]):

				mqttc.reinitialise()
				mqttc.on_connect = on_connect

				csvfile = csvDir + "/" + row[1] + ".csv"

				if os.path.isfile(csvfile):
					print("certpath; {0}".format(certPath))
					print("keypath; {0}".format(keyPath))
					print("CApath; {0}".format(caPath))
					mqttc.tls_set(caPath,
								  certfile=certPath,
								  keyfile=keyPath,
								  cert_reqs=ssl.CERT_REQUIRED,
								  tls_version=ssl.PROTOCOL_TLSv1_2,
								  ciphers=None)

					mqttc.connect(awshost, awsport, keepalive=60)
					mqttc.loop_start()
					sleep(2)

					csvIn = open(csvfile, 'r')
					readCSV = csv.reader(csvIn, delimiter=',')

					debugcounter = 0

					for sensorRows in readCSV:

						jmsg = buildJSONStrAWS(sensorRows[0],
											   sensorRows[1],
											   sensorRows[2]
											   )

						print("\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
						pprint(json.loads(jmsg))
						print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")

						if connflag == True:
							print(debugcounter)
							debugcounter = debugcounter + 1
							print("Publishing sensor readings for device: {0}".format
								  ("$aws/things/" + deviceId + "/shadow/update"))
							# Do not publish just yet
							mqttc.publish("$aws/things/" + deviceId + "/shadow/update", jmsg, qos=1)
							sleep(1)
						else:
							print("waiting for connection...")
							sleep(5)
				else:
					print("csvfile {0} does not exist in directory {1}".format(csvfile, csvDir))

	except KeyboardInterrupt:
		print("Keyboard Interrupt detected: Quitting:")
		exit(1)


if __name__ == '__main__':
	main()