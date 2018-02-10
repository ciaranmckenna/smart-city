function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 11,
        center: myLatLng
    });
    map.setOptions({
        //customise Map controls locations on screen
        mapTypeControl: true,
        mapTypeControlOptions: {
            style: google.maps.MapTypeControlStyle.HORIZONTAL_BAR,
            position: google.maps.ControlPosition.LEFT_BOTTOM
        },
        zoomControl: true,
        zoomControlOptions: {
            position: google.maps.ControlPosition.RIGHT_BOTTOM
        },
        scaleControl: true,
        streetViewControl: true,
        streetViewControlOptions: {
            position: google.maps.ControlPosition.RIGHT_BOTTOM
        },
        //Sets how far the map can zoom out
        minZoom: 5
    });
}