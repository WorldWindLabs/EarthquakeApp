from datetime import timedelta
from numpy.fft import rfft
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

name, begin, end = 'ESP-Kodiak-3', '2016-04-10', '2016-05-10'

path = '../data/' + name + '/' + begin + '-to-' + end + '.csv'

column_names = ['Date', 'X', 'Y', 'Z']

# skip 1000 rows in the csv then load 1000 rows
df = pd.read_csv(path, names=column_names, nrows=1000, skiprows=1000)

# assuming that the Alaska TZ is UTC - 9 hours
df.index = pd.to_datetime(df['Date'], utc=True) + timedelta(hours=9)

sampling_rate = 123  # Hz

df = df.resample('12300U').mean()  # this resamples the data at 123 Hz (aka: 12300 microseconds)
df = df.interpolate().dropna(how='any', axis=0)

x_axis = df['X'].values
x_freq = rfft(x_axis)  # where the magic happens, the real-valued fast fourier transform
x_amplitude = np.log10(np.abs(x_freq))  # log10 the amplitude because the differences between Hz are huge

print(len(x_amplitude),np.max(x_amplitude),np.min(x_amplitude))

# we can capture frequencies from 0 Hz up to half the sampling rate (aka: the Nyquist rate)
plt.plot(np.linspace(0,sampling_rate/2, len(x_amplitude)), x_amplitude, 'b-')

plt.xlim([-5, +70])
plt.ylim([0,11])

plt.show()

