from datetime import timedelta
import numpy as np
from scipy.signal import butter, lfilter
import matplotlib.pyplot as plt
import pandas as pd
import stationsdata as station
import loadearthquake as eaq
from math import radians, cos, sin, asin, sqrt

def butter_highpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    return b, a


def butter_highpass_filter(data, cutoff, fs, order=5):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y


def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a


def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    return km

# Station information
name, begin, end = 'ESP-Kodiak-3', '2016-05-01', '2016-05-31'
# name, begin, end = 'ESP-Kodiak-3', '2016-04-10', '2016-05-10'
path = '../data/' + name + '/' + begin + '-to-' + end + '.csv'

# Loading in the magnetometer data
column_names = ['Date', 'X', 'Y', 'Z']
df = pd.read_csv(path, names=column_names)
df.index = pd.to_datetime(df['Date'], utc=True) + timedelta(hours=9)  # this line changes Alaska time to UTC time
df.drop('Date', inplace=True, axis=1)

# Re-sampling to a 1 Second interval
sampling_rate = 1  # Hz
df = df.resample('1S').mean()  # re-sample at 1 Second intervals
df = df.interpolate().dropna(how='any', axis=0)  # interpolate any missing data and delete bad rows

# Loading in the earthquake data that is near the magnetometer station
station_coordinates = station.get(name)
earthquake = eaq.load_earthquake_data(begin, end, station_coordinates, min_magnitude="2", max_distance="300")

t = df.index  # this is our x-axis for the three plots, the time in UTC
dataX, dataY, dataZ = df['X'].values, df['Y'].values, df['Z'].values

lower_frequency, higher_frequency, order = 0.0005, 0.00075, 5

# Filter the data by passing it through a high-pass filter then through a low pass filter
x = np.abs(butter_lowpass_filter(butter_highpass_filter(dataX, lower_frequency, 1, order), higher_frequency, 1, order))
y = np.abs(butter_lowpass_filter(butter_highpass_filter(dataY, lower_frequency, 1, order), higher_frequency, 1, order))
z = np.abs(butter_lowpass_filter(butter_highpass_filter(dataZ, lower_frequency, 1, order), higher_frequency, 1, order))

f = plt.figure()

f1 = f.add_subplot(311)
f1.plot(t, x, color='g', linewidth='1')
f1.set_ylim([0, 60])  # set the y-axis of the first plot between 0 and 30
f2 = f.add_subplot(312)
f2.plot(t, y, color='g', linewidth='1')
f2.set_ylim([0, 50])  # set the y-axis of the second plot between 0 and 15
f3 = f.add_subplot(313)
f3.plot(t, z, color='g', linewidth='1')
f3.set_ylim([0, 60])  # set the z-axis of the third plot between 0 and 20

d = []
m = []

for index, row in earthquake.iterrows():
    # this will draw a vertical red line on each of the three plots if the magnitude is greater than 3
    mag = row['EQ_Magnitude']
    dist = haversine(float(row['Longitude']), float(row['Latitude']), float(station_coordinates['long']), float(station_coordinates['lati']))
    d.append(dist)
    m.append(mag)
    if (mag <= 3 and mag >= 2 and dist <= 60) or \
        (mag <= 4 and mag >= 3 and dist <= 200) or \
        (mag >= 4 and dist <= 300): 
        print(dist, mag)
        f1.axvline(index, color='r', linewidth=1)
        f2.axvline(index, color='r', linewidth=1)
        f3.axvline(index, color='r', linewidth=1)

plt.show()

plt.plot(m, d, 'ro')
plt.show()