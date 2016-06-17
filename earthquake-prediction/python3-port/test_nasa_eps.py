# NASA World Wind Earthquake Data Analysis code
import matplotlib.pyplot as plt
import pandas as pd

import loadearthquake as eaq
import loadmagnetic as mag
import plot as pt
import pyculiarity.detect_ts as pyc
import stationsdata as station

# Date format: YYYY-MM-DD

name, begin, end = 'InteleCell-Kodiak', '2014-10-22', '2014-12-22'
# name, begin, end = 'ESP-Kodiak-3', '2016-04-10', '2016-04-13'
# name, begin, end = 'ESP-Kodiak-3', '2016-04-10', '2016-05-10'
# name, begin, end = 'ESP-Kodiak-3', '2016-04-07', '2016-05-31'

stationcoord = station.get(name)
magnetic = mag.load_magnetic_data(name, begin, end)
earthquake = eaq.load_earthquake_data(begin, end, stationcoord, min_magnitude=2)


def getDataFrame(column):
    tdf = pd.DataFrame()
    tdf['timestamp'] = magnetic.Date
    tdf['mag'] = column

    eq_anom = pyc.detect_ts(tdf, maximum_anomalies=0.05, direction='both', alpha=0.05)

    return eq_anom['anoms'], tdf


fX = getDataFrame(magnetic.X)
fY = getDataFrame(magnetic.Y)
fZ = getDataFrame(magnetic.Z)

pt.plot_earthquake_anomalies_magnetic((fX, fY, fZ), earthquake)
plt.show()
