# NASA World Wind Earthquake Data Analysis code
import pyculiarity as pyc
import csv
import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import os
import urllib
import matplotlib.dates as mdates
import loadearthquake as eaq
import loadmagnetic as mag
import stationsdata as station
import plot as pt

# Date format: YYYY-MM-DD
# name, begin, end = 'InteleCell-Kodiak', '2014-10-22', '2014-12-22'
# name, begin, end = 'ESP-Kodiak-3', '2016-04-10', '2016-04-13'
name, begin, end = 'ESP-Kodiak-3', '2016-04-10', '2016-05-10'
# name, begin, end = 'ESP-Kodiak-3', '2016-04-07', '2016-05-31'
stationcoord = station.get(name)
magnetic = mag.magload(name, begin, end)
earthquake = eaq.eqload(begin, end, stationcoord)


def getDataFrame(column):
    tdf = pd.DataFrame()
    tdf['timestamp'] = magnetic.Date
    tdf['mag'] = column

	eq_anom = pyc.detect_ts(tdf, max_anoms = 0.05, direction = 'both', alpha = 0.05)

    # This creates a dataframe from the anomaly results. I am not to sure why passing eq_anom['anoms'] creates a dataframe
    return eq_anom['anoms'], tdf


fX = getDataFrame(magnetic.X)
fY = getDataFrame(magnetic.Y)
fZ = getDataFrame(magnetic.Z)

pt.plot_earthquake_anomalies_magnetic((fX, fY, fZ), earthquake)

#magnetic.plot(subplots=True)
plt.show()