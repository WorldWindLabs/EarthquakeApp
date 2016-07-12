import numpy as np
import pandas as pd
import scipy.stats as stat
import matplotlib.pyplot as plt
import seaborn as sb


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

def test_plot_anoms(mag):

    t, x, y, z = mag.index, mag.z_log_X, mag.z_log_Y, mag.z_log_Z

    columns = mag.columns.tolist()
    for g in columns:
        sb.distplot(mag[g])
        plt.show()

    MOV = movingaverage(mag, 1000).tolist()
    print(MOV)
    mag = mag[10000:]
    MOV = MOV[10000:]

    STD = np.std(MOV)
    events = []
    ind = []
    for d in range(len(mag)):
        if mag[d] > MOV[d] + 2 * STD:
            events.append([mag.index[d], mag[d]])
    events_df = pd.DataFrame(events, columns=['timestamp',
                                              'anom_events'])
    events_df.index = events_df['timestamp']
    del events_df.timestamp
    print(events_df.head())

    f = plt.figure(figsize=(15, 5))
    f1 = f.add_subplot(111)
    f1.plot(t, x, color='skyblue', linewidth=0.75, zorder=1)
    f1.plot(mag.index, MOV, color='r', linewidth=0.5, zorder=2)
    f1.scatter(events_df.index, events_df.anom_events, facecolors='none',
               edgecolors='r', linewidths=0.75, zorder=3)
    # f1.set_ylim([0, 160])
    # f1.set_xlim([mag.index[0], end])
    plt.show()