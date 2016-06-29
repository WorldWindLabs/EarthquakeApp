# NASA World Wind Earthquake Data Analysis code
import datetime as dt
from datetime import datetime
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
import seaborn as sb
import numpy as np
import clusters


def preprocess(name, magnetic, anomalies):
    y = []
    for i in range(3):
        anom_rate = anom.anomaly_rate(magnetic, anomalies[i])
        cluster_list = clusters.get(anom_rate, anomalies[i])
        features, interval = clusters.comp_features(cluster_list)

        y.append(eaq.look_relevant_earthquake(name, interval))

    return features, y
