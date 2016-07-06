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

# Date format: YYYY-MM-DD

# name, begin, end = 'InteleCell-Kodiak', '2014-10-22', '2014-12-22'
# name, begin, end = 'ESP-Kodiak-3', '2016-04-10', '2016-04-13'
# name, begin, end = 'ESP-Kodiak-3', '2016-05-19', '2016-05-22'
# name, begin, end = 'ESP-Kodiak-3', '2016-04-07', '2016-05-31'

name, begin, end = 'ESP-Kodiak-3', '2016-04-10', '2016-05-10'
# name2, begin2, end2 = 'ESP-Kodiak-2', '2016-04-10', '2016-05-10'

# name, begin, end = 'ESP-Kodiak-3', '2016-04-28', '2016-05-02'
# name, begin, end = 'ESP-Kodiak-3', '2016-06-03', '2016-06-10'
# name, begin, end = 'ESP-Kodiak-2', '2016-06-05', '2016-06-21'


name, begin, end = 'ESP-Kodiak-3', '2016-06-06', '2016-06-09'
name2, begin2, end2 = 'ESP-Kodiak-2', '2016-06-06', '2016-06-07'

stationcoord = station.get(name)
# magnetic = mag.load_db(name, begin, end)
# magnetic = mag.load_magnetic_data(name, begin, end)
magnetic1 = mag.load_db(name, begin, end)
magnetic2 = mag.load_db(name2, begin2, end2)

earthquake = eaq.load_earthquake_data(begin, end, stationcoord, min_magnitude=2.5)

# filtering data
mag_filtrd1 = bf.cheby_filter(magnetic1.copy())
mag_filtrd2 = bf.cheby_filter(magnetic2.copy())

# mag_filtrd = bf.butter_filter(magnetic.copy())

# computing anomalies
# anomalies = anom.compute_anomalies(mag.upsample_to_min(mag_filtrd))

# pt.plot_histogram(earthquake.total_anoms)  # [earthquake['total_anoms'] > 0])
# pt.plot_earthquake_anomalies_magnetic(earthquake, anomalies, mag_filtrd, figtitle = '-'.join((name,begin,end)))
# pt.plot_earthquake_magnetic(earthquake, magnetic, savefigure = True,
# 	savename = '-'.join((name,begin,end,'raw_plt.png')), figtitle = '-'.join((name,begin,end)))


# x, y = ml.preprocess(name, magnetic, anomalies)
'x, y = ml.preprocess(name, magnetic1, anomalies)'

pt.plot_eq_mag_compare(earthquake, mag_filtrd1, mag_filtrd2)
