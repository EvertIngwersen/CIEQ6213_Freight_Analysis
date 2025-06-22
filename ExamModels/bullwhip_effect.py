# -*- coding: utf-8 -*-
"""
Created on Sun Jun 22 14:21:22 2025

@author: evert
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def simulate_bullwhip(
    num_periods=52,  # Number of simulation periods (e.g., weeks)
    initial_inventory=50,
    safety_stock_factor=0.2, # Each entity orders an additional % of their forecasted demand as safety stock
    retailer_lead_time=1,
    wholesaler_lead_time=2,
    manufacturer_lead_time=3,
    base_consumer_demand=100,
    demand_fluctuation_amplitude=5 # Max variation from base demand
    
    