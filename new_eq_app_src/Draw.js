/**
 * Created by researchcomputer on 8/4/16.
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
              Metadata) {

        "use strict";

        // function Draw () {
            var drawingStates = {
                OFF: 0,
                ONE_V: 1,
                TWO_V: 2,
                ON: 3
            };
            var drawingState = drawingStates.ON;
            var earthquakeLayer;

            var alias = this;

            // Highlight Picking
            var highlightedItems = [];

            var Draw = function (wwd, Metadata) {
                var data;

                this.placeMarkCreation = function (GeoJSON, earthquakes) {
                    // Polygon Generation
                    data = GeoJSON;
                    var EarthquakeLayer = function (GeoJSON) {
                        earthquakeLayer = new WorldWind.RenderableLayer("Earthquakes");

                        for (var i = 0; i < GeoJSON.features.length; i++) {
                            // var polygon = new EQPolygon(GeoJSON.features[i].geometry['coordinates']);
                            // polygonLayer.addRenderable(polygon.polygon);

                            // var polygon = new Cylinder(GeoJSON.features[i].geometry['coordinates'], GeoJSON.features[i].properties['mag'] * 5e5);
                            // polygonLayer.addRenderable(polygon.cylinder);

                            var placeMark = new EQPlacemark(GeoJSON.features[i].geometry.coordinates, GeoJSON.features[i].properties.mag);
                            earthquakeLayer.addRenderable(placeMark.placemark);
                        }
                        return earthquakeLayer;
                    };

                    var earthquakeLayer = new EarthquakeLayer(GeoJSON);
                    wwd.addLayer(earthquakeLayer);

                    function updateMetadata() {
                        Metadata.seteq_count(GeoJSON.features.length);
                        var startdate,
                            enddate,
                            GeoJSON_dates = [];
                        for (var i = 0, len = GeoJSON.features.length; i < len; i++) {
                            GeoJSON_dates.push(new Date(GeoJSON.features[i].properties.time));
                        }
                        startdate = new Date(Math.min.apply(null, GeoJSON_dates));
                        enddate = new Date(Math.max.apply(null, GeoJSON_dates));

                        Metadata.setminDate(startdate);
                        Metadata.setmaxDate(enddate);

                        Metadata.setminMagnitude(earthquakes.minMagnitude);
                        Metadata.setmaxMagnitude(earthquakes.maxMagnitude);
                    }

                    updateMetadata();

                    return earthquakeLayer;
                };
                // The common pick-handling function.
                this.Pick = function (o) {
                    // The input argument is either an Event or a TapRecognizer. Both have the same properties for determining
                    // the mouse or tap location.
                    var x = o.clientX,
                        y = o.clientY;

                    var GeoJSON = data;

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
                                    Metadata.setMagnitude(GeoJSON.features[eq].properties.mag);
                                    Metadata.setlocation(GeoJSON.features[eq].properties.place);
                                    Metadata.settime(new Date(GeoJSON.features[eq].properties.time));
                                    Metadata.setlatitude(GeoJSON.features[eq].geometry.coordinates[1]);
                                    Metadata.setlongitude(GeoJSON.features[eq].geometry.coordinates[0]);
                                    Metadata.setdepth(GeoJSON.features[eq].geometry.coordinates[2]);
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

                this.Click = function (event) {
                    var drawLayer = new WorldWind.RenderableLayer("Drawing");
                    wwd.addLayer(drawLayer);

                    var p1 = new WorldPoint(wwd);
                    var p2 = new WorldPoint(wwd);

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
                            earthquakes.redraw(queryFig, p1, p2);
                            // drawingState = drawingStates.OFF;
                        }
                        else if (drawingState == drawingStates.ON) {
                            p1.update3Dfrom2D(x, y);

                            placeMark = new Point([p1.Long, p1.Lati, 0]);
                            drawLayer.addRenderable(placeMark.placemark);

                            drawingState = drawingStates.ONE_V;
                        }
                    }

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

                };
            };
        // }
        return Draw;
    });
