/*
 * Copyright (C) 2014 United States Government as represented by the Administrator of the
 * National Aeronautics and Space Administration. All Rights Reserved.
 */
define(function () {
    "use strict";

    var AnnotationController = function (worldWindow)   {
        this.worldWindow = worldWindow;

        this.magSlider  = $("#magSlider");
        this.dateSlider = $("#dateSlider");
        this.opacitySlider = $("#opacitySlider");

        this.magSlider.slider({
            range:   true,
            values:  [2.5, 10.0],
            min:     0.0,
            max:     10.0,
            step:    0.1,
            animate: true,
            slide:   function (event, ui)
            {
                $("#magSliderValue").html(ui.values[0].toString() + " to " +
                    ui.values[1].toString() + " Richter");

            },
            stop:    function(event, ui)
            {
                var minDate = $("#dateSlider").slider("values",0);
                var maxDate = $("#dateSlider").slider("values",1);
                worldWindow.redrawMe(ui.values[0], ui.values[1], minDate, maxDate);
            }

        });

        this.dateSlider.slider({
            range:   true,
            values:  [-30, -0],
            min:     -30,
            max:     0,
            step:    1,
            animate: true,
            slide:   function (event, ui)
            {
                $("#dateSliderValue").html(ui.values[0].toString() + " to " +
                    ui.values[1].toString() + " days");
            },
            stop:    function (event, ui)
            {
                var minMagnitude = $("#magSlider").slider("values",0);
                var maxMagnitude = $("#magSlider").slider("values",1);
                worldWindow.redrawMe(minMagnitude, maxMagnitude, ui.values[0], ui.values[1]);
            }
        });

        this.opacitySlider.slider({
            value:  50,
            // min:     0,
            // max:     100,
            // step:    5,
            animate: true,
            slide:   function (event, ui)
            {
                $("#opacitySliderValue").html(ui.value.toString() + "% opacity");
            },
            stop:    function (event, ui)
            {
                // var minMagnitude = $("#opacitySlider").slider("values",0);
                // var maxMagnitude = $("#opacitySlider").slider("values",1);
                // var minDate = $("#dateSlider").slider("values",0);
                // var maxDate = $("#dateSlider").slider("values",1);
                // window.redraw(minMagnitude, maxMagnitude, minDate, maxDate, window.limitQuery,
                //     window.polygonLayer, ui.value/100);
                console.log(worldWindow);
                worldWindow.surfaceOpacity = ui.value/100;
            }
        });

        $("#magSliderValue").html(this.magSlider.slider("values",0).toString() + " to " +
            this.magSlider.slider("values",1).toString() + " Richter");
        $("#dateSliderValue").html(this.dateSlider.slider("values",0).toString() + " to " +
            this.dateSlider.slider("values",1).toString() + " days");
        $("#opacitySliderValue").html(this.opacitySlider.slider("value").toString() + "% opacity");

    };

    return AnnotationController;
});
