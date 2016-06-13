# NASA World Wind Earthquake Data Analysis code

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

#plot_interval('10-04-16', '17-04-16', kodiak3)

####################################################################################
#Test code for analysis kodiacIC_Anomaly.csv is Kodiak intelecel data for the dates 27-05-2015 - 30-05-2015

name = 'InteleCell-Kodiak'
# YYYY-MM-DD
begin, end = '2014-10-22', '2014-12-22'

stationcoord = station.get(name)
magnetic = mag.load(name, begin, end)
earthquake = eaq.load(begin, end, stationcoord)

# Plot examples
# pt.graphXYZ(magnetic)
# pt.graphcoord(magnetic, 'Z')
