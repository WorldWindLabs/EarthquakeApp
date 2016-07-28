/*
 * Copyright (C) 2014 United States Government as represented by the Administrator of the
 * National Aeronautics and Space Administration. All Rights Reserved.
 */

// requirejs(['../src/WorldWind',
//         './LayerManager'],
//     function (ww,
//               LayerManager) {
"use strict";

// USGS API

var TestURL = 'http://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2016-04-10&endtime=2016-04-20&limit=5' +
    '&minmagnitude=2.5';

var minMagnitude = 2.5,
    maxMagnitude = 10,
    minDate = -10,
    maxDate = 0;


var currentTimeUTC = +new Date();
var minDateISO = new Date(currentTimeUTC + minDate*24*60*60*1000).toISOString().split(/[-]+/);
console.log(minDateISO);
var maxDateISO = new Date(currentTimeUTC + maxDate*24*60*60*1000).toISOString().split(/[-]+/);
console.log(maxDateISO);
minDateISO[minDateISO.length - 1] = minDateISO[minDateISO.length - 1].split('.')[0];
maxDateISO[maxDateISO.length - 1] = maxDateISO[maxDateISO.length - 1].split('.')[0];

// layer.removeAllRenderables();

var resourcesUrl = "http://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson";
var query = "starttime="+minDateISO.join('-')+"&endtime="+maxDateISO.join('-')+"&minmagnitude=" +
    minMagnitude.toString() + "&maxmagnitude=" + maxMagnitude.toString();// + "&orderby=magnitude&limit=" +
//limit.toString();
var URL = resourcesUrl + '&' + query;

console.log(URL);

