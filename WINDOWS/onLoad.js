//detects the state of readiness of the page. Once html and css has loaded fires js
$(document).ready(function() {
    console.log("ready!");
    initMap();
    getData();
    getPM10HighChartsData();
    getPM25HighChartsData();
    //could dynamically be changed function associated with the element you are clicking
    $('#traffic-b').click(function() {
        if (trafficLayer.getMap() == null) {
            //if traffic layer is disabled.. enable it
            trafficLayer.setMap(map);
            bikeLayer.setMap(null);
        } else {
            //traffic layer is enabled.. disable it
            trafficLayer.setMap(null);
        }
    });
    $('#bike-b').click(function() {
        if (bikeLayer.getMap() == null) {
            //traffic layer is disabled.. enable it
            trafficLayer.setMap(null);
            bikeLayer.setMap(map);
        } else {
            //traffic layer is enabled.. disable it
            bikeLayer.setMap(null);
        }
    });
});