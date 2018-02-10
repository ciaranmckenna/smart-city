#!usr/bin/env python
# -*- coding: utf-8 -*-

from checkStatusCode import checkStatusCode
import getDeviceHeader
import globalConfig
import requests
import json

# Declaring global variables to store the ID of each element.
unitTypeID = ""
sensor2point5TypeID = ""
sensor10TypeID = ""
deviceTypeID = ""

# If the device header has not already been created, create it.
# This allows the request to be authorized.
if getDeviceHeader.deviceHeader == "":
	getDeviceHeader.getDeviceHeader()

# Target JSON format: 
# 
# {
# 	"description" : "string",
# 	"name" : "string",
# 	"symbol" : "string"
# }

# This function creates a unit type and stores the ID of the created type.
def createUnitType():

	# Declare that unitTypeID will be written to.
	global unitTypeID

	# Set up the unit type details.
	unitName = "Particulate Matter"
	unitSymbol = "ug/m3"
	unitDescription = "Particulate matter concentration"

	# Encode the json to pass as a request.
	unitPayload = json.dumps({"description" : unitDescription,
 							  "name" : unitName,
  							  "symbol": unitSymbol})

	try:

		# Attempt the request.
		response = requests.post(globalConfig.unitTypesURL,
					  			 data = unitPayload,
					  			 headers = getDeviceHeader.deviceHeader)

		# Verify the status code, and print to console if successful.
		checkStatusCode(response.status_code, globalConfig.unitTypesURL)
		print("Unit type creation successful.")

		# Get the json data from the response body.
		response_json = response.json()

		# Get unit type ID from the response json.
		unitTypeID = response_json["id"]
		print("Unit type ID: " + unitTypeID + "\n")

	except requests.exceptions.ConnectionError as connErr:
		print("Connection Error: {0}".format(str(connErr)))
		exit(1)

	except requests.exceptions.RequestException as e:
		print("Response Exception raised on auth URL: {0}".format(str(e)))
		print("Address exception: Quitting")
		exit(1)


# Target JSON format: 
# 
# {
# 	"name" : "string",
# 	"defaultDisplayName" : "string",
# 	"version" : "string",
# 	"description" : "string",
# 	"baseType" : "string",
# 	"numericReadingType" : "SNAPSHOT",
# 	"unitTypeId" : "string",
# 	"defaultMinimumNormalOperatingValue" : number,
#	"defaultMaximumNormalOperatingValue" : number,
# 	"defaultMinimumValue" : number,
# 	"defaultMaximumValue" : number
# }

# This function creates our first sensor type and stores the ID of the created type.
def createSensor2point5Type():
	
	# Declare that sensor2point5TypeID will be written to.
	global sensor2point5TypeID

	# Set up the sensor type details.
	sensorName = "PM_2.5"
	sensorDisplayName = "PM_2.5"
	sensorVersion = "1.0"
	sensorDescription = "Particulate_matter"
	sensorBaseType = "DOUBLE"
	sensorReadingType = "SNAPSHOT"
	
	sensorUnitTypeID = unitTypeID
	
	sensorMinOperatingValue = 0.1
	sensorMaxOperatingValue = 100
	sensorDefaultMinValue = 5
	sensorDefaultMaxValue = 10

	# Encode the json to pass as a request.
	sensorPayload = json.dumps({"name" : sensorName,
								"defaultDisplayName" : sensorDisplayName,
								"version" : sensorVersion,
								"description" : sensorDescription,
								"baseType" : sensorBaseType,
								"numericReadingType" : sensorReadingType,
								"unitTypeId" : sensorUnitTypeID,
								"defaultMinimumNormalOperatingValue" : sensorMinOperatingValue,
								"defaultMaximumNormalOperatingValue" : sensorMaxOperatingValue,
								"defaultMinimumValue" : sensorDefaultMinValue,
								"defaultMaximumValue" : sensorDefaultMaxValue})

	try:

		# Attempt the request.
		response = requests.post(globalConfig.sensorTypesURL,
								 data = sensorPayload,
								 headers = getDeviceHeader.deviceHeader)

		# Verify the status code, and print to console if successful.
		checkStatusCode(response.status_code, globalConfig.sensorTypesURL)
		print("Sensor (2.5) type creation successful.")

		# Get the json data from the response body.
		response_json = response.json()

		# Get the sensor type ID from the response json.
		sensor2point5TypeID = response_json["id"]
		print("Sensor (2.5) type ID: " + sensor2point5TypeID + "\n")

	except requests.exceptions.ConnectionError as connErr:
		print("Connection Error: {0}".format(str(connErr)))
		exit(1)

	except requests.exceptions.RequestException as e:
		print("Response Exception raised on auth URL: {0}".format(str(e)))
		print("Address exception: Quitting")
		exit(1)


