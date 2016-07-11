from math import sqrt

import numpy as np
import pandas as ps
from scipy.stats import t as student_t
from statsmodels.robust.scale import mad

from pyculiarity.r_stl import stl


def detect_anoms(data, k=0.49, alpha=0.05, num_obs_per_period=None,
                 use_decomp=True, one_tail=True,
                 upper_tail=True, verbose=False):
    """
    # Detects anomalies in a time series using S-H-ESD.
    #
    # Args:
    #	 data: Time series to perform anomaly detection on.
    #	 k: Maximum number of anomalies that S-H-ESD will detect as a percentage of the data.
    #	 alpha: The level of statistical significance with which to accept or reject anomalies.
    #	 num_obs_per_period: Defines the number of observations in a single period, and used during seasonal decomposition.
    #	 use_decomp: Use seasonal decomposition during anomaly detection.
    #	 one_tail: If TRUE only positive or negative going anomalies are detected depending on if upper_tail is TRUE or FALSE.
    #	 upper_tail: If TRUE and one_tail is also TRUE, detect only positive going (right-tailed) anomalies. If FALSE and one_tail is TRUE, only detect negative (left-tailed) anomalies.
    #	 verbose: Additionally printing for debugging.
    # Returns:
    #   A dictionary containing the anomalies (anoms) and decomposition components (stl).
    """

    if num_obs_per_period is None:
        raise ValueError("must supply period length for time series decomposition")

    if len(data.columns) != 2:
        raise ValueError("number of columns isn't equal to two")

    if list(data.columns) != ["timestamp", "value"]:
        data.columns = ["timestamp", "value"]

    num_obs = len(data)

    # Check to make sure we have at least two periods worth of data for anomaly context
    if num_obs < num_obs_per_period * 2:
        raise ValueError("Anom detection needs at least 2 periods worth of data")

    # run length encode result of isnull, check for internal nulls
    if data.isnull().values.any():
        raise ValueError("detected internal nulls in the data, interpolate before using")

    # -- Step 1: Decompose data. This returns a univarite remainder which will be used
    # for anomaly detection. Optionally, we might NOT decompose.

    data = data.set_index('timestamp')

    if not isinstance(data.index, ps.Int64Index):
        resample_period = {1440: 'T', 24: 'H', 7: 'D'}
        resample_period = resample_period.get(num_obs_per_period)
        if not resample_period:
            raise ValueError('Unsupported resample period: %d' % resample_period)
        data = data.resample(resample_period)

    decomposed = stl(data.value, "periodic", np=num_obs_per_period)

    # Remove the seasonal component, and the median of the data to create the univariate remainder
    d = {'timestamp': data.index, 'value': data.value - decomposed['seasonal'] - data.value.median()}
    data = ps.DataFrame(d)

    p = {
        'timestamp': decomposed.index,
        'value': ps.to_numeric((decomposed['trend'] + decomposed['seasonal']).truncate())
    }

    data_decomposed = ps.DataFrame(p)

    # Maximum number of outliers that S-H-ESD can detect (e.g. 49% of data)
    max_outliers = int(num_obs * k)

    if max_outliers == 0:
        raise ValueError("With longterm=TRUE, AnomalyDetection splits the data into 2 week periods by default. " +
                         "You have {} observations in a period, which is too few. ".format(num_obs) +
                         "Set a higher piecewise_median_period_weeks.")

    # Define values and vectors.
    n = len(data.timestamp)
    r_idx = list(range(max_outliers))

    number_of_anomalies = 0

    # Compute test statistic until r=max_outliers values have been
    # removed from the sample.

    for i in range(1, max_outliers + 1):
        if one_tail:
            if upper_tail:
                ares = data['value'] - np.median(data['value'])
            else:
                ares = np.median(data['value']) - data['value']
        else:
            ares = np.abs((data['value'] - np.median(data['value'])))

        # protect against constant time series
        data_sigma = mad(data['value'])
        if data_sigma == 0:
            break

        ares /= float(data_sigma)

        R = np.max(ares)

        temp_max_idx = ares[ares == R].index.tolist()[0]

        r_idx[i - 1] = temp_max_idx

        data = data[data.index != r_idx[i - 1]]

        if one_tail:
            p = 1 - alpha / float(n - i + 1)
        else:
            p = 1 - alpha / float(2 * (n - i + 1))

        t = student_t.ppf(p, (n - i - 1))
        lam = t * (n - i) / float(sqrt((n - i - 1 + t ** 2) * (n - i + 1)))

        if R > lam:
            number_of_anomalies = i

    if number_of_anomalies > 0:
        r_idx = r_idx[:number_of_anomalies]
    else:
        r_idx = None

    return {
        'anoms': r_idx,
        'stl': data_decomposed
    }
