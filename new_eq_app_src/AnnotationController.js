/*
 * Copyright (C) 2014 United States Government as represented by the Administrator of the
 * National Aeronautics and Space Administration. All Rights Reserved.
 */
define(['./USGS'], function (USGS) {
    "use strict";

    var usgs = new USGS();

    var AnnotationController = function (worldWindow) {
        this.worldWindow = worldWindow;

        this.magSlider = $("#magSlider");
        this.dateSlider = $("#dateSlider");
        this.opacitySlider = $("#opacitySlider");

        this.FromDate = $("#fromdatepicker").datepicker({
            changeMonth: true,
            changeYear: true,
            showButtonPanel: true,
            yearRange: "1975:nn",
            dateFormat: "yy-mm-dd",
            onSelect: function (dateText, dateobj) {
                var dateAsString = dateText;
                console.log(dateAsString);
                var minMagnitude = $("#magSlider").slider("values", 0);
                var maxMagnitude = $("#magSlider").slider("values", 1);
                var ToDate = $("#todatepicker").datepicker("getDate");
                worldWindow.redrawMe(minMagnitude, maxMagnitude, dateAsString, ToDate);

            }
        });

        this.ToDate = $("#todatepicker").datepicker({
            changeMonth: true,
            changeYear: true,
            showButtonPanel: true,
            yearRange: "1975:nn",
            dateFormat: "yy-mm-dd",
            onSelect: function (dateText, dateobj) {
                var dateAsString = dateText;
                console.log(dateAsString);
                var minMagnitude = $("#magSlider").slider("values", 0);
                var maxMagnitude = $("#magSlider").slider("values", 1);
                var FromDate = $("#fromdatepicker").datepicker("getDate");
                worldWindow.redrawMe(minMagnitude, maxMagnitude, FromDate, dateAsString);


            }
        });

        this.magSlider.slider({
            range: true,
            values: [2.5, 10.0],
            min: 0.0,
            max: 10.0,
            step: 0.1,
            animate: true,
            slide: function (event, ui) {
                $("#magSliderValue").html(ui.values[0].toString() + " to " +
                    ui.values[1].toString() + " Richter");

            },
            stop: function (event, ui) {
                var ToDate = $("#todatepicker").datepicker("getDate");
                var FromDate = $("#fromdatepicker").datepicker("getDate");
                worldWindow.redrawMe(ui.values[0], ui.values[1], FromDate, ToDate);
            }

        });


        // this.dateSlider.slider({
        //     range:   true,
        //     values:  [-30, -0],
        //     min:     -30,
        //     max:     0,
        //     step:    1,
        //     animate: true,
        //     slide:   function (event, ui)
        //     {
        //         $("#dateSliderValue").html(ui.values[0].toString() + " to " +
        //             ui.values[1].toString() + " days");
        //     },
        //     stop:    function (event, ui)
        //     {
        //         var minMagnitude = $("#magSlider").slider("values",0);
        //         var maxMagnitude = $("#magSlider").slider("values",1);
        //         worldWindow.redrawMe(minMagnitude, maxMagnitude, ui.values[0], ui.values[1]);
        //     }
        // });

        this.opacitySlider.slider({
            value: 50,
            // min:     0,
            // max:     100,
            // step:    5,
            animate: true,
            slide: function (event, ui) {
                $("#opacitySliderValue").html(ui.value.toString() + "% opacity");
            },
            stop: function (event, ui) {
                // var minMagnitude = $("#opacitySlider").slider("values",0);
                // var maxMagnitude = $("#opacitySlider").slider("values",1);
                // var minDate = $("#dateSlider").slider("values",0);
                // var maxDate = $("#dateSlider").slider("values",1);
                // window.redraw(minMagnitude, maxMagnitude, minDate, maxDate, window.limitQuery,
                //     window.polygonLayer, ui.value/100);
                // console.log(worldWindow);
                worldWindow.surfaceOpacity = ui.value / 100;
            }
        });

        // this.queryshapeSwitch.slider({
        //     value:  50,
        //     // min:     0,
        //     // max:     100,
        //     // step:    5,
        //     animate: true,
        //     slide:   function (event, ui)
        //     {
        //         $("#queryshapeSwitchValue").html(ui.value.toString() + " state");
        //     },
        //     stop:    function (event, ui)
        //     {
        //         // var minMagnitude = $("#opacitySlider").slider("values",0);
        //         // var maxMagnitude = $("#opacitySlider").slider("values",1);
        //         // var minDate = $("#dateSlider").slider("values",0);
        //         // var maxDate = $("#dateSlider").slider("values",1);
        //         // window.redraw(minMagnitude, maxMagnitude, minDate, maxDate, window.limitQuery,
        //         //     window.polygonLayer, ui.value/100);
        //         console.log(ui.value);
        //         // worldWindow.surfaceOpacity = ui.value/100;
        //     }
        // });

        $('#submit').on("click", function () {
            alert($("#flip-1").val());
        });


        this.limiter = $("#limitSet").selectmenu({
            select: function (event, ui) {

                if ($("#limitSet").val() == '1000') {
                    var minMagnitude = $("#magSlider").slider("values", 0);
                    var maxMagnitude = $("#magSlider").slider("values", 1);
                    var FromDate = $("#fromdatepicker").datepicker("getDate");
                    var ToDate = $("#todatepicker").datepicker("getDate");
                    var limitSet = $("#limitSet").val();

                    worldWindow.redrawMe(minMagnitude, maxMagnitude, FromDate, ToDate, limitSet)
                }
                else if ($("#limitSet").val() == "balls to the wall") {
                    var minMagnitude = $("#magSlider").slider("values", 0);
                    var maxMagnitude = $("#magSlider").slider("values", 1);
                    var FromDate = $("#fromdatepicker").datepicker("getDate");
                    var ToDate = $("#todatepicker").datepicker("getDate");

                    worldWindow.redrawMe(minMagnitude, maxMagnitude, FromDate, ToDate);
                }
            }
        });


        this.reset = $("#reset").on("click", function () {
            $("#magSlider").slider("option", "values", [2.5, 10]);
            $("#magSliderValue").html($("#magSlider").slider("values", 0).toString() + " to " +
                $("#magSlider").slider("values", 1).toString() + " Richter");
            $("#fromdatepicker").datepicker("setDate", usgs.initialQuery.fromDate.split("T")[0]);
            $("#todatepicker").datepicker("setDate", usgs.initialQuery.toDate.split("T")[0]);

            worldWindow.redrawMe(usgs.initialQuery.minMag,
                usgs.initialQuery.maxMag,
                usgs.initialQuery.fromDate,
                usgs.initialQuery.toDate, true);
        });

        $("#magSliderValue").html(this.magSlider.slider("values", 0).toString() + " to " +
            this.magSlider.slider("values", 1).toString() + " Richter");
        $("#dateSliderValue").html(this.dateSlider.slider("values", 0).toString() + " to " +
            this.dateSlider.slider("values", 1).toString() + " days");
        $("#opacitySliderValue").html(this.opacitySlider.slider("value").toString() + "% opacity");
        // $("#queryshapeSwitchValue").html(this.queryshapeSwitch.slider("value").toString() + "% opacity");

    };

    return AnnotationController;
});
