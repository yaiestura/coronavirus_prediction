am4core.ready(function() {
    am4core.useTheme(am4themes_animated);

    // Create map instance
    var chart = am4core.create("chartdiv", am4maps.MapChart);
    
    // Set map definition
    chart.geodata = am4geodata_worldLow;
    
    // Set projection
    chart.projection = new am4maps.projections.Miller();
    
    // Create map polygon series
    var polygonSeries = chart.series.push(new am4maps.MapPolygonSeries());
    
    // Exclude Antartica
    polygonSeries.exclude = ["AQ"];
    
    // Make map load polygon (like country names) data from GeoJSON
    polygonSeries.useGeodata = true;
    
    // Configure series
    var polygonTemplate = polygonSeries.mapPolygons.template;
    polygonTemplate.tooltipText = "{name}";
    polygonTemplate.fill = am4core.color("#74B266");
    
    // Create hover state and set alternative fill color
    var hs = polygonTemplate.states.create("hover");
    hs.properties.fill = am4core.color("#367B25");
    
    // Create active state
    var as = polygonTemplate.states.create("active");
    as.properties.fill = am4core.color("#7B3625");
    
    chart.events.on("ready", function(ev) {
      var italy = polygonSeries.getPolygonById("IT");
      
      // Pre-zoom
      chart.zoomToMapObject(italy);
      
      // Set active state
      setTimeout(function() {
        italy.isActive = true;
      }, 1000);
    });
});
