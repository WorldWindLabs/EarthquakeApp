/**
 * Created by gagaus on 7/29/16.
 */

define([''], function(ww) {
    "use strict";

    // USGS API
    var USGS = function () {
        // Test URL
        this.TestURL = 'http://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2016-04-10&endtime=2016-04-20&limit=5' +
            '&minmagnitude=2.5';
        // Decade (2006-2016) of Earthquake data URL
        this.DecadeURL = 'http://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2006-01-01&endtime=2016-01-01' +
            '&minmagnitude=6&maxmagnitude=7';


        var currentTimeUTC = +new Date();
        var minDateISO = new Date(currentTimeUTC + -30 * 24 * 60 * 60 * 1000).toISOString().split(/[-]+/);
        var maxDateISO = new Date(currentTimeUTC + 0 * 24 * 60 * 60 * 1000).toISOString().split(/[-]+/);
        minDateISO[minDateISO.length - 1] = minDateISO[minDateISO.length - 1].split('.')[0];
        maxDateISO[maxDateISO.length - 1] = maxDateISO[maxDateISO.length - 1].split('.')[0];

        
        // Khaled's Dynamic URL (automatically updates to last 10 days)
        this.minMagnitude = 2.5,
        this.maxMagnitude = 10,

        this.FromDate = minDateISO.join('-'),
        this.ToDate = maxDateISO.join('-'),
        this.limit = 500;

        this.MinLongitude = -360;
        this.MaxLongitude = 360;
        this.MinLatitude = -90;
        this.MaxLatitude = 90;


        /**
         * @return {string}
         */

        this.getUrl = function (drawing) {
            var minMagnitude = this.minMagnitude,
                maxMagnitude = this.maxMagnitude,
                FromDate = this.FromDate,
                ToDate = this.ToDate,
                limit = this.limit;

            var resourcesUrl = "http://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson";
            var query;
            if (drawing) {
                query = "starttime=" + this.FromDate + "&endtime=" + this.ToDate + "&minmagnitude=" +
                    this.minMagnitude.toString() + "&maxmagnitude=" + this.maxMagnitude.toString() +
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

        this.setMinMagnitude = function(value) {
            this.minMagnitude = value;
        };

        this.setMaxMagnitude = function(value) {
            this.maxMagnitude = value;
        };

        this.setMinDate = function(value) {
            this.FromDate = value;
        };

        this.setMaxDate = function(value) {
            this.ToDate = value;
        };

        this.setMinLatitude = function(value) {
            this.MinLatitude = value;
        };

        this.setMaxLatitude = function(value) {
            this.MaxLatitude = value;
        };

        this.setMinLongitude = function(value) {
            this.MinLongitude = value;
        };

        this.setMaxLongitude = function(value) {
            this.MaxLongitude = value;
        };
    };

    return USGS;
});
