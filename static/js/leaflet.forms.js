// just create the basemap
var myCenter = new L.LatLng(45, 12);
var map = new L.Map('map', {
  center: myCenter,
  zoom: 10
});
var positron = L.tileLayer('http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {
  attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, &copy; <a href="http://cartodb.com/attributions">CartoDB</a>'
}).addTo(map);

// geojson with three features. two have value "parking" for property "parking" and one has value "stadium"
var locations = [{
    "type": "Feature",
    "properties": {
        "name": "Place One",
        "parking": "parking"
    },
    "geometry": {
        "type": "Point",
        "coordinates": [12.3,45.2]
    }
}, {
    "type": "Feature",
    "properties": {
        "name": "Place Two",
        "parking": "parking"
    },
    "geometry": {
        "type": "Point",
        "coordinates": [12.2,45.1]
    }
}, {
    "type": "Feature",
    "properties": {
        "name": "Place Three",
        "parking": "stadium"
    },
    "geometry": {
        "type": "Point",
        "coordinates": [12.4,45.2]
    }
}];
// create your custom icon
var myIcon = L.icon({
		iconUrl: 'http://storage9.static.itmages.com/i/17/0205/h_1486291762_8801667_05ff292e9c.png',
		iconSize: [32, 37],
		iconAnchor: [16, 37],
		popupAnchor: [0, -28]
});
// function to get value from property "name" to populate for the popup
function onEachFeature(feature, layer) {
	layer.bindPopup(feature.properties.name);
}
// filter function, change from "parking" to "stadium", to show only one marker on the map
function soffParkingFilter(feature, layer) {
  if(feature.properties.parking === "parking") return true;
}

// add geojson to the map, click on the marker to see the popup
L.geoJSON(locations, {
	pointToLayer: function (feature, latlng) {
			return L.marker(latlng, {icon: myIcon});
	},
  filter: soffParkingFilter,
	onEachFeature: onEachFeature
}).addTo(map);