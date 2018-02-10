
//calls loadZones then set the style of the zones by calling getColour function
function buildZone(defaultValue) {
    loadZones();
    //add some style
    mapStyle = map.data.setStyle(function(feature) {
        //get all the features  with the property zone and store them in variable zone
        var zone = feature.getProperty('zone');
        //call getColour and pass it the zone and pmCategory and store result in variable colour.
        var colour = getColour(zone, defaultValue);
        //return colour of zone and outline
        return {
            fillColor: colour,
            strokeWeight: 0.1
        };
    });
}



function getColour(zone, pmCategory) {
    console.log("calling get color")
    //Sets boundaries for colour change for PM10 levels
    if (pmCategory == 1) {
        //PM10
        var low_topboundary = 20;
        var medium_topboundary = 40;
        var high_topboundary = 100;
    }
    //Sets boundaries for colour change for PM2.5 levels
    else if (pmCategory == 2)
    {
        //Pm2.5
        var low_topboundary = 10;
        var medium_topboundary = 20;
        var high_topboundary = 100;
    }
    //variable to store zone total
    var zonetotal = 0;
    //if passed a one loop through devices and add up zone totals for pm10
    if (pmCategory == 1) {
        //loop to iterate over the entire device list
        for (i = 0; i < deviceList.length; i++) {
            //for each element in the devicelist that contain the zone index
            if (deviceList[i].name.includes("Zone_" + zone)) {
                //accessing the sensors asscoated with this device
                var sensorlist = deviceList[i].sensors;
                // Getting the pm10 sensor level for this device
                var pLevel = getParticulateValue(sensorlist, 'PM_10');
               //add particulate vaules to creat a zone total
                zonetotal += +pLevel
            }
        }
        //if passed a 2 loop through the devices and add up the zone totals for pm2.5
    } else if (pmCategory == 2) {
        for (x = 0; x < (deviceList.length); x++) {
            if (deviceList[x].name.includes("Zone_" + zone)) {
                zonetotal = zonetotal + (+getParticulateValue(deviceList[x].sensors, 'PM_2.5'))
            }
        }
    }
    //calculate zone average by dividing the zone total by 5, which is the number of sensors in each zone
    zoneavg = zonetotal / 5;
    //console.log("Zone " + zone + " average: " + zoneavg);
    //returning what colour to set the zone between set boundaries
    if (zoneavg > 0 && zoneavg < low_topboundary) {
        return 'green';
    } else if (zoneavg >= low_topboundary && zoneavg < medium_topboundary) {
        return 'yellow';
    } else if (zoneavg >= medium_topboundary && zoneavg < high_topboundary) {
        return 'red';
    }
    //if average is outside of these boundaries return black and log error
    else {
        console.log("Error: average is " + zoneavg);
        return 'black';
    }
}

//list of all sensors per device. Because the device contains values for both PM10 and pm 2.5 extracting out which sensor we want. Passing in the particulate level which is pm 10 or pm2.5 and looking for that in the sensor list
function getParticulateValue(sensorList, particulateLevel) {
    var value = 0
    for (z = 0; z < sensorList.length; z++) {
        if (sensorList[z].name == particulateLevel) {
            value = sensorList[z].value;
            break;
        }
    }
    return value;
}

