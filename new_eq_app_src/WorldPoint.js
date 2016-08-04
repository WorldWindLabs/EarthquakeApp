/**
 * Created by gagaus on 7/29/16.
 */

define(['./worldwindlib'],
    function(WorldWind) {

        "use strict";

        var WorldPoint = function (wwd) {

            this.wwd = wwd;

            function update3D(WorldCoordinates) {
                this.Long = WorldCoordinates[0];
                this.Lati = WorldCoordinates[1];
                this.Alti = WorldCoordinates[2];
            }

            function update2D(pixelCoordinates) {
                this.X = pixelCoordinates.X;
                this.Y = pixelCoordinates.Y;
            }

            this.update3Dfrom2D = function (x, y) {
                var pickList = wwd.pick(wwd.canvasCoordinates(x, y));

                this.X = x;
                this.Y = y;

                this.Long = pickList.objects[0].position.longitude;
                this.Lati = pickList.objects[0].position.latitude;
                this.Alti = pickList.objects[0].position.altitude;
            };

            this.setLong = function(value) {
                this.Long = value
            };

            this.setLati = function (value) {
                this.Lati = value
            };


            function update2Dfrom3D(x, y) {
                var pickList = wwd.pick(wwd.canvasCoordinates(x, y));

                this.X = pixelCoordinates.X;
                this.Y = pixelCoordinates.Y;

                this.Long = pickList.objects[0].position.longitude;
                this.Lati = pickList.objects[0].position.latitude;
                this.Alti = pickList.objects[0].position.altitude;
            }



        };

        return WorldPoint;
    });
