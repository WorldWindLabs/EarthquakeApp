# Data analysis code helper module, breaking up big files into smaller ones

import datetime
from time import process_time
import loadmagnetic as mag
import pandas as pd

name, begin, end = 'ESP-Kodiak-3', '2016-04-10', '2016-05-10'
# name, begin, end = 'ESP-Kodiak-3', '2016-03-31', '2016-06-21'


# name, begin, end = 'ESP-Kenny-Lake-1', '2016-04-01', '2016-06-21'
# name, begin, end = 'ESP-Kenny-Lake-1', '2016-04-01', '2016-04-02'


def divide_into_chuncks(name, begin, end, num_parts=8):
    '''
    Function to slice station data in to num_parts pieces.

    :param name: (string) station name
    :param min_date: (string '%YY-%MM-%DD') Limit to events on or after the specified start time
    :param max_date: (string '%YY-%MM-%DD') Limit to events on or before the specified end time
    :param num_parts: (int) number of pieces to divide the original file
    '''
    for i in range(2, num_parts):
        n = 80000000
        magnetic = mag.load_magnetic_data(name, begin, end, skiprows=3301000 + i * n, nrows=n)

        column_names = ['X', 'Y', 'Z']
        new_begin = magnetic.index[0].strftime("%Y-%m-%d")
        new_end = magnetic.index[-1].strftime("%Y-%m-%d")

        magnetic = magnetic[column_names]
        path = '../data/test2/' + name + '/' + new_begin + '-to-' + new_end
        magnetic.to_csv(path + '.csv', colums=column_names, header=False)
        print("done writing")

        (mag.upsample_to_sec(magnetic)).to_csv(path + 'sec.csv', colums=column_names, header=False)
        print("done writing sec sample")


def slice_data(station):
    '''
    Function that slices a huge csv into daily csv files

    :param station: (string) station name

    '''

    def str_time(time):
        # Returns time in datetime date type (YYYY-MM-DD)from string
        return datetime.strptime(time[:10], '%Y-%m-%d')

    def str_time_s(time):
        # Returns time in datetime date type (ISO8601) from string
        return datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')

    def get_time(n):
        # Returns n-th time in csv file as datetime date type
        return str_time_s(pd.read_csv(path_csv, names=column_names, nrows=1, skiprows=n - 1).Date[0])

    def row_counter():
        # Returns the number of lines in csv file on path_csv
        # PS: It does not work if the file is >30GB
        file = open(path_csv)
        return len(file.readlines())

    def binarySearch(item):
        # Looks for the line with item as index
        first = skip + 1
        last = row_count
        found = False

        if item > get_time(first) and item < get_time(first + 1):
            return first

        while first <= last and not found:
            midpoint = (first + last) // 2
            if get_time(midpoint) == item:
                found = True
            else:
                if item < get_time(midpoint):
                    last = midpoint - 1
                else:
                    first = midpoint + 1

        return midpoint

    def cut_data(begin, end):
        # Returns the number of rows to skip and to load
        index_begin = binarySearch(begin)
        index_end = binarySearch(end)
        return index_end - index_begin - 1, index_begin

    start = process_time()

    column_names = ['Date', 'X', 'Y', 'Z']

    path_csv = '../data/' + station + '/' + station + '.csv'
    path_db = '../data/' + station + '/'
    # create folder for each month
    for month in range(1, 13):
        if not os.path.exists(path_db + str(month)):
            os.makedirs(path_db + str(month))

    row_count = row_counter()
    last_time = get_time(row_count)
    initial_time = get_time(1)

    current_day = str_time(initial_time.strftime('%Y-%m-%d'))
    skip = 0
    # get data from csv until the last day
    while last_time > current_day:
        print(current_day)
        nxt_day = current_day + timedelta(days=1)

        nrow, skip = cut_data(current_day, nxt_day)
        # loads from big csv
        day = pd.read_csv(path_csv, names=column_names, nrows=nrow, skiprows=skip)
        # writes to day file
        day.to_csv(path_db + str(current_day.month) + '/' + str(current_day.day) + '.csv', colums=column_names,
                   header=False)

        skip += nrow
        current_day = nxt_day

    print(" --- took", round(process_time() - start, 2), " s")
