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

	for i, data in enumerate(anorm_rates):
	    temp_index = []
	    # temp_anoms = []
	    for index, row in data.iterrows():
	        if row['log_z_score_zero_trans'] > 1.96:
	            temp_index.append(index)

	    cluster_pts.append(temp_index)

	clusters_intervals = []

	for data in cluster_pts:
		tmp = []
		first_on_cluster = True
		last_time = data[0]
		for i, time in enumerate(data):
			if first_on_cluster:
				ini_time = time
				first_on_cluster = False

			elif time - data[i-1] > dt.timedelta(hours=4):
				tmp.append((ini_time, data[i-1]))
				first_on_cluster = True
			
		if not first_on_cluster:
			tmp.append((ini_time, data[-1]))
		clusters_intervals.append(tmp)

	clusters = []
	for i, axis in enumerate(clusters_intervals):
		tmp = []
		for inter in axis:
			cut = anomalies[i][inter[0]:inter[1]]
			if len(cut):
				tmp.append(cut)
		clusters.append(tmp)

	return clusters

def get_mean(df_c):
    df = pd.DataFrame()
    df['unix_time'] = df_c.index.astype(np.int64)
    df_mean = df.unix_time.mean()
    df_dt = pd.to_datetime(df_mean)
    # print(df_mean)
    # print(df_dt)
    return df_dt

def get_std(df_c):
    df = pd.DataFrame()
    df['unix_time'] = df_c.index.astype(np.int64)
    df_std = df.unix_time.std()
    df_dt = pd.to_timedelta(df_std)
    # print(df_std)
    # print(df_dt)
    return df_dt

def comp_features(anomalies_clusters): 
    features = []
    interval = []
    for axis in anomalies_clusters:
        feat_axis = []
        interval_axis = []
        for cluster in axis:
            mean = get_mean(cluster)
            feat_axis.append([len(cluster), #size
                 (cluster.timestamp[-1]-cluster.timestamp[0])/len(cluster), # time density
                 (mean -  cluster.timestamp[0])/len(cluster), # time diameter
                 (get_std(cluster)), # time standard deviation
                 (max(cluster.anoms) -  min(cluster.anoms))/len(cluster), # value interval
                 (cluster.anoms.mean() -  cluster.anoms[0])/len(cluster), # value diameter
                 cluster.anoms.std(), # value standard deviation
                 max(cluster.anoms) # max value
                 # TODO: confidence interval radius 
                ])
            interval_axis.append((min(cluster.timestamp), max(cluster.timestamp)))

        interval.append(interval_axis)
        features.append(feat_axis)
        
    return features, interval