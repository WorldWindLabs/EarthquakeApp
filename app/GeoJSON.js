/*
 * Copyright (C) 2014 United States Government as represented by the Administrator of the
 * National Aeronautics and Space Administration. All Rights Reserved.
 */

var limitQuery = 50;

var redraw = function(minMagnitude, maxMagnitude, minDate, maxDate, limit, layer)
{
	console.log("fuck " + limit.toString());
	var currentTimeUTC = +new Date();
	var minDateISO = new Date(currentTimeUTC + minDate*24*60*60*1000).toISOString().split(/[-]+/);
	var maxDateISO = new Date(currentTimeUTC + maxDate*24*60*60*1000).toISOString().split(/[-]+/);
	minDateISO[minDateISO.length - 1] = minDateISO[minDateISO.length - 1].split('.')[0];
	maxDateISO[maxDateISO.length - 1] = maxDateISO[maxDateISO.length - 1].split('.')[0];

	layer.removeAllRenderables();
	console.log("removed renders");
	var resourcesUrl = "http://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson";
	var query = "starttime="+minDateISO.join('-')+"&endtime="+maxDateISO.join('-')+"&minmagnitude=" +
	            minMagnitude.toString() + "&maxmagnitude=" + maxMagnitude.toString() + "&orderby=magnitude&limit=" + limit.toString();
	var polygonGeoJSON = new WorldWind.GeoJSONParser(resourcesUrl + "&" + query);
	console.log("got query");
	polygonGeoJSON.load(shapeConfigurationCallback, layer);
	console.log("loaded geojson shit");
};


var shapeConfigurationCallback = function (geometry, properties)
{
	var configuration = {};

	var placemarkAttributes = new WorldWind.PlacemarkAttributes(null);
	placemarkAttributes.imageScale = 0.1;
	placemarkAttributes.imageColor = WorldWind.Color.WHITE;
	placemarkAttributes.labelAttributes.offset = new WorldWind.Offset(
		WorldWind.OFFSET_FRACTION, 0.5,
		WorldWind.OFFSET_FRACTION, 1.5);
	placemarkAttributes.imageSource = WorldWind.configuration.baseUrl + "images/white-dot.png";

	if (geometry.isPointType() || geometry.isMultiPointType())
	{
		configuration.attributes = new WorldWind.PlacemarkAttributes(placemarkAttributes);

		/*
		 if (properties && properties.place)
		 {
		 configuration.name = properties.place;
		 }
		 */

		if (properties && properties.time)
		{
			var date = (+new Date(properties.time));
			var utcDate  = (+new Date());

			if (utcDate - date > (30*24*60*60*1000))
			{
				configuration.attributes.imageColor = WorldWind.Color.GREEN;
			}
			else if (utcDate - date > (8*24*60*60*1000))
			{
				configuration.attributes.imageColor = WorldWind.Color.YELLOW;
			}
			else if (utcDate - date > (24*60*60*1000))
			{
				configuration.attributes.imageColor = WorldWind.Color.ORANGE;
			}
			else
			{
				configuration.attributes.imageColor = WorldWind.Color.RED;
			}
		}

		if (properties && properties.mag)
		{
			var min = $("#magSlider").slider("values",0);
			var max = $("#magSlider").slider("values",1);
			configuration.attributes.imageScale = ((properties.mag - min + 1) / (max - min)) * 0.25;
		}
	}


	return configuration;
};

requirejs(['../src/WorldWind', './LayerManager', './AnnotationController', './CoordinateController'],
    function (ww, LayerManager, AnnotationController, CoordinateController)
    {
        "use strict";

        WorldWind.Logger.setLoggingLevel(WorldWind.Logger.LEVEL_WARNING);

        var wwd = new WorldWind.WorldWindow("canvasOne");

	    var annotationController = new AnnotationController(wwd);

        var layers = [
            {layer: new WorldWind.BMNGLayer(), enabled: true},
            {layer: new WorldWind.BMNGLandsatLayer(), enabled: false},
            {layer: new WorldWind.CompassLayer(), enabled: false},
            {layer: new WorldWind.CoordinatesDisplayLayer(wwd), enabled: true},
            {layer: new WorldWind.ViewControlsLayer(wwd), enabled: false}
        ];

        for (var l = 0; l < layers.length; l++)
        {
            layers[l].layer.enabled = layers[l].enabled;
            wwd.addLayer(layers[l].layer);
        }

	    var polygonLayer = new WorldWind.RenderableLayer("Polygon");
	    wwd.addLayer(polygonLayer);

	    var layerManger = new LayerManager(wwd);

	    var minMagnitude = $("#magSlider").slider("values",0);
	    var maxMagnitude = $("#magSlider").slider("values",1);
	    var minDate = $("#dateSlider").slider("values",0);
	    var maxDate = $("#dateSlider").slider("values",1);

	    window.redraw(minMagnitude,maxMagnitude,minDate,maxDate, window.limitQuery, polygonLayer);

	    wwd.goTo(new WorldWind.Position(31.956578,35.945695,25500*1000))


    });