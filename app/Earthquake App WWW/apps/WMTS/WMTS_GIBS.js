/*
 * Copyright (C) 2014 United States Government as represented by the Administrator of the
 * National Aeronautics and Space Administration. All Rights Reserved.
 */
/**
 * @version $Id: WMTS_GIBS.js 2016-06-09 rsirac $
 */


requirejs(['../../src/WorldWind',
        '../../examples/MyLayerManager'],
    function (ww, LayerManager) {
        "use strict";

        ww.configuration.baseUrl += "../";

        WorldWind.Logger.setLoggingLevel(WorldWind.Logger.LEVEL_WARNING);

        var wwd = new WorldWind.WorldWindow("canvasOne");

        // NASA layers
        var wmtsCapabilities;

        $.get('http://map1.vis.earthdata.nasa.gov/wmts-webmerc/wmts.cgi?SERVICE=WMTS&request=GetCapabilities', function (response) {
            wmtsCapabilities = new WorldWind.WmtsCapabilities(response);
        })
            .done(function () {
                // Internal layer
                var layers = [
                    {layer: new WorldWind.BMNGLandsatLayer(), enabled: true}
                ];

	            var data = [];

                // GIBS layers
                for (var i = 0 ; i < wmtsCapabilities.contents.layer.length ; i++ ) {
	                var gibs_layer = new WorldWind.WmtsLayer(WorldWind.WmtsLayer.formLayerConfiguration(wmtsCapabilities.contents.layer[i]), "2016-07-21");
	                data.push(gibs_layer.displayName);

                    layers.push({layer: gibs_layer, enabled: false});
                }

	            var html_layers = "<label><select class=\"combobox\"><option></option>";

	            for (var j = 0; j < data.length; j++)
	            {
		            html_layers += "<option><a >" + data[j] + "</a></option>";
	            }

	            html_layers += "</select></label>";

	            $("#layers_options").html(html_layers);

	            // Internal layers
                layers.push(
                    {layer: new WorldWind.CompassLayer(), enabled: false},
                    {layer: new WorldWind.CoordinatesDisplayLayer(wwd), enabled: true},
                    {layer: new WorldWind.ViewControlsLayer(wwd), enabled: true}
                );

                for (var l = 0; l < layers.length; l++) {
                    layers[l].layer.enabled = layers[l].enabled;
                    wwd.addLayer(layers[l].layer);
                }

                // Create a layer manager for controlling layer visibility.
                var layerManager = new LayerManager(wwd);

	            $('.combobox').combobox();

            });
    });