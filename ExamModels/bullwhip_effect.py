# -*- coding: utf-8 -*-
"""
Created on Sun Jun 22 14:21:22 2025

@author: evert
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


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
        self.orders_received = [] # History of orders received by this entity (from downstream)
        self.fulfilled_demand_history = [] # History of demand fulfilled by this entity

        # Queue to simulate goods in transit
        # Initialize with zeros. The actual "delivery" is handled by pop/append.
        self.incoming_queue = [0] * lead_time
        # Note: A queue of size `lead_time` initialized with zeros ensures that for the first
        # `lead_time` periods, nothing 'arrives' that was explicitly ordered by this entity,
        # which is correct.

    def receive_goods(self, period):
        received_amount = 0
        # Only attempt to receive if there's something in the queue.
        # The items in the queue represent what's "in transit" for this period.
        if self.incoming_queue:
            received_amount = self.incoming_queue.pop(0)
            self.inventory += received_amount
        return received_amount

    def fulfill_demand(self, demand_amount):
        fulfilled = min(self.inventory, demand_amount)
        self.inventory -= fulfilled
        self.fulfilled_demand_history.append(fulfilled)
        return fulfilled

    def place_order(self, current_period_orders_received, upstream_lead_time):
        # Forecast: Simplistic - based on current period's orders received
        forecasted_demand = current_period_orders_received

        # Calculate target inventory: What we want to have at the start of the next period.
        # This includes current forecast + safety stock for the forecast + demand during lead time.
        # It's an "order-up-to" logic.
        target_inventory_level = int(forecasted_demand * (1 + self.safety_stock_factor) +
                                     (forecasted_demand * upstream_lead_time))

        # Calculate order quantity needed to reach the target inventory level
        # factoring in current inventory.
        order_qty = max(0, target_inventory_level - self.inventory)

        self.orders_placed.append(order_qty)
        return order_qty

    def add_to_incoming_queue(self, quantity):
        # Add to this entity's incoming queue (goods coming FROM its supplier)
        self.incoming_queue.append(quantity)


# --- 2. Simulation Function (Orchestrator) ---
def simulate_bullwhip_oop(
    num_periods=152,
    initial_inventory=0,
    safety_stock_factor=0.2,
    retailer_lead_time=2, # Retailer receives from wholesaler
    wholesaler_lead_time=2, # Wholesaler receives from manufacturer
    manufacturer_lead_time=2, # Manufacturer produces / receives from raw material supplier
    base_consumer_demand=10,
    demand_fluctuation_amplitude=10
):
    # Initialize entities
    retailer = SupplyChainEntity("Retailer", initial_inventory, retailer_lead_time, safety_stock_factor)
    wholesaler = SupplyChainEntity("Wholesaler", initial_inventory, wholesaler_lead_time, safety_stock_factor)
    manufacturer = SupplyChainEntity("Manufacturer", initial_inventory, manufacturer_lead_time, safety_stock_factor)

    # Data storage lists (These will hold history for the DataFrame)
    consumer_demand_history = []
    retailer_orders_to_wholesaler_history = []
    retailer_inventory_history = [] # Now correctly capturing per period
    wholesaler_orders_to_manufacturer_history = []
    wholesaler_inventory_history = [] # Now correctly capturing per period
    manufacturer_production_orders_history = []
    manufacturer_inventory_history = [] # Now correctly capturing per period


    # --- Simulation Loop ---
    for t in range(num_periods):
        # --- 1. Generate Consumer Demand ---
        current_consumer_demand = int(base_consumer_demand +
                                      demand_fluctuation_amplitude * np.sin(2 * np.pi * t / (num_periods / 2)))
        if current_consumer_demand < 0:
            current_consumer_demand = 0
        consumer_demand_history.append(current_consumer_demand)

        # --- 2. Process Supply Chain from Upstream to Downstream for Order Fulfillment & Inventory Update ---
        # (It's generally better to process inventory updates before placing new orders)

        # Manufacturer: Fulfill orders for wholesaler, update inventory
        # First, goods 'arrive' from its internal production based on its lead time
        manufacturer.receive_goods(t) # Manufacturer's internal lead time
        wholesaler_demand_on_manufacturer = (wholesaler_orders_to_manufacturer_history[t-1] if t > 0 else 0)
        manufacturer.fulfill_demand(wholesaler_demand_on_manufacturer)
        manufacturer_inventory_history.append(manufacturer.inventory) # Capture inventory after fulfillment

        # Wholesaler: Fulfill orders for retailer, update inventory
        wholesaler.receive_goods(t) # Goods from manufacturer arrive
        retailer_demand_on_wholesaler = (retailer_orders_to_wholesaler_history[t-1] if t > 0 else 0)
        wholesaler.fulfill_demand(retailer_demand_on_wholesaler)
        wholesaler_inventory_history.append(wholesaler.inventory) # Capture inventory after fulfillment

        # Retailer: Fulfill consumer demand, update inventory
        retailer.receive_goods(t) # Goods from wholesaler arrive
        retailer.fulfill_demand(current_consumer_demand)
        retailer_inventory_history.append(retailer.inventory) # Capture inventory after fulfillment


        # --- 3. Place New Orders (Downstream to Upstream) ---
        # Orders are always placed based on current period's perceived demand/fulfillment

        # Retailer places order to Wholesaler
        # Retailer uses current consumer demand as its forecast for next order
        retailer_order = retailer.place_order(current_consumer_demand, wholesaler_lead_time)
        wholesaler.add_to_incoming_queue(retailer_order) # Retailer's order enters wholesaler's queue
        retailer_orders_to_wholesaler_history.append(retailer_order)

        # Wholesaler places order to Manufacturer
        # Wholesaler uses current retailer order as its forecast for next order
        wholesaler_order = wholesaler.place_order(retailer_order, manufacturer_lead_time)
        manufacturer.add_to_incoming_queue(wholesaler_order) # Wholesaler's order enters manufacturer's queue
        wholesaler_orders_to_manufacturer_history.append(wholesaler_order)

        # Manufacturer places production order (for itself)
        # Manufacturer uses current wholesaler order as its forecast for next production
        prod_order = manufacturer.place_order(wholesaler_order, manufacturer_lead_time)
        manufacturer.add_to_incoming_queue(prod_order) # Manufacturer's production order enters its own 'production' queue
        manufacturer_production_orders_history.append(prod_order)


    # Final DataFrame construction - ensuring all lists are populated within the ONE loop
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

# Accessing historical inventory from the DataFrame
print("\nRetailer Inventory History (First 5 periods):")
print(simulation_df['Retailer_Inventory'].head())

print("\nManufacturer Inventory History (Last 5 periods):")
print(simulation_df['Manufacturer_Inventory'].tail())
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    