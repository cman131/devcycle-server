
  $(document).ready(function () {
  
    init();
    
    var UPDATE_DELAY = 1000;
    var RESUME_DELAY = 3000;
    var BLOCK_SIZE = 3;
    
    var projection = new OpenLayers.Projection("EPSG:4326")
    var queuedFrames = [];
    var frameBlock = 0;
    var totalFrames = 0;
    var playingInterval = 0;
    var playTimer;
    
    var point_layer = new OpenLayers.Layer.Vector("rider_points", {renderers: ['Canvas']});
    
    map.addLayer(point_layer);
    
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
    
    var formatDate = function(date) {
      var hours   = date.getHours();
      var minutes = date.getMinutes();

      if (hours   < 10) {hours   = "0"+hours;}
      if (minutes < 10) {minutes = "0"+minutes;}
      
      return (date.getMonth() + 1) + "/" + date.getDate() + "/" + date.getFullYear() + " " + hours + ":" + minutes;
    }
    
    var drawRiderPoints = function(data) {
          point_layer.destroyFeatures();
          
          var times = data.shift();    
          var start_time = new Date(times.start * 1000);
          var end_time = new Date(times.end * 1000);     
          $("#playback_time").html("<b>" + formatDate(end_time) + "<b>");
          
          var percent = (playingInterval + 1)/totalFrames * 100;
          $("#playback_progess_bar").width(percent + "%");
          if(playingInterval == 0) {
            $("#playback_progress").addClass('active');
          } else if(playingInterval + 1 == totalFrames) {
            $("#playback_progress").removeClass('active');
          }
          
          $(data).each(function() {
              _this = this;
              var lonLat = new OpenLayers.LonLat( _this[1], _this[2])
                .transform(
                  projection, // transform from WGS 1984
                  map.getProjectionObject() // to Spherical Mercator Projection
                );
                
              var point = new OpenLayers.Geometry.Point(lonLat.lon, lonLat.lat);
              
              //determine speed style
              var style; 
              if(_this[0] < 3 ) {
                  style = slow_speed_style;  
              }else if(_this[0] < 5) {
                  style = caution_speed_style;
              } else {
                  style = healthy_speed_style;
              }
              
              var feature = new OpenLayers.Feature.Vector(point, null, style);
              point_layer.addFeatures([feature]);
          });  
    };
    
    var queueFrames = function(data) {
      totalFrames = data.total;
      $(data.frames).each(function() {
        queuedFrames.push(this);
      });  
    }
    
    var getPlaybackData = function() {
         var request = $.ajax({
          url: '/playback/frames/',
          data: {
            block: frameBlock
          },
          type: 'GET'
        }).done(function (data) {
          queueFrames(data);   
        }).fail(function () {
          frameBlock = frameBlock - BLOCK_SIZE;
          if(playTimer != null) {
            clearTimeout(playTimer);
          }
          alert("Error with playback. Please refresh page and play again.");
        });
        frameBlock = frameBlock + BLOCK_SIZE;
        return request;
    };
    
    var play = function() {
      
      if(queuedFrames.length === 0 && playingInterval === totalFrames) {
        $('#pause').hide();
        $('#play').show();
        
        frameBlock = 0;
        playingInterval = 0;
         
        return;
      }
      drawRiderPoints(queuedFrames.shift());
      playingInterval = playingInterval + 1;
      if(queuedFrames.length < BLOCK_SIZE && queuedFrames.length + playingInterval < totalFrames) {
        getPlaybackData();
      }
      playTimer = setTimeout(play, UPDATE_DELAY);  
    }
    
    $('#play').click(function() {
        $("#playback_progess_bar").width(0 + "%");
        var request = getPlaybackData();
        $('#play').hide();
        $('#pause').show();
    
      $.when(request).done(function(){
        play();
      });  
    });
    
    $('#pause').click(function() {
      $('#pause').hide();
      $('#restart').show();
      $("#playback_progress").removeClass('active');
      clearTimeout(playTimer); 
    });
    
    $('#restart').click(function() {
      $('#restart').hide();
      $('#pause').show();
      $("#playback_progress").addClass('active');
      playTimer = setTimeout(play, RESUME_DELAY);      
    });  

  });
