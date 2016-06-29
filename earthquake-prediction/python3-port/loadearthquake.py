# NASA World Wind Earthquake load data code
from time import process_time
from urllib.parse import urlencode
import pandas as pd
from math import radians, cos, sin, asin, sqrt
import numpy as np
import stationsdata as station
import plot as pt
import loadearthquake as eaq



def load_earthquake_data(min_date, max_date, origin, min_magnitude="4", max_distance="300"):
    print("Loading earthquake data", end='')

    start = process_time()
    resources_url = "http://earthquake.usgs.gov/fdsnws/event/1/query"

    dict_json = {
        "format": "csv",
        "starttime": min_date,
        "endtime": max_date,
        "minmagnitude": min_magnitude,
        "latitude": origin['lati'],
        "longitude": origin['long'],
        "maxradiuskm": max_distance
    }

    def haversine(lon1, lat1, lon2, lat2):
        """
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        km = 6367 * c
        return km

    data_frame = pd.read_csv(resources_url + "?" + urlencode(dict_json), encoding='utf8')
    data_frame = data_frame[['time', 'latitude', 'longitude', 'mag']]
    data_frame.columns = ['DateTime', 'Latitude', 'Longitude', 'EQ_Magnitude']
    data_frame['DateTime'] = pd.to_datetime(data_frame['DateTime'], utc=True)
    data_frame.set_index('DateTime', inplace=True)
    dist = []
    for index, row in data_frame.iterrows():
        dist.append(haversine(float(row['Longitude']), float(row['Latitude']), \
                              float(origin['long']), float(origin['lati'])))
    data_frame['distance'] = dist

    # created this metric based on magnitude and distance, is in shaking amplitude, not energy released, log transformed
    data_frame['eq_influence'] = np.log((10 ** data_frame['EQ_Magnitude']) / data_frame['distance'])

    print(" --- took", round(process_time() - start, 2), " s")

    # pt.plot_AxB(data_frame['EQ_Magnitude'], data_frame['distance'])

    return data_frame


def get_relevant_earthquake():
    name = 'ESP-Kodiak-3'
    stationcoord = station.get(name)

    earthquake = eaq.load_earthquake_data('2016-04-19', '2016-06-22', stationcoord, min_magnitude=2.5)
    return earthquake.sort_values(by = 'eq_influence', ascending = False).head()


def add_anomalies(eq, anom):
    earthquake = pd.concat([eq, anom], axis=1, join_axes=[eq.index])
    earthquake['total_anoms'] = earthquake.X_anoms + earthquake.Y_anoms + earthquake.Z_anoms
    return earthquake