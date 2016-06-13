# NASA World Wind Earthquake load data code

import csv
import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import urllib
import matplotlib.dates as mdates

def load(minDate, maxDate, origin, minMagnitude = "0", maxdist = "900"):
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