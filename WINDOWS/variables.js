//declaring global variables which are hoisted to all other scripts
var myLatLng = {
    lat: 54.597315,
    lng: -5.929325
};
var markers = [];
var map;
var mapStyle;
var features;


var deviceList;
var trafficLayer = new google.maps.TrafficLayer();
var bikeLayer = new google.maps.BicyclingLayer();
