# Loading and processing Magnetic Field data module

import json
import os
import urllib.request
from datetime import datetime
from datetime import timedelta
from time import process_time

import data.stationsdata as st
import numpy as np
import pandas as pd


def load_magnetic(station, min_date, max_date, download = False):
    '''
    Auxiliary function to parse magnetic data request

    - When download = False, it loads data from .csv files. The program doesn't parse it,
     so make sure the file exists in path.

    - InteleCell data is outdated, it has 1 sample per minute
    - InteleCell download data NOT IMPLEMENTED

    :param station: (string) station name
    :param min_date: (string '%YY-%MM-%DD') Limit to events on or after the specified start time
    :param max_date: (string '%YY-%MM-%DD') Limit to events on or before the specified end time
    :param download: (bool) If True, then download from Alaska's InfluxDB. Else, load from csv files

    :return: magnetic: (dataframe; columns = Date, X, Y, Z; index = Date)

            Columns:
            Date: Time of the magnetic field measurement
            [Axis]: Magnetic field in [Axis]

            index:
            Date: Time of the magnetic field measurement
    '''
    start = process_time()
    path = '../data/' + station + '/' + min_date + '-to-' + max_date + '.csv'
    
    if station[:3] == 'ESP': 
        if not download:
            print("Loading magnetic data", end='')
            magnetic = load_magnetic_data_esp(path)

        else:
            print("Getting magnetic data", end='')
            magnetic = get_magnetic_data_esp(station, min_date, max_date)

        print(" --- took", round(process_time() - start, 2), " s")
        return magnetic

    elif station[:10] == "InteleCell":
        if not download:
            print("Loading magnetic data", end='')
            magnetic = load_magnetic_data_intele(path)

        else:
            Exception("Getting InteleCell data from server not implemented")

        print(" --- took", round(process_time() - start, 2), " s")

        return magnetic

    else:
        Exception("ERROR - No station recognized")

def load_magnetic_data_esp(path):
    '''
    Loads ESP magnetic field data from path csv file
    :param path: (string) path to csv file
    :return: magnetic: (dataframe; columns = Date, X, Y, Z; index = Date)

            Columns:
            Date: Time of the magnetic field measurement
            [Axis]: Magnetic field in [Axis]

            index:
            Date: Time of the magnetic field measurement
    '''
    column_names = ['Date', 'X', 'Y', 'Z']
    
    df = pd.read_csv(path, names=column_names)
    df.index = pd.to_datetime(df['Date'], utc=True)
    df.interpolate().dropna(how='any', axis=0)

    return df

def load_magnetic_data_intele(path):
    '''
   Loads InteleCell magnetic field data from path csv file
   :param path: (string) path to csv file
   :return: magnetic: (dataframe; columns = Date, X, Y, Z; index = Date)

           Columns:
           Date: Time of the magnetic field measurement
           [Axis]: Magnetic field in [Axis]

           index:
           Date: Time of the magnetic field measurement
       '''
    column_names = ['Date', 'X', 'Y', 'Z']
    
    df = pd.read_csv(path)
    df.drop('Unnamed: 4', axis=1, inplace=True)
    df.columns = column_names
    df.index = pd.to_datetime(df.Date, utc=True)
    df.dropna(how='any', axis=0)

    return df

def load_from_db(station, min_date, max_date, sample_size=10):
    '''
    This function creates a SQL query and downloads data from
    Alaska's InfluxD, returning it as a dataframe.

    :param station: (string) station name
    :param min_date: (string '%YY-%MM-%DD') Limit to events on or after the specified start time
    :param max_date: (string '%YY-%MM-%DD') Limit to events on or before the specified end time
    :param sample_size: (int) desired number of points from the data

    :return: magnetic: (dataframe; columns = Date, X, Y, Z; index = Date)

            Columns:
            Date: Time of the magnetic field measurement
            [Axis]: Magnetic field in [Axis]

            index:
            Date: Time of the magnetic field measurement
        '''

    print("Loading magnetic data", end='')

    column_names = ['Date', 'X', 'Y', 'Z']
    start = process_time()
    resources_url = "http://143.232.136.208:8086/query"

    # creates url from SQL
    url = resources_url + "?" + "q=select+*+from+"
    url += st.get_esp_name(station)
    url += "+where+time+>+'" + min_date + "'"
    url += "+and+time+<+'" + max_date + "'"
    # url += "+limit+" + str(sample_size)
    url += "&db=test_hmr"

    # gets data from  server
    res = urllib.request.urlopen(url)
    str_data = res.read().decode('ascii')
    dict_data = json.loads(str_data)
    path = dict_data['results'][0]['series'][0]
    # parse data to data frame
    df_data = pd.DataFrame(path['values'], columns=column_names)
    df_data.index = pd.to_datetime(df_data['Date'], utc=True)
    df_data.dropna(how='any', axis=0)

    print(" --- took", round(process_time() - start, 2), " s")
    return df_data

