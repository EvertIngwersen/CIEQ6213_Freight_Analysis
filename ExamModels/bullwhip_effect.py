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
    demand_fluctuation_amplitude=5): # Max variation from base demand
    
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

    # --- Simulation Loop ---
    for t in range(num_periods):
        # 1. Generate Consumer Demand
        # A slight sine wave fluctuation for illustration
        df.loc[t, 'Consumer_Demand'] = int(base_consumer_demand +
                                           demand_fluctuation_amplitude * np.sin(2 * np.pi * t / (num_periods / 2)))
        if df.loc[t, 'Consumer_Demand'] < 0: # Ensure demand is not negative
            df.loc[t, 'Consumer_Demand'] = 0

        # --- Retailer Logic ---
        # Receive goods from wholesaler based on lead time
        if t >= retailer_lead_time:
            df.loc[t, 'Retailer_Inventory'] = df.loc[t-1, 'Retailer_Inventory'] + retailer_incoming_queue.pop(0)

        # Fulfill consumer demand
        # (Simplified: assume all demand is met if inventory > 0, otherwise lost sales)
        fulfilled_demand = min(df.loc[t, 'Retailer_Inventory'], df.loc[t, 'Consumer_Demand'])
        df.loc[t, 'Retailer_Inventory'] -= fulfilled_demand

        # Retailer's Order to Wholesaler
        # Forecast: Based on previous period's orders received (which were consumer demand)
        # We'll simplify: retailer uses its *own fulfilled demand* as a proxy for its forecast
        # and adds safety stock based on this.
        forecasted_demand = df.loc[t, 'Consumer_Demand'] # Or more realistically, a moving average of past demand
        required_inventory = forecasted_demand + (forecasted_demand * safety_stock_factor)
        
        # Order amount to bring inventory up to required level + cover forecasted demand during lead time
        # The 'wholesaler_lead_time' is important here, as retailer needs to order enough for this period + lead time
        order_quantity = max(0, int(required_inventory - df.loc[t, 'Retailer_Inventory'] +
                                    (forecasted_demand * retailer_lead_time)))
        df.loc[t, 'Retailer_Orders_Wholesaler'] = order_quantity
        retailer_incoming_queue.append(order_quantity)


        # --- Wholesaler Logic ---
        # Receive goods from manufacturer based on lead time
        if t >= wholesaler_lead_time:
            df.loc[t, 'Wholesaler_Inventory'] = df.loc[t-1, 'Wholesaler_Inventory'] + wholesaler_incoming_queue.pop(0)

        # Fulfill retailer's orders
        fulfilled_retailer_order = min(df.loc[t, 'Wholesaler_Inventory'], df.loc[t, 'Retailer_Orders_Wholesaler'])
        df.loc[t, 'Wholesaler_Inventory'] -= fulfilled_retailer_order

        # Wholesaler's Order to Manufacturer
        # Forecast: Based on previous period's orders received from retailer
        forecasted_demand_wholesaler = df.loc[t, 'Retailer_Orders_Wholesaler']
        required_inventory_wholesaler = forecasted_demand_wholesaler + (forecasted_demand_wholesaler * safety_stock_factor)

        order_quantity_wholesaler = max(0, int(required_inventory_wholesaler - df.loc[t, 'Wholesaler_Inventory'] +
                                                (forecasted_demand_wholesaler * wholesaler_lead_time)))
        df.loc[t, 'Wholesaler_Orders_Manufacturer'] = order_quantity_wholesaler
        wholesaler_incoming_queue.append(order_quantity_wholesaler)


        # --- Manufacturer Logic ---
        # Receive 'produced' goods (internal lead time)
        if t >= manufacturer_lead_time:
            df.loc[t, 'Manufacturer_Inventory'] = df.loc[t-1, 'Manufacturer_Inventory'] + manufacturer_production_queue.pop(0)

        # Fulfill wholesaler's orders
        fulfilled_wholesaler_order = min(df.loc[t, 'Manufacturer_Inventory'], df.loc[t, 'Wholesaler_Orders_Manufacturer'])
        df.loc[t, 'Manufacturer_Inventory'] -= fulfilled_wholesaler_order

        # Manufacturer's Production Order
        # Forecast: Based on previous period's orders received from wholesaler
        forecasted_demand_manufacturer = df.loc[t, 'Wholesaler_Orders_Manufacturer']
        required_inventory_manufacturer = forecasted_demand_manufacturer + (forecasted_demand_manufacturer * safety_stock_factor)

        production_order_quantity = max(0, int(required_inventory_manufacturer - df.loc[t, 'Manufacturer_Inventory'] +
                                                 (forecasted_demand_manufacturer * manufacturer_lead_time)))
        df.loc[t, 'Manufacturer_Production_Orders'] = production_order_quantity
        manufacturer_production_queue.append(production_order_quantity)


    return df

# --- Run the Simulation ---
simulation_results = simulate_bullwhip()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    