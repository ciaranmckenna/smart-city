#!usr/bin/env python
# -*- coding: utf-8 -*-

# Main Concert URL
concertURL = 'pool1.iotpdev.com'

# Authentication
realm = 'authenticate'
authTokenAPI = '/auth/realms/' + realm +'/protocol/openid-connect/token'
authURL = 'https://sso.' + concertURL + authTokenAPI

# API access
apiURL = 'https://api.' + concertURL

unitTypesAPI = '/api/1/unit-types'
sensorTypesAPI = '/api/1/sensor-types'
deviceTypesAPI = '/api/1/device-types'

accountsAPI = '/api/1/accounts'

devicesAPI = '/api/1/devices'
deviceSnapshotAPI = '/api/1/devices/snapshot'
deviceReportingAPI = '/api/1/reporting/devices/'

# Actual URLs
unitTypesURL = apiURL + unitTypesAPI
sensorTypesURL = apiURL + sensorTypesAPI
deviceTypesURL = apiURL + deviceTypesAPI

accountsURL = apiURL + accountsAPI

devicesURL = apiURL + devicesAPI
deviceSnapshotURL = apiURL + deviceSnapshotAPI
deviceReportingURL = apiURL + deviceReportingAPI

csvFileDir = '/csvFileDir'
wincsvFileDir = '\\csvFileDir'

# This section is subject to change!
deviceTypeName = 'Environmental_Sensor'
accountName = 'Account 1'
ownerID = '1a38c627-218d-4e07-9bcb-49a119d6434a'

sensorTwoPointFiveID = 'eb2c4892-0bb1-4e6d-8362-7b3cdae8d4d0'
sensorTenID = 'ba246383-3972-4db0-a9de-c43d9bc762c0'

RegDevicesFile = 'RegisteredDevices'

BASEDEVNAME = 'device-'
MAXDEVDEVICES = 15
