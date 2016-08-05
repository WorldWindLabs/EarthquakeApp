/**
 * Created by gagaus on 7/29/16.
 */

define(['./worldwindlib'],
    function(WorldWind) {

        "use strict";

        function EQPlacemark(coordinates, magnitude) {

            var longitude = coordinates[0],
                latitude = coordinates[1],
                depth = coordinates[2];

            var placemark, highlightAttributes,
                placemarkAttributes = new WorldWind.PlacemarkAttributes(null);

            var canvas = document.createElement("canvas"),
                ctx2d = canvas.getContext("2d");
            var size = Math.abs(magnitude * 5),
                c = size / 2 - 0.5,
                outerRadius = size / 2.2;
            canvas.width = size;


            canvas.height = size;

            if (0 < magnitude && magnitude <= 2.5) {
                ctx2d.fillStyle = ('rgb(0, 255, 0)');
            } else if (2.5 < magnitude && magnitude <= 5) {
                ctx2d.fillStyle = ('rgb(255, 255, 0)');
            } else if (5 < magnitude && magnitude<= 7.5) {
                ctx2d.fillStyle = ('rgb(255, 165, 0)');
            } else if (7.5 < magnitude && magnitude <= 10) {
                ctx2d.fillStyle = ('rgb(255, 0, 0)');
            } else {
                ctx2d.fillStyle = ('rgb(255, 255, 255)');
            }
            ctx2d.globalAlpha = 0.85;
            ctx2d.arc(c, c, outerRadius, 0, 2 * Math.PI, false);
            ctx2d.fill();

            // Create the placemark.
            placemark = new WorldWind.Placemark(new WorldWind.Position(latitude, longitude, -depth * 1000));
            placemark.altitudeMode = WorldWind.RELATIVE_TO_GROUND;
            placemark.data = this;
            //placemark.indexInRenderables = self._baseLayer.renderables.length-1;
            //this._indexInRenderables = self._baseLayer.renderables.length-1;
            // Create the placemark attributes for the placemark.
            placemarkAttributes = new WorldWind.PlacemarkAttributes(placemarkAttributes);

            // Wrap the canvas created above in an ImageSource object to specify it as the placemark image source.
            // placemarkAttributes.imageSource = './images/dot-red.png';
            placemarkAttributes.imageSource = new WorldWind.ImageSource(canvas);

            placemarkAttributes.imageScale = magnitude / 1e1;
            // placemarkAttributes.imageColor = new WorldWind.Color(1, 1, 1, 0.55);


            placemark.attributes = placemarkAttributes;
            // Create the highlight attributes for this placemark. Note that the normal attributes are specified as
            // the default highlight attributes so that all properties are identical except the image scale. You could
            // instead vary the color, image, or other property to control the highlight representation.
            highlightAttributes = new WorldWind.PlacemarkAttributes(placemarkAttributes);
            highlightAttributes.imageScale = 1.2;
            // highlightAttributes.imageSource = './images/dot-red.png';
            highlightAttributes.imageSource = new WorldWind.ImageSource(canvas);

            placemark.highlightAttributes = highlightAttributes;
            this.placemark = placemark;
            this.placemark.center = new WorldWind.Position(latitude, longitude);
        }

        return EQPlacemark;
    });
