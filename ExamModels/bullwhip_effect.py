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
    
    """
    Simulates the bullwhip effect in a simplified supply chain.

    Args:
        num_periods (int): Total number of simulation periods.
        initial_inventory (int): Starting inventory for all entities.
        safety_stock_factor (float): Factor for additional stock ordered beyond forecast.
        retailer_lead_time (int): Lead time for retailer to receive goods from wholesaler.
        wholesaler_lead_time (int): Lead time for wholesaler to receive goods from manufacturer.
        manufacturer_lead_time (int): Lead time for manufacturer to produce/receive raw materials.
        base_consumer_demand (int): Average consumer demand per period.
        demand_fluctuation_amplitude (int): Max deviation from base demand for consumer.

    Returns:
        pd.DataFrame: A DataFrame containing the simulation results.
    """
    
    # Initialize data storage
    data = {
        'Period': list(range(num_periods)),
        'Consumer_Demand': [0] * num_periods,
        'Retailer_Orders_Wholesaler': [0] * num_periods,
        'Retailer_Inventory': [initial_inventory] * num_periods,
        'Wholesaler_Orders_Manufacturer': [0] * num_periods,
        'Wholesaler_Inventory': [initial_inventory] * num_periods,
        'Manufacturer_Production_Orders': [0] * num_periods,
        'Manufacturer_Inventory': [initial_inventory] * num_periods,
    }

    df = pd.DataFrame(data)

    # Queues for incoming orders/production (representing lead times)
    retailer_incoming_queue = [0] * wholesaler_lead_time
    wholesaler_incoming_queue = [0] * manufacturer_lead_time
    manufacturer_production_queue = [0] * manufacturer_lead_time # Manufacturer's own production lead time