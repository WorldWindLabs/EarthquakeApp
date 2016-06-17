# NASA World Wind Earthquake Forecast Plot code

import datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import loadearthquake as leq
import loadmagnetic as lmag


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

    plt.axvline(datetime.datetime(2014, 10, 23, 8, 30, 24))      # 2014-10-23T08:30:24Z

    f.autofmt_xdate()

    plt.show()


# TODO: fix this function
def plot_interval(init, final, origin):
    magnetic_data = lmag.load_magnetic_data(init + "-to-" + final + ".csv")

    earthquakes = leq.load_earthquake_data(init, final, origin)

    graph_xyz(magnetic_data['vectors'])

    for d in range(3):
        graph_coordinates(magnetic_data['vectors'], d)

    plt.show()


def plot_earthquake_anomalies_magnetic(axis, earthquake):
    fX, fY, fZ = axis
    (eqX, tdfX) = fX
    (eqY, tdfY) = fY
    (eqZ, tdfZ) = fZ

    f = plt.figure()
    f1 = f.add_subplot(311)
    f1.plot(tdfX.timestamp, tdfX.value, color='b')
    f2 = f.add_subplot(312)
    f2.plot(tdfY.timestamp, tdfY.value, color='g')
    f3 = f.add_subplot(313)
    f3.plot(tdfZ.timestamp, tdfZ.value, color='orange')

    for index, row in earthquake.iterrows():
        if 4 > row['EQ_Magnitude'] > 3:
            f1.axvline(index, color='grey', linewidth=0.75)
            f2.axvline(index, color='grey', linewidth=0.75)
            f3.axvline(index, color='grey', linewidth=0.75)
        elif row['EQ_Magnitude'] > 4:
            f1.axvline(index, color='r', linewidth=1)
            f2.axvline(index, color='r', linewidth=1)
            f3.axvline(index, color='r', linewidth=1)

    f1.scatter(eqX.index, eqX.anoms, color='r')
    f2.scatter(eqY.index, eqY.anoms, color='r')
    f3.scatter(eqZ.index, eqZ.anoms, color='r')
    plt.show()
