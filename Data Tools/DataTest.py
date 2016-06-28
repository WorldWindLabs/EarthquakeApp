import pandas as pd
import matplotlib.pyplot as plt

path = '/Users/GEFS/Desktop/data.csv'

columns = ['Date','x','y','z']
df = pd.read_csv(path,header=None,names=columns)
df.index = pd.to_datetime(df['Date'], utc=True)
df.drop('Date', inplace=True, axis=1)


df = df.resample('60S').mean()  # re-sample at 1 Second intervals
df = df.interpolate().dropna(how='any', axis=0)  # interpolate any missing data and delete bad rows

df.plot()

plt.show()



#print(df.head())