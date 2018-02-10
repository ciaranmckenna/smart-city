#!/usr/bin/env python
# -*- coding: utf-8 -*-

# These two lines ensure the JSON data will print to our webpage.
print ("Content-type: text/html")
print 

from checkStatusCode import checkStatusCode
from getDeviceHeader import getDeviceHeader
import globalConfig
import json
import requests

# Store a local copy of the device header here.
deviceHeader = getDeviceHeader()

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

# Wrap the json data in a list to turn it into valid json.
jsonArray = []

# Add each device's details to this list.
for device in json_data:
	jsonArray += [device]

# Print the json.
print (json.dumps(jsonArray))