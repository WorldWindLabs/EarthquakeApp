# NASA World Wind Earthquake Forecast Plot code

import csv
import numpy as np
import os
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import urllib
import matplotlib.dates as mdatess
import loadmagnetic as lmag
import loadearthquake as leq
# import cairo

def graphXYZ(data):

	f, ax1 = plt.subplots(1, figsize = (10,6))
	plt.plot(data['X'], 'b-')
	plt.ylabel('X')

	plt.plot(data['Y'], 'r-')
	plt.ylabel('Y')

	plt.plot(data['Z'], 'y-')
	plt.ylabel('Z')

	plt.plot(np.linalg.norm(data, axis = 1), 'g-')
	plt.ylabel('norm')

	plt.show()
	# f.savefig(os.path.join(outdir, "-".join(["XYZgraph"]) + ".png"), format='png')
	# plt.close()
	
def graphcoord(data, axis):

	f = plt.figure(figsize = (10, 6))
	plt.plot(data[axis], 'b-')
	plt.ylabel(axis)
       
	plt.show()
	# f.savefig(os.path.join(outdir, "-".join(["graphcoord"]) + ".png"), format='png')
	# plt.close()

def graphcoord_time(vector, axis):

	time = mdates.drange(datetime.datetime(2014, 10, 21, 16), 
                     datetime.datetime(2014, 10, 25, 16),
                     datetime.timedelta(minutes=15))

	f = plt.figure()

	plt.plot_date(time, vector[axis]/50000, 'b-')
	plt.ylabel(axis)
	# 2014-10-23T08:30:24Z
	plt.axvline(datetime.datetime(2014, 10, 23, 8, 30, 24))

	f.autofmt_xdate()
	
	plt.show()
	# f.savefig(os.path.join(outdir, "-".join([str.axis, "graphcoord_time"]) + ".png"), format='png')
	# plt.close()

# TODO: graph the derivate
#def graphderivate(vector):
	# diff = []

	# for i, v in enumerate(vector):
	# 	if i > 1:
	# 		diff.append(np.linalg.norm(v - vector[i-1]))

	# for i, x in enumerate(diff):
	# 	if x < 5000:
	# 		diff[i] = 0

	# f = plt.figure(figsize = (10, 6))
	# plt.plot(diff)
	
	# plt.show()
	# f.savefig(os.path.join(outdir, "-".join(["graphdiff"]) + ".png"), format='png')
	# plt.close()

def plot_interval(init, final, origin):
	magnetic_data = lmag.magload(init + "-to-" + final + ".csv")

	earthquakes = leq.eqload(init, final, origin)

	graphXYZ(magnetic_data['vectors'])

	#graphdiff(magnetic_data['vectors'])
        
	for d in range(3):
		graphcoord(magnetic_data['vectors'], d)

	plt.show()
	#graphcoord_time(magnetic_data['vectors'], 0)

def plot_earthquake_anomalies_magnetic(axis, earthquake):
	fX, fY, fZ = axis
	(eqX, tdfX) = fX
	(eqY, tdfY) = fY
	(eqZ, tdfZ) = fZ

	f, ax1 = plt.subplots(1)
	tdfX.plot(ax = ax1) 
	tdfY.plot(ax = ax1) 
	tdfZ.plot(ax = ax1) 


	for index, row in earthquake.iterrows():
		if row['EQ_Magnitude'] > 3:
			ax1.axvline(index, color = 'brown', linewidth = 0.75)

	ax1.scatter(eqX.index, eqX.anoms, color = 'r')
	ax1.scatter(eqY.index, eqY.anoms, color = 'r')
	ax1.scatter(eqZ.index, eqZ.anoms, color = 'r')
	plt.show()

