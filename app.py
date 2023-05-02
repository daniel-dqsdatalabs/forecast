# -*- coding: utf-8 -*-
# ==============================================================================
# filename          : app.py
# email             : daniel@dqsdatalabs.com
# date              : 01.05.2023
# version           : 0.01
# ==============================================================================


from src.utils import *
from src.forecast import Predictor


if __name__ == "__main__":
    instance = Predictor()
    instance.run()