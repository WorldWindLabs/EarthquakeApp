# NASA World Wind Earthquake load data code

from datetime import timedelta
from time import process_time
import pandas as pd
import bandfilter as bf
import urllib

def load_magnetic_data(station, min_date, max_date, filter_data = False, download = False):
    start = process_time()
    path = '../data/' + station + '/' + min_date + '-to-' + max_date + '.csv'
    
    if station[:3] == 'ESP': 
        if not download:
            print("Loading magnetic data", end='')
            df = load_magnetic_data_esp(path)

        else:
            print("Getting magnetic data", end='')
            df = get_magnetic_data_esp(station, min_date, max_date)

        if filter_data:
            df = bf.filter(df)

        else:     
            df = df.resample('1T').mean() 
            df = df.interpolate().dropna(how='any', axis=0)

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
    df.interpolate().dropna(how='any', axis=0)

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