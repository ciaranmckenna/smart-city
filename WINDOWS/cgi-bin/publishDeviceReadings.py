#!/usr/bin/python

##################
#
#global variable
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

# vars are empty
csvDir = devDir = deviceId = awshost = certPath = keyPath = caPath = " "
connflag = "false"
awsport = 8883

#function for building up a message in JSON to be accepted by AWS including two sensor readings, a timestamp and gps data.
def buildJSONStrAWS(s1,s2,tstamp,lat=54.6004142, lon=-5.930640):



	message = {}
	state = {}
	reported = {}
	latest = {}
	location = {}

	sensors = {}
	#sensor recording Particulate Matter 2.5
	sensors ['PM_2.5'] = s1
	#sensor recording Particulate Matter 10
	sensors ['PM_10'] = s2

	#location data in degrees
	location['lat'] = lat
	location['lon'] = lon
	# *1000 to convert from milli - seconds to seconds
	location['timestamp'] = int(tstamp) * 1000
	
	latest['sensors'] = sensors
	latest['timestamp'] = int(tstamp) * 1000
	reported['latest'] = latest
	reported['location'] = location
	state['reported'] = reported
	message['state'] = state

	return json.dumps(message)

#retrieves the device details needed for pubishing and writes them to a folder. Each folder represents a single device
def getDeviceDetails(devId):
	# making the following global variables csvDir, devDir, deviceId, awshost, certPath, keyPath, caPath
	global csvDir, devDir, deviceId, awshost, certPath, keyPath, caPath
	# assigning the location of the csv directory (Returns a string representing the current working directory)
	csvDir = os.getcwd() + globalConfig.csvFileDir
	# error mg if the directory can't be found
	if not os.path.isdir(csvDir):
		print("Directory {} holding CSV files does not exist\n".format(csvDir))
		return 0
	# location of the device directory
	devDir = os.getcwd() + "\\" + devId
	# error message directory holding files doesn't exist
	if not os.path.isdir(devDir):
		print("Directory {} holding dev files does not exist\n".format(devDir))
		return 0
	# error message file doesn't exist in directory
	if not os.path.isfile(devDir + "\\" + "deviceId"):
		print("File {0} does not exist in directory {1}\n".format(deviceId, devDir))
		return 0
	# csv fie read
	f = open(devDir + "\\" + "deviceId", 'r')
	deviceId = f.read()
	f.close()
	# error messgae file doesnt exist in directory
	if not os.path.isfile(devDir + "\\" + "awshost"):
		print("File {0} does not exist in directory {1}\n".format(deviceId, devDir))
		return 0
	# reading aws host
	f = open(devDir + "\\" + "awshost", 'r')
	awshost = f.read()
	f.close()

	#appending permission certifications and error messages if they don't exist
	certPath = devDir + "\\" + devId + ".cert.pem"
	print("CertPath : {0}".format(certPath))
	if not os.path.isfile(certPath):
		print("certPath file {0} does not exist in directory {1}\n".format(certPath, devDir))
		return 0

	keyPath = devDir + "\\" + devId + ".private.key"

	if not os.path.isfile(keyPath):
		print("keyPath file {0} does not exist in directory {1}\n".format(keyPath, devDir))
		return 0

	caPath = "root-CA.crt"

	return 1

	# This function connects the client to the broker
def on_connect(client, userdata, flags, rc):
	global connflag
	connflag = True
	if rc == 0:
		print("Connection status: successful")
	elif rc == 1:
		print("Connection status: Connection refused")

	# reading the csv file passing the data via mqtt
def main():
	mqttc = paho.Client()
	mqttc.on_connect = on_connect

	# looking for reg devices file path 	
	if not os.path.isfile(globalConfig.RegDevicesFile):
		print("File {0} does not exist in directory {1}\n".format(globalConfig.RegDevicesFile, csvDir))
		return 0
	# wrapped in a try except to allow user to exit gracefully if need be.	
	try:
		# reading from regDevice file that contains sensor name and id
		regIn = open(globalConfig.RegDevicesFile, 'r')
		readReg = csv.reader(regIn, delimiter=',')
		for row in readReg:
			# reading from the reg file, gets permission certs 
			if getDeviceDetails(row[1]):
				mqttc.reinitialise()
				mqttc.on_connect = on_connect
				# csvFile used for verification
				csvfile = csvDir + "\\" + row[1] + ".csv"
				# looks for csvFile
				if os.path.isfile(csvfile):
					print("certpath; {0}".format(certPath))
					print("keypath; {0}".format(keyPath))
					print("CApath; {0}".format(caPath))
					#encryption format applied to data passed
					mqttc.tls_set(caPath,
								  certfile=certPath,
								  keyfile=keyPath,
								  cert_reqs=ssl.CERT_REQUIRED,
								  tls_version=ssl.PROTOCOL_TLSv1_2,
								  ciphers=None)

					mqttc.connect(awshost, awsport, keepalive=60)
					mqttc.loop_start()
					sleep(2)

					# from each row within the CSV file, create the message in JSON format
					csvIn = open(csvfile, 'r')
					readCSV = csv.reader(csvIn, delimiter=',')

					for sensorRows in readCSV:

						jmsg = buildJSONStrAWS(sensorRows[0],
											   sensorRows[1],
											   sensorRows[2]
											   )

						print("\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
						pprint(json.loads(jmsg))
						print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")

						if connflag == True:
							print("Publishing sensor readings for device: {0}".format
								  ("$aws/things/" + deviceId + "/shadow/update"))
							# publishing the csv file values
							#To successfully run this script uncomment the line below
							#mqttc.publish("$aws/things/" + deviceId + "/shadow/update", jmsg, qos=1)
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