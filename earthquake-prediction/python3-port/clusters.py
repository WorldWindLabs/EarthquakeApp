# NASA World Wind Earthquake Data Analysis code
import datetime as dt
from datetime import datetime
from time import process_time
import matplotlib.pyplot as plt
import loadearthquake as eaq
import loadmagnetic as mag
import plot as pt
import pyculiarity.detect_ts as pyc
import stationsdata as station
import pandas as pd
import bandfilter as bf
import statsmodels.api as sm
import detectanomalies as anom
import seaborn as sb
import numpy as np


def get(anorm_rates, anomalies):
    # extracts the clusters in dates, albeit sloppily
    cluster_pts = []
    for index, row in anorm_rates.iterrows():
        if row['log_z_score_zero_trans'] > 1.96:
            cluster_pts.append(index)

    # gets the cluster time intervals
    clusters_intervals = []
    first_on_cluster, last_time = True, cluster_pts[0]

    for i, time in enumerate(cluster_pts):
        if first_on_cluster:
            ini_time = time
            first_on_cluster = False

        elif time - cluster_pts[i - 1] > dt.timedelta(hours=2):
            clusters_intervals.append((ini_time, cluster_pts[i - 1]))
            first_on_cluster = True

    if not first_on_cluster:
        clusters_intervals.append((ini_time, cluster_pts[-1]))

    # gets the anomaly points
    clusters = []
    for begin, end in clusters_intervals:
        cut = anomalies[begin:end]
        if len(cut):  # TODO: why?
            clusters.append(cut)

    return clusters


def get_mean(df_c):
    df = pd.DataFrame()
    df['unix_time'] = df_c.index.astype(np.int64)
    df_mean = df.unix_time.mean()
    df_dt = pd.to_datetime(df_mean)
    return df_dt


def get_std(df_c):
    df = pd.DataFrame()
    df['unix_time'] = df_c.index.astype(np.int64)
    df_std = df.unix_time.std()
    df_dt = pd.to_timedelta(df_std)
    return df_dt


def comp_features(anomalies_clusters):
    features = []
    interval = []

    for cluster in anomalies_clusters:
        mean = get_mean(cluster)
        features.append([len(cluster),  # size
                         ((cluster.timestamp[-1] - cluster.timestamp[0]) / len(cluster)).total_seconds(),  # time density
                         ((mean - cluster.timestamp[0]) / len(cluster)).total_seconds(),  # time diameter
                         (get_std(cluster)).total_seconds(),  # time standard deviation
                         (max(cluster.anoms) - min(cluster.anoms)) / len(cluster),  # value interval
                         (cluster.anoms.mean() - cluster.anoms[0]) / len(cluster),  # value diameter
                         cluster.anoms.std(),  # value standard deviation
                         max(cluster.anoms)  # max value
                         # TODO: confidence interval radius
                         ])
        interval.append((min(cluster.timestamp), max(cluster.timestamp)))

    return features, interval
