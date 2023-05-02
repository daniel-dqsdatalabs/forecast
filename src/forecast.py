# -*- coding: utf-8 -*-
# ==============================================================================
# filename          : forecast.py
# email             : daniel@dqsdatalabs.com
# date              : 02.05.2023
# version           : 0.01
# ==============================================================================

import io
import holidays
import pandas as pd
import matplotlib as mlp
from prophet import Prophet
from prophet.plot import plot_cross_validation_metric
from prophet.diagnostics import cross_validation, performance_metrics

from .config import *
from .utils import *


class Predictor:
    
    @trace
    def __init__(self):
        self.forecast = None
        self.performance = None
        self.dataset = self.preprocess_data()
        self.model = Prophet(seasonality_mode="multiplicative", interval_width=0.95)
        
    @property 
    def train_data(self):
        dataset = self.dataset[self.dataset['ds'] < '2019-01-01']
        return dataset.set_index("ds")
    
    @property 
    def test_data(self):
        dataset = self.dataset[self.dataset['ds'] >= '2019-01-01']
        dataset = self.dataset[self.dataset['ds'] < '2020-01-01']
        return dataset.set_index("ds")
    
    @property 
    def actual_data(self):
        dataset = self.dataset[self.dataset['ds'] >= '2020-01-01']
        dataset = self.dataset[self.dataset['ds'] < '2021-01-01']
        return dataset.set_index("ds")
    
    @property
    def forecast_data(self):        
        return self.forecast[['ds','yhat']]
        
    @trace 
    def add_seasonality(self):
        """ """
        ...

        
    @trace
    def preprocess_data(self):
        """ data quality """
        dataset = create_dataset()
        br_holidays = holidays.Brazil()
        dataset['holiday'] = dataset['ds'].dt.weekday >= 5
        dataset[dataset["holiday"].apply(lambda d: d in br_holidays)]
        dataset = dataset.groupby(['ds']).sum().reset_index()
        return dataset

    @trace
    def predict(self):
        """ forecasting """
        self.model.fit(self.dataset)
        future = self.model.make_future_dataframe(periods=365)
        self.forecast = self.model.predict(future)

    @trace
    def evaluate(self):
        """ model accuracy """

        self.performance = performance_metrics(
            cross_validation(
                self.model, 
                initial='3650 days', 
                period='180 days', 
                horizon='365 days',
                parallel="processes",
            )
        )
        
    @trace
    def generate_report(self):
        """ save report """
        
        dataset = pd.merge(self.actual_data, self.forecast_data, on='ds')
        dataset['actual_vs_forecast'] = (dataset['y'] - dataset['yhat']) / dataset['y'] * 100
        dataset = dataset.rename(columns={"y": "actual_2020", "yhat": "forecast_2020"}) 
        dataset.to_excel(RESULT_FILE_PATH, index=False)
    
    @trace
    def log_results(self):
        """ log results """
        
        if not any((isinstance(self.performance, pd.DataFrame), self.performance)):
            raise Exception(
                """ Performance Metrics Not Found """
            )
            
        mae = self.performance['mae'].mean()
        mse = self.performance['mse'].mean()
        rmse = self.performance['rmse'].mean()
        mape = self.performance['mape'].mean()
        
        logger.info(f"INFO:Mean Absolute Error (MAE): {mae * 100:.2f}%")
        logger.info(f"INFO:Mean Squared Error (MSE): {mse * 100:.2f}%")
        logger.info(f"INFO:Root Mean Squared Error (RMSE): {rmse * 100:.2f}%")
        logger.info(f"INFO:Mean Absolute Percentage Error (MAPE): {mape * 100:.2f}%")

    @trace
    def run(self):
        """ get results """
        
        self.predict()
        self.evaluate()
        self.log_results()
        self.generate_report()



