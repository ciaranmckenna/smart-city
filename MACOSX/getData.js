//function to get data from server takes parameter pmCategory to know which pm data to load by default
function getData(pmCategory) {
    //Create new InfoWindow object
    var infowindow = new google.maps.InfoWindow();
    // if no pmCategory has been set, set it to pm2.5 by default
    if (!pmCategory) {
        pmCategory = 2;
    }
    //URL that request is sent to. Returns a list of all devices and there current readings. SNapshot API. further investigation needs to be done into the correct use of the Concert API. As we believe this is doing more than is needed. bringing back too much data
    var api = "./cgi-bin/getDeviceDetails.py";
    //jQuery to load JSON-encoded data from the server using a GET HTTP request. takes in a request object that is returneded and converts it into json. json is a human readable data structure that js well to handle
    $.getJSON(api, {
        format: "json"
    })
    //waiting for api call to rturn. Assign handlers immediately after making the request.
        .done(function(data) {
            //Iterate over the JSON returned object, executing a function for each matched element
            $.each(data, function(i, devices) {
                //For every element in the loop return the latitude and longitude and store it as a variable.
                var latLng = new google.maps.LatLng(devices.reportedLocation.latitude, devices.reportedLocation.longitude);
                // Add a marker to the map using te latLng variable.
                var marker = new google.maps.Marker({
                    position: latLng,
                    map: map
                });
                //Pushes marker to an array. maintaing a refernce to the add makeres incase there is a need for further manipulation
                markers.push(marker);
                // Registering a click even with each marker for set of location data within the device
                google.maps.event.addListener(marker, 'click', (function(marker, i) {
                    return function() {
                        //create a InfoWindow element which is displayed on click containing device name and current sensor readings
                        infowindow.setContent(devices.name + '<br/>' + 'PM 10 Value' + " " + getParticulateValue(devices.sensors, 'PM_10') + '<br/>' + 'PM 2.5 Value' + " " + getParticulateValue(devices.sensors, 'PM_2.5') + '<br/>');
                        infowindow.open(map, marker);
                    }
                })(marker, i));
            });
            // map.data.forEach(function(feature) {
            //     map.data.remove(feature);
            // });

            deleteZone();

            //JSON response from the api fully converted. Stored as  global variable
            deviceList = data;


            buildZone(pmCategory);
        })
        //If request fails, show alert and log error if something happened t the server shows theres a problem with connecting to the server but the page doesnt break
        .fail(function() {
            alert("Error. Failed to get device details!")
            console.log( "Error. Failed to get device details!" );
        });
}

//jQuery 'GET' request Ajax call to call the python scripts to call the api returns. Returns a collection of sensors readings per device.
// done function waits until it gets a response. for each device it returns a list of sensor readings
function getPM10HighChartsData() {
    var api = "./cgi-bin/getReportingDataPM10.py";
    $.getJSON(api, {
        format: "json",
        async: true
    })
        .done(function(data) {
            $.each(data, function(i, readings) {
                var deviceReadings = {
                    //calls get device name to set the name of each device
                    name: getDeviceName(readings.deviceId),
                    //takes the timestamp and reverses it
                    data: readings.sensors[0].readings.map(vl => [vl.reportedTimestamp, vl.sensorValue]).reverse()
            };
                //console.log(JSON.stringify(deviceReadings));
                //calls the highcharts object and adds the data to highcharts
                pm10Chart.addSeries(deviceReadings)

            });
        })
        .fail(function() {
            alert("Error. Failed to find historical data!")
            console.log( "Error. Failed to to find historical data!" );
        });
}

//jQuery 'GET' request Ajax call to call the python scripts to call the api returns. Returns a collection of sensors readings per device.
// done function waits until it gets a response. for each device it returns a list of sensor readings
function getPM25HighChartsData() {
    var api = "./cgi-bin/getReportingDataPM25.py";
    $.getJSON(api, {
        format: "json",
        async: true

    })
        .done(function(data) {
            $.each(data, function(i, readings) {

                var deviceReadings = {
                   //calls get device name to set the name of each device
                    name: getDeviceName(readings.deviceId),
                    //takes the timestamp and reverses it
                    data: readings.sensors[0].readings.map(vl => [vl.reportedTimestamp, vl.sensorValue]).reverse()
            };
                //console.log(JSON.stringify(deviceReadings));
                //calls the highcharts object and adds the data to highcharts
                pm25Chart.addSeries(deviceReadings);
            });
        });

}


//when called imports GeoJSON polygons if not alreay loaded load her in
function loadZones() {
    if (features == null) {
        features = map.data.loadGeoJson('./cgi-bin/geo.py');
    }
}
