# NASA World Wind Earthquake Data Analysis code
import datetime
from time import process_time
import matplotlib.pyplot as plt
import loadearthquake as eaq
import loadmagnetic as mag
import plot as pt
import pyculiarity.detect_ts as pyc
import stationsdata as station
import pandas as pd
import statsmodels.api as sm
import seaborn as sb

# Date format: YYYY-MM-DD

# name, begin, end = 'InteleCell-Kodiak', '2014-10-22', '2014-12-22'
# name, begin, end = 'ESP-Kodiak-3', '2016-04-10', '2016-04-13'
name, begin, end = 'ESP-Kodiak-3', '2016-04-10', '2016-05-10'
# name, begin, end = 'ESP-Kodiak-3', '2016-04-07', '2016-05-31'

stationcoord = station.get(name)
magnetic = mag.load_magnetic_data(name, begin, end, filter_data=True).reset_index()
earthquake = eaq.load_earthquake_data(begin, end, stationcoord, min_magnitude=2)

# upsampling to one minute
magnetic.index = magnetic.Date
magnetic = magnetic.resample('1T').mean()
magnetic = magnetic.interpolate().dropna(how='any', axis=0)
magnetic['Date'] = magnetic.index


def get_data_frame(column):
    print("Detecting anomalies for", column, "axis", end='')
    start = process_time()

    df = magnetic[['Date', column]]
    df.columns = ["timestamp", "value"]

    df = df[df.value < 100]

    # TODO: mess around with maximum_anomalies and alpha to improve resulting plots
    eq_anom = pyc.detect_ts(df, maximum_anomalies=0.025, direction='both', alpha=0.15)

    print(" --- took", round(process_time() - start, 2), " s")
    return eq_anom['anoms'], df

fX, fY, fZ = get_data_frame('X'), get_data_frame('Y'), get_data_frame('Z')

x_anom, _ = fX
y_anom, _ = fY
z_anom, _ = fZ

major_eq = earthquake.ix[earthquake.EQ_Magnitude > 2.5]

X_anoms = []
Y_anoms = []
Z_anoms = []
for index, row in major_eq.iterrows():
    end_date = index
    start_date = end_date - datetime.timedelta(hours=24)
    tempX = x_anom[start_date:end_date]
    tempY = y_anom[start_date:end_date]
    tempZ = z_anom[start_date:end_date]
    X_anoms.append(len(tempX.index))
    Y_anoms.append(len(tempY.index))
    Z_anoms.append(len(tempZ.index))
    # print(len(temp.index))
x_anomalies = pd.Series(X_anoms)
y_anomalies = pd.Series(Y_anoms)
z_anomalies = pd.Series(Z_anoms)
major_eq['X_anomalies'] = x_anomalies.values
major_eq['Y_anomalies'] = y_anomalies.values
major_eq['Z_anomalies'] = z_anomalies.values

# Anomaly Distribution Plot
total_anoms = []
for index, row in major_eq.iterrows():
    total_anoms.append(row.X_anomalies + row.Y_anomalies + row.Z_anomalies)
t_anoms = pd.Series(total_anoms)
major_eq['total'] = t_anoms.values

print(major_eq.ix[:, 'total':])

d = []
f = plt.figure()
for data in major_eq['total']:
    if data > 0:
        d.append(data)
anom_dat = pd.Series(d)
sb.distplot(anom_dat)
plt.show()

# eq_mag_model = sm.OLS.from_formula('EQ_Magnitude ~ X_anomalies + Y_anomalies +\
#                                       Z_anomalies', data = major_eq)
# eq_mag_model_fitted = eq_mag_model.fit()
# print(eq_mag_model_fitted.summary())

# sb.regplot('EQ_Magnitude', 'X_anomalies', data= major_eq)
# plt.show()

# mod_diagnostics(eq_mag_model, merge_df)


pt.plot_earthquake_anomalies_magnetic((fX, fY, fZ), earthquake)
plt.show()
