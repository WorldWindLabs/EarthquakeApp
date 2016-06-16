# NASA World Wind Earthquake load data code

import csv
import numpy as np
import os
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import urllib
import matplotlib.dates as mdates

def magload(station, begin, end):
	print "Loading magnetic data"
	path = '../data/' + station + '/' + begin + '-to-' + end + '.csv'

	if station[:10] == "InteleCell":
		colnames = ['Date', 'X', 'Y', 'Z']
		df = pd.read_csv(path)
		del df['Unnamed: 4']
		df.columns = colnames
		df.interpolate()
		dft = pd.to_datetime(df.Date)
		df.index = dft

		return df

	elif station[:3] == 'ESP':
		colnames = ['Date', 'X', 'Y', 'Z']
		df = pd.read_csv(path, names = colnames)
		# temp = []
		# for d in df['Date']:
		# 	temp.append(d.split('.')[0])
		# df['Date'] = temp
		dft = pd.to_datetime(df.Date)
		df.Date = df.Date.astype('object')
		df.index = dft
		df = df.resample('1T').mean()
		df['Date'] = df.index
		df = df.interpolate()
		return df

	else:
		print "ERROR - No station recognized"


# print load('InteleCell-Kodiak', '2014-10-22', '2014-12-22')