// JQuery API Calling
$.get(TestURL, function (EQ) {
    console.log(EQ.features[0].properties.mag);
    console.log(EQ.features[0].geometry.coordinates);
    placeMarkCreation(EQ);
});
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Data Display
// function dataDisplay(EQ_GeoJSON) {
    var latitudePlaceholder = document.getElementById('latitude');
    var longitudePlaceholder = document.getElementById('longitude');
    var magnitudePlaceholder = document.getElementById('magnitude');
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
    // Create the custom image for the placemark.
    var canvas = document.createElement("canvas"),
        ctx2d = canvas.getContext("2d"),
        size = 64, c = size / 2 - 0.5, innerRadius = 5, outerRadius = 20;

    canvas.width = size;
    canvas.height = size;

    var gradient = ctx2d.createRadialGradient(c, c, innerRadius, c, c, outerRadius);
    gradient.addColorStop(0, 'rgb(255, 255, 255)');
    gradient.addColorStop(0.5, 'rgb(255, 255, 255)');
    gradient.addColorStop(1, 'rgb(255, 255, 255)');

    ctx2d.fillStyle = gradient;
    ctx2d.arc(c, c, outerRadius, 0, 2 * Math.PI, false);
    ctx2d.fill();

    // Placemark Globals
    var placemark,
        placemarkAttributes = new WorldWind.PlacemarkAttributes(null),
        highlightAttributes,
        placemarkLayer = new WorldWind.RenderableLayer('Earthquakes');

    placemarkAttributes.imageScale = 3;
    placemarkAttributes.imageOffset = new WorldWind.Offset(
        WorldWind.OFFSET_FRACTION, 0.5,
        WorldWind.OFFSET_FRACTION, 0.5);
    placemarkAttributes.imageColor = WorldWind.Color.WHITE;
    placemarkAttributes.imageSource = new WorldWind.ImageSource(canvas);
    placemarkAttributes.labelAttributes.offset = new WorldWind.Offset(
        WorldWind.OFFSET_FRACTION, 0.5,
        WorldWind.OFFSET_FRACTION, 1.0);
    placemarkAttributes.labelAttributes.imageScale = 5
    placemarkAttributes.labelAttributes.color = WorldWind.Color.YELLOW;

    // Placemark Generation
    for (var i = 0, len = GeoJSON.features.length; i < len; i++) {
        var longitude = GeoJSON.features[i].geometry.coordinates[0];
        var latitude = GeoJSON.features[i].geometry.coordinates[1];
        placemark = new WorldWind.Placemark(new WorldWind.Position(latitude, longitude,
            1e2), true, placemarkAttributes);
        placemark.label = 'lat: ' + latitude.toString() + 'long: ' + longitude.toString() + 'mag: '+ GeoJSON.features[i].properties.mag.toString();
        // Highlight attributes
        highlightAttributes = new WorldWind.PlacemarkAttributes(placemarkAttributes);
        highlightAttributes.imageScale = 5;
        placemark.highlightAttributes = highlightAttributes;
        // console.log(placemark);

        placemarkLayer.addRenderable(placemark);
    }
    wwd.addLayer(placemarkLayer);

    // Polygon Generation

    // var polygon,
    //     polyhighlightAttributes,
    //     polygonLayer = new WorldWind.RenderableLayer("Depth (KM)");
    //
    // var polygonAttributes = new WorldWind.ShapeAttributes(null);
    //
    // polygonAttributes.drawInterior = true;
    // polygonAttributes.drawOutline = false;
    // polygonAttributes.outlineColor = WorldWind.Color.BLUE;
    // polygonAttributes.interiorColor = WorldWind.Color.WHITE;
    // polygonAttributes.imageColor = WorldWind.Color.WHITE;
    // // polygonAttributes.drawVerticals = polygon.extrude;
    // polygonAttributes.applyLighting = true;
    //
    // for (var i = 0, len = GeoJSON.features.length; i < len; i++) {
    //
    //     var boundaries = [];
    //     boundaries[0] = [];
    //     var altitude = GeoJSON.features[i].geometry['coordinates'][2] * -1000 * 4; // multiplying by a fixed constant to improve visibility
    //     GeoJSON.features[i].geometry['coordinates'][2] = 0;
    //     // var x = ((GeoJSON.features[i].properties.mag - min + 1) / (max - min));
    //     boundaries[0].push(new WorldWind.Position(GeoJSON.features[i].geometry['coordinates'][1] - 1, GeoJSON.features[i].geometry['coordinates'][0] - 1, altitude));
    //     boundaries[0].push(new WorldWind.Position(GeoJSON.features[i].geometry['coordinates'][1] - 1, GeoJSON.features[i].geometry['coordinates'][0] + 1, altitude));
    //     boundaries[0].push(new WorldWind.Position(GeoJSON.features[i].geometry['coordinates'][1] + 1, GeoJSON.features[i].geometry['coordinates'][0] + 1, altitude));
    //     boundaries[0].push(new WorldWind.Position(GeoJSON.features[i].geometry['coordinates'][1] + 1, GeoJSON.features[i].geometry['coordinates'][0] - 1, altitude));
    //
    //     polygon = new WorldWind.Polygon(boundaries, null);
    //     polygon.altitudeMode = WorldWind.ABSOLUTE;
    //     polygon.extrude = true;
    //     polygon.textureCoordinates = [
    //         [new WorldWind.Vec2(0, 0), new WorldWind.Vec2(1, 0), new WorldWind.Vec2(1, 1), new WorldWind.Vec2(0, 1)]
    //     ];
    //     // Highlight Attributes
    //     polyhighlightAttributes = new WorldWind.ShapeAttributes(polygonAttributes);
    //     polyhighlightAttributes.outlineColor = WorldWind.Color.RED;
    //     polygonAttributes.highlightAttributes = polyhighlightAttributes;
    //
    //     polygon.attributes = polygonAttributes;
    //
    //     polygonLayer.addRenderable(polygon);
    // }

    // wwd.addLayer(polygonLayer);

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

        // Highlight the items picked by simply setting their highlight flag to true.
        if (pickList.objects.length > 0) {
            for (var p = 0; p < pickList.objects.length; p++) {
                pickList.objects[p].userObject.highlighted = true;
                latitudePlaceholder.textContent = GeoJSON.features[p].geometry.coordinates[1];
                longitudePlaceholder.textContent = GeoJSON.features[p].geometry.coordinates[0];
                magnitudePlaceholder.textContent = GeoJSON.features[p].properties.mag;

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

};

// });