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



# Date format: YYYY-MM-DD

# name, begin, end = 'InteleCell-Kodiak', '2014-10-22', '2014-12-22'
# name, begin, end = 'ESP-Kodiak-3', '2016-04-10', '2016-04-13'
# name, begin, end = 'ESP-Kodiak-3', '2016-05-19', '2016-05-22'
# name, begin, end = 'ESP-Kodiak-3', '2016-04-07', '2016-05-31'
name, begin, end = 'ESP-Kodiak-3', '2016-04-10', '2016-05-10'
# name, begin, end = 'ESP-Kodiak-3', '2016-06-04', '2016-06-07'
# name, begin, end = 'ESP-Kodiak-2', '2016-06-15', '2016-06-16'

# name, begin, end = 'ESP-Kodiak-3', '2016-04-28', '2016-05-02'
# name, begin, end = 'ESP-Kodiak-3', '2016-06-03', '2016-06-10'
# name, begin, end = 'ESP-Kodiak-2', '2016-06-05', '2016-06-21'

##################################################################
# Single Station Analysis

# Data Load
stationcoord = station.get(name)
# magnetic = mag.load_db(name, begin, end)
# magnetic = mag.slice_data(name, begin, end)
magnetic = mag.load_magnetic_data(name, begin, end)
earthquake = eaq.load_earthquake_data(begin, end, stationcoord, min_magnitude=2.5)

# Filtering Data
mag_filtrd = bf.butter_filter(magnetic.copy())

# Setting Sample Rate (1min res or Full Res)
resampled_df = mag.upsample_to_min(mag_filtrd)
# jury_rigged_df = mag.jury_rig_dates(mag_filtrd)

# # Computing Anomalies
anomalies = anom.compute_anomalies(resampled_df)

# # Plotting
pt.plot_earthquake_anomalies_magnetic(earthquake, anomalies, resampled_df, figtitle='-'.join((name, begin, end)))
# pt.plot_earthquake_anomalies_magnetic(earthquake, anomalies, mag_filtrd, figtitle='-'.join((name, begin, end)))
# pt.plot_earthquake_magnetic(earthquake, magnetic, figtitle='-'.join((name, begin, end)))

# Machine Learning Pre-processing
# x, y = ml.preprocess(name, magnetic, anomalies)

##################################################################
# Comparing Two Stations

# name, begin, end = 'ESP-Kodiak-3', '2016-06-06', '2016-06-09'
# name2, begin2, end2 = 'ESP-Kodiak-2', '2016-06-06', '2016-06-07'

# Data Load
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

mag_df = new_anom_det.normality_test(mag_filtrd)
# mag_df = new_anom_det.normality_test(magnetic)
# mag_df = bf.butter_filter(mag_df)

new_anom_det.test_plot_anoms(mag_filtrd)

# print(mag_df.head())
