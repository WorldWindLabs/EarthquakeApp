import numpy as np
import pandas as pd
import scipy.stats as stat
import matplotlib.pyplot as plt
import seaborn as sb



def movingaverage(interval, window_size):
    window = np.ones(int(window_size)) / float(window_size)
    return np.convolve(interval, window, 'same')


def weighted_moving_average(x, y, step_size=0.05, width=1):
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


def anom_det(mag):
    columns = mag.columns.tolist()
    # for g in columns:
    #     sb.distplot(mag[g])
    #     plt.show()

    # mag = mag[10000:]

    events_ls = []
    for g in columns:
        MOV = movingaverage(mag[g], 1000).tolist()
        # MOV = MOV[10000:]
        STD = np.std(MOV)

        events = []
        ind = []
        for d in range(len(mag[g])):
            if mag[g][d] > MOV[d] + 2 * STD:
                events.append([mag.index[d], mag[g][d]])
        events_df = pd.DataFrame(events, columns=['timestamp',
                                                  'anoms'])
        events_df.index = events_df['timestamp']
        events_ls.append(events_df)
    return events_ls[0], events_ls[1], events_ls[2]