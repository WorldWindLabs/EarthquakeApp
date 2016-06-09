# Plot magnetic field data 

import csv
import numpy as np
import datetime
import matplotlib.pyplot as plt
import urllib
import matplotlib.dates as mdates

path = '../data/Kodiak-3/'
# path = '../data/Kodiak-InteleCell/'

def graphXYZ():
	plt.plot(vector.T[0], 'b-')
	plt.ylabel('X')

	plt.plot(vector.T[1], 'r-')
	plt.ylabel('Y')

	plt.plot(vector.T[2], 'y-')
	plt.ylabel('Z')

	plt.plot(np.linalg.norm(vector, axis = 1), 'g-')
	plt.ylabel('norm')

	plt.show()

def graphcoord(axis):
	plt.plot(vector.T[axis]/50000, 'b-')
	plt.ylabel(axis)

	plt.show()

def graphcoord_time(axis):
	time = mdates.drange(datetime.datetime(2014, 10, 21, 16), 
                     datetime.datetime(2014, 10, 25, 16),
                     datetime.timedelta(minutes=15))

	fig = plt.figure()

	plt.plot_date(time, vector.T[axis]/50000, 'b-')
	plt.ylabel(axis)
	# 2014-10-23T08:30:24Z
	plt.axvline(datetime.datetime(2014, 10, 23, 8, 30, 24))

	fig.autofmt_xdate()
	plt.show()

def graphdiff():
	diff = []

	for i, v in enumerate(vector):
		if i > 1:
			diff.append(np.linalg.norm(v - vector[i-1]))

	for i, x in enumerate(diff):
		if x < 5000:
			diff[i] = 0

	plt.plot(diff)
	plt.show()

def loadmagnetic(file):
	with open(path + file, 'rb') as csvfile:

		row_count = sum(1 for row in csvfile)
		vector = np.zeros((row_count, 3))
		time = []

	with open(path + file, 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		
		for i, row in enumerate(reader):
			if row and len(row) == 4:
				time.append(row[0])
				vector[i] = row[1:]
		return {'times': time, 'vectors': vector}

def getearthquake(minDate, maxDate, origin):
	
	minMagnitude = "4.8"
	maxMagnitude = "10"

	maxdist = "900"

	resourcesUrl = "http://earthquake.usgs.gov/fdsnws/event/1/query?format=csv"
	dates = "&starttime="+minDate+"&endtime="+maxDate
	magnitutes = "&minmagnitude=" + minMagnitude + "&maxmagnitude=" + maxMagnitude 
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

def plot_interval(init, final, origin):
	magnetic_data = loadmagnetic(init + "-to-" + final + ".csv")

	earthquakes = getearthquake(init, final, origin)

	# graphXYZ()

	# graphdiff()

	# graphcoord(2)

	# graphcoord_time(t, 0)

kodiak3 = {'lati': "57.747225", 'long': "-152.496467"}
plot_interval('10-04-16', '17-04-16', kodiak3)

