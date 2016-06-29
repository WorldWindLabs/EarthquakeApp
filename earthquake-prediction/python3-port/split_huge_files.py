# NASA World Wind Earthquake Data Analysis code
import datetime
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
import csv

name, begin, end = 'ESP-Kodiak-3', '2016-04-10', '2016-05-10'																																																																									
name, begin, end = 'ESP-Kodiak-3', '2016-03-31', '2016-06-21'																																																																									
# name, begin, end = 'ESP-Kenny-Lake-1', '2016-04-01', '2016-06-21'
# name, begin, end = 'ESP-Kenny-Lake-1', '2016-04-01', '2016-04-02'

num_parts = 8

for i in range(2, num_parts):
	n = 80000000
	magnetic = mag.load_magnetic_data(name, begin, end, skiprows = 3301000+i*n, nrows = n)

	column_names = ['X', 'Y', 'Z']
	new_begin = magnetic.index[0].strftime("%Y-%m-%d")
	new_end = magnetic.index[-1].strftime("%Y-%m-%d")

	magnetic = magnetic[column_names]	
	path = '../data/test2/' + name + '/' + new_begin + '-to-' + new_end
	magnetic.to_csv(path + '.csv', colums = column_names, header = False)
	print("done writing")

	(mag.upsample_to_sec(magnetic)).to_csv(path + 'sec.csv', colums = column_names, header = False)
	print("done writing sec sample")
	# pt.plot_magnetic(magnetic, savename = name+begin+end)
