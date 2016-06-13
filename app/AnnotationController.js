/*
 * Copyright (C) 2014 United States Government as represented by the Administrator of the
 * National Aeronautics and Space Administration. All Rights Reserved.
 */
define(function () {
    "use strict";

    var AnnotationController = function (worldWindow)
    {
	    this.worldWindow = worldWindow;

	    this.magSlider  = $("#magSlider");
	    this.dateSlider = $("#dateSlider");

	    this.magSlider.slider({
		                          range:   true,
		                          values:  [5.0, 7.0],
		                          min:     0.0,
		                          max:     7.0,
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
			                                   window.redraw(ui.values[0], ui.values[1], minDate, maxDate, window.limitQuery,
			                                                 worldWindow.layers[worldWindow.layers.length-1]);
		                                   }


	                          });

	    this.dateSlider.slider({
		                           range:   true,
		                           values:  [-15, -7],
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
			                                    window.redraw(minMagnitude, maxMagnitude, ui.values[0], ui.values[1],  window.limitQuery,
			                                                  worldWindow.layers[worldWindow.layers.length-1]);

		                                    }
	                           });

	    $("#magSliderValue").html(this.magSlider.slider("values",0).toString() + " to " +
	                              this.magSlider.slider("values",1).toString() + " Richter");
	    $("#dateSliderValue").html(this.dateSlider.slider("values",0).toString() + " to " +
	                               this.dateSlider.slider("values",1).toString() + " days");


    };

	return AnnotationController;
});