import numpy as np
import pandas as pd
import scipy.stats as stat
import matplotlib.pyplot as plt
import seaborn as sb
from time import process_time


def movingaverage(interval, window_size):
    '''
        Creates a moving average with inputs of interval (data) and window size (in # of datapoints)
        uses numpy convolution (np.convolve()) to create a moving average window.

        INPUTS:
        interval = (series, list, array like) time series data for moving average to be created
        window_size
        '''
    w = np.ones(int(window_size)) / float(window_size)
    return np.convolve(interval, w, 'same')


def weightedmovingaverage(interval, window_size):
    '''
        Creates a weighted moving average with inputs of interval (data) and
        window size (in # of datapoints) uses numpy convolution and cumulative
        sum (np.convolve() & np.cumsum()) to create a weighted moving average window.
        '''
    window = np.cumsum(np.ones(window_size, dtype=float), axis=0)
    w = window / np.sum(window)
    return np.convolve(interval, w, 'same')


def weighted_moving_average(x, y, step_size=0.05, width=1):
    '''
        Another method of creating a weighted moving average. Utilizes numpy arrays.
        (IN TESTING)
        '''
    bin_centers = np.arange(np.min(x), np.max(x) - 0.5 * step_size, step_size) + 0.5 * step_size
    bin_avg = np.zeros(len(bin_centers))

    # We're going to weight with a Gaussian function
    def gaussian(x, amp=1, mean=0, sigma=1):
        return amp * np.exp(-(x - mean) ** 2 / (2 * sigma ** 2))

    for index in range(0, len(bin_centers)):
        bin_center = bin_centers[index]
        weights = gaussian(x, mean=bin_center, sigma=width)
        bin_avg[index] = np.average(y, weights=weights)

    return bin_centers, bin_avg


def normality_test(dataframe):
    '''
        A normailty test for data within a data frame. Input a pandas dataframe and it will
        analyze it for the individual data series' skew and kurtosis to determine normailty.
        If data is not normal, it will create a transformed data series to normalize data
        (CURRENTLY ONLY WORKS FOR LOG NORMAL TRANSFORMAITONS)
        '''
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
                    break
            if transformed == True:
                print('Data', index, 'has been transformed, is now normal.')
                pass
            else:
                print('Error processing the data.')
                break
    if transformed == True:
        log_ls = ['log_X', 'log_Y', 'log_Z']
        for d in log_ls:
            dataframe['z_' + d] = (dataframe[d] - dataframe[d].mean()) / dataframe[d].std()
    else:
        print('Error processing the data.')
        pass

    return dataframe


def anom_det(mag, window=1000, method='weighted', threshold=2, correction=False, correctionfactor=10000):
    '''
        Anomaly detection algo utilizing moving averages to determine anomalous data points.
        for use with time series data. Outputs a tuple consisting of the first three data series'
        anomalous data points in dataframe format (columns = timestamp, anoms; index = timestamp).

        INPUTS:
        mag: dataframe to be analyzed
        window: windo for moving average (in # of data points)
        method: weighted or means moving average
        threshold: (1 = 68.3% confidence, 2 = 95% confidence, 3 = 99.7% confidence, > 3 = 99.99- % confidence)
                    standard deviation threshold in which anomalies will be detected
        correction: (boolean) compensation for data recording errors at start of a series
                    (created in digital signal procesisng)
        correctionfactor: number of rows to be removed to compensate for DSP recording errors

        OUTPUT:
        Tuple of 3 dataframes of the first 3 series in the mag input DF
        (for magnetic data analysis X,Y,Z)
        To retrieve in easily in DF format call function like so:

        df_1, df_2, df_3 = anom_det(mag, window = 1000, method = 'weighted'.....etc.)
        '''
    print("Weighted running average anomaly detection", end='')
    start = process_time()

    columns = mag.columns.tolist()

    # for g in columns:
    #     sb.distplot(mag[g])
    #     plt.show()

    if correction == True:
        mag = mag[correctionfactor:]

    events_ls = []
    for g in columns:

        if method == 'weighted':
            MOV = weightedmovingaverage(mag[g], window).tolist()
        else:
            MOV = movingaverage(mag[g], window).tolist()
        STD = np.std(MOV)

        events = []
        ind = []
        for d in range(len(mag[g])):
            if mag[g][d] > MOV[d] + threshold * STD:
                events.append([mag.index[d], mag[g][d]])
        events_df = pd.DataFrame(events, columns=['timestamp',
                                                  'anoms'])
        events_df.index = events_df['timestamp']
        events_ls.append(events_df)
    print(" --- took", round(process_time() - start, 2), " s")
    return events_ls[0], events_ls[1], events_ls[2]
