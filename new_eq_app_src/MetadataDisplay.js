/**
 * Created by researchcomputer on 8/4/16.
 */

define([''], function(ww) {
    "use strict";

    // Data Display
    var Metadata = function () {
        // Individual Earthquakes
        this.magnitudePlaceholder = document.getElementById('magnitude');
        this.locPlaceholder = document.getElementById('location');
        this.eventdatePlaceholder = document.getElementById('time');
        this.latitudePlaceholder = document.getElementById('latitude');
        this.longitudePlaceholder = document.getElementById('longitude');
        this.depthPlaceholder = document.getElementById('depth');

        // Query Metadata
        this.earthquakecountPlaceholder = document.getElementById('eq_count');
        this.min_datePlaceholder = document.getElementById('minDate');
        this.max_datePlaceholder = document.getElementById('maxDate');
        this.minMagnitudePlaceholder = document.getElementById('minMagnitude');
        this.maxMagnitudePlaceholder = document.getElementById('maxMagnitude');
    };

    Metadata.prototype.setMagnitude = function(value) {
        this.magnitudePlaceholder.textContent = value;
    };

    Metadata.prototype.setlocation = function (value) {
        this.locPlaceholder.textContent = value;
    };

    Metadata.prototype.settime = function (value) {
        this.eventdatePlaceholder.textContent = value;
    };

    Metadata.prototype.setlatitude = function (value) {
        this.latitudePlaceholder.textContent = value;
    };

    Metadata.prototype.setlongitude = function (value) {
        this.longitudePlaceholder.textContent = value;
    };

    Metadata.prototype.setdepth = function (value) {
        this.depthPlaceholder.textContent = value;
    };

    Metadata.prototype.seteq_count = function (value) {
        this.earthquakecountPlaceholder.textContent = value;
    };

    Metadata.prototype.setminDate = function (value) {
        this.min_datePlaceholder.textContent = value;
    };

    Metadata.prototype.setmaxDate = function (value) {
        this.max_datePlaceholder.textContent = value;
    };

    Metadata.prototype.setminMagnitude = function (value) {
        this.minMagnitudePlaceholder.textContent = value;
    };

    Metadata.prototype.setmaxMagnitude = function (value) {
        this.maxMagnitudePlaceholder.textContent = value;
    };

    return Metadata;

});