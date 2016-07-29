/**
 * Created by gagaus on 7/29/16.
 */

define([''], function(ww) {
    "use strict";

    // USGS API
    var USGS = function () {
        // Test URL
        var TestURL = 'http://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2016-04-10&endtime=2016-04-20&limit=5' +
            '&minmagnitude=2.5';
        // Decade (2006-2016) of Earthquake data URL
        var DecadeURL = 'http://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2006-01-01&endtime=2016-01-01' +
            '&minmagnitude=6&maxmagnitude=7';

        // Khaled's Dynamic URL (automatically updates to last 10 days)
        this.minMagnitude = 2.5,
        this.maxMagnitude = 10,
        this.minDate = -30,
        this.maxDate = 0 ,
        this.limit = 500;

        /**
         * @return {string}
         */

        this.url = DynamicDT(this.minMagnitude, this.maxMagnitude, this.minDate, this.maxDate, this.limit);
    };

    function DynamicDT(minMagnitude, maxMagnitude, minDate, maxDate, limit) {
        var currentTimeUTC = +new Date();
        var minDateISO = new Date(currentTimeUTC + minDate * 24 * 60 * 60 * 1000).toISOString().split(/[-]+/);
        console.log(minDateISO);
        var maxDateISO = new Date(currentTimeUTC + maxDate * 24 * 60 * 60 * 1000).toISOString().split(/[-]+/);
        console.log(maxDateISO);
        minDateISO[minDateISO.length - 1] = minDateISO[minDateISO.length - 1].split('.')[0];
        maxDateISO[maxDateISO.length - 1] = maxDateISO[maxDateISO.length - 1].split('.')[0];

        var resourcesUrl = "http://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson";
        var query = "starttime=" + minDateISO.join('-') + "&endtime=" + maxDateISO.join('-') + "&minmagnitude=" +
            minMagnitude.toString() + "&maxmagnitude=" + maxMagnitude.toString() + "&limit=" + limit.toString();
        // + "&orderby=magnitude;

        var url = resourcesUrl + '&' + query;
        return url;
    }

    return USGS;
});