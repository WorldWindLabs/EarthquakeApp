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
        './TectonicPlateLayer'],
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
              TectonicPlateLayer) {

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
        function redrawMe(minMagnitude, maxMagnitude, minDate, maxDate) {
            earthquakes.setMinDate(minDate);
            earthquakes.setMaxDate(maxDate);
            earthquakes.setMinMagnitude(minMagnitude);
            earthquakes.setMaxMagnitude(maxMagnitude);

            $.get(earthquakes.getUrl(), function (EQ) {
                wwd.removeLayer(earthquakeLayer);
                placeMarkCreation(EQ);
            });
        }

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//         this.p1 = {};
//         this.p2 = {};

        var p1 = {};
        var p2 = {};

        function placeMarkCreation(GeoJSON) {
            var minMagnitude = $("#magSlider").slider("values", 0);
            var maxMagnitude = $("#magSlider").slider("values", 1);
            var minDate = $("#dateSlider").slider("values", 0);
            var maxDate = $("#dateSlider").slider("values", 1);
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

            var drawingStates = {
                OFF : 0,
                ONE_V : 1,
                TWO_V : 2,
                ON: 3
            };

            var drawLayer = new WorldWind.RenderableLayer("Drawing");
            wwd.addLayer(drawLayer);
            var drawingState = drawingStates.ON;

            var handleClick = function (event) {
                // drawCircle();

                if (drawingState != drawingStates.OFF && $("#flip-1").val() != "off") {
                    var x = event.clientX,
                        y = event.clientY;

                    var pickList = wwd.pick(wwd.canvasCoordinates(x, y)),
                        long = pickList.objects[0].position.longitude,
                        lati = pickList.objects[0].position.latitude,
                        alti = pickList.objects[0].position.altitude;

                    var earthCoordinates = [long, lati, 0];
                    var placeMark = new Point(earthCoordinates);
                    drawLayer.addRenderable(placeMark.placemark);
                    if (drawingState == drawingStates.ONE_V) {
                        p2.X = x;
                        p2.Y = y;
                        p2.Long = long;
                        p2.Lati = lati;
                        drawFig(p1, p2);
                        queriesRegion(p1, p2);
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

            function queriesRegion(p1, p2) {
                var minLong = Math.min(p2.Long, p1.Long);
                var maxLong = Math.max(p2.Long, p1.Long);

                var minLati = Math.min(p2.Lati, p1.Lati);
                var maxLati = Math.max(p2.Lati, p1.Lati);

                earthquakes.setMinLatitude(minLati);
                earthquakes.setMaxLatitude(maxLati);
                earthquakes.setMinLongitude(minLong);
                earthquakes.setMaxLongitude(maxLong);

                var drawing = 1;

                $.get(earthquakes.getUrl(drawing), function (EQ) {
                    wwd.removeLayer(earthquakeLayer);
                    placeMarkCreation(EQ);
                });

            }

            function drawFig(p1, p2) {
                if ($("#flip-1").val() == "rectangle") {
                    drawRectangle(p1, p2);
                }
                else if ($("#flip-1").val() == "circle") {
                    drawCircle(p1, p2);
                }
            }

            function drawRectangle(p1, p2) {
                drawLayer.addRenderable(new Rectangle(p1, p2));
            }

            function drawCircle(p1, p2) {
                function getDistanceFromLatLonInKm(lat1,lon1,lat2,lon2) {
                    var R = 6371; // Radius of the earth in km
                    var dLat = deg2rad(lat2-lat1);  // deg2rad below
                    var dLon = deg2rad(lon2-lon1);
                    var a =
                            Math.sin(dLat/2) * Math.sin(dLat/2) +
                            Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) *
                            Math.sin(dLon/2) * Math.sin(dLon/2)
                        ;
                    var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
                    var d = R * c; // Distance in km
                    return d;
                }

                function deg2rad(deg) {
                    return deg * (Math.PI/180)
                }

                var radius = getDistanceFromLatLonInKm(p1.Lati, p1.Long, p2.Lati, p2.Long);

                var minLong = Math.min(p2.Long, p1.Long);
                var maxLong = Math.max(p2.Long, p1.Long);

                var minLati = Math.min(p2.Lati, p1.Lati);
                var maxLati = Math.max(p2.Lati, p1.Lati);

                var canvas = document.createElement("canvas"),
                    ctx2d = canvas.getContext("2d"),
                    size = 64, c = size / 2  - 0.5, innerRadius = 5, outerRadius = 30;

                canvas.width = size;
                canvas.height = size;

                var gradient = ctx2d.createRadialGradient(c, c, outerRadius-1, c, c, outerRadius);
                gradient.addColorStop(0, 'rgb(255, 0, 0)');
                gradient.addColorStop(0.5, 'rgb(0, 255, 0)');
                gradient.addColorStop(1, 'rgb(255, 0, 0)');

                // ctx2d.fillStyle = gradient;
                ctx2d.arc(c, c, outerRadius, 0, 2 * Math.PI, false);
                ctx2d.fill();


                var mydownloadingImage = new Image();
                mydownloadingImage.onload = function(){
                    // imageCircle.src = this.src;
                };
                mydownloadingImage.src = "./images/circle.png";

                // Create the mesh's positions.
                var meshPositions = [];
                for (var lat = minLati; lat <= maxLati; lat += 0.5) {
                    var row = [];
                    for (var lon = minLong; lon <= maxLong; lon += 0.5) {
                        row.push(new WorldWind.Position(lat, lon, 100e3));
                    }

                    meshPositions.push(row);
                }

                // Create the mesh.
                var mesh = new WorldWind.GeographicMesh(meshPositions, null);

                // Create and assign the mesh's attributes.
                var meshAttributes = new WorldWind.ShapeAttributes(null);
                // meshAttributes.outlineColor = WorldWind.Color.BLUE;
                meshAttributes.drawOutline = false;
                meshAttributes.interiorColor = new WorldWind.Color(1, 1, 1, 0.7);
                meshAttributes.imageSource = new WorldWind.ImageSource(mydownloadingImage);
                meshAttributes.applyLighting = false;
                mesh.attributes = meshAttributes;

                // Create and assign the mesh's highlight attributes.
                var highlightAttributes = new WorldWind.ShapeAttributes(meshAttributes);
                highlightAttributes.outlineColor = WorldWind.Color.WHITE;
                mesh.highlightAttributes = highlightAttributes;

                // Add the shape to the layer.
                drawLayer.addRenderable(mesh);
            }

            // Listen for mouse moves and highlight the placemarks that the cursor rolls over.
            wwd.addEventListener("mousemove", handlePick);

            // Listen for taps on mobile devices and highlight the placemarks that the user taps.
            var tapRecognizer = new WorldWind.TapRecognizer(wwd, handlePick);

            // Listen for mouse moves and highlight the placemarks that the cursor rolls over.
            wwd.addEventListener("mousedown", handleClick);

        }

    });
