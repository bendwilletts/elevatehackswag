
// Initialize and add the map
function initMap() {
  // The location of Uluru
  var toronto = {lat: 43.6532, lng: -79.3832}; //43.6532° N, 79.3832
  // The map, centered at Uluru
  var map = new google.maps.Map(
      document.getElementById('map'), {zoom: 10, center: toronto});
  // The marker, positioned at Uluru
  //var marker = new google.maps.Marker({position: toronto, map: map});
}

function sidebar_click(button) {
	button.classList.toggle("btn-light");
	button.classList.toggle("btn-dark");
	button.classList.toggle("active");
}

console.log("hello World");
$(document).ready(function() {
	
  initMap();
  var key = "AIzaSyBKCC5OXs0cKovC04ht8K4LvXfwvvHDfEc";
});
