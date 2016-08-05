/*
 * Copyright (C) 2014 United States Government as represented by the Administrator of the
 * National Aeronautics and Space Administration. All Rights Reserved.
 */
define(['./Circle',
        './Cylinder',
        './LayerManager',
        './EQPolygon',
        './EQPlacemark',
        './USGS',
        './worldwindlib',
        './AnnotationController',
        './Point',
        './Rectangle',
        './TectonicPlateLayer',
        './WorldPoint',
        './Draw',
        './MetadataDisplay'],
    function (Circle,
              Cylinder,
              LayerManager,
              EQPolygon,
              EQPlacemark,
              USGS,
              WorldWind,
              AnnotationController,
              Point,
              Rectangle,
              TectonicPlateLayer,
              WorldPoint,
              Draw,
              Metadata) {

        "use strict";

        // WorldWind Canvas
        WorldWind.Logger.setLoggingLevel(WorldWind.Logger.LEVEL_WARNING);

        var wwd = new WorldWind.WorldWindow("canvasOne");
        // Enable sub-surface rendering for the World Window.
        wwd.subsurfaceMode = true;
        // Enable deep picking in order to detect the sub-surface shapes.
        wwd.deepPicking = true;
        // Make the surface semi-transparent in order to see the sub-surface shapes.
        wwd.surfaceOpacity = 0.5;

        var Control = function () {
            var earthquakes =  new USGS(wwd, this);
            var metadata = new Metadata();
            this.handler = new Draw(wwd, metadata);
            var Opacity = 0.5;
            var UIController = new AnnotationController(wwd, earthquakes.parameters, this);

            this.redraw = function () {
                earthquakes.redraw(this.handler);
            };

            this.getOpacity = function () {
                return this.Opacity;
            };

            this.setOpacity = function (value) {
                this.Opacity = value;
                wwd.surfaceOpacity = this.Opacity;
            };

            this.initializeHandlers = function () {
                // Listen for mouse moves and highlight the placemarks that the cursor rolls over.
                wwd.addEventListener("mousemove", myControl.handler.Pick);

                // Listen for taps on mobile devices and highlight the placemarks that the user taps.
                var tapRecognizer = new WorldWind.TapRecognizer(wwd, myControl.handler.Pick);

                // Listen for mouse moves and highlight the placemarks that the cursor rolls over.
                wwd.addEventListener("mousedown", myControl.handler.Click);
            };

        };

        var layers = [
            {layer: new WorldWind.BMNGLayer(), enabled: true},
            {layer: new WorldWind.CompassLayer(), enabled: false},
            {layer: new WorldWind.CoordinatesDisplayLayer(wwd), enabled: true},
            {layer: new WorldWind.ViewControlsLayer(wwd), enabled: true},
            {layer: new TectonicPlateLayer, enabled: true}
        ];

        for (var l = 0; l < layers.length; l++) {
            layers[l].layer.enabled = layers[l].enabled;
            wwd.addLayer(layers[l].layer);
        }

        // Layer Manager
        var layerManger = new LayerManager(wwd);

        var myControl  = new Control();
        myControl.redraw();

    });
