#!/usr/bin/env python
# -*- coding: utf-8 -*-

# These two lines ensure the JSON data will print to our webpage.
print ("Content-type: text/html")
print ()

from checkStatusCode import checkStatusCode
from getDeviceHeader import getDeviceHeader
import globalConfig
import json
import requests

# Store a local copy of the device header here.
deviceHeader = getDeviceHeader()

# This list stores all attributes needed to create the reportingListURL below.
reportingList = []
reportingList.append('https://api.pool1.iotpdev.com/api/1/reporting?')

# This list stores each sensor ID of each device. (2 sensors/15 devices = 30 sensor IDs)
sensorIDs = []

try: 

	# Attempt to get a snapshot of all devices currently registered within Concert.
	response = requests.get(globalConfig.deviceSnapshotURL, 
					        headers=deviceHeader)

	# Validate the status code.
	checkStatusCode(response.status_code, globalConfig.deviceSnapshotURL)

except requests.exceptions.ConnectionError as connErr:
	print("Connection Error: {0}".format(str(connErr)))
	exit(1)

except requests.exceptions.RequestException as e:
	print("Response Exception raised on auth URL: {0}".format(str(e)))
	print("Address exception: Quitting")
	exit(1)

# Parse the json data from the response.
json_data = response.json()

# For each device,
for device in json_data:

	# Append the device ID to the reportingListURL.
	deviceID = device['id']
	reportingList.append("deviceIds=" + deviceID + "&")

	# As this script is for PM10, only store the sensor ID of the PM10 sensor.
	for sensor in device['sensors']:
		if sensor['name'] == "PM_10":
			sensorIDs.append(sensor['id'])
	
# For each PM10 sensor, append the sensor ID to the reportingListURL.
for sensor in sensorIDs:
	reportingList.append("sensorIds=" + sensor + "&")

# Finish the reportingListURL (NORMAL - return all values stored for each sensor requested)
reportingList.append("reportingQueryType=NORMAL")

# Turn the list into a string.
reportingURL = ''.join(reportingList)

try: 

	# Attempt to get all values from all devices currently registered within Concert.
	response = requests.get(reportingURL, 
					        headers=deviceHeader)

	# Validate the status code.
	checkStatusCode(response.status_code, globalConfig.deviceSnapshotURL)

except requests.exceptions.ConnectionError as connErr:
	print("Connection Error: {0}".format(str(connErr)))
	exit(1)

except requests.exceptions.RequestException as e:
	print("Response Exception raised on auth URL: {0}".format(str(e)))
	print("Address exception: Quitting")
	exit(1)

# Parse the json data from the response.
json_data = response.json()

# For each reading, convert from a string to an float.
# This is so HighCharts can accept the reading.
for device in json_data:
	for sensor in device['sensors']:
		for reading in sensor['readings']:
			reading['sensorValue'] = float(reading['sensorValue'])

# Wrap the json data in a list to turn it into valid json.
jsonArray = []

# Add each device's details to this list.
for device in json_data:
	jsonArray += [device]

# Print the json.
print (json.dumps(jsonArray))