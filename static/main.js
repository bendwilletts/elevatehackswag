var map;  
// Initialize and add the map
function initMap() {
  // The location of Uluru
  var toronto = {lat: 43.6532, lng: -79.3832}; //43.6532° N, 79.3832
  // The map, centered at Uluru
  map = new google.maps.Map(
      document.getElementById('map'), {zoom: 10, center: toronto});
  // The marker, positioned at Uluru
  //var marker = new google.maps.Marker({position: toronto, map: map});
}

$(document).ready(function() {
	
  initMap();
});