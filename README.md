NASA World Wind Earthquake Data Analysis Sandbox ----- Ver 1 (Python 3)
=======================================================================
**Organization:** NASA Ames Research Center (PX)  
**Partners:** Trillium Learning, Kodiak School District  
**Managers:** Patrick Hogan, Ron Fortunato  
**Authors:** Gabriel Militão, Benjamin Chang, Khaled Sharif, Farah Salah  
**Backend Team:** Enika Biswas, Nidhi Jain  
**Field Team (AK):** Seraphim McGann, Kiae Shin, Teyo DeGuzman

**Based on:** [Dr. Friedemann Freund's work](http://geo.arc.nasa.gov/sg/cv/esddir3cv-freund.html)

* St-Laurent, F., J. S. Derr, and F. Freund (2006), Earthquake Lights and Stress-Activation
 of Positive Hole Charge Carriers in Rocks, Phys. Chem. of the Earth, 31, 305-312.

* Freund, F., A. Takeuchi, and B. W. S. Lau (2006), Electric currents streaming out of stressed
 igneous rocks: A step towards understanding pre-earthquake low frequency EM emissions,
 Phys. Chem. of the Earth, 31, 389-396.

1. Introduction
---
This project aims to apply Dr. Friedemann Freund’s theory of earthquake precursor science. Dr. Freund's theory states that during the time leading up to large earthquakes the Earth generates intense energy bursts, detectable by their affect to the electromagnetic (EM) field, and caused by tectonic forces stressing the local rock mass. These high energy bursts cause very short-lived fluctuations to the local magnetic field, as well as a variety of atmospheric and ionosphere phenomena. This project aims to observe this phenomenon using historic and real time data, with the ultimate goal of observing a live anomalous EM field fluctuation and accurately forecasting an earthquake within a specified geographical range.

This project analyses the magnetic field data collected in Alaska, the most seismically active region in the world. First, common magnetic signals are filtered through multi-signal noise canceling to enable observation of the baseline magnetic signal. Second, an anomaly detection algorithm is applied to the data, identifying abnormal points in the data that may be indicative of a pending earthquake. Then, an algorithm clusters the anomalous points, and then generates features statistically. Machine learning algorithms are fed the anomalous features extracted from historical data to build “Earthquake Sensory Precursors” that can be then used to forecast, in real time, future earthquakes.

Working with NASA Ames Research Center (PX), Trillium Learning, and the Kodiak AK School District, a small team of interns is working to analyze and understand magnetic field data being recorded in Kodiak, AK to determine whether or not earthquake forecasting can be accomplished through interpretation of magnetic field fluctuations.

2. Required Packages
---
In order for the whole repository to function properly, these packages must be installed on python 3:

Packages:
* time
* datetime
* matplotlib
* pandas
* numpy
* seaborn
* scipy
* sklearn
* statsmodels.api

3. Input Data
---
###Data Query
Because the data being recorded in Alaska is very large (>10g due to the high resolution of 123hz) and currently being accessed from a database, most of the analyzable data is not publicly available.
However we encourage the implementation of this code with independent data sources. Loading the data should be as simple as reading (or parsing) your data into a pandas dataframe, and implementing that dataframe across the available modules for analysis.

###Input Data
**Magnetic**  
Magnetic data (field vectors) needs to be a either readable or otherwise easily parsed.
Format must be timestamps, X, Y, Z. The current magnetic data is being sampled at 123hz.

**Earthquake**  
Earthquake data can be easily read into the analysis environment using the `loadearthquake.()` function.
This loads from the USGS API database. It is likely that earthquakes of less than magnitude 3 and of greater
 distance than 300km from the magnetometer station will not have much influence over the magnetic field vectors.

4. Analysis
-----------
###Data structure
The raw magnetic data (at 1 to 123hz) has a diurnal signal pattern.
![raw unfiltered data](https://github.com/NASAWorldWindResearch/EarthquakeApp/blob/master/documentation_pix/example_raw_data.png)
###Filtering
In order to eliminate this, we can utilize a bandpass filter `bandfilter.butterfilter()` to allow for finer analysis of how earthquake signals may affect the magnetic field vectors.
![filtered data](https://github.com/NASAWorldWindResearch/EarthquakeApp/blob/master/documentation_pix/example_filtered.png)
###Anomaly Detection
Two methods of anomaly detection are included in the repository. The first one is from Twitter's anomaly detection library ported into python 2. We then ported that library into python 3 (pycularity).
The other method involves using numpy convolution to create a moving average to detect anomalies `new_anom_det.det_anoms()`. They both accomplish similar results.
![anomalies](https://github.com/NASAWorldWindResearch/EarthquakeApp/blob/master/documentation_pix/example_anom.png)
###Earthquake Forecasting (theoretical)
By analyzing the data in this fashion, we should be able to observe perturbations in the magnetic field vectors, allowing for machine learning to build a confidence on earthquakes occurring in the near future.
![earthquake det](https://github.com/NASAWorldWindResearch/EarthquakeApp/blob/master/documentation_pix/example_eq_det.png)
(The red line is an earthquake event of magnitude >3 within 300km of this magnetic anomaly)

5. Outputs
----------
###Plots
Several plots can be created:
* A subplot of the magnetic vectors plotted against earthquake events and a scatter plot of anomalous points `plot.plot_earthquake_anomalies_magnetic()`
* Distribution plots (histograms) of the data can be generated `plot.plot_histogram()`
* or you can compare two magnetic data sets `plot.plot_eq_mag_compare()`
* etc. explore the plotting functions written!

###Machine Learning Earthquake Forecasting
Still in testing, definitely not complete....but...

You can generate features using the `learning.preprocess()` function. These generated functions can be fed into sklearn functions to generate results, albeit arbitrary results (for the time being).

6. NASA Web World Wind Earthquake Application
---------------------------------------------
You can view the preliminary application for the earthquake app. Open the GeoJSON.html (EarthquakeApp/app/Earthquake App WWW/examples/GeoJSON.html) in a web server (Webstorm does this automatically) to run the web app.
![screencap of app](https://github.com/NASAWorldWindResearch/EarthquakeApp/blob/master/documentation_pix/app_screencap.png)

###Goals:
* Allow for viewing of recent earthquakes (epicenter, hypocenter, age of EQ, magnitude)
* Display of associated data in separate box (date, magnitude, coordinates, relative location, relative age, etc.)
* Query functionality for access to the USGS API from front end interface
* Time series of EQ
* EQ Forecasting implementation

###How to use:
Still being built, instructions coming soon.

***
Updated as of 30/07/2016 (July 30th, 2016)
