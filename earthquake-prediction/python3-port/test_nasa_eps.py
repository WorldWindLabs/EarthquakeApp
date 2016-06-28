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
import seaborn as sb
import numpy as np

# Date format: YYYY-MM-DD

# name, begin, end = 'InteleCell-Kodiak', '2014-10-22', '2014-12-22'
# name, begin, end = 'ESP-Kodiak-3', '2016-04-10', '2016-04-13'
# name, begin, end = 'ESP-Kodiak-3', '2016-05-19', '2016-05-22'
# name, begin, end = 'ESP-Kodiak-3', '2016-04-07', '2016-05-31'
name, begin, end = 'ESP-Kodiak-3', '2016-04-10', '2016-05-10'
# name, begin, end = 'ESP-Kodiak-3', '2016-04-28', '2016-05-02'
# name, begin, end = 'ESP-Kodiak-2', '2016-06-05', '2016-06-21'

stationcoord = station.get(name)
magnetic = mag.load_magnetic_data(name, begin, end)

earthquake = eaq.load_earthquake_data(begin, end, stationcoord, min_magnitude=2.5)

# computing anomalies
mag_filtrd = bf.cheby_filter(magnetic.copy())
# mag_filtrd = bf.butter_filter(magnetic.copy())
anomalies = anom.compute_anomalies(mag.upsample_to_min(mag_filtrd))
anoms_per_eq = anom.compute_anomalies_for_earthquake(earthquake, anomalies)
earthquake = eaq.add_anomalies(earthquake, anoms_per_eq)

# pt.plot_histogram(earthquake.total_anoms)  # [earthquake['total_anoms'] > 0])
# pt.plot_earthquake_anomalies_magnetic(earthquake, anomalies, mag_filtrd)
# pt.plot_earthquake_magnetic(earthquake, magnetic)

mag_interval = magnetic.resample('10T').mean()
# print(mag_interval)

X = anomalies[0]
Y = anomalies[1]
Z = anomalies[2]

anom_rate = []
for index, row in mag_interval.iterrows():
    end = index
    start = end - datetime.timedelta(hours=2)
    temp = X.anoms[start:end]
    anom_rate.append(len(temp.index)/2)

X_anom_r = pd.DataFrame()
X_anom_r['anom_r'] = pd.Series(anom_rate)
X_anom_r['log_anom_r'] = np.log(X_anom_r['anom_r'])
X_anom_r.index = mag_interval.index
X_anom_r = X_anom_r[X_anom_r.log_anom_r >= 0]
X_anom_r['log_z_score'] = ((X_anom_r['log_anom_r']-X_anom_r['log_anom_r'].mean())/X_anom_r['log_anom_r'].std())
print(X_anom_r.head(20))
sb.distplot(X_anom_r['log_anom_r'])
plt.show()

# print(X_anom_r.head())


# f1 = f.add_subplot(311)
# f1.plot(magnetic.index, magnetic.X, color='b', linewidth='1', zorder=1)
# f1.set_ylim([0, 60])
# f2 = f.add_subplot(312)
# f2.plot(magnetic.index, magnetic.Y, color='g', linewidth='1', zorder=1)
# f2.set_ylim([0, 60])
# f3 = f.add_subplot(313)
# f3.plot(magnetic.index, magnetic.Z, color='orange', linewidth='1')
# f3.set_ylim([0, 60])
