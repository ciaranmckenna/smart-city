#!usr/bin/env python
# -*- coding: utf-8 -*-

from checkStatusCode import checkStatusCode
import getDeviceHeader
import globalConfig

import requests

# If the device header has not already been created, create it.
# This allows the request to be authorized.
if getDeviceHeader.deviceHeader == "":
	getDeviceHeader.getDeviceHeader()

# This is where all the device ID's will be stored.
deviceIDList = []

# Retrieve all device ID's and store in a list.
def getDeviceIDList():

	global deviceIDList
	
	try:

		# Retrieve all devices currently within Concert.
		response = requests.get(globalConfig.devicesURL,
						        headers = getDeviceHeader.deviceHeader)

		checkStatusCode(response.status_code, globalConfig.devicesURL)

		response_json = response.json()

		# Iterate through each device and check the name.
		for device in response_json:

			# If the name contains our special testing name,
			# add the ID to the device ID list.
			if "Device_" in device['name']:

				# Only add the ID if it is not already within the list.
				if device['id'] not in deviceIDList:
					deviceIDList += [device['id']]

	except requests.exceptions.ConnectionError as connErr:
		print("Connection Error: {0}".format(str(connErr)))
		exit(1)

	except requests.exceptions.RequestException as e:
		print("Response Exception raised on auth URL: {0}".format(str(e)))
		print("Address exception: Quitting")
		exit(1)