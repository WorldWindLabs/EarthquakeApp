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
	path = '../data/' + station + '/' + begin + '-to-' + end + '.csv'

	colnames = ['Date', 'X', 'Y', 'Z']
	df = pd.read_csv(path)
	del df['Unnamed: 4']
	df.columns = colnames
	df.interpolate()
	dft = pd.to_datetime(df.Date)
	df.index = dft
	del df['Date']

	return df

# print load('InteleCell-Kodiak', '2014-10-22', '2014-12-22')
