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
        './WorldPoint'],
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
              WorldPoint) {

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
        wwd.redrawMe = redrawMe;
        var earthquakes = new USGS();
        var annotationController = new AnnotationController(wwd);

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

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// JQuery API Calling
        $.get(earthquakes.getUrl(), function (EQ) {
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
        var earthquakeLayer;
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

        var drawingStates = {
            OFF : 0,
            ONE_V : 1,
            TWO_V : 2,
            ON: 3
        };
        var drawingState = drawingStates.ON;

        function redrawMe(minMagnitude, maxMagnitude, minDate, maxDate, reset) {
            if (reset === true) {
                earthquakes.setMinDate(earthquakes.initialQuery.fromDate);
                earthquakes.setMaxDate(earthquakes.initialQuery.toDate);
                earthquakes.setMinMagnitude(earthquakes.initialQuery.minMag);
                earthquakes.setMaxMagnitude(earthquakes.initialQuery.maxMag);
            }
            else {
                var minMagnitude = $("#magSlider").slider("values", 0);
                var maxMagnitude = $("#magSlider").slider("values", 1);

                var FromDate = $("#fromdatepicker").datepicker("getDate");
                var ToDate = $("#todatepicker").datepicker("getDate");

                earthquakes.setMinDate(FromDate);
                earthquakes.setMaxDate(ToDate);
                earthquakes.setMinMagnitude(minMagnitude);
                earthquakes.setMaxMagnitude(maxMagnitude);

                var minLong = Math.min(p2.Long, p1.Long);
                var maxLong = Math.max(p2.Long, p1.Long);

                var minLati = Math.min(p2.Lati, p1.Lati);
                var maxLati = Math.max(p2.Lati, p1.Lati);
            }
            var drawOpition = 0;
            var drawFig = 0;
            $.get(earthquakes.getUrl(drawOpition, drawingState, drawFig), function (EQ) {
                wwd.removeLayer(earthquakeLayer);
                placeMarkCreation(EQ);
            });
        }

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        var p1 = new WorldPoint(wwd);
        var p2 = new WorldPoint(wwd);
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//  Pre-populate dropdowns with initial dates
        $("#fromdatepicker").datepicker("setDate", earthquakes.initialQuery.fromDate.split("T")[0]);
        $("#todatepicker").datepicker("setDate", earthquakes.initialQuery.toDate.split("T")[0]);
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        function placeMarkCreation(GeoJSON) {
            var minMagnitude = $("#magSlider").slider("values", 0);
            var maxMagnitude = $("#magSlider").slider("values", 1);

            var opacity = $("#opacitySlider").slider("value");

            var FromDate = $("#fromdatepicker").datepicker("getDate");
            var ToDate = $("#todatepicker").datepicker("getDate");
            // console.log(MaxDatePicker);


            // window.redraw(minMagnitude,maxMagnitude,minDate,maxDate, window.limitQuery, window.polygonLayer, wwd.surfaceOpacity, opacity);

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
            // Polygon Generation
            function polygonGeneration() {
                earthquakeLayer = new WorldWind.RenderableLayer("Earthquakes");

                for (var i = 0; i < GeoJSON.features.length; i++) {
                    // var polygon = new EQPolygon(GeoJSON.features[i].geometry['coordinates']);
                    // polygonLayer.addRenderable(polygon.polygon);

                    // var polygon = new Cylinder(GeoJSON.features[i].geometry['coordinates'], GeoJSON.features[i].properties['mag'] * 5e5);
                    // polygonLayer.addRenderable(polygon.cylinder);

                    var placeMark = new EQPlacemark(GeoJSON.features[i].geometry.coordinates, GeoJSON.features[i].properties.mag);
                    earthquakeLayer.addRenderable(placeMark.placemark);
                }
            }
            polygonGeneration();
            wwd.addLayer(earthquakeLayer);


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

            minMagnitudePlaceholder.textContent = earthquakes.minMagnitude;
            maxMagnitudePlaceholder.textContent = earthquakes.maxMagnitude;

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

            var drawLayer = new WorldWind.RenderableLayer("Drawing");
            wwd.addLayer(drawLayer);


            var handleClick = function (event) {
                if (drawingState != drawingStates.OFF && $("#flip-1").val() != "off") {
                    var x = event.clientX,
                        y = event.clientY;
                    var placeMark;

                    if (drawingState == drawingStates.ONE_V) {
                        p2.update3Dfrom2D(x, y);

                        placeMark = new Point([p2.Long, p2.Lati, 0]);
                        drawLayer.addRenderable(placeMark.placemark);

                        var queryFig = drawFig(p1, p2);
                        drawingState = drawingStates.TWO_V;
                        redrawMe(queryFig);
                        // drawingState = drawingStates.OFF;
                    }
                    else if (drawingState == drawingStates.ON) {
                        p1.update3Dfrom2D(x, y);

                        placeMark = new Point([p1.Long, p1.Lati, 0]);
                        drawLayer.addRenderable(placeMark.placemark);

                        drawingState = drawingStates.ONE_V;
                    }
                }
            };

            function drawFig(p1, p2) {
                if ($("#flip-1").val() == "rectangle") {
                    return drawRectangle(p1, p2);
                }
                else if ($("#flip-1").val() == "circle") {
                    return drawCircle(p1, p2);
                }
            }

            function drawRectangle(p1, p2) {
                var myRectangle = new Rectangle(p1, p2);
                drawLayer.addRenderable(myRectangle);
                return myRectangle;
            }

            function drawCircle(p1, p2) {
                var myCircle = new Circle(p1, p2);
                // drawLayer.addRenderable(myCircle);
                return myCircle;
            }

            // Listen for mouse moves and highlight the placemarks that the cursor rolls over.
            wwd.addEventListener("mousemove", handlePick);

            // Listen for taps on mobile devices and highlight the placemarks that the user taps.
            var tapRecognizer = new WorldWind.TapRecognizer(wwd, handlePick);

            // Listen for mouse moves and highlight the placemarks that the cursor rolls over.
            wwd.addEventListener("mousedown", handleClick);

        }

    });
