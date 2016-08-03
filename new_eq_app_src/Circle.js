/**
 * Created by gagaus on 7/29/16.
 */

define(['./worldwindlib'],
    function(WorldWind) {

        "use strict";

        function Circle(p1, p2) {

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
            // meshAttributes.drawOutline = false;
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

        return Circle;
    });
