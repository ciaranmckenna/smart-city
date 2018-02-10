#!usr/bin/env python
# -*- coding: utf-8 -*-

from checkStatusCode import checkStatusCode
import globalConfig

import getpass
import requests

# This device header will be accessible by all other scripts on the server.
deviceHeader = ""

def getDeviceHeader():

	# Declare that deviceHeader will be written to.
	global deviceHeader

	# Set up the default authentication headers.
	authHeaders = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}

	# Prompt user for username and password.
	userName = "iotpadminuser" # input("Username: ")
	password = "P@55w0rd" # getpass.getpass("Password for {0}".format(userName))

	# Appears to not work if wrapped in json.dumps(),
	# unlike the other requests.
	authPayload = {"client_id" : "postman",
				   "username" : userName,
				   "password" : password,
				   "grant_type" : "password"}

	try:

		# Print URL to screen for verification.
		# print("authURL: {0}".format(globalConfig.authURL))

		# Attempt the login post, and store the response.
		response = requests.post(globalConfig.authURL,
								 data = authPayload,
								 headers = authHeaders)

		checkStatusCode(response.status_code, globalConfig.authURL)

	except requests.exceptions.ConnectionError as connErr:
		print("Connection Error: {0}".format(str(connErr)))
		exit(1)

	except requests.exceptions.RequestException as e:
		print("Response Exception raised on auth URL: {0}".format(str(e)))
		print("Address exception: Quitting")
		exit(1)

	# Use the access token from the response to create the device header, which
	# can be accessed globally.
	deviceHeader = {"Authorization" : "Bearer " + response.json()['access_token'],
				    "Content-Type" : "application/json"}

	return deviceHeader