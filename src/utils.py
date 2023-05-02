# -*- coding: utf-8 -*-
# ==============================================================================
# filename          : utils.py
# email             : daniel@dqsdatalabs.com
# date              : 02.05.2023
# version           : 0.01
# ==============================================================================

import os
import traceback
import functools
import pandas as pd

from .config import *


def file_exists(path: str):
    return os.path.isfile(path)
    
def create_dataset():
    """ create dataset """
    if not file_exists(CSV_DATASET_PATH):
        raise FileNotFoundError("ERROR: CSV File not found")

    dataset = pd.read_csv(
        CSV_DATASET_PATH, sep=";", engine="python"
    )
    
    dataset = dataset.rename(columns={"Data": "ds", "VEP": "y"})
    dataset['ds'] = pd.to_datetime(dataset['ds'], format="%d/%m/%Y %H:%M")
    
    dataset = dataset.sort_values('ds')
    dataset = dataset.reset_index(drop=True)
    
    return dataset

def trace(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"INFO: Executing {func.__name__} with args: {args} and kwargs: {kwargs}")
        try:
            result = func(*args, **kwargs)
            logger.info(f"INFO: {func.__name__} executed successfully with result: {result}")
            return result
        except Exception as e:
            logger.error(f"{func.__name__} raised an exception: {str(e)}", "ERROR")
            traceback.print_exc()
            raise
    return wrapper







