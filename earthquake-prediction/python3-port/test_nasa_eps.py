# NASA World Wind Earthquake Data Analysis code

from time import process_time
import matplotlib.pyplot as plt
import loadearthquake as eaq
import loadmagnetic as mag
import plot as pt
import pyculiarity.detect_ts as pyc
import stationsdata as station

# Date format: YYYY-MM-DD

# name, begin, end = 'InteleCell-Kodiak', '2014-10-22', '2014-12-22'
# name, begin, end = 'ESP-Kodiak-3', '2016-04-10', '2016-04-13'
name, begin, end = 'ESP-Kodiak-3', '2016-04-10', '2016-05-10'
# name, begin, end = 'ESP-Kodiak-3', '2016-04-07', '2016-05-31'

stationcoord = station.get(name)
magnetic = mag.load_magnetic_data(name, begin, end).reset_index()
earthquake = eaq.load_earthquake_data(begin, end, stationcoord, min_magnitude=1)


def get_data_frame(column):
    print("Detecting anomalies for", column, "axis", end='')
    start = process_time()

    df = magnetic[['Date', column]]
    df.columns = ["timestamp", "value"]

    # TODO: mess around with maximum_anomalies and alpha to improve resulting plots
    eq_anom = pyc.detect_ts(df, maximum_anomalies=0.025, direction='both', alpha=0.15)

    print(" --- took", round(process_time() - start, 2), " s")
    return eq_anom['anoms'], df


fX, fY, fZ = get_data_frame('X'),get_data_frame('Y'),get_data_frame('Z')
pt.plot_earthquake_anomalies_magnetic((fX, fY, fZ), earthquake)
plt.show()
