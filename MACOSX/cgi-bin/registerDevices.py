#!usr/bin/env python
# -*- coding: utf-8 -*-

from checkStatusCode import checkStatusCode
import createDeviceTypes
import getDeviceHeader
import getDeviceIDList
import globalConfig

import json
import requests
import time
import random
from pprint import pprint
import os
import errno

# If the device header has not already been created, create it.
# This allows the request to be authorized.
if getDeviceHeader.deviceHeader == "":
	getDeviceHeader.getDeviceHeader()

if getDeviceIDList.deviceIDList == []:
	getDeviceIDList.getDeviceIDList()

# These are used to hack together locations for the sensors in Zone 3.
latIndex = 0
longIndex = 0
lats = []
longs = []

def registerDevice():

	global latIndex
	global longIndex

	# These are used in the for loop below to name devices appropriately.
	deviceIndex = 1
	zoneIndex = 1

	for x in range(0, int(globalConfig.MAXDEVDEVICES)):

		# Every 5 devices, the zone index is incremented and the device index is reset to 1.
		# i.e. instead of Zone_1_Device_5, Zone_1_Device_6, this will lead to 
		# Zone_1_Device_5, Zone_2_Device_1, as it should be.
		if x != 0 and x % 5 == 0:
			zoneIndex = zoneIndex + 1
			deviceIndex = 1
			latIndex = 0
			longIndex = 0

		# Name the device using the logic described above.
		deviceName = "Zone_{0}_Device_{1}".format(zoneIndex, deviceIndex)
		deviceDescription = "Zone_{0}".format(zoneIndex)

		# Increment the device index.
		deviceIndex = deviceIndex + 1

		# If no device Type ID exists in createDeviceTypes, perform a
		# get request and get the ID.
		if createDeviceTypes.deviceTypeID == "":

			try:

				deviceResponse = requests.get(globalConfig.deviceTypesURL,
											  headers = getDeviceHeader.deviceHeader)

				checkStatusCode(deviceResponse.status_code, globalConfig.deviceTypesURL)

				deviceResponse_json = deviceResponse.json()

			except requests.exceptions.ConnectionError as connErr:
				print("Connection Error: {0}".format(str(connErr)))
				exit(1)

			except requests.exceptions.RequestException as e:
				print("Response Exception raised on auth URL: {0}".format(str(e)))
				print("Address exception: Quitting")
				exit(1)

			for deviceType in deviceResponse_json:
				
				# Set the device type ID.
				if deviceType['name'] == "Environmental_Sensor":

					createDeviceTypes.deviceTypeID = deviceType["id"]
	
		devicePayload = json.dumps({"description" : deviceDescription,
									"location" : {"latitude" : generateRandomLatitudeByZone(zoneIndex),
												  "longitude" : generateRandomLongitudeByZone(zoneIndex)},
									"name" : deviceName,
									"owner" : globalConfig.ownerID,
									"typeId" : createDeviceTypes.deviceTypeID})

		print (devicePayload)

		try:

			response = requests.post(globalConfig.devicesURL,
						  			 data = devicePayload,
						  			 headers = getDeviceHeader.deviceHeader)

			checkStatusCode(response.status_code, globalConfig.devicesURL)

			createdDevice = response.json()

		except requests.exceptions.ConnectionError as connErr:
			print("Connection Error: {0}".format(str(connErr)))
			exit(1)

		except requests.exceptions.RequestException as e:
			print("Response Exception raised on auth URL: {0}".format(str(e)))
			print("Address exception: Quitting")
			exit(1)

		deviceID = createdDevice["id"]

		getDeviceIDList.deviceIDList.insert(x, deviceID)

		# Create file structure		
		devFile = open(globalConfig.RegDevicesFile, 'a')

		currentDir = os.getcwd()
		deviceDir = currentDir + '/' + deviceID

		if mkdir_p(deviceDir):

			devFile.write(createdDevice['name'] + ',' + deviceID + '\n')

			fileName = 'deviceId'
			f = open(deviceDir + '/' + fileName, 'w')
			f.write(deviceID)
			f.close()

			fileName = 'awsHost'
			f = open(deviceDir + '/' + fileName, 'w')
			f.write(createdDevice['mqtt']['host'])
			f.close()

			fileName = deviceID + '.private.key'
			f = open(deviceDir + '/' + fileName, 'w')
			f.write(createdDevice['mqtt']['privateKey'])
			f.close()

			fileName = deviceID + '.cert.pem'
			f = open(deviceDir + '/' + fileName, 'w')
			f.write(createdDevice['mqtt']['certificate'])
			f.close()

			fileName = deviceID + '.public.key'
			f = open(deviceDir + '/' + fileName, 'w')
			f.write(createdDevice['mqtt']['publicKey'])
			f.close()


def generateRandomLatitudeByZone(zoneIndex):
	
	global lats
	global latIndex

	if int(zoneIndex) == 1:
		lats = [54.59608585608891, 54.588924843677376, 54.5953897018016, 54.60026253191197, 54.60468735199844]
		latIndex = latIndex + 1
		return lats[(latIndex - 1)]

	elif int(zoneIndex) == 2:
		lats = [54.65049820947117, 54.638379748734394, 54.63182235423758, 54.62168611914537, 54.60796836872569]
		latIndex = latIndex + 1
		return lats[(latIndex - 1)]

	elif int(zoneIndex) == 3:
		lats = [54.56529452128724, 54.566190235926385, 54.58807936328479, 54.575146300013515, 54.584597788534744]
		latIndex = latIndex + 1
		return lats[(latIndex - 1)]


def generateRandomLongitudeByZone(zoneIndex):
	
	global longs 
	global longIndex

	if int(zoneIndex) == 1:
		longs = [-5.950641632080078, -5.932102203369141, -5.915365219116211, -5.936822891235352, -5.927381515502929]
		longIndex = longIndex + 1
		return longs[(longIndex - 1)]

	elif int(zoneIndex) == 2:
		longs = [-5.921459197998047, -5.923004150390624, -5.912017822265625, -5.9235191345214835, -5.920257568359375]
		longIndex = longIndex + 1
		return longs[(longIndex - 1)]

	elif int(zoneIndex) == 3:
		longs = [-5.99578857421875, -5.974674224853515, -5.9580230712890625, -5.97381591796875, -5.943946838378905]
		longIndex = longIndex + 1
		return longs[(longIndex - 1)]


def mkdir_p(path):

	try:

		os.makedirs(path)

	except OSError as exc:

		if exc.errno == errno.EEXIST and os.path.isdir(path):
			return 1
			pass

		else:
			print("Directory {0} could not be created.".format(path))
			raise
			return 0

	return 1

if __name__ == "__main__":
	registerDevice()