var map;
var uLat;
var uLong;
var infowindow;


function initMap() {

  var toronto = {lat: 43.6532, lng: -79.3832}; //43.6532 N, 79.3832 W
  // The map, centered at Toronto
  map = new google.maps.Map(
      document.getElementById('map'), {zoom: 10, center: toronto});


  $.get("http://localhost:5000/getChildCareData", {lat: uLat, lon: uLong}, function(data){
    var child_care_centers = JSON.parse(data);
    for(var i=0; i<Object.keys(child_care_centers).length; i++){
      new_marker(child_care_centers[i]);
    }
  });
}

//infowindow = new google.maps.InfoWindow();


function loc_infowindow(info) {
  return `<table class='table'>
      <tbody>
        <tr> 
          <th scope="row">` + info.LOC_NAME + `</th>
        <tr>
          <th scope="row">Phone</th>
          <td>` + info.PHONE + `</td>
        </tr>
        </tbody>
        </table>`;
}
      
function new_marker(info) {
  var marker = new google.maps.Marker({
    position: {lat: info.LATITUDE, lng: info.LONGITUDE},
    map: map,
    title: info.LOC_NAME
  });

  infowindow = new google.maps.InfoWindow({
    content: loc_infowindow(info)
  });
  
  marker.addListener('click', function() {
    //infowindow.setContent(loc_infowindow(info))
    infowindow.setContent(
    `<table class='table'>
    <tbody>
      <tr> 
        <th scope="row">` + info.LOC_NAME + `</th>
      <tr>
        <th scope="row">Phone</th>
        <td>` + info.PHONE + `</td>
      </tr>
      </tbody>
    </table>`)
    infowindow.open(map, marker);
  });
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