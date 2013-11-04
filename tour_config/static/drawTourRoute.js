  var route_layer;
  
  $(document).ready(function () {
  
    var projection = new OpenLayers.Projection("EPSG:4326")
    
    var drawTourRoute = function(data) {
      var style = {
          strokeColor: "#000000",
          strokeWidth: 3,
          strokeDashstyle: "dashdot",
          pointRadius: 6,
          pointerEvents: "visiblePainted",
          title: 'route'
      };
      
      route_layer = new OpenLayers.Layer.Vector("tour_route");
      
      var pointList = [];
        $(data.route[0]).each(function( index ) {
            var _this = this;
            var lonLat = new OpenLayers.LonLat( _this[0], _this[1])
              .transform(
                projection, // transform from WGS 1984
                map.getProjectionObject() // to Spherical Mercator Projection
              );
            var point = new OpenLayers.Geometry.Point(lonLat.lon, lonLat.lat);
            pointList.push(point);
        });
        
        var lineFeature = new OpenLayers.Feature.Vector(
            new OpenLayers.Geometry.LineString(pointList),null,style);
  
        route_layer.addFeatures([lineFeature]);      
        map.addLayer(route_layer);    
      };
      
      var getTourRoute = function() {
        $.ajax({
          url: '/route/',
          type: 'GET'
        }).done(function (data) {
            if (data.route.length > 0) {
                drawTourRoute (data);  
            }
          }).fail(function () {
            alert("Error retrieving route");
          });
      };
      
    //draw route on map
    getTourRoute();
    
  });
