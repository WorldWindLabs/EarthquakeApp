# NASA World Wind Earthquake Data Analysis code
import datetime as dt
from datetime import datetime
from time import process_time
import matplotlib.pyplot as plt
import loadearthquake as eaq
import loadmagnetic as mag
import plot as pt
import pyculiarity.detect_ts as pyc
import stationsdata as station
import pandas as pd
import bandfilter as bf
import statsmodels.api as sm
import detectanomalies as anom
import seaborn as sb
import numpy as np
import clusters as cl
import learning as ml
import scipy.stats as stat
import new_anom_det
from sklearn import svm

'''
NASA World Wind Earthquake Data Analysis Sandbox [Ver 1 (Python 3)]
###################################################################################################
Organization: NASA Ames Research Center (PX)
Partners: Trillium Learning, Kodiak School District
Managers: Patrick Hogan, Ron Fortunado
Authors: Gabriel Militão, Benjamin Chang, Khaled Sharif, Farah Salah
Backend Team: Enika Biswas, Nidhi Jain
Field Team (AK): Seraphim McGann, Kiae Shin, Teyo DeGuzman

Based on: Dr. Friedemann Fruend's work: (http://geo.arc.nasa.gov/sg/cv/esddir3cv-freund.html)

            -St-Laurent, F., J. S. Derr, and F. Freund (2006), Earthquake Lights and Stress-Activation
             of Positive Hole Charge Carriers in Rocks, Phys. Chem. of the Earth, 31, 305-312.
            -Freund, F., A. Takeuchi, and B. W. S. Lau (2006), Electric currents streaming out of stressed
             igneous rocks: A step towards understanding pre-earthquake low frequency EM emissions,
             Phys. Chem. of the Earth, 31, 389-396.
###################################################################################################
1.
This file is a space to utilize the data analysis tools written to analyze magnetic field vectors
their relationship with earthquake events. Based on Dr. Friedemann Freund's theories, tectonic
plate stresses on rock build up energy (electricity) several hours prior to an earthquake. This
energy should be detectable in the form of magnetic field anomalies.

Working with NASA Ames Research Center (PX), Trillium Learning, and the Kodiak AK School District,
a small team of interns is tirelessly working to analyze and understand magnetic field data being
recorded in Kodiak, AK to determine whether or not earthquake forecasting can be accomplished
through the interpretation of magnetic field variations.
###################################################################################################
2.
This sandbox should be used to analyze magnetic field data. It takes 2 basic inputs:

magnetic field data: in the form of X, Y, and Z vector data (timeseries)
earthquake data: event data retrieved from the USGS API

automated retrieval of data can be accomplished through the 'data' folder functions
###################################################################################################
3.
In order for the whole repository to function properly, these packages must be installed on python 3:

Packages:
time
datetime
matplotlib
pandas
numpy
seaborn
scipy
sklearn
statsmodels.api

Repository Modules:
loadmagnetic
plot
stationsdata
bandfilter
detectanomalies
clusters
learning
new_anom_det
###################################################################################################

'''
# Date format: YYYY-MM-DD

# name, begin, end = 'InteleCell-Kodiak', '2014-10-22', '2014-12-22'
# name, begin, end = 'ESP-Kodiak-3', '2016-04-10', '2016-04-13'
# name, begin, end = 'ESP-Kodiak-3', '2016-05-19', '2016-05-22'
# name, begin, end = 'ESP-Kodiak-3', '2016-04-07', '2016-05-31'
# name, begin, end = 'ESP-Kodiak-3', '2016-04-15', '2016-05-05'
name, begin, end = 'ESP-Kodiak-3', '2016-04-10', '2016-05-10'
# name, begin, end = 'ESP-Kodiak-3', '2016-06-04', '2016-06-07'
# name, begin, end = 'ESP-Kodiak-2', '2016-06-15', '2016-06-16'

# name, begin, end = 'ESP-Kodiak-3', '2016-04-28', '2016-05-02'
# name, begin, end = 'ESP-Kodiak-3', '2016-06-03', '2016-06-10'
# name, begin, end = 'ESP-Kodiak-2', '2016-06-05', '2016-06-21'

