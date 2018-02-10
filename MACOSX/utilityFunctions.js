
//looping through deviceist. passing in an id and using this vaule to compare against the list. when there is a match extract the coresponding name
function getDeviceName(id){
    var name="";
    for (var i=0; i<deviceList.length;i++){

        if (id ==  deviceList[i].id){
            name = deviceList[i].name;
            break;
        }
    }
    return name;
}


//Loops through the array of markers and adds them to the map
function setMapOnAll(map) {
    for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(map);
    }
}

//Sets all markers to show on the map
function showMarkers() {
    setMapOnAll(map);
}

//clears all markers from the map
function clearMarkers() {
    setMapOnAll(null);
}

//loopin round the map dat object and deleting the zone
function deleteZone() {
    map.data.forEach(function(feature) {
        map.data.remove(feature);
    });
}



//passes getData the pmCategory 1 so it gets back pm10 values

function pm10() {
    getData(1);
}

//passes getData the pmCategory 2 so it gets back pm2.5 values
function pm25() {
    getData(2);
}

