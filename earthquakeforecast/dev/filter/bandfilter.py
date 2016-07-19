from time import process_time
import numpy as np
from scipy.signal import butter, cheby1, cheby2, lfilter
import pandas as pd
import data.stationsdata as station
import data.earthquake as eaq
import plot as pt

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

def butter_filter(df, lower_frequency = 0.0005, higher_frequency = 0.00075, order = 5):
    print("Filtering magnetic data", end='')
    start = process_time()

    # Re-sampling to a 1 Second interval
    df.drop('Date', inplace=True, axis=1)

    # sampling_rate = 1  # Hz
    # df = df.resample('1S').mean()  # re-sample at 1 Second intervals
    # df = df.interpolate().dropna(how='any', axis=0)  # interpolate any missing data and delete bad rows

    dataX, dataY, dataZ = df['X'].values, df['Y'].values, df['Z'].values

    # Filter the data by passing it through a high-pass filter then through a low pass filter
    x = np.abs(butter_lowpass_filter(butter_highpass_filter(dataX, lower_frequency, 1, order), higher_frequency, 1, order))
    y = np.abs(butter_lowpass_filter(butter_highpass_filter(dataY, lower_frequency, 1, order), higher_frequency, 1, order))
    z = np.abs(butter_lowpass_filter(butter_highpass_filter(dataZ, lower_frequency, 1, order), higher_frequency, 1, order))

    df['X'], df['Y'], df['Z'] = x, y, z

    print(" --- took", round(process_time() - start, 2), " s")

    return df

def cheby_design(cutoff, fs, type, order):
    return cheby1(N=order, rp=2.5, Wn=cutoff / (0.5 * fs), btype=type, analog=False)

def cheby_highpass_filter(data, cutoff, fs, order):
    b, a = cheby_design(cutoff, fs, type="high", order=order)
    y = lfilter(b, a, data)
    return y


def cheby_lowpass_filter(data, cutoff, fs, order=5):
    b, a = cheby_design(cutoff, fs, type="low", order=order)
    y = lfilter(b, a, data)
    return y

def cheby_filter(df, lower_frequency = 0.0005, higher_frequency = 0.00075, order = 5):
    print("Filtering magnetic data", end='')
    start = process_time()

    # Re-sampling to a 1 Second interval
    df.drop('Date', inplace=True, axis=1)

    # sampling_rate = 1  # Hz
    # df = df.resample('1S').mean()  # re-sample at 1 Second intervals
    # df = df.interpolate().dropna(how='any', axis=0)  # interpolate any missing data and delete bad rows

    dataX, dataY, dataZ = df['X'].values, df['Y'].values, df['Z'].values

    # Filter the data by passing it through a high-pass filter then through a low pass filter
    x = np.abs(cheby_lowpass_filter(cheby_highpass_filter(dataX, lower_frequency, 1, order), higher_frequency, 1, order))
    y = np.abs(cheby_lowpass_filter(cheby_highpass_filter(dataY, lower_frequency, 1, order), higher_frequency, 1, order))
    z = np.abs(cheby_lowpass_filter(cheby_highpass_filter(dataZ, lower_frequency, 1, order), higher_frequency, 1, order))

    df['X'], df['Y'], df['Z'] = x, y, z

    print(" --- took", round(process_time() - start, 2), " s")

    return df

def test():
    # Station information
    name, begin, end = 'ESP-Kodiak-3', '2016-05-01', '2016-05-31'
    # name, begin, end = 'ESP-Kodiak-3', '2016-04-10', '2016-05-10'
    path = '../data/' + name + '/' + begin + '-to-' + end + '.csv'

    # Loading in the magnetometer data
    column_names = ['Date', 'X', 'Y', 'Z']
    df = pd.read_csv(path, names=column_names)
    df.index = pd.to_datetime(df['Date'], utc=True)
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

    df['X'], df['Y'], df['Z'] = x, y, z 

    pt.plot_earthquake_magnetic(df, earthquake)
