# -*- coding: utf-8 -*-
"""
Created on Sun Jun 22 14:21:22 2025

@author: evert
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# --- 1. Define the Supply Chain Entity Class ---
class SupplyChainEntity:
    def __init__(self, name, initial_inventory, lead_time, safety_stock_factor):
        self.name = name
        self.inventory = initial_inventory
        self.lead_time = lead_time
        self.safety_stock_factor = safety_stock_factor

        self.orders_placed = []  # History of orders placed by this entity
        self.orders_received = [] # History of orders received by this entity
        self.fulfilled_demand_history = [] # History of demand fulfilled by this entity

        # Queue to simulate goods in transit
        self.incoming_queue = [0] * lead_time # Represents goods ordered by this entity, on their way

    def receive_goods(self, period):
        # Goods arrive if enough time has passed for the lead time
        if period >= self.lead_time:
            # Pop the oldest item from the queue and add to inventory
            received_amount = self.incoming_queue.pop(0)
            self.inventory += received_amount
            return received_amount
        return 0 # Nothing received yet if lead time not met

    def fulfill_demand(self, demand_amount):
        fulfilled = min(self.inventory, demand_amount)
        self.inventory -= fulfilled
        self.fulfilled_demand_history.append(fulfilled)
        return fulfilled

    def place_order(self, current_period_orders_received, upstream_lead_time):
        # Forecast: Simplistic - based on current period's orders received
        # A more sophisticated forecast (e.g., moving average) would be better in reality
        forecasted_demand = current_period_orders_received

        # Calculate required inventory: forecast + safety stock + demand during lead time
        required_inventory = forecasted_demand + (forecasted_demand * self.safety_stock_factor)
        required_inventory_during_lead_time = forecasted_demand * upstream_lead_time

        # Calculate order quantity
        order_qty = max(0, int(required_inventory + required_inventory_during_lead_time - self.inventory))
        self.orders_placed.append(order_qty)
        return order_qty

    def add_to_incoming_queue(self, quantity):
        # Add to this entity's incoming queue (goods coming FROM its supplier)
        # This is typically called by the *supplier* of this entity when an order is placed on them
        self.incoming_queue.append(quantity)


# --- 2. Simulation Function (Orchestrator) ---
def simulate_bullwhip_oop(
    num_periods=52,
    initial_inventory=50,
    safety_stock_factor=0.2,
    retailer_lead_time=1, # Retailer receives from wholesaler
    wholesaler_lead_time=2, # Wholesaler receives from manufacturer
    manufacturer_lead_time=3, # Manufacturer produces / receives from raw material supplier
    base_consumer_demand=100,
    demand_fluctuation_amplitude=5
):
    # Initialize entities
    retailer = SupplyChainEntity("Retailer", initial_inventory, retailer_lead_time, safety_stock_factor)
    wholesaler = SupplyChainEntity("Wholesaler", initial_inventory, wholesaler_lead_time, safety_stock_factor)
    manufacturer = SupplyChainEntity("Manufacturer", initial_inventory, manufacturer_lead_time, safety_stock_factor)

    # Data storage for plotting/analysis
    consumer_demand_history = []
    retailer_orders_to_wholesaler_history = []
    wholesaler_orders_to_manufacturer_history = []
    manufacturer_production_orders_history = []

    # --- Simulation Loop ---
    for t in range(num_periods):
        # --- 1. Generate Consumer Demand ---
        current_consumer_demand = int(base_consumer_demand +
                                      demand_fluctuation_amplitude * np.sin(2 * np.pi * t / (num_periods / 2)))
        if current_consumer_demand < 0:
            current_consumer_demand = 0
        consumer_demand_history.append(current_consumer_demand)

        # --- 2. Process Supply Chain from Downstream to Upstream ---

        # Manufacturer (receives orders from Wholesaler)
        # Receive goods (produced internally after lead time)
        manufacturer.receive_goods(t)

        # Fulfill orders received from Wholesaler in *previous* period
        # For the first period, wholesaler_orders_to_manufacturer_history[t-1] won't exist.
        # We assume initial orders are 0 for lead time periods.
        wholesaler_demand_on_manufacturer = (wholesaler_orders_to_manufacturer_history[t-1]
                                             if t > 0 else 0)
        manufacturer.fulfilled_demand_history.append(manufacturer.fulfill_demand(wholesaler_demand_on_manufacturer))

        # Manufacturer places production order
        prod_order = manufacturer.place_order(wholesaler_demand_on_manufacturer, manufacturer_lead_time)
        manufacturer.add_to_incoming_queue(prod_order) # This is its own production queue
        manufacturer_production_orders_history.append(prod_order)


        # Wholesaler (receives orders from Retailer)
        # Receive goods from Manufacturer
        wholesaler.receive_goods(t)

        # Fulfill orders received from Retailer in *previous* period
        retailer_demand_on_wholesaler = (retailer_orders_to_wholesaler_history[t-1]
                                          if t > 0 else 0)
        wholesaler.fulfilled_demand_history.append(wholesaler.fulfill_demand(retailer_demand_on_wholesaler))

        # Wholesaler places order to Manufacturer
        wholesaler_order = wholesaler.place_order(retailer_demand_on_wholesaler, manufacturer_lead_time)
        # Add this order to manufacturer's incoming queue
        manufacturer.add_to_incoming_queue(wholesaler_order)
        wholesaler_orders_to_manufacturer_history.append(wholesaler_order)


        # Retailer (receives demand from Consumer)
        # Receive goods from Wholesaler
        retailer.receive_goods(t)

        # Fulfill consumer demand
        retailer.fulfilled_demand_history.append(retailer.fulfill_demand(current_consumer_demand))

        # Retailer places order to Wholesaler
        retailer_order = retailer.place_order(current_consumer_demand, wholesaler_lead_time) # Retailer uses actual consumer demand for its forecast
        # Add this order to wholesaler's incoming queue
        wholesaler.add_to_incoming_queue(retailer_order)
        retailer_orders_to_wholesaler_history.append(retailer_order)


    # Prepare results for easy access and plotting
    results_df = pd.DataFrame({
        'Period': list(range(num_periods)),
        'Consumer_Demand': consumer_demand_history,
        'Retailer_Orders_Wholesaler': retailer_orders_to_wholesaler_history,
        'Retailer_Inventory': retailer.inventory, # This will just be the final inventory, not historical
        'Retailer_Fulfilled_Demand': retailer.fulfilled_demand_history,
        'Wholesaler_Orders_Manufacturer': wholesaler_orders_to_manufacturer_history,
        'Wholesaler_Inventory': wholesaler.inventory,
        'Wholesaler_Fulfilled_Demand': wholesaler.fulfilled_demand_history,
        'Manufacturer_Production_Orders': manufacturer_production_orders_history,
        'Manufacturer_Inventory': manufacturer.inventory,
        'Manufacturer_Fulfilled_Demand': manufacturer.fulfilled_demand_history,
    })

    # To get historical inventory, we need to capture it each step of the loop
    # Let's re-run a simplified version or adjust to capture history properly.
    # For now, let's just make the lists into Series for the DF.
    # The inventories are not captured per step in this current structure, only final.
    # To fix this, we need to append inventory to a list within the loop for each entity.

    # Re-running with proper history capture within the class or directly in loop
    # Let's adjust the entity to store history directly within the simulation
    # as the class itself would become too verbose.

    # --- Refined approach for storing historical data ---
    # We will still use the classes for logic, but gather the data into lists in the main loop
    # for easy DataFrame creation afterwards.

    # Initialize entities (again, for a clean run if you re-execute this cell)
    retailer = SupplyChainEntity("Retailer", initial_inventory, retailer_lead_time, safety_stock_factor)
    wholesaler = SupplyChainEntity("Wholesaler", initial_inventory, wholesaler_lead_time, safety_stock_factor)
    manufacturer = SupplyChainEntity("Manufacturer", initial_inventory, manufacturer_lead_time, safety_stock_factor)

    # Data storage lists (reset)
    consumer_demand_history = []
    retailer_orders_to_wholesaler_history = []
    retailer_inventory_history = []
    wholesaler_orders_to_manufacturer_history = []
    wholesaler_inventory_history = []
    manufacturer_production_orders_history = []
    manufacturer_inventory_history = []


    for t in range(num_periods):
        current_consumer_demand = int(base_consumer_demand +
                                      demand_fluctuation_amplitude * np.sin(2 * np.pi * t / (num_periods / 2)))
        if current_consumer_demand < 0:
            current_consumer_demand = 0
        consumer_demand_history.append(current_consumer_demand)

        # Manufacturer first (processes orders from prior period)
        manufacturer.receive_goods(t)
        wholesaler_demand_on_manufacturer = (wholesaler_orders_to_manufacturer_history[t-1] if t > 0 else 0)
        manufacturer.fulfill_demand(wholesaler_demand_on_manufacturer) # This updates internal inventory
        manufacturer_inventory_history.append(manufacturer.inventory) # Capture history
        prod_order = manufacturer.place_order(wholesaler_demand_on_manufacturer, manufacturer_lead_time)
        manufacturer.add_to_incoming_queue(prod_order)
        manufacturer_production_orders_history.append(prod_order)

        # Wholesaler next
        wholesaler.receive_goods(t)
        retailer_demand_on_wholesaler = (retailer_orders_to_wholesaler_history[t-1] if t > 0 else 0)
        wholesaler.fulfill_demand(retailer_demand_on_wholesaler)
        wholesaler_inventory_history.append(wholesaler.inventory)
        wholesaler_order = wholesaler.place_order(retailer_demand_on_wholesaler, manufacturer_lead_time)
        manufacturer.add_to_incoming_queue(wholesaler_order) # Wholesaler orders from manufacturer
        wholesaler_orders_to_manufacturer_history.append(wholesaler_order)

        # Retailer last (processes consumer demand for current period)
        retailer.receive_goods(t)
        retailer.fulfill_demand(current_consumer_demand)
        retailer_inventory_history.append(retailer.inventory)
        retailer_order = retailer.place_order(current_consumer_demand, wholesaler_lead_time)
        wholesaler.add_to_incoming_queue(retailer_order) # Retailer orders from wholesaler
        retailer_orders_to_wholesaler_history.append(retailer_order)


    # Final DataFrame construction
    results_df = pd.DataFrame({
        'Period': list(range(num_periods)),
        'Consumer_Demand': consumer_demand_history,
        'Retailer_Orders_Wholesaler': retailer_orders_to_wholesaler_history,
        'Retailer_Inventory': retailer_inventory_history,
        'Wholesaler_Orders_Manufacturer': wholesaler_orders_to_manufacturer_history,
        'Wholesaler_Inventory': wholesaler_inventory_history,
        'Manufacturer_Production_Orders': manufacturer_production_orders_history,
        'Manufacturer_Inventory': manufacturer_inventory_history,
    })

    return results_df, retailer, wholesaler, manufacturer

# --- Run the Simulation ---
# Now, simulate_bullwhip_oop returns the DataFrame AND the entity objects
simulation_df, retailer_obj, wholesaler_obj, manufacturer_obj = simulate_bullwhip_oop()

# --- Plotting the Results (Same as before) ---
plt.figure(figsize=(14, 8))

plt.plot(simulation_df['Period'], simulation_df['Consumer_Demand'], label='Consumer Demand (Retail Outflow)', linewidth=2, linestyle='--', color='blue')
plt.plot(simulation_df['Period'], simulation_df['Retailer_Orders_Wholesaler'], label='Retailer Orders to Wholesaler', linewidth=2, color='green')
plt.plot(simulation_df['Period'], simulation_df['Wholesaler_Orders_Manufacturer'], label='Wholesaler Orders to Manufacturer', linewidth=2, color='orange')
plt.plot(simulation_df['Period'], simulation_df['Manufacturer_Production_Orders'], label='Manufacturer Production Orders', linewidth=2, color='red')

plt.title('Bullwhip Effect in a Simplified Supply Chain (OOP)')
plt.xlabel('Time Period (Weeks)')
plt.ylabel('Order Quantity / Demand')
plt.legend()
plt.grid(True, linestyle=':', alpha=0.7)
plt.axhline(y=100, color='grey', linestyle='-.', label='Base Demand Level')
plt.tight_layout()
plt.show()

# --- How to Access Variables ---

print("\n--- Accessing Entity Variables After Simulation ---")

# Accessing final inventory of each entity:
print(f"Final Retailer Inventory: {retailer_obj.inventory}")
print(f"Final Wholesaler Inventory: {wholesaler_obj.inventory}")
print(f"Final Manufacturer Inventory: {manufacturer_obj.inventory}")

# Accessing history stored within the objects (e.g., all orders placed by retailer)
print("\nFirst 5 orders placed by Retailer:")
print(retailer_obj.orders_placed[:5])

print("\nFirst 5 orders received by Wholesaler (from Retailer):")
# Note: Orders received by wholesaler are the retailer's placed orders,
# captured in retailer_orders_to_wholesaler_history in the DataFrame.
# The entity's 'orders_received' within the class would need to be explicitly populated if needed.
# For now, the DataFrame `simulation_df` is the primary record for all historical flows.
print(simulation_df['Retailer_Orders_Wholesaler'].head())

# Accessing historical inventory from the DataFrame
print("\nRetailer Inventory History (First 5 periods):")
print(simulation_df['Retailer_Inventory'].head())

print("\nManufacturer Inventory History (Last 5 periods):")
print(simulation_df['Manufacturer_Inventory'].tail())

# You can now manipulate retailer_obj, wholesaler_obj, manufacturer_obj
# or use the simulation_df for further analysis.
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    