# -*- coding: utf-8 -*-
# ==============================================================================
# filename          : config.py
# email             : daniel@dqsdatalabs.com
# date              : 01.05.2023
# version           : 0.01
# ==============================================================================


import os
import sys
import logging
from pathlib import Path
from datetime import datetime


""" GLOBAL """

DATABASE = ""
BASE_PATH =  Path(__file__).parent.parent
DATE = int(round(datetime.now().timestamp()))
FILES_PATH = os.path.join(BASE_PATH, "files")
CSV_DATASET_PATH = f"{FILES_PATH}/dataset.csv"
LOG_FILE_PATH = f"{FILES_PATH}/logs/run_{DATE}.log"
RESULT_FILE_PATH = f"{FILES_PATH}/results/actual_vs_forecast.xlsx"

""" LOGGER """

logging.basicConfig(
    filename=LOG_FILE_PATH, 
    filemode='w', level=logging.INFO, 
    format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S'
)

logger = logging.getLogger(__name__)