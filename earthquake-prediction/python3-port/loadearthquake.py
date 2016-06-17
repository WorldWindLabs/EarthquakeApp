# NASA World Wind Earthquake load data code

from time import process_time
from urllib.parse import urlencode
import pandas as pd


def load_earthquake_data(min_date, max_date, origin, min_magnitude="4", max_distance="300"):
    print("Loading earthquake data",end='')
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

    data_frame = pd.read_csv(resources_url + "?" + urlencode(dict_json), encoding='utf8')
    data_frame = data_frame[['time', 'latitude', 'longitude', 'mag']]
    data_frame.columns = ['DateTime', 'Latitude', 'Longitude', 'EQ_Magnitude']
    data_frame['DateTime'] = pd.to_datetime(data_frame['DateTime'], utc=True)
    data_frame.set_index('DateTime', inplace=True)

    print(" --- took",round(process_time()-start,2)," s")

    return data_frame
