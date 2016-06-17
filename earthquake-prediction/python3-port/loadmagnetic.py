# NASA World Wind Earthquake load data code

import pandas as pd


def load_magnetic_data(station, begin, end):
    print("Loading magnetic data")
    path = '../data/' + station + '/' + begin + '-to-' + end + '.csv'

    if station[:10] == "InteleCell":
        column_names = ['Date', 'X', 'Y', 'Z']
        df = pd.read_csv(path)
        del df['Unnamed: 4']
        df.columns = column_names
        df.interpolate()
        dft = pd.to_datetime(df.Date, utc=True)
        df.index = dft

        return df

    elif station[:3] == 'ESP':
        column_names = ['Date', 'X', 'Y', 'Z']
        df = pd.read_csv(path, names=column_names)
        dft = pd.to_datetime(df.Date, utc=True)
        df.Date = df.Date.astype('object')
        df.index = dft
        df = df.resample('1T').mean()
        df['Date'] = df.index
        df = df.interpolate()
        return df

    else:
        print("ERROR - No station recognized")

