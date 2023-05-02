# -*- coding: utf-8 -*-
# ==============================================================================
# filename          : test.py
# email             : daniel@dqsdatalabs.com
# date              : 01.05.2023
# version           : 0.01
# ==============================================================================


import unittest
import pandas as pd
from road_toll_forecast import RoadTollForecast


class TestRoadTollForecast(unittest.TestCase):
    def setUp(self):
        self.forecast = RoadTollForecast()

    def test_generate_sample_data(self):
        df = self.forecast.generate_sample_data()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 29220)
        self.assertEqual(set(df.columns), {'date', 'vehicle_type', 'toll_name', 'num_vehicles'})

    def test_preprocess_data(self):
        df = self.forecast.generate_sample_data()
        df_grouped = self.forecast.preprocess_data(df)
        self.assertIsInstance(df_grouped, pd.DataFrame)
        self.assertEqual(set(df_grouped.columns), {'ds', 'y'})

    def test_evaluate(self):
        df = self.forecast.generate_sample_data()
        df_grouped = self.forecast.preprocess_data(df)

        train = df_grouped[df_grouped['ds'] < '2019-01-01']
        test = df_grouped[df_grouped['ds'] >= '2019-01-01']

        self.forecast.fit(train)
        future = self.forecast.model.make_future_dataframe(periods=365)
        forecast = self.forecast.predict(future)
        mape = self.forecast.evaluate(test, forecast)

        self.assertIsInstance(mape, float)
        self.assertGreaterEqual(mape, 0)


if __name__ == '__main__':
    unittest.main()
