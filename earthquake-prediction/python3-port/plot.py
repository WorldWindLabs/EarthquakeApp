# NASA World Wind Earthquake Forecast Plot code

import datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sb
import pandas as pd
from scipy import signal


def graph_xyz(data):
    plt.subplots(1, figsize=(10, 6))
    plt.plot(data['X'], 'b-')
    plt.ylabel('X')

    plt.plot(data['Y'], 'r-')
    plt.ylabel('Y')

    plt.plot(data['Z'], 'y-')
    plt.ylabel('Z')

    plt.plot(np.linalg.norm(data, axis=1), 'g-')
    plt.ylabel('norm')

    plt.show()


def graph_coordinates(data, axis):
    plt.figure(figsize=(10, 6))
    plt.plot(data[axis], 'b-')
    plt.ylabel(axis)

    plt.show()


def graph_coordinates_time(vector, axis):
    time = mdates.drange(datetime.datetime(2014, 10, 21, 16),
                         datetime.datetime(2014, 10, 25, 16),
                         datetime.timedelta(minutes=15))

    f = plt.figure()

    plt.plot_date(time, vector[axis] / 50000, 'b-')
    plt.ylabel(axis)

    plt.axvline(datetime.datetime(2014, 10, 23, 8, 30, 24))  # 2014-10-23T08:30:24Z

    f.autofmt_xdate()

    plt.show()


# TODO: fix this function
# def plot_interval(init, final, origin):
#     magnetic_data = lmag.load_magnetic_data(init + "-to-" + final + ".csv")

#     earthquakes = leq.load_earthquake_data(init, final, origin)

#     graph_xyz(magnetic_data['vectors'])

#     for d in range(3):
#         graph_coordinates(magnetic_data['vectors'], d)

#     plt.show()


def plot_earthquake_anomalies_magnetic(earthquake, anomalies, magnetic, savefigure=False,
                                       savename='test_eq_anom_plt.png', figtitle=None):
    anomX, anomY, anomZ = anomalies

    anomX = anomX[100000:]
    anomY = anomY[100000:]
    anomZ = anomZ[100000:]
    magnetic = magnetic[100000:]


    f = plt.figure(figsize=(10, 5))
    f1 = f.add_subplot(311)
    f1.plot(magnetic.index, magnetic.X, color='b', linewidth='1', zorder=1)
    f1.set_ylim([0, 60])
    f2 = f.add_subplot(312)
    f2.plot(magnetic.index, magnetic.Y, color='g', linewidth='1', zorder=1)
    f2.set_ylim([0, 60])
    f3 = f.add_subplot(313)
    f3.plot(magnetic.index, magnetic.Z, color='orange', linewidth='1', zorder=1)
    f3.set_ylim([0, 60])

    # my_win = 20
    # mw1 = pd.rolling_mean(magnetic.X, window = my_win, center = True)
    # f1.plot(magnetic.index, mw1, color = 'r', linewidth = '1')
    # mw2 = pd.rolling_mean(magnetic.Y, window = my_win, center = True)
    # f2.plot(magnetic.index, mw2, color = 'r', linewidth = '1')    
    # mw3 = pd.rolling_mean(magnetic.Z, window = my_win, center = True)
    # f3.plot(magnetic.index, mw3, color = 'r', linewidth = '1')

    for index, row in earthquake.iterrows():
        if 4 > row['EQ_Magnitude'] > 3:
            f1.axvline(index, color='grey', linewidth=0.75, zorder=1)
            f2.axvline(index, color='grey', linewidth=0.75, zorder=1)
            f3.axvline(index, color='grey', linewidth=0.75, zorder=1)
        elif row['EQ_Magnitude'] > 4:
            f1.axvline(index, color='r', linewidth=1)
            f2.axvline(index, color='r', linewidth=1)
            f3.axvline(index, color='r', linewidth=1)

    f1.scatter(anomX.index, anomX.anoms, color='r', zorder=2)
    f2.scatter(anomY.index, anomY.anoms, color='r', zorder=2)
    f3.scatter(anomZ.index, anomZ.anoms, color='r', zorder=2)

    f.suptitle(figtitle)
    if savefigure == True:
        f = plt.savefig(savename, bbox_inches='tight')
        plt.close()
    else:
        plt.show()


