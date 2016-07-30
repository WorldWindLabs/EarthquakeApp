/**
 * Created by gagaus on 7/29/16.
 */

define(['./worldwindlib'],
    function(WorldWind) {

    "use strict";

    function EQPolygon(coordinates) {

        var latitude = coordinates[1],
            longitude = coordinates[0],
            depth = coordinates[2];

        var height = 0.12;

        var polyhighlightAttributes;

        var polygonAttributes = new WorldWind.ShapeAttributes(null);

        polygonAttributes.drawInterior = true;
        polygonAttributes.drawOutline = false;
        polygonAttributes.outlineColor = WorldWind.Color.YELLOW;
        polygonAttributes.interiorColor = WorldWind.Color.YELLOW;
        // polygonAttributes.imageColor = WorldWind.Color.WHITE;
        polygonAttributes.applyLighting = true;

        var boundaries = [];
        boundaries[0] = [];
        var altitude = Math.abs(depth) * -1000; // multiplying by a fixed constant to improve visibility
        depth = Math.abs(depth);

        boundaries[0].push(new WorldWind.Position(latitude - 1, longitude - 1, altitude));
        boundaries[0].push(new WorldWind.Position(latitude - 1, longitude + 1, altitude));
        boundaries[0].push(new WorldWind.Position(latitude + 1, longitude + 1, altitude));
        boundaries[0].push(new WorldWind.Position(latitude + 1, longitude - 1, altitude));

        this.polygon = new WorldWind.Polygon(boundaries, null);
        this.polygon.altitudeMode = WorldWind.ABSOLUTE;
        this.polygon.extrude = true;
        this.polygon.textureCoordinates = [
            [new WorldWind.Vec2(0, 0), new WorldWind.Vec2(1, 0), new WorldWind.Vec2(1, 1), new WorldWind.Vec2(0, 1)]
        ];
        // Highlight Attributes
        polyhighlightAttributes = new WorldWind.ShapeAttributes(polygonAttributes);

        // var date = (+new Date(GeoJSON.features[i].properties.time));
        // var utcDate  = (+new Date());
        //
        // if (utcDate - date > (30*24*60*60*1000))
        // {
        //     polygonAttributes.interiorColor = WorldWind.Color.GREEN;
        // }
        // else if (utcDate - date > (8*24*60*60*1000))
        // {
        //     polygonAttributes.interiorColor = WorldWind.Color.YELLOW;
        // }
        // else if (utcDate - date > (24*60*60*1000))
        // {
        //     polygonAttributes.interiorColor = WorldWind.Color.ORANGE;
        // }
        // else
        // {
        //     polygonAttributes.interiorColor = WorldWind.Color.RED;
        // }
        //
        // polygonAttributes.drawInterior = true;
        // polygonAttributes.drawOutline = false;
        // polygonAttributes.applyLighting = true;
        // polygonAttributes.drawVerticals = this.polygon.extrude;
        // Highlighting
        polyhighlightAttributes.outlineColor = WorldWind.Color.RED;
        polyhighlightAttributes.interiorColor = WorldWind.Color.RED;
        polygonAttributes.highlightAttributes = polyhighlightAttributes;
        this.polygon.highlightAttributes = polyhighlightAttributes;
        this.polygon.attributes = polygonAttributes;

        this.polygon.center = new WorldWind.Position(latitude, longitude);

        // this.render = function(dc) {
        //     var cylinderBoundaries = flatten(this.cylinder._boundaries);
        //     var someBoundary = cylinderBoundaries[0];
        //     var currHeight = someBoundary;
        //     //console.log(currHeight);
        //     //var eyeDistance = Math.abs(dc.eyePosition.altitude - currHeight.altitude);
        //
        //     //var eyeDistance = positionDistances(dc.eyePosition, currHeight);
        //     ////console.log('eyeDistance :', eyeDistance);
        //     ////var visibilityScale = Math.max(0.0, Math.min(1, this.eyeDistanceScalingThreshold / eyeDistance));
        //     //var visibilityScale = eyeDistance / 1e4;
        //     cylinderBoundaries.forEach(function(boundary) {
        //         //console.log('scalling down');
        //         //console.log(visibilityScale, ' ', eyeDistance, ' ', currHeight);
        //
        //         // method one
        //         //if(Math.floor(visibilityScale) < 1) {
        //         //
        //         //    boundary.altitude = 0;//visibilityScale * height;
        //         //} else {
        //         //    boundary.altitude = height;
        //         //}
        //
        //
        //         // method 2
        //         if(dc.eyePosition.altitude < height) {
        //             boundary.altitude = 0
        //             this.enabled = false;
        //         } else {
        //             boundary.altitude = height;
        //             this.enabled  = true;
        //         }
        //
        //
        //
        //         //boundary.altitude = visibilityScale * height;
        //     });
        //     //(eyeDistance / this.cylinder.eyeDistanceScalingThreshold);
        //     //Math.max(0.0, Math.min(1, this.cylinder.eyeDistanceScalingThreshold /
        //     //eyeDistance));
        //
        //     //if(true) {
        //     //    cylinderBoundaries.forEach(function (boundary) {
        //     //        var temp = visibilityScale * height;
        //     //        boundary.altitude = Math.min(height, temp);
        //     //    });
        //     //}
        //
        //
        //     //if(Math.floor(visibilityScale) < 1) {
        //     //    //console.log('rendering at ', visibilityScale);
        //     //    cylinderBoundaries.forEach(function (boundary) {
        //     //    //    console.log('visible ', visibilityScale);
        //     //    //    console.log('scalling down to ', visibilityScale * height);
        //     //        boundary.altitude = visibilityScale * height;
        //     //    });
        //     //}
        //
        //     //console.log(this.cylinder.eyeDistanceScalingThreshold);
        //     //cylinderBoundaries.forEach(function(boundary) {
        //     //    boundary.altitude = visibilityScale * boundary.altitude;
        //     //});
        //     //if(Math.floor(visibilityScale) <= 1) {
        //     //    console.log('rendering at ', visibilityScale);
        //     //    cylinderBoundaries.forEach(function (boundary) {
        //     //        boundary.altitude = visibilityScale * this.initialHeight;
        //     //    });
        //     //}
        //     //} else {
        //     //    cylinderBoundaries.forEach(function(boundary) {
        //     //       boundary.altitude = this.initialHeight;
        //     //    });
        //     //}
        //
        //     this.cylinder.render(dc);
        //
        // }
    }

    return EQPolygon;
});