# This function creates a sensor type and stores the ID of the created type.
def createSensor10Type():
	
	# Declare that sensor10TypeID will be written to.
	global sensor10TypeID

	# Set up the sensor type details.
	sensorName = "PM_10"
	sensorDisplayName = "PM_10"
	sensorVersion = "1.0"
	sensorDescription = "Particulate_matter"
	sensorBaseType = "DOUBLE"
	sensorReadingType = "SNAPSHOT"
	
	sensorUnitTypeID = unitTypeID
	
	sensorMinOperatingValue = 0.1
	sensorMaxOperatingValue = 100
	sensorDefaultMinValue = 5
	sensorDefaultMaxValue = 10

	# Encode the json to pass as a request.
	sensorPayload = json.dumps({"name" : sensorName,
								"defaultDisplayName" : sensorDisplayName,
								"version" : sensorVersion,
								"description" : sensorDescription,
								"baseType" : sensorBaseType,
								"numericReadingType" : sensorReadingType,
								"unitTypeId" : sensorUnitTypeID,
								"defaultMinimumNormalOperatingValue" : sensorMinOperatingValue,
								"defaultMaximumNormalOperatingValue" : sensorMaxOperatingValue,
								"defaultMinimumValue" : sensorDefaultMinValue,
								"defaultMaximumValue" : sensorDefaultMaxValue})

	try:

		# Attempt the request.
		response = requests.post(globalConfig.sensorTypesURL,
								 data = sensorPayload,
								 headers = getDeviceHeader.deviceHeader)

		# Verify the status code, and print to console if successful.
		checkStatusCode(response.status_code, globalConfig.sensorTypesURL)
		print("Sensor type creation successful.")

		# Get the json data from the response body.
		response_json = response.json()

		# Get the sensor type ID from the response json.
		sensor10TypeID = response_json["id"]
		print("Sensor type ID: " + sensor10TypeID + "\n")

	except requests.exceptions.ConnectionError as connErr:
		print("Connection Error: {0}".format(str(connErr)))
		exit(1)

	except requests.exceptions.RequestException as e:
		print("Response Exception raised on auth URL: {0}".format(str(e)))
		print("Address exception: Quitting")
		exit(1)


# Target JSON format: 
# 
# {
# 	"name": "string",
# 	"sensorTypeIds": [
# 	{
# 		"id": "string"
# 	}],
# 	"version": "string"
# }

# This function creates a device type and stores the ID of the created type.
def createDeviceType():
	
	# Declare that deviceTypeID will be written to.
	global deviceTypeID

	# Set up the device type details.
	deviceTypeName = "Environmental_Sensor"
	deviceTypeSensor2point5TypeID = sensor2point5TypeID
	deviceTypeSensor10TypeID = sensor10TypeID
	deviceTypeVersion = "1.0"

	# Encode the json to pass as a request.
	deviceTypePayload = json.dumps({"name" : deviceTypeName,
									"sensorTypeIds" : [
									{
										"id" : deviceTypeSensor2point5TypeID
									},
									{
										"id" : deviceTypeSensor10TypeID
									}],
									"version" : deviceTypeVersion})

	try:

		# Attempt the request.
		response = requests.post(globalConfig.deviceTypesURL,
								 data = deviceTypePayload,
								 headers = getDeviceHeader.deviceHeader)

		# Verify the status code, and print to console if successful.
		checkStatusCode(response.status_code, globalConfig.deviceTypesURL)
		print("Device type creation successful.")

		# Get the json data from the response body.
		response_json = response.json()

		# Get the sensor type ID from the response json.
		deviceTypeID = response_json["id"]
		print("Device type ID: " + deviceTypeID + "\n")

	except requests.exceptions.ConnectionError as connErr:
		print("Connection Error: {0}".format(str(connErr)))
		exit(1)

	except requests.exceptions.RequestException as e:
		print("Response Exception raised on auth URL: {0}".format(str(e)))
		print("Address exception: Quitting")
		exit(1)


