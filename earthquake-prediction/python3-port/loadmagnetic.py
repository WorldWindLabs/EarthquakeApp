# NASA World Wind Earthquake load data code

from datetime import timedelta
from time import process_time
from datetime import datetime
import pandas as pd
import bandfilter as bf
from urllib.parse import urlencode
import json 
import urllib.request
import stationsdata as st
from pandas.io.json import json_normalize
import numpy as np
import os
from os import listdir
from os.path import isfile, join
import csv 

def load_magnetic_data(station, min_date, max_date, download = False):
    start = process_time()
    path = '../data/' + station + '/' + min_date + '-to-' + max_date + '.csv'
    
    if station[:3] == 'ESP': 
        if not download:
            print("Loading magnetic data", end='')
            df = load_magnetic_data_esp(path)

        else:
            print("Getting magnetic data", end='')
            df = get_magnetic_data_esp(station, min_date, max_date)

        # if filter_data:
        #     df = bf.filter(df)

        # else:     
        #     df = df.resample('1T').mean() 
        #     df = df.interpolate().dropna(how='any', axis=0)

        print(" --- took", round(process_time() - start, 2), " s")
        return df

    elif station[:10] == "InteleCell":
        if not download:
            print("Loading magnetic data", end='')
            df = load_magnetic_data_intele(path)

        else:
            Exception("Get InteleCell data not implemented")

        print(" --- took", round(process_time() - start, 2), " s")

        return df

    else:
        Exception("ERROR - No station recognized")

def load_magnetic_data_esp(path):
    column_names = ['Date', 'X', 'Y', 'Z']
    
    df = pd.read_csv(path, names=column_names)
    df.index = pd.to_datetime(df['Date'], utc=True)
    df.interpolate().dropna(how='any', axis=0)

    return df

def load_magnetic_data_intele(path):
    column_names = ['Date', 'X', 'Y', 'Z']
    
    df = pd.read_csv(path)
    df.drop('Unnamed: 4', axis=1, inplace=True)
    df.columns = column_names
    df.index = pd.to_datetime(df.Date, utc=True)
    df.dropna(how='any', axis=0)

    return df

def get_magnetic_data_esp(esp_station, min_date, max_date, intranet = False):

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

def upsample_to_min(magnetic):
    magnetic = magnetic.resample('1T').mean()
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

def load_db(station, min_date, max_date, sample_size = 10):
    print("Loading magnetic data", end='')

    column_names = ['Date', 'X', 'Y', 'Z']
    start = process_time()
    resources_url = "http://143.232.136.208:8086/query"

    url = resources_url + "?" + "q=select+*+from+"
    url += st.get_esp_name(station)
    url += "+where+time+>+'" + min_date + "'"
    url += "+and+time+<+'" + max_date + "'"
    # url += "+limit+" + str(sample_size) 
    url += "&db=test_hmr"

    res = urllib.request.urlopen(url)
    str_data = res.read().decode('ascii')
    dict_data = json.loads(str_data)
    path = dict_data['results'][0]['series'][0]
    df_data = pd.DataFrame(path['values'], columns = column_names)
    df_data.index = pd.to_datetime(df_data['Date'], utc=True)
    df_data.dropna(how='any', axis=0)
       
    print(" --- took", round(process_time() - start, 2), " s")
    # print(df_data)
    return df_data

def slice_data(station):
    
    def str_time(time):
        return datetime.strptime(time[:10], '%Y-%m-%d')
    
    def str_time_s(time):
        return datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')

    def get_time(n):
        return str_time_s(pd.read_csv(path_csv, names=column_names, nrows = 1, skiprows = n-1).Date[0])

    def row_counter():
        file = open(path_csv)
        return len(file.readlines())

    def estimate_time(min_date, initial_time):
        return int(max((min_date - initial_time).total_seconds(), 0))

    def binarySearch(item):
        first = skip+1
        last = row_count
        found = False

        if item > get_time(first) and item < get_time(first+1):
            return first

        while first<=last and not found:
            midpoint = (first + last)//2
            if get_time(midpoint) == item:
                found = True
            else:
                if item < get_time(midpoint):
                    last = midpoint-1
                else:
                    first = midpoint+1
  
        return midpoint

    def cut_data(begin, end):
        index_begin = binarySearch(begin)
        index_end = binarySearch(end)
        return index_end - index_begin - 1, index_begin

    start = process_time()

    column_names = ['Date', 'X', 'Y', 'Z']
    
    path_csv = '../data/' + station + '/' + station + '.csv'
    path_db  = '../data/' + station + '/'

    for month in range(1, 13):
        if not os.path.exists(path_db + str(month)):
            os.makedirs(path_db + str(month))
    
    row_count = row_counter()        
    last_time = get_time(row_count)
    initial_time = get_time(1)

    current_day = str_time(initial_time.strftime('%Y-%m-%d'))
    skip = 0

    while last_time > current_day:
        print(current_day)
        nxt_day = current_day+timedelta(days=1)

        nrow, skip = cut_data(current_day, nxt_day)
        day = pd.read_csv(path_csv, names=column_names, nrows = nrow, skiprows = skip)        
        day.to_csv(path_db + str(current_day.month) + '/' + str(current_day.day) + '.csv', colums = column_names, header = False)
    
        skip += nrow 
        current_day = nxt_day

    print(" --- took", round(process_time() - start, 2), " s")

def get_data(station, min_date, max_date):
    
    def str_time(time):
        return datetime.strptime(time[:10], '%Y-%m-%d')

    start = process_time()

    column_names = ['Date', 'X', 'Y', 'Z']
    
    min_date = str_time(min_date)
    max_date = str_time(max_date)
    
    path_db  = '../data/' + station + '/'

    current_day = str_time(min_date.strftime('%Y-%m-%d'))

    df = pd.DataFrame()

    while current_day <= max_date:
        df_aux = pd.read_csv(path_db + str(current_day.month) + '/' + str(current_day.day) + '.csv', names=column_names)
        df = df.append(df_aux)
        current_day += timedelta(days=1)

    df.index = pd.to_datetime(df['Date'], utc=True)
    df.interpolate().dropna(how='any', axis=0)

    print(" --- took", round(process_time() - start, 2), " s")
    return df

name, begin, end = 'ESP-Kodiak-4', '2016-06-04', '2016-06-17'

# get_data(name, begin, end)

# slice_data('ESP-Kodiak-1')
# slice_data('ESP-Kodiak-2')
# slice_data('ESP-Kodiak-3')
# slice_data('ESP-Kodiak-4')