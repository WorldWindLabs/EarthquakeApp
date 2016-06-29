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

# Date format: YYYY-MM-DD

# name, begin, end = 'InteleCell-Kodiak', '2014-10-22', '2014-12-22'
# name, begin, end = 'ESP-Kodiak-3', '2016-04-10', '2016-04-13'
# name, begin, end = 'ESP-Kodiak-3', '2016-05-19', '2016-05-22'
# name, begin, end = 'ESP-Kodiak-3', '2016-04-07', '2016-05-31'
# name, begin, end = 'ESP-Kodiak-3', '2016-04-10', '2016-05-10'
# # name, begin, end = 'ESP-Kodiak-3', '2016-04-28', '2016-05-02'
# # name, begin, end = 'ESP-Kodiak-2', '2016-06-05', '2016-06-21'
# stationcoord = station.get(name)
# earthquake = eaq.load_earthquake_data(begin, end, stationcoord, min_magnitude=2.5)



stations = [['ESP-Kenny-Lake-1', '2016-04-01', '2016-04-19'],
            ['ESP-Kenny-Lake-1', '2016-04-19', '2016-05-05'],
            ['ESP-Kenny-Lake-1', '2016-04-28', '2016-05-02'],
            ['ESP-Kenny-Lake-1', '2016-05-05', '2016-05-24'],
            ['ESP-Kenny-Lake-1', '2016-05-19', '2016-05-22'],
            ['ESP-Kenny-Lake-1', '2016-05-24', '2016-06-16'],
            ['ESP-Kenny-Lake-1', '2016-06-16', '2016-06-21'],
            ['ESP-Kodiak-2', '2016-06-05', '2016-06-21'],
            ['ESP-Kodiak-3', '2016-04-07', '2016-04-30'],
            ['ESP-Kodiak-3', '2016-04-10', '2016-04-17'],
            ['ESP-Kodiak-3', '2016-04-28', '2016-05-02'],
            ['ESP-Kodiak-3', '2016-05-19', '2016-05-22'],
            ['ESP-Kodiak-3', '2016-06-03', '2016-06-10'],
            ['ESP-Kodiak-4', '2016-06-04', '2016-06-21']]

dates_w_morethan_3_eqs = []

for item in stations:
    name, begin, end = item
    stationcoord = station.get(name)
    earthquake = eaq.load_earthquake_data(begin, end, stationcoord, min_magnitude=4)

    if len(earthquake.index) >= 1:
        dates_w_morethan_3_eqs.append(item)

print(dates_w_morethan_3_eqs)

# stations2 = [['ESP-Kenny-Lake-1', '2016-04-19', '2016-05-05'], 
# 			['ESP-Kodiak-3', '2016-04-07', '2016-04-30'], 
			# ['ESP-Kodiak-3', '2016-04-28', '2016-05-02']]

for item in dates_w_morethan_3_eqs:
	name, begin, end = item
	# loading the magnetic data
	stationcoord = station.get(name)
	earthquake = eaq.load_earthquake_data(begin, end, stationcoord, min_magnitude=2.5)
	magnetic = mag.load_magnetic_data(name, begin, end)
	# computing anomalies
	# mag_filtrd = bf.cheby_filter(magnetic.copy())
	mag_filtrd = bf.butter_filter(magnetic.copy())
	anomalies = anom.compute_anomalies(mag.upsample_to_min(mag_filtrd))

	anoms_per_eq = anom.compute_anomalies_for_earthquake(earthquake, anomalies)
	earthquake = eaq.add_anomalies(earthquake, anoms_per_eq)

	# pt.plot_histogram(earthquake.total_anoms)  # [earthquake['total_anoms'] > 0])
	pt.plot_earthquake_anomalies_magnetic(earthquake, anomalies, mag_filtrd, savefigure = True, 
		savename = '-'.join((name,begin,end,'anom_filtered_plt.png')), figtitle = '-'.join((name,begin,end)))
	pt.plot_earthquake_magnetic(earthquake, magnetic, savefigure = True,
		savename = '-'.join((name,begin,end,'raw_plt.png')), figtitle = '-'.join((name,begin,end)))


'''
anorm_rates = anom.compute_cluster(magnetic, anomalies)
# print(anorm_rates)

# temporary visualization of anom rate against the earthquake/mag data
def plot_earthquake_anomalies_magnetic(earthquake, anomalies, magnetic, X, Y, Z):
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

    plt.show()

# plot_earthquake_anomalies_magnetic(earthquake, anomalies, mag_filtrd, X, Y, Z)

# extracts the clusters in dates, albeit sloppily
cluster_pts = []

for i, data in enumerate(anorm_rates):
    temp_index = []
    # temp_anoms = []
    for index, row in data.iterrows():
        if row['log_z_score_zero_trans'] > 1.96:# and index in anomalies[i].index:
            temp_index.append(index)
            # temp_anoms.append(anomalies[i].loc[index].anoms)

    # temp = pd.DataFrame()
    # temp['Date'] = temp_index
    # temp['anoms'] = temp_anoms
    # temp.index = temp['Date']
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

feat, means = anom.cluster(clusters)

x = feat[0]

def look_earthquake(radius, h, times):
	y = []
	for cluster_t in times:
		earthquake = eaq.load_earthquake_data(datetime.isoformat(cluster_t),
			 datetime.isoformat(cluster_t+dt.timedelta(hours=h)), 
			 stationcoord, 
			 max_distance = radius, 
			 min_magnitude = 3)

		if len(earthquake.index) >= 1:
			y.append(True)
		else:
			y.append(False)
	return y

y = []
for i in range(3):
	y.append(look_earthquake("400", 10, means[i]))

print(y)
'''