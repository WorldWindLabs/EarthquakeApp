# NASA World Wind Earthquake Data Analysis code
import pyculiarity as pyc
import csv
import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import os
import urllib
import matplotlib.dates as mdates
import loadearthquake as eaq
import loadmagnetic as mag
import stationsdata as station
import plot as pt

#srcdir = os.path.join(os.path.expanduser("~"),"EarthquakeApp","earthquake-prediction", 'dev')
#os.chdir(srcdir)

#plot_interval('10-04-16', '17-04-16', kodiak3)

####################################################################################
#Test code for analysis kodiacIC_Anomaly.csv is Kodiak intelecel data for the dates 27-05-2015 - 30-05-2015

# name = 'InteleCell-Kodiak'
name = 'ESP-Kodiak-3'
# YYYY-MM-DD
# begin, end = '2014-10-22', '2014-12-22'
begin, end = '2016-04-10', '2016-04-13'

stationcoord = station.get(name)
magnetic = mag.magload(name, begin, end)

print magnetic.head()

earthquake = eaq.eqload(begin, end, stationcoord)

tdfX = pd.DataFrame()
tdfX['timestamp'] = magnetic.Date
tdfX['magx'] = magnetic.X
eq_anom = pyc.detect_ts(tdfX, max_anoms = 0.1, direction = 'both', alpha = 0.05)

#This creates a dataframe from the anomaly results. I am not to sure why passing eq_anom['anoms'] creates a dataframe
eqX = eq_anom['anoms']

tdfY = pd.DataFrame()
tdfY['timestamp'] = magnetic.Date
tdfY['magx'] = magnetic.Y
eq_anom = pyc.detect_ts(tdfY, max_anoms = 0.1, direction = 'both', alpha = 0.05)

#This creates a dataframe from the anomaly results. I am not to sure why passing eq_anom['anoms'] creates a dataframe
eqY = eq_anom['anoms']

tdfZ = pd.DataFrame()
tdfZ['timestamp'] = magnetic.Date
tdfZ['magx'] = magnetic.Z
eq_anom = pyc.detect_ts(tdfZ, max_anoms = 0.1, direction = 'both', alpha = 0.05)
#print eq_anom

#This creates a dataframe from the anomaly results. I am not to sure why passing eq_anom['anoms'] creates a dataframe
eqZ = eq_anom['anoms']

f, ax1 = plt.subplots(1)
tdfX.plot(ax = ax1) 
tdfY.plot(ax = ax1) 
tdfZ.plot(ax = ax1) 


for index, row in earthquake.iterrows():
	if row['EQ_Magnitude'] > 3:
		ax1.axvline(index, color = 'brown', linewidth = 0.75)
	else:
		pass


ax1.scatter(eqX.index, eqX.anoms, color = 'r')
ax1.scatter(eqY.index, eqY.anoms, color = 'r')
ax1.scatter(eqZ.index, eqZ.anoms, color = 'r')
plt.show()