/**
 * Created by gagaus on 7/29/16.
 */

define(['./Draw'], function(Draw) {
    "use strict";

    // USGS API
    var USGS = function (wwd, control) {
        var currentTimeUTC = +new Date();
        var minDateISO = new Date(currentTimeUTC + -30 * 24 * 60 * 60 * 1000).toISOString().split(/[-]+/);
        var maxDateISO = new Date(currentTimeUTC + 0 * 24 * 60 * 60 * 1000).toISOString().split(/[-]+/);
        minDateISO[minDateISO.length - 1] = minDateISO[minDateISO.length - 1].split('.')[0];
        maxDateISO[maxDateISO.length - 1] = maxDateISO[maxDateISO.length - 1].split('.')[0];

        var queryParameters = function () {
            // Khaled's Dynamic URL (automatically updates to last 10 days)
            this.minMagnitude = 2.5;
            this.maxMagnitude = 10;

            this.FromDate = minDateISO.join('-');
            this.ToDate = maxDateISO.join('-');
            this.Limit = 500;

            this.MinLongitude = -360;
            this.MaxLongitude = 360;
            this.MinLatitude = -90;
            this.MaxLatitude = 90;

            this.initialQuery = {minMag: 2.5,
                maxMag: 10,
                fromDate: minDateISO.join('-'),
                toDate: maxDateISO.join('-')},

            // getInitialQuery: function () {
            //     return this.initialQuery;
            // }

            // this.getFromDate = function () {
            //     return this.FromDate;
            // };

            // this.getToDate = function () {
            //     return this.ToDate;
            // };

            // this.getMinMagnitude = function () {
            //     return this.MinMagnitude;
            // };

            // this.getMaxMagnitude = function () {
            //     return this.MaxMagnitude;
            // };

            // this.getLimit = function (value) {
            //     return this.Limit;
            // };

            this.updateLatLong = function (p1, p2) {
                var minLong = Math.min(p2.Long, p1.Long);
                var maxLong = Math.max(p2.Long, p1.Long);

                var minLati = Math.min(p2.Lati, p1.Lati);
                var maxLati = Math.max(p2.Lati, p1.Lati);

                this.MinLatitude = minLati;
                this.MinLongitude = minLong;
                this.MaxLatitude = maxLati;
                this.MaxLongitude = maxLong;
                //
                // this.setMaxLatitude(maxLati);
                // this.setMinLongitude(minLong);
                // this.setMaxLongitude(maxLong);
            },

            this.setFromDate = function (value) {
                this.FromDate = value;
            },
            
            this.setToDate = function (value) {
                this.ToDate = value;
            },
            
            this.setMinMagnitude = function (value) {
                this.minMagnitude = value;
            },
            
            this.setMaxMagnitude = function (value) {
                this.maxMagnitude = value;
            },
            
            this.setLimit = function (value) {
                this.Limit = value;
            },
            
            this.setMinLatitude = function(value) {
                this.MinLatitude = value;
            },
            
            this.setMaxLatitude = function(value) {
                this.MaxLatitude = value;
            },
            
            this.setMinLongitude = function(value) {
                this.MinLongitude = value;
            },
            
            this.setMaxLongitude = function(value) {
                this.MaxLongitude = value;
            }
        };

        this.parameters = new queryParameters();

        this.getUrl = function (drawingType, drawingState, figure) {
            var minMagnitude = this.parameters.minMagnitude,
                maxMagnitude = this.parameters.maxMagnitude,
                FromDate = this.parameters.FromDate,
                ToDate = this.parameters.ToDate,
                limit = this.parameters.Limit;

            var resourcesUrl = "http://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson";
            var query;
            if (drawingType == 'circle' && drawingState == 2) {
                query = "starttime=" + FromDate +
                    "&endtime=" + ToDate +
                    "&minmagnitude=" + minMagnitude.toString() +
                    "&maxmagnitude=" + maxMagnitude.toString() +
                    "&longitude=" + figure.origin.Long.toString() +
                    "&latitude=" + figure.origin.Lati.toString() +
                    "&maxradiuskm=" + figure.radius3D.toString();
            }
            else if (drawingType == 'rectangle' && drawingState == 2) {
                query = "starttime=" + FromDate +
                    "&endtime=" + ToDate +
                    "&minmagnitude=" + minMagnitude.toString() +
                    "&maxmagnitude=" + maxMagnitude.toString() +
                    "&minlongitude=" + this.MinLongitude.toString() +
                    "&maxlongitude=" + this.MaxLongitude.toString() +
                    "&minlatitude=" + this.MinLatitude.toString() +
                    "&maxlatitude=" + this.MaxLatitude.toString();
                //+ "&limit=" + limit.toString();
                // + "&orderby=magnitude;
            }
            else {
                query = "starttime=" + FromDate + "&endtime=" + ToDate + "&minmagnitude=" +
                    minMagnitude.toString() + "&maxmagnitude=" + maxMagnitude.toString();
                //+ "&limit=" + limit.toString();
                // + "&orderby=magnitude;
            }

            var url = resourcesUrl + '&' + query;
            console.log(url);
            return url;
        };

        var earthquakes = this;
        var firstTime = true;
        var layer;

        this.redraw = function(draw) {
            var drawOption = $("#flip-1").val();
            var drawingState = 0;
            var drawFig = 1;

            if (firstTime) {
                $.get(this.getUrl(drawOption, drawingState, drawFig), function (EQ) {
                    layer = draw.placeMarkCreation(EQ, earthquakes);
                    control.initializeHandlers();
                });
                firstTime = false;
            }
            else {
                // var p1 = drawFig.p1;
                // var p2 = drawFig.p2;
                // this.parameters.updateLatLong(p1, p2);

                $.get(this.getUrl(drawOption, drawingState, drawFig), function (EQ) {
                    wwd.removeLayer(layer);
                    layer = draw.placeMarkCreation(EQ, earthquakes);
                });
            }
        };

    };

    return USGS;
});
