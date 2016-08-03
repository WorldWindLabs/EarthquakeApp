/*
 * Copyright (C) 2014 United States Government as represented by the Administrator of the
 * National Aeronautics and Space Administration. All Rights Reserved.
 */
define(['./Cylinder',
        './LayerManager',
        './EQPolygon',
        './EQPlacemark',
        './USGS',
        './worldwindlib',
        './AnnotationController'],
    function (Cylinder,
              LayerManager,
              EQPolygon,
              EQPlacemark,
              USGS,
              WorldWind,
              AnnotationController) {

        "use strict";

        var redrawMe = function (minMagnitude, maxMagnitude, minDate, maxDate) {
            new_eq.setMinDate(minDate);
            new_eq.setMaxDate(maxDate);
            new_eq.setMinMagnitude(minMagnitude);
            new_eq.setMaxMagnitude(maxMagnitude);

            $.get(new_eq.getUrl(), function (EQ) {
                console.log(EQ.features.length);

                var layer = wwd.layers[5];
                layer.removeAllRenderables();
                wwd.layers = wwd.layers.slice(0, 5);
                placeMarkCreation(EQ);
            });
        };

        var new_eq = new USGS();

        // WorldWind Canvas
        WorldWind.Logger.setLoggingLevel(WorldWind.Logger.LEVEL_WARNING);

        var wwd = new WorldWind.WorldWindow("canvasOne");
        // Enable sub-surface rendering for the World Window.
        wwd.subsurfaceMode = true;
        // Enable deep picking in order to detect the sub-surface shapes.
        wwd.deepPicking = true;
        // Make the surface semi-transparent in order to see the sub-surface shapes.
        wwd.surfaceOpacity = 0.5;
        wwd.redrawMe = redrawMe;
        var annotationController = new AnnotationController(wwd);

        var layers = [
            {layer: new WorldWind.BMNGLayer(), enabled: true},
            // {layer: new WorldWind.BMNGLandsatLayer(), enabled: false},
            // {layer: new WorldWind.BingAerialWithLabelsLayer(null), enabled: false},
            // {layer: new WorldWind.CompassLayer(), enabled: false},
            {layer: new WorldWind.CoordinatesDisplayLayer(wwd), enabled: true},
            {layer: new WorldWind.ViewControlsLayer(wwd), enabled: true}
        ];

        for (var l = 0; l < layers.length; l++) {
            layers[l].layer.enabled = layers[l].enabled;
            wwd.addLayer(layers[l].layer);
        }

        // Layer Manager
        var layerManger = new LayerManager(wwd);

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// JQuery API Calling
        $.get(new_eq.getUrl(), function (EQ) {
            placeMarkCreation(EQ);
        });
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Data Display
// Individual Earthquakes
        var magnitudePlaceholder = document.getElementById('magnitude');
        var locPlaceholder = document.getElementById('location');
        var eventdatePlaceholder = document.getElementById('time');
        var latitudePlaceholder = document.getElementById('latitude');
        var longitudePlaceholder = document.getElementById('longitude');
        var depthPlaceholder = document.getElementById('depth');
// Query Metadata
        var earthquakecountPlaceholder = document.getElementById('eq_count');
        var min_datePlaceholder = document.getElementById('minDate');
        var max_datePlaceholder = document.getElementById('maxDate');
        var minMagnitudePlaceholder = document.getElementById('minMagnitude');
        var maxMagnitudePlaceholder = document.getElementById('maxMagnitude');

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        function placeMarkCreation(GeoJSON) {


            var minMagnitude = $("#magSlider").slider("values", 0);
            var maxMagnitude = $("#magSlider").slider("values", 1);
            var minDate = $("#dateSlider").slider("values", 0);
            var maxDate = $("#dateSlider").slider("values", 1);
            var opacity = $("#opacitySlider").slider("value");

            // window.redraw(minMagnitude,maxMagnitude,minDate,maxDate, window.limitQuery, window.polygonLayer, wwd.surfaceOpacity, opacity);

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
            // Polygon Generation
            var polygonGeneration = function () {
                var polygonLayer = new WorldWind.RenderableLayer("Depth (KM)");

                for (var i = 0; i < GeoJSON.features.length; i++) {
                    // var polygon = new EQPolygon(GeoJSON.features[i].geometry['coordinates']);
                    // polygonLayer.addRenderable(polygon.polygon);

                    // var polygon = new Cylinder(GeoJSON.features[i].geometry['coordinates'], GeoJSON.features[i].properties['mag'] * 5e5);
                    // polygonLayer.addRenderable(polygon.cylinder);

                    var placeMark = new EQPlacemark(GeoJSON.features[i].geometry.coordinates, GeoJSON.features[i].properties.mag);
                    polygonLayer.addRenderable(placeMark.placemark);
                }
                return polygonLayer;
            };
            wwd.addLayer(polygonGeneration());


////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
            // Metadata Display
            earthquakecountPlaceholder.textContent = GeoJSON.features.length;
            var startdate,
                enddate,
                GeoJSON_dates = [];
            for (var i = 0, len = GeoJSON.features.length; i < len; i++) {
                GeoJSON_dates.push(new Date(GeoJSON.features[i].properties.time));
            }
            startdate = new Date(Math.min.apply(null, GeoJSON_dates));
            enddate = new Date(Math.max.apply(null, GeoJSON_dates));

            min_datePlaceholder.textContent = startdate;
            max_datePlaceholder.textContent = enddate;

            minMagnitudePlaceholder.textContent = new_eq.minMagnitude;
            maxMagnitudePlaceholder.textContent = new_eq.maxMagnitude;

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
            // Highlight Picking
            var highlightedItems = [];

            // The common pick-handling function.
            var handlePick = function (o) {
                // The input argument is either an Event or a TapRecognizer. Both have the same properties for determining
                // the mouse or tap location.
                var x = o.clientX,
                    y = o.clientY;

                var redrawRequired = highlightedItems.length > 0; // must redraw if we de-highlight previously picked items

                // De-highlight any previously highlighted placemarks.
                for (var h = 0; h < highlightedItems.length; h++) {
                    highlightedItems[h].highlighted = false;
                }
                highlightedItems = [];

                // Perform the pick. Must first convert from window coordinates to canvas coordinates, which are
                // relative to the upper left corner of the canvas rather than the upper left corner of the page.
                var pickList = wwd.pick(wwd.canvasCoordinates(x, y));
                if (pickList.objects.length > 0) {
                    redrawRequired = true;
                }

                if (pickList.objects.length > 1) {
                    redrawRequired = true;
                }

                // Highlight the items picked by simply setting their highlight flag to true.
                if (pickList.objects.length > 0) {
                    for (var p = 0; p < pickList.objects.length; p++) {
                        pickList.objects[p].userObject.highlighted = true;
                        for (var eq = 0; eq < GeoJSON.features.length; eq++) {
                            if (pickList.objects[p].userObject.center &&
                                GeoJSON.features[eq].geometry.coordinates[1] == pickList.objects[p].userObject.center.latitude &&
                                GeoJSON.features[eq].geometry.coordinates[0] == pickList.objects[p].userObject.center.longitude) {
                                magnitudePlaceholder.textContent = GeoJSON.features[eq].properties.mag;
                                locPlaceholder.textContent = GeoJSON.features[eq].properties.place;
                                eventdatePlaceholder.textContent = new Date(GeoJSON.features[eq].properties.time);
                                latitudePlaceholder.textContent = GeoJSON.features[eq].geometry.coordinates[1];
                                longitudePlaceholder.textContent = GeoJSON.features[eq].geometry.coordinates[0];
                                depthPlaceholder.textContent = GeoJSON.features[eq].geometry.coordinates[2];
                            }
                        }

                        // Keep track of highlighted items in order to de-highlight them later.
                        highlightedItems.push(pickList.objects[p].userObject);

                        // Detect whether the placemark's label was picked. If so, the "labelPicked" property is true.
                        // If instead the user picked the placemark's image, the "labelPicked" property is false.
                        // Applications might use this information to determine whether the user wants to edit the label
                        // or is merely picking the placemark as a whole.
                        if (pickList.objects[p].labelPicked) {
                            console.log("Label picked");
                        }
                    }
                }

                // Update the window if we changed anything.
                if (redrawRequired) {
                    wwd.redraw(); // redraw to make the highlighting changes take effect on the screen
                }
            };

            var drawingStates = {
                OFF : 0,
                ONE_V : 1,
                TWO_V : 2,
                ON: 3
            };

            var drawLayer = new WorldWind.RenderableLayer("Drawing");
            wwd.addLayer(drawLayer);
            var drawingState = drawingStates.ON;
            var p1 = {}, 
                p2 = {};

            var handleClick = function (event) {

                if (drawingState != drawingStates.OFF) {
                    var x = event.clientX,
                        y = event.clientY;

                    var pickList = wwd.pick(wwd.canvasCoordinates(x, y)),
                        long = pickList.objects[0].position.longitude,
                        lati = pickList.objects[0].position.latitude,
                        alti = pickList.objects[0].position.altitude;

                    var earthCoordinates = [long, lati, 0];
                    var placeMark = new EQPlacemark(earthCoordinates, 7);
                    drawLayer.addRenderable(placeMark.placemark);
                    if (drawingState == drawingStates.ONE_V) {
                        p2.X = x;
                        p2.Y = y;
                        p2.Long = long;
                        p2.Lati = lati;
                        drawrectangle(p1, p2);
                        drawingState = drawingStates.OFF;
                    }
                    else if (drawingState == drawingStates.ON) {
                        drawingState = drawingStates.ONE_V;
                        p1.X = x;
                        p1.Y = y;
                        p1.Long = long;
                        p1.Lati = lati;
                    }

                }
            };

            var drawrectangle = function (p1, p2) {

                var minLong = Math.min(p2.Long, p1.Long);
                var maxLong = Math.max(p2.Long, p1.Long);

                var minLati = Math.min(p2.Lati, p1.Lati);
                var maxLati = Math.max(p2.Lati, p1.Lati);

                var boundaries = [];
                boundaries[0] = []; 
                boundaries[0].push(new WorldWind.Position(minLati, minLong, 1e5));
                boundaries[0].push(new WorldWind.Position(maxLati, minLong, 1e5));
                boundaries[0].push(new WorldWind.Position(maxLati, maxLong, 1e5));
                boundaries[0].push(new WorldWind.Position(minLati, maxLong, 1e5));

                // Create the polygon and assign its attributes.
                var polygon = new WorldWind.Polygon(boundaries, null);
                polygon.altitudeMode = WorldWind.ABSOLUTE;
                polygon.extrude = true;
                polygon.textureCoordinates = [
                    [new WorldWind.Vec2(0, 0), new WorldWind.Vec2(1, 0), new WorldWind.Vec2(1, 1), new WorldWind.Vec2(0, 1)]
                ];

                var polygonAttributes = new WorldWind.ShapeAttributes(null);
                // Specify a texture for the polygon and its four extruded sides.
                polygonAttributes.drawInterior = false;
                polygonAttributes.drawOutline = true;
                polygonAttributes.outlineColor = WorldWind.Color.BLUE;
                polygonAttributes.interiorColor = WorldWind.Color.WHITE;
                polygonAttributes.drawVerticals = polygon.extrude;
                polygonAttributes.applyLighting = true;
                polygon.attributes = polygonAttributes;
                var highlightAttributes = new WorldWind.ShapeAttributes(polygonAttributes);
                highlightAttributes.outlineColor = WorldWind.Color.RED;
                polygon.highlightAttributes = highlightAttributes;

                drawLayer.addRenderable(polygon);
            };

            // Listen for mouse moves and highlight the placemarks that the cursor rolls over.
            wwd.addEventListener("mousemove", handlePick);
            // wwd.addEventListener("mousemove", rectangleDrawer);

            // Listen for taps on mobile devices and highlight the placemarks that the user taps.
            var tapRecognizer = new WorldWind.TapRecognizer(wwd, handlePick);

            // Listen for mouse moves and highlight the placemarks that the cursor rolls over.
            wwd.addEventListener("mousedown", handleClick);



        }

    });
