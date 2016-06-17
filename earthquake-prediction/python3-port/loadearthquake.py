# NASA World Wind Earthquake load data code

import io
import sys
from urllib.parse import urlencode
import pandas as pd
import requests


def load_earthquake_data(min_date, max_date, origin, min_magnitude="4", max_distance="300"):
    print("Loading earthquake data")

    resourcesUrl = "http://earthquake.usgs.gov/fdsnws/event/1/query"

    dict_json = {
        "format": "csv",
        "starttime": min_date,
        "endtime": max_date,
        "minmagnitude": min_magnitude,
        "latitude": origin['lati'],
        "longitude": origin['long'],
        "maxradiuskm": max_distance
    }

    resp = requests.get(resourcesUrl+"?"+urlencode(dict_json))
    if resp.status_code != 200:
        print("Error", resp.status_code, resp.content)
        sys.exit()

    data_frame = pd.read_csv(io.BytesIO(resp.content), encoding='utf8')[['time','latitude','longitude','mag']]
    data_frame.columns = ['DateTime', 'Latitude', 'Longitude', 'EQ_Magnitude']
    data_frame['DateTime'] = pd.to_datetime(data_frame['DateTime'], utc=True)
    data_frame.set_index('DateTime', inplace=True)

    return data_frame
