/*
 * Copyright (C) 2014 United States Government as represented by the Administrator of the
 * National Aeronautics and Space Administration. All Rights Reserved.
 */
define(['./Cylinder',
    './LayerManager',
    './EQPolygon',
    './EQPlacemark',
    './USGS',
    './worldwindlib'],
    function(Cylinder,
     LayerManager,
     EQPolygon,
     EQPlacemark,
     USGS,
     WorldWind) {

    "use strict";

    var new_eq = new USGS();

    // layer.removeAllRenderables();


////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// JQuery API Calling
    $.get(new_eq.DecadeURL, function (EQ) {
        console.log(EQ.features[0].properties.mag);
        console.log(EQ.features[0].geometry.coordinates);
        placeMarkCreation(EQ);
    });
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Data Display
// function dataDisplay(EQ_GeoJSON) {
    var magnitudePlaceholder = document.getElementById('magnitude');
    var locPlaceholder = document.getElementById('location');
    var eventdatePlaceholder = document.getElementById('time');
    var latitudePlaceholder = document.getElementById('latitude');
    var longitudePlaceholder = document.getElementById('longitude');
    var depthPlaceholder = document.getElementById('depth');
// }

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    function placeMarkCreation(GeoJSON) {

        // WorldWind Canvas
        WorldWind.Logger.setLoggingLevel(WorldWind.Logger.LEVEL_WARNING);

        var wwd = new WorldWind.WorldWindow("canvasOne");
        // Enable sub-surface rendering for the World Window.
        wwd.subsurfaceMode = true;
        // Enable deep picking in order to detect the sub-surface shapes.
        wwd.deepPicking = true;
        // Make the surface semi-transparent in order to see the sub-surface shapes.
        wwd.surfaceOpacity = 0.5;

        // var annotationController = new AnnotationController(wwd);

        var layers = [
            {layer: new WorldWind.BMNGLayer(), enabled: true},
            {layer: new WorldWind.BMNGLandsatLayer(), enabled: false},
            {layer: new WorldWind.BingAerialWithLabelsLayer(null), enabled: false},
            {layer: new WorldWind.CompassLayer(), enabled: false},
            {layer: new WorldWind.CoordinatesDisplayLayer(wwd), enabled: true},
            // {layer: new WorldWind.ViewControlsLayer(wwd), enabled: true}
        ];

        for (var l = 0; l < layers.length; l++) {
            layers[l].layer.enabled = layers[l].enabled;
            wwd.addLayer(layers[l].layer);
        }
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        // Polygon Generation
        var polygonGeneration = function () {
            var polygonLayer = new WorldWind.RenderableLayer("Depth (KM)");

            for (var i = 0; i < GeoJSON.features.length; i++) {
                // var polygon = new EQPolygon(GeoJSON.features[i].geometry['coordinates']);
                // polygonLayer.addRenderable(polygon.polygon);

                // var polygon = new Cylinder(GeoJSON.features[i].geometry['coordinates'], GeoJSON.features[i].properties['mag'] * 5e5);
                // polygonLayer.addRenderable(polygon.cylinder);

                var placeMark = new EQPlacemark(GeoJSON.features[i].geometry['coordinates'], GeoJSON.features[i].properties['mag']);
                polygonLayer.addRenderable(placeMark.placemark);
            }
            return polygonLayer;
        };
        wwd.addLayer(polygonGeneration());

        // Layer Manager
        var layerManger = new LayerManager(wwd);

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

        // Listen for mouse moves and highlight the placemarks that the cursor rolls over.
        wwd.addEventListener("mousemove", handlePick);

        // Listen for taps on mobile devices and highlight the placemarks that the user taps.
        var tapRecognizer = new WorldWind.TapRecognizer(wwd, handlePick);

    }

});
