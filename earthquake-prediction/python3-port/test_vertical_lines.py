from datetime import timedelta
import numpy as np
from scipy.signal import butter, cheby1, cheby2, lfilter
import matplotlib.pyplot as plt
import pandas as pd
import stationsdata as station
import loadearthquake as eaq
import seaborn as sb


def butter_design(cutoff, fs, type, order):
    return butter(N=order, Wn=cutoff / (0.5 * fs), btype=type, analog=False)


def cheby_design(cutoff, fs, type, order):
    return cheby1(N=order, rp=2.5, Wn=cutoff / (0.5 * fs), btype=type, analog=False)


def butter_highpass_filter(data, cutoff, fs, order):
    b, a = butter_design(cutoff, fs, type="high", order=order)
    y = lfilter(b, a, data)
    return y


def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_design(cutoff, fs, type="low", order=order)
    y = lfilter(b, a, data)
    return y


def cheby_highpass_filter(data, cutoff, fs, order):
    b, a = cheby_design(cutoff, fs, type="high", order=order)
    y = lfilter(b, a, data)
    return y


def cheby_lowpass_filter(data, cutoff, fs, order=5):
    b, a = cheby_design(cutoff, fs, type="low", order=order)
    y = lfilter(b, a, data)
    return y


def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n


# Station information
name, begin, end = 'ESP-Kodiak-3', '2016-04-10', '2016-05-10'
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

# Create this metric based on magnitude and distance, is in shaking amplitude, not energy released, log transformed.
earthquake['eq_influence'] = np.log((10 ** earthquake['EQ_Magnitude']) / earthquake['distance'])

t = df.index  # this is our x-axis for the three plots, the time in UTC
dataX, dataY, dataZ = df['X'].values, df['Y'].values, df['Z'].values

lower_frequency, higher_frequency, order = 0.0005, 0.00075, 5

# Filter the data by passing it through a high-pass filter then through a low pass filter.
# Chebyshev filters are slightly more complicated than Butterworth filters but they filter better.
x = np.abs(cheby_lowpass_filter(cheby_highpass_filter(dataX, lower_frequency, 1, order), higher_frequency, 1, order))
y = np.abs(cheby_lowpass_filter(cheby_highpass_filter(dataY, lower_frequency, 1, order), higher_frequency, 1, order))
z = np.abs(cheby_lowpass_filter(cheby_highpass_filter(dataZ, lower_frequency, 1, order), higher_frequency, 1, order))

# There is some weird stuff in the first bit of the filtered data. This has to do with
# the way digital filters work, the reason behind that is beyond the scope of this example,
# so we'll just delete that bit of the data and move on.
t = t[1e5:]
x = x[1e5:]
y = y[1e5:]
z = z[1e5:]

# Create an exponential moving average for each of the sensor readings
x_avg = pd.ewma(x, com=500)
y_avg = pd.ewma(y, com=500)
z_avg = pd.ewma(y, com=500)

f = plt.figure()

# Plot the averages in a thin black line
plt.plot(t, x_avg, color='k', linewidth=0.5)
plt.plot(t, y_avg, color='k', linewidth=0.5)
plt.plot(t, z_avg, color='k', linewidth=0.5)

plt.ylim([0, 100])

# Generate the mean for each sensor reading so we can know when the average passes this
# My multiplication by 3 is arbitrary, and you can change that to whatever suits you.
mean_x, mean_y, mean_z = np.mean(x)*3, np.mean(y)*3, np.mean(z)*3

# Plot the mean as thick horizontal lines; this is just for you when you're viewing the graph manually.
plt.axhline(mean_x, color='b', linewidth=2)
plt.axhline(mean_y, color='y', linewidth=2)
plt.axhline(mean_z, color='k', linewidth=2)

# For each point in each moving average, if the moving avg jumps from below the avg to above it, draw a vertical line.
for i in range(1,len(t)):
    if x_avg[i] > mean_x >= x_avg[i-1]:
        plt.axvline(t[i],color='b', linewidth=0.5)
    if y_avg[i] > mean_y >= y_avg[i - 1]:
        plt.axvline(t[i], color='y', linewidth=0.5)
    if z_avg[i] > mean_z >= z_avg[i - 1]:
        plt.axvline(t[i], color='k', linewidth=0.5)

# Also plot the earthquakes according to their influence
for index, row in earthquake.iterrows():
    if t[-1] > index > t[0]:
        if row['eq_influence'] > 0.75:
            plt.axvline(index, color='r', linewidth=3)


plt.show()
