from struct import *
import pandas as pd
import numpy as np

with open('../data/123 Hz/wb_esp_alaska_1_hires20160620.bin') as f:
    data_lines = f.readlines()

n_lines = len(data_lines)
sampling_frequency = 123
time_period = 1.0 / sampling_frequency

timestamp = [None] * n_lines * sampling_frequency
x_axis, y_axis, z_axis = np.empty((n_lines * sampling_frequency, 1)),\
                         np.empty((n_lines * sampling_frequency, 1)),\
                         np.empty((n_lines * sampling_frequency, 1))

nT = 100000

counter = 0
for test_line in data_lines:
    fields = test_line.split(",")

    sub_counter = 0
    for i in range(0, len(fields[3]), 12):
        value = fields[3][i:i + 12]

        try:
            value = bytearray.fromhex(value)
        except ValueError:
            continue

        (x, y, z) = unpack('>hhh', value)

        timestamp[counter] = fields[0][:-1] + '.' + str(int(1e6 * sampling_frequency * sub_counter)).zfill(6) + 'Z'
        x_axis[counter], y_axis[counter], z_axis[counter] = x, y, z

        counter += 1
        sub_counter += 1

data_frame = pd.DataFrame()
data_frame['timestamp'] = pd.to_datetime(timestamp,infer_datetime_format=True,utc=True)
data_frame['x_axis'] = ((x_axis / 15000) * nT).astype(np.float32)
data_frame['y_axis'] = ((y_axis / 15000) * nT).astype(np.float32)
data_frame['z_axis'] = ((z_axis / 15000) * nT).astype(np.float32)
data_frame.set_index('timestamp', inplace=True)

data_frame = data_frame.interpolate().dropna(how='any', axis=0)
data_frame = data_frame.resample(str(int(time_period*1e6))+'U').mean().interpolate()

print(data_frame)
