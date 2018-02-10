#!usr/bin/env python
# -*- coding: utf-8 -*-

import string
import csv
import random
import time
import globalConfig
import configparser


# This array gives the minimum and maximum values per hour for PM10.
HOURLY_MIN_MAX_VALUES_PM10 = [[5.0, 25.0],  # 00:00
                              [5.0, 25.0],  # 01:00
                              [5.0, 25.0],  # 02:00
                              [5.0, 25.0],  # 03:00
                              [5.0, 25.0],  # 04:00
                              [5.0, 25.0],  # 05:00
                              [10.0, 25.0],  # 06:00
                              [30.0, 50.0],  # 07:00
                              [40.0, 60.0],  # 08:00
                              [50.0, 70.0],  # 09:00
                              [40.0, 60.0],  # 10:00
                              [20.0, 40.0],  # 11:00
                              [25.0, 45.0],  # 12:00
                              [25.0, 45.0],  # 13:00
                              [20.0, 40.0],  # 14:00
                              [20.0, 40.0],  # 15:00
                              [40.0, 60.0],  # 16:00
                              [45.0, 70.0],  # 17:00
                              [55.0, 80.0],  # 18:00
                              [45.0, 65.0],  # 19:00
                              [20.0, 40.0],  # 20:00
                              [15.0, 35.0],  # 21:00
                              [10.0, 30.0],  # 22:00
                              [10.0, 30.0],  # 23:00
                              ]

# This array gives the minimum and maximum values per hour for PM2.5.
HOURLY_MIN_MAX_VALUES_PM2_5 = [[0.0, 10.0],  # 00:00
                               [0.0, 10.0],  # 01:00
                               [0.0, 10.0],  # 02:00
                               [0.0, 10.0],  # 03:00
                               [0.0, 10.0],  # 04:00
                               [0.0, 10.0],  # 05:00
                               [0.0, 15.0],  # 06:00
                               [5.0, 25.0],  # 07:00
                               [10.0, 30.0],  # 08:00
                               [15.0, 30.0],  # 09:00
                               [15.0, 30.0],  # 10:00
                               [5.0, 15.0],  # 11:00
                               [5.0, 20.0],  # 12:00
                               [5.0, 20.0],  # 13:00
                               [5.0, 20.0],  # 14:00
                               [5.0, 20.0],  # 15:00
                               [10.0, 30.0],  # 16:00
                               [15.0, 35.0],  # 17:00
                               [20.0, 40.0],  # 18:00
                               [15.0, 35.0],  # 19:00
                               [5.0, 20.0],  # 20:00
                               [0.0, 10.0],  # 21:00
                               [0.0, 15.0],  # 22:00
                               [0.0, 15.0],  # 23:00
                               ]

# This function returns a random floating-point value between the values passed in as arguments.
def getRandPMSize(a,b):
    return random.uniform(a,b)

# This function converts a date into an epoch time measurement.
# time.strptime() formats the given date and passed the output to time.mktime(), which returns a 
# floating-point Epoch time (seconds that have elapsed since 00:00, 1st January 1970)
def getEpochDate(strDate):
    return time.mktime(time.strptime(strDate, "%d.%m.%Y %H:%M:%S"))


# This function creates the CSV file containing simulated data for both environmental sensors, plus a timestamp.
def makeACSVFile(fname, timeDiff, noRows, startTime):

    # The value returned by getEpochDate is converted into an int.
    currentTime = int(startTime);

    # This syntax allows the CSV file to be written to.
    with open (fname, 'w')as csvOut:

        # For each row (number specified by noRows argument).
        for i in range (0,noRows):

            # Index = Hour of the day for each measurement.
            idx = int(((currentTime - startTime)/3600)%24)
            #int((123456 - 123456)/3600)%24  = 0
            # int(((123456+3600) - 123456)/3600)%24  = 1
            # int(((123456+3600+3600) - 123456)/3600)%24  = 2
            #=24 


            # If idx is greater than 24, it is into the next day and therefore idx is reset and startTime is incremented by 24 hours.
            if idx >= 24:
                startTime += (3600)
                idx = 0
            # startTime + 3600
            # startTime + 3600 + 3600

            # These 3 lines represent the values that actually get written to the CSV file: one reading per sensor and a timestamp.
            Sensor1 = round(getRandPMSize(HOURLY_MIN_MAX_VALUES_PM10[idx][0],HOURLY_MIN_MAX_VALUES_PM10[idx][1]),2)
            Sensor2 = round(getRandPMSize(HOURLY_MIN_MAX_VALUES_PM2_5 [idx][0], HOURLY_MIN_MAX_VALUES_PM2_5 [idx][1]),2)
            Sensor3 = int(currentTime)

            # Write to the file.
            csvOut.write("{0},{1},{2},\n".format(Sensor1, Sensor2, Sensor3))

            # Increment the current time by the specified time between readings, 900sec equates to 15 mins.
            currentTime += timeDiff
            #for next row - move the start time on a bit to simulate the device sending data


def main():

    # Use to read in properties that can be configured before script execution
    config = configparser.ConfigParser()
    config.read('smartCitiesConfig.ini')
    config.sections()

    # This is used as the start date for the generated readings.
    # The start date is read from the smart cities conf properties file (flexibility of code)
    startDateTime = config['createDeviceReadings']['startDateTime']
    timeDiff =  int(config['createDeviceReadings']['timeDiff'])
    noRows =  int(config['createDeviceReadings']['noRows'])

    # Open and read from the 'RegisteredDevices' file.
    csvIn = open(globalConfig.RegDevicesFile, 'r')
    readCSV = csv.reader(csvIn, delimiter=',')

    # Generate a CSV file for each device contained within.
    for row in readCSV:

        # Filename is set to 'deviceID + .csv', 900 = time between readings in seconds (i.e. 15 mins, (60sec x 15 = 900sec))
        # 672 = number of rows (publishing every 15 minutes for a week = 672 values)
        
        startTime = getEpochDate(startDateTime)
        makeACSVFile((row[1] + ".csv"),timeDiff,noRows,startTime)


if __name__ == '__main__':
    main()




