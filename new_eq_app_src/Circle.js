/**
 * Created by gagaus on 7/29/16.
 */

define(['./Rectangle',
    './worldwindlib',
    './WorldPoint'],
    function(Rectangle,
             WorldWind,
             WorldPoint) {

        "use strict";

        var Circle = function (p1, p2) {

            var R = 6371; // Radius of the earth in km

            function getDistanceFromLatLonInKm(lat1,lon1,lat2,lon2) {
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

            function rad2deg(rad) {
                return rad * (180/Math.PI)
            }

            function distance2d(p1, p2) {
                return Math.sqrt(Math.pow(p1.X-p2.X, 2) + Math.pow(p2.Y-p1.Y, 2));
            }

            var minLong = Math.min(p2.Long, p1.Long);
            var maxLong = Math.max(p2.Long, p1.Long);

            var minLati = Math.min(p2.Lati, p1.Lati);
            var maxLati = Math.max(p2.Lati, p1.Lati);

            var renderedCircle = function () {
                var canvas = document.createElement("canvas"),
                    ctx2d = canvas.getContext("2d"),
                    radius = distance2d(p1,p2),
                    size = 2*radius,
                    c = radius;

                canvas.width = size;
                canvas.height = size;

                ctx2d.arc(c, c, radius, 0, 2 * Math.PI, false);
                ctx2d.fill();

                return canvas;
            };


            var CircleImage = new Image();
            CircleImage.onload = function(){
                // imageCircle.src = this.src;
            };
            CircleImage.src = "./images/circle.png";

            this.origin = p1;
            this.radius3D = getDistanceFromLatLonInKm(p1.Lati, p1.Long, p2.Lati, p2.Long);

            this.radius2D = distance2d(p1,p2);

            var alpha = rad2deg(this.radius3D/R);

            var lowerVertex = new WorldPoint(p1.wwd);
            lowerVertex.setLong(p1.Long - alpha);
            lowerVertex.setLati(p1.Lati - alpha);

            var upperVertex = new WorldPoint(p1.wwd);
            upperVertex.setLong(p1.Long + alpha);
            upperVertex.setLati(p1.Lati + alpha);

            var square = new Rectangle(lowerVertex, upperVertex);

            square.origin = p1;
            square.radius3D = this.radius3D;
            square.attributes.imageSource = new WorldWind.ImageSource(CircleImage);
            square.attributes.drawInterior = true;

            return square;
        };

        return Circle;
    });