##################################################################
# Data Load Processes

# Station Metadata Load
stationcoord = station.get(name)
# magnetic = mag.load_db(name, begin, end)
# magnetic = mag.slice_data(name, begin, end)
# magnetic = mag.load_magnetic_data(name, begin, end)

# Magnetic Data Load
magnetic = mag.load_magnetic_data(name, begin, end)
magnetic = magnetic[130000:]
pt.plot_magnetic(magnetic)
mag_filtrd = bf.butter_filter(magnetic.copy())
mag_filtrd = mag_filtrd[10000:]
pt.plot_magnetic(mag_filtrd)
'''
# Earthquake Data Load
# earthquake = eaq.load_earthquake_data(begin, end, stationcoord, min_magnitude=1.5)

# Filtering Data

Setting Sample Rate (1sec, 1min or Full Res)
resampled_df = mag.upsample_to_sec(mag_filtrd)
# jury_rigged_df = mag.jury_rig_dates(mag_filtrd)

# DSP Correction
mag_filtrd = mag_filtrd[10000:]

##################################################################
# Single Station Visualization and analysis (PYCULARITY ANOM DET ALGO)

# # Computing Anomalies
# anomalies = anom.compute_anomalies(resampled_df)
# print(anomalies)
# # Plotting
# pt.plot_earthquake_anomalies_magnetic(earthquake, anomalies, resampled_df, figtitle='-'.join((name, begin, end)))
# pt.plot_earthquake_anomalies_magnetic(earthquake, anomalies, mag_filtrd, figtitle='-'.join((name, begin, end)))
# pt.plot_earthquake_magnetic(earthquake, magnetic, figtitle='-'.join((name, begin, end)))

# Machine Learning Pre-processing
# x, y = ml.preprocess(name, magnetic, anomalies)

##################################################################
# Comparing Two Stations (PYCULARITY ANOM DET ALGO)

# 2 Station Metadata
# name, begin, end = 'ESP-Kodiak-3', '2016-06-06', '2016-06-09'
# name2, begin2, end2 = 'ESP-Kodiak-2', '2016-06-06', '2016-06-07'

# Station metadata, magnetic, earthquake data Load
# stationcoord = station.get(name)
# earthquake = eaq.load_earthquake_data(begin, end, stationcoord, min_magnitude=2.5)
# magnetic1 = mag.load_db(name, begin, end)
# magnetic2 = mag.load_db(name2, begin2, end2)

# Filtering
# mag_filtrd1 = bf.cheby_filter(magnetic1.copy())
# mag_filtrd2 = bf.cheby_filter(magnetic2.copy())

# Plotting
# pt.plot_eq_mag_compare(earthquake, mag_filtrd1, mag_filtrd2)

##################################################################
# New Anomaly Detection Function Build

# Normailty Test and data transformation (IN TESTING)
# mag_df = new_anom_det.normality_test(mag_filtrd)
# mag_df = new_anom_det.normality_test(magnetic)

# DSP Correction
mag_filtrd = mag_filtrd[10000:]

# New Anomaly Detection
anoms = new_anom_det.anom_det(resampled_df,threshold = 3, window = 300, correction = True, correctionfactor = 20)

# Plot
pt.plot_earthquake_anomalies_magnetic(earthquake, anoms, mag_filtrd, figtitle='-'.join((name, begin, end)), savefigure = True, savename = ('-'.join((name, begin, end))+'.png'))

# Machine Learning
clf = svm.SVC(probability = True)
x, y = ml.preprocess(name, magnetic, anoms)
clf.fit(x[1], y[1])

name, begin, end = 'ESP-Kodiak-3', '2016-05-12', '2016-05-22'

magnetic = mag.get_data(name, begin, end)
mag_filtrd = bf.butter_filter(magnetic.copy())
resampled_df = mag.upsample_to_sec(mag_filtrd)
mag_filtrd = mag_filtrd[10000:]
anoms = new_anom_det.anom_det(resampled_df,threshold = 3, window = 300, correction = True, correctionfactor = 20)

x, y = ml.preprocess(name, magnetic, anoms)
'''
