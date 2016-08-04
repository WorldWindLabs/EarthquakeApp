/**
 * Created by gagaus on 8/3/16.
 */

define(['./worldwindlib'],
    function(WorldWind) {

    "use strict";

    function TectonicPlateLayer() {
        var shapeConfigurationCallback = function (geometry, properties) {
            var configuration = {};
            configuration.attributes = new WorldWind.ShapeAttributes(null);
            configuration.attributes.drawOutline = true;
            configuration.attributes.outlineColor = new WorldWind.Color(
                0.6 * configuration.attributes.interiorColor.red,
                0.3 * configuration.attributes.interiorColor.green,
                0.3 * configuration.attributes.interiorColor.blue,
                1.0);
            configuration.attributes.outlineWidth = 1.0;
            return configuration;
        };

        var plateBoundariesLayer = new WorldWind.RenderableLayer("World Borders");
        var plateBoundariesJSON = new WorldWind.GeoJSONParser("./new_eq_app_files/plate_boundaries.json");
        plateBoundariesJSON.load(shapeConfigurationCallback, plateBoundariesLayer);
        return plateBoundariesLayer;
    }

    return TectonicPlateLayer;
});
