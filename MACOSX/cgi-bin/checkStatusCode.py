#!usr/bin/env python
# -*- coding: utf-8 -*-

# This function checks if the status code of a REST request is 200/201,
# signifying a successful request. If not, the program exits with a log message.
def checkStatusCode(status_code, URL):
	
	# Status codes 200 and 201 represent a successful request, so the function
	# simply returns to the code that called it and continues.
	if status_code == 200 or status_code == 201:
		return

	# If the request is unsuccessful, both the URL and the status code of
	# the failed request are printed.
	else:
		print("Call to URL {0} failed with status code {1}".format(URL, status_code))
		print("Exiting")
		exit(1)