def plot_earthquake_magnetic(earthquake, mag, savefigure=False, savename='test_eq_plt.png', figtitle=None):
    t, x, y, z = mag.index, mag.X, mag.Y, mag.Z
    f = plt.figure(figsize=(10, 5))

    f1 = f.add_subplot(311)
    f1.plot(t, x, color='g', linewidth='1')
    # f1.set_ylim([0, 25])  # set the y-axis of the first plot between 0 and 30
    f2 = f.add_subplot(312)
    f2.plot(t, y, color='g', linewidth='1')
    # f2.set_ylim([0, 10])  # set the y-axis of the second plot between 0 and 15
    f3 = f.add_subplot(313)
    f3.plot(t, z, color='g', linewidth='1')
    # f3.set_ylim([0, 20])  # set the z-axis of the third plot between 0 and 20

    for index, row in earthquake.iterrows():
        # this will draw a vertical red line on each of the three plots if the magnitude is greater than 3
        if 4 > row['EQ_Magnitude'] > 3:
            f1.axvline(index, color='grey', linewidth=0.75)
            f2.axvline(index, color='grey', linewidth=0.75)
            f3.axvline(index, color='grey', linewidth=0.75)
        elif row['EQ_Magnitude'] > 4:
            f1.axvline(index, color='r', linewidth=1)
            f2.axvline(index, color='r', linewidth=1)
            f3.axvline(index, color='r', linewidth=1)
    f.suptitle(figtitle)
    if savefigure == True:
        f = plt.savefig(savename, bbox_inches='tight')
        plt.close()
    else:
        plt.show()


def plot_AxB(a, b):
    plt.plot(a, b, 'ro')
    plt.show()


def plot_histogram(data, bins=30):
    sb.distplot(data, bins)
    plt.show()


def plot_magnetic(t, x, y, z):
    f = plt.figure()

    f1 = f.add_subplot(311)
    f1.plot(t, x, color='b', linewidth='1')
    f1.set_ylim([0, 20])  # set the y-axis of the first plot between 0 and 30
    f2 = f.add_subplot(312)
    f2.plot(t, y, color='g', linewidth='1')
    f2.set_ylim([0, 10])  # set the y-axis of the first plot between 0 and 30
    f3 = f.add_subplot(313)
    f3.plot(t, z, color='orange', linewidth='1')
    f3.set_ylim([0, 10])  # set the y-axis of the first plot between 0 and 30
    plt.show()


def plot_Y(y):
    plt.plot(y)
    plt.show()


def plot_fft(input_signal):
    fs = 1 / 123
    f, Pxx = signal.welch(input_signal, fs, nperseg=1024)
    plt.subplot(211)
    plt.plot(input_signal)
    plt.subplot(212)
    plt.plot(f, Pxx)
    plt.xlim([0, 1])
    plt.show()


