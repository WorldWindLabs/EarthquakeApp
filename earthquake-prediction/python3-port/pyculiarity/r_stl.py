# -*- coding: utf-8 -*-

import pandas
import rpy2.robjects as robjects
from numpy import asarray, int64


def stl(data, ns, np=None):
    """
    Seasonal-Trend decomposition procedure based on LOESS

    data : pandas.Series

    ns : int
        Length of the seasonal smoother.
        The value of  ns should be an odd integer greater than or equal to 3.
        A value ns>6 is recommended. As ns  increases  the  values  of  the
        seasonal component at a given point in the seasonal cycle (e.g., January
        values of a monthly series with  a  yearly cycle) become smoother.

    np : int
        Period of the seasonal component.
        For example, if  the  time series is monthly with a yearly cycle, then
        np=12.
        If no value is given, then the period will be determined from the
        ``data`` timeseries.
    """

    # make sure that data doesn't start or end with nan
    if isinstance(data,pandas.core.series.Series):
        if data.isnull().values.any():
            raise ValueError("data contains nans, cannot perform stl")
    else:
        raise TypeError("expected data input of type pandas series")

    ts_rpy = robjects.r['ts']
    stl_rpy = robjects.r['stl']

    if isinstance(data.index[0], int64):
        start = int(data.index[0])
    else:
        start = robjects.IntVector([data.index[0].year, data.index[0].month])

    ts = ts_rpy(robjects.FloatVector(asarray(data)), start=start, frequency=np)

    result = stl_rpy(ts, "periodic", robust=True)

    res_ts = asarray(result[0])
    try:
        res_ts = pandas.DataFrame({"seasonal": pandas.Series(res_ts[:, 0], index=data.index),
                                   "trend": pandas.Series(res_ts[:, 1], index=data.index),
                                   "remainder": pandas.Series(res_ts[:, 2], index=data.index)})
    except:
        return res_ts, data

    return res_ts
