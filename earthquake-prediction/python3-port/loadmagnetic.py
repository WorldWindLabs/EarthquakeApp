# NASA World Wind Earthquake load data code

from datetime import timedelta
from time import process_time
import pandas as pd


def load_magnetic_data(station, begin, end):
    print("Loading magnetic data", end='')

    start = process_time()
    path = '../data/' + station + '/' + begin + '-to-' + end + '.csv'

    if station[:10] == "InteleCell":
        column_names = ['Date', 'X', 'Y', 'Z']
        df = pd.read_csv(path)
        df.drop('Unnamed: 4', axis=1, inplace=True)
        df.columns = column_names

        # assuming that the Alaska TZ is UTC - 9 hours
        df.index = pd.to_datetime(df.Date, utc=True) + timedelta(hours=9)

        df.interpolate().dropna(how='any', axis=0)

        print(" --- took", round(process_time() - start, 2), " s")

        return df

    elif station[:3] == 'ESP':
        column_names = ['Date', 'X', 'Y', 'Z']
        df = pd.read_csv(path, names=column_names)

        # assuming that the Alaska TZ is UTC - 9 hours
        df.index = pd.to_datetime(df['Date'], utc=True) + timedelta(hours=9)

        df = df.resample('1T').mean()
        df = df.interpolate().dropna(how='any', axis=0)

        print(" --- took", round(process_time() - start, 2), " s")

        return df

    else:
        print("ERROR - No station recognized")