# temporary visualization of anom rate against the earthquake/mag data
def plot_earthquake_anomalies_magnetic2(earthquake, anomalies, magnetic, X, Y, Z, savefigure=False,
                                        savename='test_anom_rate_plt.png', figtitle=None):
    anomX, anomY, anomZ = anomalies

    f = plt.figure()

    f1 = f.add_subplot(611)
    f1.plot(magnetic.index, magnetic.X, color='b', linewidth='1', zorder=1)
    f1.set_ylim([0, 60])
    f1.set_xlim([begin, end])

    f2 = f.add_subplot(612)
    f2.plot(X.index, X.log_z_score_zero_trans, color='b', linewidth='1', zorder=1)
    f2.set_xlim([begin, end])

    f3 = f.add_subplot(613)
    f3.plot(magnetic.index, magnetic.Y, color='g', linewidth='1', zorder=1)
    f3.set_ylim([0, 60])
    f3.set_xlim([begin, end])

    f4 = f.add_subplot(614)
    f4.plot(Y.index, Y.log_z_score_zero_trans, color='g', linewidth='1', zorder=1)
    f4.set_xlim([begin, end])

    f5 = f.add_subplot(615)
    f5.plot(magnetic.index, magnetic.Z, color='orange', linewidth='1', zorder=1)
    f5.set_ylim([0, 60])
    f5.set_xlim([begin, end])

    f6 = f.add_subplot(616)
    f6.plot(Z.index, Z.log_z_score_zero_trans, color='orange', linewidth='1', zorder=1)
    f6.set_xlim([begin, end])

    # my_win = 20
    # mw1 = pd.rolling_mean(magnetic.X, window = my_win, center = True)
    # f1.plot(magnetic.index, mw1, color = 'r', linewidth = '1')
    # mw2 = pd.rolling_mean(magnetic.Y, window = my_win, center = True)
    # f2.plot(magnetic.index, mw2, color = 'r', linewidth = '1')
    # mw3 = pd.rolling_mean(magnetic.Z, window = my_win, center = True)
    # f3.plot(magnetic.index, mw3, color = 'r', linewidth = '1')

    for index, row in earthquake.iterrows():
        if 4 > row['EQ_Magnitude'] > 3:
            f1.axvline(index, color='grey', linewidth=0.75)
            f3.axvline(index, color='grey', linewidth=0.75)
            f5.axvline(index, color='grey', linewidth=0.75)
        elif row['EQ_Magnitude'] > 4:
            f1.axvline(index, color='r', linewidth=1)
            f3.axvline(index, color='r', linewidth=1)
            f5.axvline(index, color='r', linewidth=1)

    f1.scatter(anomX.index, anomX.anoms, color='r', zorder=2)
    f3.scatter(anomY.index, anomY.anoms, color='r', zorder=2)
    f5.scatter(anomZ.index, anomZ.anoms, color='r', zorder=2)

    # TODO add shading showing where significant clusters are
    # plots = [f1, f2, f3, f4, f5, f6]
    # for d in X.
    f.suptitle(figtitle)
    if savefigure == True:
        f = plt.savefig(savename, bbox_inches='tight')
        plt.close()
    else:
        plt.show()

def plot_eq_mag_compare(eq, mag1, mag2, savefigure=False, savename='test_eq_mag.png', figtitle=None):
    t1, x1, y1, z1 = mag1.index, mag1.X, mag1.Y, mag1.Z
    t2, x2, y2, z2 = mag2.index, mag2.X, mag2.Y, mag2.Z

    mag1 = mag1[100000:]
    mag2 = mag2[100000:]

    f = plt.figure(figsize=(10, 5))

    f1 = f.add_subplot(611)
    f1.plot(t1, x1, color='b', linewidth='1', zorder=1)
    f1.set_ylim([0, 20])

    f2 = f.add_subplot(612)
    f2.plot(t2, x2, color='b', linewidth='1', zorder=1)
    f2.set_ylim([0, 20])

    f3 = f.add_subplot(613)
    f3.plot(t1, y1, color='g', linewidth='1', zorder=1)
    f3.set_ylim([0, 20])

    f4 = f.add_subplot(614)
    f4.plot(t2, y2, color='g', linewidth='1', zorder=1)
    f4.set_ylim([0, 20])

    f5 = f.add_subplot(615)
    f5.plot(t1, z1, color='orange', linewidth='1', zorder=1)
    f5.set_ylim([0, 20])

    f6 = f.add_subplot(616)
    f6.plot(t2, z2, color='orange', linewidth='1', zorder=1)
    f6.set_ylim([0, 20])

    for index, row in eq.iterrows():
        # this will draw a vertical red line on each of the three plots if the magnitude is greater than 3
        if 4 > row['EQ_Magnitude'] > 3:
            f1.axvline(index, color='grey', linewidth=0.75)
            f2.axvline(index, color='grey', linewidth=0.75)
            f3.axvline(index, color='grey', linewidth=0.75)
            f4.axvline(index, color='grey', linewidth=0.75)
            f5.axvline(index, color='grey', linewidth=0.75)
            f6.axvline(index, color='grey', linewidth=0.75)
        elif row['EQ_Magnitude'] > 4:
            f1.axvline(index, color='r', linewidth=1)
            f2.axvline(index, color='r', linewidth=1)
            f3.axvline(index, color='r', linewidth=1)
            f4.axvline(index, color='r', linewidth=1)
            f5.axvline(index, color='r', linewidth=1)
            f6.axvline(index, color='r', linewidth=1)
    f.suptitle(figtitle)
    if savefigure == True:
        f = plt.savefig(savename, bbox_inches='tight')
        plt.close()
    else:
        plt.show()
