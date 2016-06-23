# NASA World Wind Earthquake Data Analysis code
import datetime
from time import process_time
import matplotlib.pyplot as plt
import loadearthquake as eaq
import loadmagnetic as mag
import plot as pt
import pyculiarity.detect_ts as pyc
import stationsdata as station
import pandas as pd
import statsmodels.api as sm
import detectanomalies as anom
# Date format: YYYY-MM-DD

# name, begin, end = 'InteleCell-Kodiak', '2014-10-22', '2014-12-22'
# name, begin, end = 'ESP-Kodiak-3', '2016-04-10', '2016-04-13'
name, begin, end = 'ESP-Kodiak-3', '2016-04-10', '2016-05-10'
# name, begin, end = 'ESP-Kodiak-3', '2016-04-07', '2016-05-31'

stationcoord = station.get(name)
magnetic = mag.load_magnetic_data(name, begin, end, filter_data = True).reset_index()
earthquake = eaq.load_earthquake_data(begin, end, stationcoord, min_magnitude=2.5)

# upsampling to one minute
magnetic.index = magnetic.Date
magnetic = magnetic.resample('1T').mean()
magnetic = magnetic.interpolate().dropna(how='any', axis=0)
magnetic['Date'] = magnetic.index

anomalies = anom.compute_anomalies(magnetic)
anoms_per_eq  = anom.compute_anomalies_for_earthquake(earthquake, anomalies)

earthquake = pd.concat([earthquake, anoms_per_eq], axis=1, join_axes=[earthquake.index])
earthquake['total_anoms'] = earthquake['X_anoms'] + earthquake['Y_anoms'] + earthquake['Z_anoms']

pt.plot_histogram(earthquake['total_anoms']#[earthquake['total_anoms'] > 0])
pt.plot_earthquake_anomalies_magnetic(earthquake, anomalies, magnetic)

