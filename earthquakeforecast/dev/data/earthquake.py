# Loading and processing Earthquake data module

import data.stationsdata as station
import datetime as dt
import pandas as pd
import numpy as np
from math import radians, cos, sin, asin, sqrt
from datetime import datetime
from time import process_time
from urllib.parse import urlencode

def load_earthquakes(min_date, max_date, origin, min_magnitude=4, max_distance="300"):
    '''
    Loads earthquake data from USGS api and returns a data frame with the data

    :param min_date: (string '%YY-%MM-%DD') Limit to events on or after the specified start time
    :param max_date: (string '%YY-%MM-%DD') Limit to events on or before the specified end time
    :param origin: ({'lati': latitude, 'long': longitude}) Coordinates from to point
                    which the earthquake's epicenter has to be within 'max_distance' from
    :param min_magnitude: (Int) Limit to events with a magnitude larger than the specified minimum.
    :param max_distance: Limit to events within the specified maximum number of kilometers from
                        the origin
    :return: earthquakes: (dataframe; columns = DateTime, Latitude, Longitude, EQ_Magnitude, distance, eq_influence;
            index = Date)

            Columns:
            Date: Time of the earthquake
            Latitude: Latitude of the epicenter
            Longitude: Longitude of the epicenter
            Magnitude: Earthquake magnitude
            Distance: Distance from the origin
            Influence: magnitude/ log(distance)

            index:
            Date: Dates from earthquakes
    '''
    print("Loading earthquake data", end='')

    start = process_time()
    resources_url = "http://earthquake.usgs.gov/fdsnws/event/1/query"
    # json for the query
    dict_json = {
        "format": "csv",
        "starttime": min_date,
        "endtime": max_date,
        "minmagnitude": str(min_magnitude),
        "latitude": origin['lati'],
        "longitude": origin['long'],
        "maxradiuskm": max_distance
    }

    def haversine(lon1, lat1, lon2, lat2):
        '''
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees)

        :param lon1: Longitude of point 1
        :param lat1: Latitude of point 1
        :param lon2: Longitude of point 2
        :param lat2: Latitude of point 2

        :return: Distance between the two points
        '''

        # convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        km = 6367 * c
        return km

    # Creates data frame from USGS data
    earthquakes = pd.read_csv(resources_url + "?" + urlencode(dict_json), encoding='utf8')
    earthquakes = earthquakes[['time', 'latitude', 'longitude', 'mag']]
    earthquakes.columns = ['Date', 'Latitude', 'Longitude', 'Magnitude']
    earthquakes['Date'] = pd.to_datetime(earthquakes['Date'], utc=True)
    earthquakes.set_index('Date', inplace=True)

    # Creates dist column with distances from the epicenters to the origin
    dist = []
    for index, row in earthquakes.iterrows():
        dist.append(haversine(float(row['Longitude']), float(row['Latitude']), \
                              float(origin['long']), float(origin['lati'])))
    earthquakes['Distance'] = dist

    # Created this metric based on magnitude and distance, is in shaking amplitude, not energy released, log transformed
    earthquakes['Influence'] = np.log((10 ** earthquakes['Magnitude']) / earthquakes['Distance'])

    print(" --- took", round(process_time() - start, 2), " s")

    return earthquakes

def get_relevant_earthquake(name, min_date, max_date):
    '''
    Function to get relevant earthquakes (higher 'influence' parameters) for a certain
      period of time for a specific station

    :param name: (string) Station name
    :param min_date: (string '%YY-%MM-%DD') Limit to events on or after the specified start time
    :param max_date: (string '%YY-%MM-%DD') Limit to events on or before the specified end time

    :return: data frame with top five relevant earthquakes
            (dataframe; columns = DateTime, Latitude, Longitude, EQ_Magnitude, distance, eq_influence;
            index = Date)

            Columns:
            Date: Time of the earthquake
            Latitude: Latitude of the epicenter
            Longitude: Longitude of the epicenter
            Magnitude: Earthquake magnitude
            Distance: Distance from the origin
            Influence: magnitude/ log(distance)

            index:
            Date: Dates from earthquakes
    '''
    stationcoord = station.get(name)

    earthquake = eaq.load_earthquake_data(min_date, max_date, stationcoord, min_magnitude=2.5)
    return earthquake.sort_values(by = 'Influence', ascending = False).head()

def add_anomalies(eq, anom):
    '''
    Incorporate anomalies for earthquake into earthquake data frame

    :param eq: (dataframe) dataframe of earthquake data
    :param anom: (dataframe) output from detectanomalies/compute_anomalies_for_earthquake()
    :return: new dataframe of earthquake with anomaly data
            earthquakes: (dataframe; columns = eq.columns, X_anoms, Y_anoms, Z_anoms, total_anoms;
            index = Date)

            Columns:
            '[Axis]_anoms': list of number of anomalies, in order for each event in your earthquake DF.
            'total_anoms': list of total number of anomalies in all axes within a period of time before the earthquake

            index:
            Date: Dates from earthquakes

    '''
    earthquake = pd.concat([eq, anom], axis=1, join_axes=[eq.index])
    earthquake['total_anoms'] = earthquake.X_anoms + earthquake.Y_anoms + earthquake.Z_anoms
    return earthquake

def look_relevant_earthquake(name, times, distance = 400, h = 10, min_mag = 2.5):
    '''
    Search for earthquakes within a time interval with a few restrictions for the station

    :param name: (string) station name
    :param times: list of datetime intervals, formatted as tuples (initial_time, end_time)
    :param distance: (int) distance from the station
    :param h: (int) number of hours after the end of the interval to look for earthquake
    :param min_mag: (int) minimum magnitude to look for earthquake

    :return: (bool list) for each interval, answer if there's at least one relevant earthquake
            satisfying the restrictions
    '''
    ans = []
    stationcoord = station.get(name)

    for begin, end in times:
        earthquake = load_earthquakes(datetime.isoformat(begin),
             datetime.isoformat(end+dt.timedelta(hours=h)), 
             stationcoord, 
             max_distance = distance,
             min_magnitude = min_mag)

        if len(earthquake.index) >= 1:
            ans.append(True)
        else:
            ans.append(False)

    return ans

