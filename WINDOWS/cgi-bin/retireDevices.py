#!usr/bin/env python
# -*- coding: utf-8 -*-

from checkStatusCode import checkStatusCode
import getDeviceHeader
import getDeviceIDList
import globalConfig

import requests
import json
import os
import csv
import errno
import shutil

# If the device header has not already been created, create it.
# This allows the request to be authorized.
if getDeviceHeader.deviceHeader == "":
	getDeviceHeader.getDeviceHeader()

if getDeviceIDList.deviceIDList == []:
	getDeviceIDList.getDeviceIDList()

# This function will retire all existing devices. 
def retireExistingDevices():
		
	currentDir = os.getcwd()

	csvIn = open(globalConfig.RegDevicesFile,'r')
	readCSV = csv.reader(csvIn, delimiter = ',')	

	for row in readCSV:	

		try:

			retirePayload = json.dumps("RETIRED")

			retireResponse = requests.put(globalConfig.devicesURL + "/" + row[1] + "/status",
						 		          data = retirePayload,
						                  headers = getDeviceHeader.deviceHeader)

			# checkStatusCode(retireResponse.status_code, globalConfig.devicesURL + "/" + row[1] + "/status")

			deleteResponse = requests.delete(globalConfig.devicesURL + "/" + row[1], 
				                             headers = getDeviceHeader.deviceHeader)

			# checkStatusCode(deleteResponse.status_code, globalConfig.devicesURL + "/" + row[1])
		   
		except requests.exceptions.ConnectionError as connErr:
			print("Connection Error: {0}".format(str(connErr)))
			exit(1)

		except requests.exceptions.RequestException as e:
			print("Response Exception raised on auth URL: {0}".format(str(e)))
			print("Address exception: Quitting")
			exit(1)
		
		dirToDelete = currentDir + "/" + row[1]
		shutil.rmtree(dirToDelete)
				
		print("Deleted: {0} with ID: {1}\n".format(row[0],row[1]))
			
	csvIn.close()
	os.remove(globalConfig.RegDevicesFile)
	print("Removed: {}\n".format(globalConfig.RegDevicesFile))

if __name__ == "__main__":
	retireExistingDevices()