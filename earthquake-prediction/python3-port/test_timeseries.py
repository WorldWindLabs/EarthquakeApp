from nose.tools import eq_
from pyculiarity.detect_ts import detect_ts
import unittest
from unittest import TestCase
import pandas as pd
import os


class TestTS(TestCase):
    def setUp(self):
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.raw_data = pd.read_csv(os.path.join(self.path, 'pyculiarity-testing-files/raw_data.csv'), usecols=['timestamp', 'count'])

    def test_both_directions_with_plot(self):
        results = detect_ts(self.raw_data, maximum_anomalies=0.02, direction='both', only_last='day', plot=False)
        eq_(len(results['anoms'].columns), 2)
        eq_(len(results['anoms'].iloc[:, 1]), 25)

    def test_both_directions_e_value_longterm(self):
        results = detect_ts(self.raw_data, maximum_anomalies=0.02, direction='both', long_term=True, plot=False,
                            e_value=True)
        eq_(len(results['anoms'].columns), 3)
        eq_(len(results['anoms'].iloc[:, 1]), 131)

    def test_both_directions_e_value_threshold_med_max(self):
        results = detect_ts(self.raw_data, maximum_anomalies=0.02, direction='both', threshold="med_max", e_value=True)
        eq_(len(results['anoms'].columns), 3)
        eq_(len(results['anoms'].iloc[:, 1]), 4)


if __name__ == '__main__':
    unittest.main()
