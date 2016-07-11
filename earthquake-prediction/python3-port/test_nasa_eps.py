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

# Date format: YYYY-MM-DD

# name, begin, end = 'InteleCell-Kodiak', '2014-10-22', '2014-12-22'
# name, begin, end = 'ESP-Kodiak-3', '2016-04-10', '2016-04-13'
# name, begin, end = 'ESP-Kodiak-3', '2016-05-19', '2016-05-22'
# name, begin, end = 'ESP-Kodiak-3', '2016-04-07', '2016-05-31'
name, begin, end = 'ESP-Kodiak-3', '2016-04-10', '2016-05-10'
# name, begin, end = 'ESP-Kodiak-3', '2016-04-28', '2016-05-02'
# name, begin, end = 'ESP-Kodiak-3', '2016-06-03', '2016-06-10'
# name, begin, end = 'ESP-Kodiak-2', '2016-06-05', '2016-06-21'

##################################################################
# Single Station Analysis

# Data Load
stationcoord = station.get(name)
# magnetic = mag.load_db(name, begin, end)
magnetic = mag.load_magnetic_data(name, begin, end)
earthquake = eaq.load_earthquake_data(begin, end, stationcoord, min_magnitude=2.5)

# Filtering Data
mag_filtrd = bf.butter_filter(magnetic.copy())


# resampled_df = mag.upsample_to_min(mag_filtrd)
# jury_rigged_df = mag.jury_rig_dates(mag_filtrd)

# # Computing Anomalies
# anomalies = anom.compute_anomalies(mag.upsample_to_min(mag_filtrd))

# pt.plot_magnetic(jury_rigged_df)
# # Plotting
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

def movingaverage(interval, window_size):
    window = np.ones(int(window_size)) / float(window_size)
    return np.convolve(interval, window, 'same')


def normality_test(dataframe):
    def describe(data):
        ls = data.columns.tolist()
        desc = []
        for i in ls:
            desc.append(stat.describe(data[i]))
        skew = ([item[4] for item in desc])
        kurtosis = ([item[5] for item in desc])
        normal_test = pd.DataFrame({'skew': skew,
                                    'kurtosis': kurtosis}, index=data.columns.tolist())
        return normal_test

    normal_test = describe(dataframe)
    for index, row in normal_test.iterrows():
        transformed = False
        if -1 < row['skew'] < 1 or transformed == True:
            print('Data', index, 'is normal.')
            pass
        elif row['skew'] < -1 or row['skew'] > 1:
            print('Data', index, 'is not normal.')
            while transformed == False:
                if transformed == True:
                    print('Data', index, 'is normal.')
                    pass
                elif row['skew'] > 1:
                    print('Data', index, 'is positively skewed. Attempting log(10) data transformation for normality.')
                    dataframe['log_' + index] = np.log(dataframe[index])
                    transformed = True
                elif row['skew'] < -1:
                    # TODO: ADAPT FUNCTION FOR THIS CIRCUMSTANCE
                    print('Data', index, 'is negatively skewed TODO: ADAPT FUNCTION FOR THIS CIRCUMSTANCE')
            if transformed == True:
                print('Data', index, 'has been transformed, is now normal.')
                pass
    if transformed == True:
        log_ls = ['log_X', 'log_Y', 'log_Z']
        for d in log_ls:
            dataframe['z_' + d] = (dataframe[d] - dataframe[d].mean()) / dataframe[d].std()

    return dataframe


mag_df = normality_test(mag_filtrd)


# for g in log_ls:
#     sb.distplot(mag_filtrd[g])
#     plt.show()

MOV = movingaverage(mag_df.z_log_X, 1000).tolist()
# print(MOV)
mag_df = mag_df[10000:]
MOV = MOV[10000:]

STD = np.std(MOV)
events = []
ind = []
for d in range(len(mag_df.z_log_X)):
    if mag_df.z_log_X[d] > MOV[d] + 2 * STD:
        events.append([mag_df.index[d], mag_df.z_log_X[d]])
events_df = pd.DataFrame(events, columns=['timestamp',
                                          'anom_events'])
events_df.index = events_df['timestamp']
# del events_df.timestamp
print(events_df.head())

f = plt.figure(figsize=(15, 5))
f1 = f.add_subplot(111)
f1.plot(mag_df.index, mag_df.z_log_X, color='skyblue', linewidth=0.75, zorder=1)
f1.plot(mag_df.index, MOV, color='r', linewidth=0.5, zorder=2)
f1.scatter(events_df.index, events_df.anom_events, facecolors='none',
           edgecolors='r', linewidths=0.75, zorder=3)
# f1.set_ylim([0, 160])
f1.set_xlim([mag_df.index[0], end])
plt.show()

print(mag_df.head())
