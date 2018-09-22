var map;
var uLat;
var uLong;


function initMap() {
  // The location of Uluru
  var toronto = {lat: 43.6532, lng: -79.3832}; //43.6532° N, 79.3832
  // The map, centered at Uluru
  map = new google.maps.Map(
      document.getElementById('map'), {zoom: 10, center: toronto});


  $.get("http://localhost:5000/getChildCareData", {lat: uLat, lon: uLong}, function(data){
    var child_care_centers = JSON.parse(data);
    for(var i=0; i<Object.keys(child_care_centers).length; i++){
      var marker = new google.maps.Marker({
        position: {lat: child_care_centers[i].LATITUDE, lng: child_care_centers[i].LONGITUDE},
        map: map,
        title: child_care_centers[i].LOC_NAME
      });
    }
  });
  // The marker, positioned at Uluru
  //var marker = new google.maps.Marker({position: toronto, map: map});
}

function sidebar_click(button) {
	button.classList.toggle("btn-light");
	button.classList.toggle("btn-dark");
	button.classList.toggle("active");
}

$(document).ready(function() {
  uLat = "43.599911"
  uLong = "-79.504631"
  initMap();
});