# Check to see if the unit/sensor/device type currently exists.
# If so, grab its ID and pass it on. If not, create it.
def validateTypes():

	# Declare that these global variables will (may) be written to.
	global unitTypeID
	global sensor2point5TypeID
	global sensor10TypeID
	global deviceTypeID

	# Flags used when iterating through response data.
	unitFound = False
	sensor2point5Found = False
	sensor10Found = False
	deviceFound = False

	# This section deals with the unit type.
	# Get the list of unit types and check each to see if it
	# matches what we are trying to create.
	# If it already exists, ignore it and move on.
	
	try: 

		unitResponse = requests.get(globalConfig.unitTypesURL,
					 			    headers = getDeviceHeader.deviceHeader)

		checkStatusCode(unitResponse.status_code, globalConfig.unitTypesURL)

		unitResponse_json = unitResponse.json()

	except requests.exceptions.ConnectionError as connErr:
		print("Connection Error: {0}".format(str(connErr)))
		exit(1)

	except requests.exceptions.RequestException as e:
		print("Response Exception raised on auth URL: {0}".format(str(e)))
		print("Address exception: Quitting")
		exit(1)

	# This iterates through each returned unit type.
	# (will be an empty list if none exist)
	for unitType in unitResponse_json:

		# If the name of the unit type matches what we want to create (i.e. it already exists), 
		# assign its ID to the unitTypeID variable, break out of the loop and move on.
		if unitType['name'] == "Particulate Matter":
			print("\nUnit type already exists.")			
			unitTypeID = unitType['id']
			unitFound = True
			break

	# If all unit types have been iterated through and the corresponding
	# unit type has not been found, create it.
	if unitFound == False:
		print("Creating unit type..")
		createUnitType()

	# This section deals with the sensor type.

	try:

		sensorResponse = requests.get(globalConfig.sensorTypesURL,
									  headers = getDeviceHeader.deviceHeader)

		checkStatusCode(sensorResponse.status_code, globalConfig.sensorTypesURL)

		sensorResponse_json = sensorResponse.json()

	except requests.exceptions.ConnectionError as connErr:
		print("Connection Error: {0}".format(str(connErr)))
		exit(1)

	except requests.exceptions.RequestException as e:
		print("Response Exception raised on auth URL: {0}".format(str(e)))
		print("Address exception: Quitting")
		exit(1)

	# PM2.5
	for sensorType in sensorResponse_json:
		if sensorType['name'] == "PM_2.5":
			print("Sensor type already exists.")
			sensor2point5TypeID = sensorType['id']
			sensor2point5Found = True
			break

	if sensor2point5Found == False:
		print("Creating sensor type..")
		createSensor2point5Type()

	# PM10
	for sensorType in sensorResponse_json:
		if sensorType['name'] == "PM_10":
			print("Sensor type already exists.")
			sensor10TypeID = sensorType['id']
			sensor10Found = True
			break

	if sensor10Found == False:
		print("Creating sensor type..")
		createSensor10Type()

	# This section deals with the device type.
	
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
		if deviceType['name'] == "Environmental_Sensor":
			print("Device type already exists.")
			deviceTypeID = deviceType['id']
			deviceFound = True
			break

	if deviceFound == False:
		print("Creating device type..")
		createDeviceType()

# Check the types, and create if necessary.
if __name__ == '__main__':
	validateTypes()