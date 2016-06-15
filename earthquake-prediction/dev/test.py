# NASA World Wind Earthquake Data Analysis code
import pysal as ps
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

name = 'InteleCell-Kodiak'
# YYYY-MM-DD
begin, end = '2014-10-22', '2014-12-22'

stationcoord = station.get(name)
magnetic = mag.magload(name, begin, end)
earthquake = eaq.eqload(begin, end, stationcoord)

# Plot examples
# pt.graphXYZ(magnetic)
# pt.graphcoord(magnetic, 'Z')

#magnetic = magnetic.reset_index()
magnetic['Date'] = magnetic.index
tdf = pd.DataFrame()
tdf['timestamp'] = magnetic.Date
tdf['magx'] = magnetic.X

eq_anom = pyc.detect_ts(tdf, max_anoms = 0.1, direction = 'both', alpha = 0.05)
#print eq_anom

#This creates a dataframe from the anomaly results. I am not to sure why passing eq_anom['anoms'] creates a dataframe
eqa = eq_anom['anoms']

f, ax1 = plt.subplots(1)
tdf.plot(ax = ax1) 
ax1.scatter(eqa.index, eqa.anoms, color = 'r')
plt.show()