NASA World Wind Earthquake Data Analysis Sandbox ----- Ver 1 (Python 3)
=======================================================================
**Organization:** NASA Ames Research Center (PX)  
**Partners:** Trillium Learning, Kodiak School District  
**Managers:** Patrick Hogan, Ron Fortunado  
**Authors:** Gabriel Militão, Benjamin Chang, Khaled Sharif, Farah Salah  
**Backend Team:** Enika Biswas, Nidhi Jain  
**Field Team (AK):** Seraphim McGann, Kiae Shin, Teyo DeGuzman

**Based on:** [Dr. Friedemann Fruend's work](http://geo.arc.nasa.gov/sg/cv/esddir3cv-freund.html)

* St-Laurent, F., J. S. Derr, and F. Freund (2006), Earthquake Lights and Stress-Activation
 of Positive Hole Charge Carriers in Rocks, Phys. Chem. of the Earth, 31, 305-312.
 
* Freund, F., A. Takeuchi, and B. W. S. Lau (2006), Electric currents streaming out of stressed
 igneous rocks: A step towards understanding pre-earthquake low frequency EM emissions,
 Phys. Chem. of the Earth, 31, 389-396.

1. Introduction
---
This project aims to apply practically Dr. Freidemann Freund’s theory of earthquake sensory precursors. Dr. Freund's theory 
states that several hours prior to large earthquakes the Earth sends out intense energy bursts, detectable as electromagnetic fields, 
caused by the tectonic plate stressing the local crust. These EM field bursts consists of sudden local magnetic field fluctuations and a 
variety of atmospheric and ionospheric phenomena. This project aims to observe this phenomenon in historic and real time data, with the 
ultimate goal of observing a live anomalous EM field fluctuation and accurately forecasting an earthquake within a specified geographical range. 

This project analyses the magnetic field data collected in Alaska, the most seismically active region in the world. First, common magnetic signals 
are filtered through multi-signal noise canceling to enable observation of the baseline magnetic signal. Second, an anomaly detection algorithm is 
applied to the data, identifying abnormal points in the data that may be indicative of a pending earthquake. Then, an algorithm clusters the anomalous 
points, and then generates features statistically. Machine learning algorithms are fed the anomalous features extracted from historical data to 
build “Earthquake Sensory Precursors” that can be then used to forecast, in real time, future earthquakes.

Working with NASA Ames Research Center (PX), Trillium Learning, and the Kodiak AK School District, a small team of interns is tirelessly working 
to analyze and understand magnetic field data being recorded in Kodiak, AK to determine whether or not earthquake forecasting can be accomplished 
through the interpretation of magnetic field variations.

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

Repository Modules:
* loadmagnetic
* plot
* stationsdata
* bandfilter
* detectanomalies
* clusters
* learning
* new_anom_det

3. Input Data
---
###Data Query
Because the data is very large (>10g) and currently being accessed from a database, most of the analyzable data is not publicly available. 
However we encourage the implementation of this code with independent data sources. Loading the data should be as simple as reading (or parsing) your data into a pandas dataframe, and implementing that dataframe across the available modules for analysis.

###Input Data
**Magnetic**  
Magnetic data (field vectors) needs to be a either readable or otherwise easily parsed. 
Format must be timestamps, X, Y, Z. The current magnetic data is being sampled at 123hz.

**Earthquake**  
Earthquake data can be easily read into the analysis environment using the 'loadearthquake' function. 
This loads from the USGS API database. It is likely that earthquakes of less than magnitude 3 and of greater
 distance than 300km from the magnetometer station will not have much influence over the magnetic field vectors.
 
4. Analysis
-----------
###Data structure
The raw magnetic data (at 1 to 123hz) has a diurnal signal pattern. 
![raw unfiltered data](https://github.com/NASAWorldWindResearch/EarthquakeApp/tree/master/documentation_pix/example_raw_data.png)
In order to eliminate this, we can utilize a bandpass filter (bandfilter.butterfilter()) to allow for finer analysis of how earthquake signals may affect the magnetic field vectors.
The data is not a normal distribution.

###
 
5. Outputs
----------
###Plots
Several plots can be created:
* A subplot of the magnetic vectors plotted against earthquake events and a scatter plot of anomalous points (plot.plot_earthquake_anomalies_magnetic())
* Distribution plots (histograms) of the data can be generated (plot.plot_histogram())
* or you can compare two magnetic data sets (plot.plot_eq_mag_compare())
* etc. explore the plotting functions written!

###Machine Learning Earthquake Forecasting
Still in testing, definitely not complete....but...

You can generate features using the learning.preprocess() function. These generated functions can be fed into sklearn functions to generate results, albeit arbitrary results (for the time being).

-------
Updated as of: 18/07/2016
