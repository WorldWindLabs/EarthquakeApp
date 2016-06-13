# NASA World Wind Earthquake Data Analysis code
# Frozen code is an spatial analysis package, if you want you can download these packages
# none of it is currently used in the code, but I have it here incase it comes in handy.
'''
import geopandas as gpd
import os
import fiona
import folium
import numpy as np
import seaborn as sb
import shapely 
from shapely.geometry import Point, LineString
import pandas as pd
import matplotlib.pyplot as plt
import pysal as ps
from pysal.contrib.viz import mapping as maps
import matplotlib.cm as cms
# Enable replication
import random
random.seed(123456789)
np.random.seed(123456789)

# Imported from PySQL -- do not change
from pysal.esda.mapclassify import Quantiles, Equal_Interval, Fisher_Jenks
schemes = {'equal_interval': Equal_Interval, \
           'quantiles': Quantiles, \
           'fisher_jenks': Fisher_Jenks}

srcdir = os.path.join(os.path.expanduser("~"),"Desktop","NASA Proj")
shpdir = os.path.join(srcdir,'shapes')
datdir = os.path.join(srcdir,'data')
outdir = os.path.join(srcdir,'results')

os.chdir(srcdir)
'''
#Gabriel's code
import csv
import numpy as np
import datetime
import matplotlib.pyplot as plt
import urllib
import matplotlib.dates as mdates

path = '/Kodiak-3/'
# path = '../data/Kodiak-InteleCell/'

def graphXYZ(vector):
	
	f, ax1 = plt.subplots(1, figsize = (10,6))
	plt.plot(vector.T[0], 'b-')
	plt.ylabel('X')

	plt.plot(vector.T[1], 'r-')
	plt.ylabel('Y')

	plt.plot(vector.T[2], 'y-')
	plt.ylabel('Z')

	plt.plot(np.linalg.norm(vector, axis = 1), 'g-')
	plt.ylabel('norm')

        f.savefig(os.path.join(outdir, "-".join(["XYZgraph"]) + ".png"), format='png')
	plt.close()
	

def graphcoord(vector, axis):
	f = plt.figure(figsize = (10, 6))
	plt.plot(vector.T[axis]/50000, 'b-')
	plt.ylabel(axis)
        
        f.savefig(os.path.join(outdir, "-".join(["graphcoord"]) + ".png"), format='png')
	plt.close()

def graphcoord_time(vector, axis):
	time = mdates.drange(datetime.datetime(2014, 10, 21, 16), 
                     datetime.datetime(2014, 10, 25, 16),
                     datetime.timedelta(minutes=15))

	f = plt.figure()

	plt.plot_date(time, vector.T[axis]/50000, 'b-')
	plt.ylabel(axis)
	# 2014-10-23T08:30:24Z
	plt.axvline(datetime.datetime(2014, 10, 23, 8, 30, 24))

	f.autofmt_xdate()
	
	f.savefig(os.path.join(outdir, "-".join([str.axis, "graphcoord_time"]) + ".png"), format='png')
	plt.close()

def graphdiff(vector):
	diff = []

	for i, v in enumerate(vector):
		if i > 1:
			diff.append(np.linalg.norm(v - vector[i-1]))

	for i, x in enumerate(diff):
		if x < 5000:
			diff[i] = 0

	f = plt.figure(figsize = (10, 6))
	plt.plot(diff)
	f.savefig(os.path.join(outdir, "-".join(["graphdiff"]) + ".png"), format='png')
	plt.close()

def loadmagnetic(file):
	with open(datdir + path + file, 'rb') as csvfile:

		row_count = sum(1 for row in csvfile)
		vector = np.zeros((row_count, 3))
		time = []

	with open(datdir + path + file, 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		
		for i, row in enumerate(reader):
			if row and len(row) == 4:
				time.append(row[0])
				vector[i] = row[1:]
		return {'times': time, 'vectors': vector}

def getearthquake(minDate, maxDate, origin):
	
	minMagnitude = "0"
	#maxMagnitude = "10"

	maxdist = "900"

	resourcesUrl = "http://earthquake.usgs.gov/fdsnws/event/1/query?format=csv"
	dates = "&starttime="+minDate+"&endtime="+maxDate
	magnitutes = "&minmagnitude"+minMagnitude
	local = "&latitude=" + origin['lati'] + "&longitude=" + origin['long'] + "&maxradiuskm=" + maxdist

	opener = urllib.FancyURLopener({})
	f = opener.open(resourcesUrl + dates + magnitutes + local)
	data = f.read()
	
	def parse_csv(data):
		earthquakes = []

		for line in data.split('\n'):
			eq = line.split(',')
			if len(eq) > 4:
				# earthquakes.append({'time': eq[0], 'latitude': eq[1], 'longitude': eq[2], 'mag': eq[4]})
				earthquakes.append([eq[0], eq[1], eq[2], eq[4]])

		return earthquakes[1:]

	return parse_csv(data)

xyzgroup1 = [0, 1, 2]
def plot_interval(init, final, origin):
	magnetic_data = loadmagnetic(init + "-to-" + final + ".csv")

	earthquakes = getearthquake(init, final, origin)

	graphXYZ(magnetic_data['vectors'])

	graphdiff(magnetic_data['vectors'])
        
        for d in xyzgroup1:
	   graphcoord(magnetic_data['vectors'], d)

	#graphcoord_time(magnetic_data['vectors'], 0)
	
#kodiak3 = {'lati': "57.747225", 'long': "-152.496467"}
#plot_interval('10-04-16', '17-04-16', kodiak3)

####################################################################################
#Test code for analysis kodiacIC_Anomaly.csv is Kodiak intelecel data for the dates 27-05-2015 - 30-05-2015

kodiakIC = {'lati': '57.79348', 'long': '-152.3932'}

header = ['DateTime', 'X', 'Y', 'Z']
colnames = ['Date', 'X', 'Y', 'Z']
df = pd.read_csv(os.path.join(datdir,'kodiakIC_Anomaly.csv'))
del df['Unnamed: 4']
df.columns = colnames
df.interpolate()
dft = pd.to_datetime(df.Date)
df.index = dft
del df['Date']

#f = plt.figure()
#f = df['X'].plot()
#plt.show()

#DATE FORMAT FOR 'getearthquake()' IS AMERICAN, YEAR FIRST
eq = getearthquake('2015-05-27', '2015-05-30', kodiakIC)

header1 = ['DateTime', 'Latitude', 'Longitude', 'EQ_Magnitude']
eqdf = pd.DataFrame(eq, columns = header1)
eqt = pd.to_datetime(eqdf.DateTime)
eqdf.index = eqt

del eqdf['DateTime']

