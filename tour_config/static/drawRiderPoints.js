
  $(document).ready(function () {
    
    init();
  
    var projection = new OpenLayers.Projection("EPSG:4326");
    
    var drawRiderPoints = function(data) {
        var SpeedStyle = function(color){
          this.pointRadius = 3,
          this.strokeOpacity = 0.5,
          this.fillOpacity = 0.5,
          this.strokeColor = color,
          this.fillColor = color
        };
        
        var slow_speed_style = new SpeedStyle("#FF0000");
        
        var caution_speed_style = new SpeedStyle("#FF9900");
        
        var healthy_speed_style = new SpeedStyle("#00FF00");
        
        layer = new OpenLayers.Layer.Vector("rider_points", {renderers: ['Canvas']});
        
        $(data.locations).each(function() {
            _this = this;
            var pointCount = _this.length;
            $(_this).each(function(index) {
              _that = this;
              var lonLat = new OpenLayers.LonLat( _that[1], _that[2])
                .transform(
                  projection, // transform from WGS 1984
                  map.getProjectionObject() // to Spherical Mercator Projection
                );
                
              var point = new OpenLayers.Geometry.Point(lonLat.lon, lonLat.lat);
              
              //determine speed sytle
              var style; 
              if(_that[0] < 3 ) {
                  style = slow_speed_style;  
              }else if(_that[0] < 5) {
                  style = caution_speed_style;
              } else {
                  style = healthy_speed_style;
              }
              
              style.fillOpacity = 0.6 - (0.6 * index / pointCount); 
              
              var feature = new OpenLayers.Feature.Vector(point, null, style);
              layer.addFeatures([feature]);
            }); 
        });
        map.addLayer(layer); 
    };
    
    var getRiderPoints = function() {
         $.ajax({
          url: '/location_update/recent/',
          type: 'GET'
        }).done(function (data) {
          drawRiderPoints(data);   
        }).fail(function () {
          alert("Error retrieving points");
        });
    };
    
    //populate map
    getRiderPoints();
    setInterval(getRiderPoints, 300000);
  });
