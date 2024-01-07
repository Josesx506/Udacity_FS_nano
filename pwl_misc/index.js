function initMap() {
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 14,
        center: { lat: 6.441864, lng: 3.469624 },
        mapTypeId: "terrain",
    });

  
    // Declare outerCoords as a global variable. 
    // These initial coordinates can be anywhere in the world because they'll be updated by the map boundaries
    let outerCoords = [ 
      { lat: 6.780472, lng: 3.814708 }, 
      { lat: 6.348258, lng: 3.814708 },
      { lat: 6.348258, lng: 3.296062 },
      { lat: 6.780472, lng: 3.296062 },
      { lat: 6.780472, lng: 3.814708 }, 
    ];
  
    // Function to update the outer polygon based on the current map bounds
    function updateOuterPolygon() {
      const bounds = map.getBounds();
      const ne = bounds.getNorthEast();
      const sw = bounds.getSouthWest();
  
      // Update outerCoords based on the current map bounds.
      // This is implemented in a clockwise version from the NE
      outerCoords = [
        { lat: ne.lat(), lng: ne.lng() },
        { lat: sw.lat(), lng: ne.lng() },
        { lat: sw.lat(), lng: sw.lng() },
        { lat: ne.lat(), lng: sw.lng() },
        { lat: ne.lat(), lng: ne.lng() },
      ];
  
      // Set the paths for the polygon
      lekkiRectangle.setPaths([outerCoords, innerCoords]);
    }
    
    // Define the LatLng coordinates for the polygon's path. A kml polygon can be inserted here.
    // Note: This inner polygon MUST be anticlockwise from the NE to create a hole in the outerCoords
    const innerCoords = [
        { lat: 6.464471, lng: 3.496661 },
        { lat: 6.464471, lng: 3.453797 },
        { lat: 6.444400, lng: 3.423797 },
        { lat: 6.421468, lng: 3.453797 },
        { lat: 6.421468, lng: 3.496661 },
        { lat: 6.464471, lng: 3.496661 },
    ];

    // Add an event listener to update the outer polygon when the bounds change
    google.maps.event.addListener(map, 'bounds_changed', updateOuterPolygon);
  
    // Construct the polygon with the initial outerCoords.
    const lekkiRectangle = new google.maps.Polygon({
      paths: [outerCoords, innerCoords],
      strokeColor: "white",
      strokeOpacity: 0.0,
      strokeWeight: 2,
      fillColor: "gray",
      fillOpacity: 0.5,
      // zIndex: 2,
      clickable: true,
    });

    
    // Get the geographic coordinates from the mouse click
    google.maps.event.addListener(map, 'click', function(e){
      var lng = e.latLng.lng();
      var lat = e.latLng.lat();
      console.log(lng,lat)
    });
    
    // Apply the polygon to the map object
    lekkiRectangle.setMap(map);

  }
  
  window.initMap = initMap;
  