def resample_to_min(magnetic):
    '''
    Resample magnetic field data to minute

    :param magnetic: (dataframe) dataframe of magnetic data (series: X, Y, Z)
    :return: resampled dataframe
    '''

    magnetic = magnetic.resample('1T').mean()
    magnetic = magnetic.interpolate().dropna(how='any', axis=0)
    magnetic['Date'] = magnetic.index

    return magnetic

def resample_to_sec(magnetic):
    '''
        Resample magnetic field data to second

        :param magnetic: (dataframe) dataframe of magnetic data (series: X, Y, Z)
        :return: resampled dataframe
        '''
    magnetic = magnetic.resample('1S').mean()
    magnetic = magnetic.interpolate().dropna(how='any', axis=0)
    magnetic['Date'] = magnetic.index
    # magnetic = magnetic[10000:]

    return magnetic

def jury_rig_dates(magnetic):

    magnetic.index = magnetic.index.astype(np.int64)
    initial_time = magnetic.index[0]
    magnetic.index = ((60) * (magnetic.index - initial_time)) + initial_time
    magnetic.index = pd.to_datetime(magnetic.index)

    # magnetic.X = magnetic.X + 0.011111111
    # magnetic.Y = magnetic.Y + 0.011111111
    # magnetic.Z = magnetic.Z + 0.011111111
    # print(magnetic.head())
    magnetic = magnetic.resample('1T').mean()
    magnetic = magnetic.interpolate().dropna(how='any', axis=0)
    # print(magnetic.head())
    magnetic['Date'] = magnetic.index
    magnetic.index = magnetic['Date']
    # magnetic = magnetic[10000:]

    return magnetic

def get_data(station, min_date, max_date):
    '''
    Loads data from daily files and concatenate them

    :param station: (string) station name
    :param min_date: (string '%YY-%MM-%DD') Limit to events on or after the specified start time
    :param max_date: (string '%YY-%MM-%DD') Limit to events on or before the specified end time
    :return: magnetic: (dataframe; columns = Date, X, Y, Z; index = Date)

            Columns:
            Date: Time of the magnetic field measurement
            [Axis]: Magnetic field in [Axis]

            index:
            Date: Time of the magnetic field measurement
    '''
    def str_time(time):
        # Returns time in datetime date type (YYYY-MM-DD)from string
        return datetime.strptime(time[:10], '%Y-%m-%d')

    start = process_time()

    column_names = ['Date', 'X', 'Y', 'Z']
    
    min_date = str_time(min_date)
    max_date = str_time(max_date)
    
    path_db  = '../data/' + station + '/'

    current_day = str_time(min_date.strftime('%Y-%m-%d'))

    magnetic = pd.DataFrame()
    # get data until the last day
    while current_day <= max_date:
        magnetic_aux = pd.read_csv(path_db + str(current_day.month) + '/' + str(current_day.day) + '.csv', names=column_names)
        magnetic = magnetic.append(magnetic_aux)
        current_day += timedelta(days=1)

    magnetic.index = pd.to_datetime(magnetic['Date'], utc=True)
    magnetic.interpolate().dropna(how='any', axis=0)

    print(" --- took", round(process_time() - start, 2), " s")
    return magnetic

def get_magnetic_data_esp(esp_station, min_date, max_date, intranet = False):
    '''
     Loads ESP magnetic field data from influxDB

    :param station: (string) station name
    :param min_date: (string '%YY-%MM-%DD') Limit to events on or after the specified start time
    :param max_date: (string '%YY-%MM-%DD') Limit to events on or before the specified end time
    :param intranet: (bool) If True, download from  local DB. If False, download from Alaska.

    :return: magnetic: (dataframe; columns = Date, X, Y, Z; index = Date)

               Columns:
               Date: Time of the magnetic field measurement
               [Axis]: Magnetic field in [Axis]

               index:
               Date: Time of the magnetic field measurement
    '''

    station_map = { 'ESP-Kenny-Lake-1' : 10,
                    'ESP-Kodiak-2' : 11,
                    'ESP-Kodiak-3' : 7,
                    'ESP-Kodiak-4' : 8 }

    if intranet:
        resources_url = "http://10.193.20.17/download/"
    else:
        resources_url = "http://24.237.235.227/download/"

    dict_json = {
        "sensor": station_map[esp_station],
        "order": "asc",
        "format": "csv",
        "start_date": min_date,
        "end_date": max_date,
        "submit" : "Download+Data"
    }

    df = pd.read_csv(resources_url + "?" + urllib.parse.urlencode(dict_json), encoding='utf8',header=None)
    df.columns = ['Date', 'X', 'Y', 'Z']
    df.index = pd.to_datetime(df.Date, utc=True)

    return df
