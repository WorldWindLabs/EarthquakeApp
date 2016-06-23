import datetime
import pandas as pd
import pyculiarity.detect_ts as pyc
from time import process_time

def compute_anomalies(mag):
	return get_anom(mag, 'X'), get_anom(mag, 'Y'), get_anom(mag, 'Z')


def get_anom(magnetic, column):
    print("Detecting anomalies for", column, "axis", end='')
    start = process_time()

    df = magnetic[['Date', column]]
    df.columns = ["timestamp", "value"]

    # df = df[df.value < 100]

    # TODO: mess around with maximum_anomalies and alpha to improve resulting plots
    eq_anom = pyc.detect_ts(df, maximum_anomalies=0.025, direction='pos', alpha=0.15)

    print(" --- took", round(process_time() - start, 2), " s")
    return eq_anom['anoms']

def compute_anomalies_for_earthquake(eq, anomalies, time = 24):
	x, y, z = anomalies
	anoms = comp_anom_for_eq(eq, x, time), comp_anom_for_eq(eq, y, time), comp_anom_for_eq(eq, z, time)
	return pd.DataFrame({'X_anoms': anoms[0],
						 'Y_anoms': anoms[1],
						 'Z_anoms': anoms[2]},
						 index = eq.index)

def comp_anom_for_eq(earthquake, anomaly, interval):
    X_anoms = []
    
    for index, row in earthquake.iterrows():
        end = index
        start = end - datetime.timedelta(hours= interval)
        tempX = anomaly[start:end]

        X_anoms.append(len(tempX.index))

    return X_anoms
