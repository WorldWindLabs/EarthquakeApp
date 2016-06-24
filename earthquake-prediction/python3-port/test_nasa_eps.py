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
import bandfilter as bf
import statsmodels.api as sm
import detectanomalies as anom
# Date format: YYYY-MM-DD

# name, begin, end = 'InteleCell-Kodiak', '2014-10-22', '2014-12-22'
# name, begin, end = 'ESP-Kodiak-3', '2016-04-10', '2016-04-13'
# name, begin, end = 'ESP-Kodiak-3', '2016-05-19', '2016-05-22'
# name, begin, end = 'ESP-Kodiak-3', '2016-04-07', '2016-05-31'
# name, begin, end = 'ESP-Kodiak-3', '2016-04-10', '2016-05-10'
name, begin, end = 'ESP-Kodiak-3', '2016-04-28', '2016-05-02'

stationcoord = station.get(name)
magnetic = mag.load_magnetic_data(name, begin, end)
mag_filtrd = bf.cheby_filter(magnetic)

earthquake = eaq.load_earthquake_data(begin, end, stationcoord, min_magnitude=2.5)

# computing anomalies
mag_filtrd = bf.filter(magnetic.copy())
anomalies = anom.compute_anomalies(mag.upsample_to_min(mag_filtrd))
anoms_per_eq  = anom.compute_anomalies_for_earthquake(earthquake, anomalies)
earthquake = eaq.add_anomalies(earthquake, anoms_per_eq)

pt.plot_histogram(earthquake.total_anoms)#[earthquake['total_anoms'] > 0])
pt.plot_earthquake_anomalies_magnetic(earthquake, anomalies, mag_filtrd)
pt.plot_earthquake_magnetic(earthquake, magnetic)