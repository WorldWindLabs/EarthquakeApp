# Anomaly detection module

import datetime
from time import process_time
import pandas as pd
import numpy as np

import sys, os
lib_path = os.path.abspath(os.path.join('anomdetec'))
sys.path.append(lib_path)
import pyculiarity.detect_ts as pyc


def compute_anomalies(mag):
    '''
    Anomaly detection function for all axes directly from magnetic field

    :param mag: (dataframe) dataframe of magnetic data (series: X, Y, Z)

    :return: Tuple of anomaly data frames for each axes
    '''
    return get_anom(mag, 'X'), get_anom(mag, 'Y'), get_anom(mag, 'Z')


def get_anom(magnetic, axis):
    '''
    Axis anomaly detection helper function

    :param magnetic: (dataframe) dataframe of magnetic data (series: X, Y, Z)
    :param axis: One of the three axes ('X', 'Y', 'Z')

    :return: Data frame containing timestamps, values for the anomalies in that axis.
    '''
    print("Detecting anomalies for", axis, "axis", end='')
    start = process_time()

    # preprocessing data
    df = magnetic[['Date', axis]]
    df.columns = ["timestamp", "value"]

    # using pyculiarity to detect anomalies
    # TODO: mess around with maximum_anomalies and alpha to improve resulting plots
    eq_anom = pyc.detect_ts(df, maximum_anomalies=0.025, direction='pos', alpha=0.05)

    print(" --- took", round(process_time() - start, 2), " s")
    return eq_anom['anoms']


def compute_anomalies_for_earthquake(earthquake, anomalies, interval=24):
    '''
    Compiles known anomalies in timeseries for a specified event (earthquakes)

    :param earthquake: (pd dataframe) DF of earthquake events (timestamps, magnitudes, locations, etc.)
    :param anomaly: (dataframe) DF of anomalies in a timeseries (magnetic data)
    :param interval: (int) hours before an event (earthquake) in which to search for anomalies and compile

    :return pd: (dataframe; columns = X_anoms, Y_anoms, Z_anoms; index = Date)

            Columns:
            '[Axis]_anoms': list of number of anomalies in [Axis] within a period of time before the earthquake

            index:
            Date: Dates from input dataframe (earthquake)
    '''
    
    anoms = []
    for axis in range(len(anomalies)):
        axis_anoms = []
        anomaly = anomalies[axis]
        for index, row in earthquake.iterrows():
            end = index
            start = end - datetime.timedelta(hours=interval)
            axis_temp = anomaly[start:end]

            axis_anoms.append(len(axis_temp.index))

        anoms.append(axis_anoms)

    return pd.DataFrame({'X_anoms': anoms[0],
                         'Y_anoms': anoms[1],
                         'Z_anoms': anoms[2]},
                        index=earthquake.index)

def anomaly_rate(magnetic, anomalies, num_h=4):
    '''
    Creates anomaly 'rates' to be adapted into features for machine learning algorithms
    The anomaly 'rates' are anomalies per hour, and determine clusters of anomalies to be analyzed
    as normal or anomalous datapoints.

    :param magnetic: (dataframe) dataframe of magnetic data (series: X, Y, Z)
    :param anomalies: (dataframe) output of anomaly detection functions, (X, Y, Z)
    :param num_h: hour window in which to search for anomalies for creating an anomaly 'rate'

    :return anom_r: (dataframe; columns = anom_r, log_anom_r, log_z_score, log_z_score_zero_trans;
            index = Date)

            Columns:
            anom_r: anomalies/num_h (hour rate param)
            log_anom_r: log(10) transformation of anonm_r
            log_z_score: z score of log_anom_r
            log_z_score_zero_trans: series minimum transformation of data (absolute values)

            index:
            Date: Dates from input dataframe (magnetic)
        '''

    mag_interval = magnetic.resample('10T').mean()

    anom_rate = []
    for index, row in mag_interval.iterrows():
        end = index
        start = end - datetime.timedelta(hours=num_h)
        temp = anomalies.anoms[start:end]
        anom_rate.append(len(temp.index)/num_h)

    anom_r = pd.DataFrame()
    anom_r['anom_r'] = pd.Series(anom_rate)
    anom_r['log_anom_r'] = np.log(anom_r['anom_r'])
    anom_r.index = mag_interval.index
    anom_r = anom_r[anom_r.log_anom_r >= 0]
    anom_r['log_z_score'] = ((anom_r['log_anom_r']-anom_r['log_anom_r'].mean())/anom_r['log_anom_r'].std())
    anom_r['log_z_score_zero_trans'] = anom_r.log_z_score + abs(anom_r['log_z_score'].min())
    anom_r['Date'] = anom_r.index
   
    return anom_r