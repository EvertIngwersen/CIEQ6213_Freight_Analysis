# -*- coding: utf-8 -*-
"""
Created on Mon May 26 13:59:56 2025

@author: evert
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import gurobipy as gp
from gurobipy import GRB

conversion_factor = 1000 # Conversion factor from metric tonne to barrel (1 metric tonne = 7.6 barrels)
start_time = 1
total_time = 1600
# Load CSV
file_path = r"C:\Users\evert\Documents\TU-Delft\TIL Master\CIEQ6213 Freight Transport Networks and Systems\CIEQ6213_Freight_Analysis\old_works\oil_csv.csv" 
df = pd.read_csv(file_path)

# Load Bunkering CSV
file_path_bunker = r"C:\Users\evert\Documents\TU-Delft\TIL Master\CIEQ6213 Freight Transport Networks and Systems\CIEQ6213_Freight_Analysis\old_works\Daily_Bunker_Fuel_Prices_20250528.csv"
df_bunker = pd.read_csv(file_path_bunker)
print(df_bunker.head())

# Clean column names and convert 'date' to datetime for both
df.columns = df.columns.str.strip()
df['date'] = pd.to_datetime(df['date'])

df_bunker.columns = df_bunker.columns.str.strip()
df_bunker['date'] = pd.to_datetime(df_bunker['Day'], format='%m/%d/%Y')

# Get date range of df_bunker
start_date = df_bunker['date'].min()
end_date = df_bunker['date'].max()

# Filter df oil price to only include dates within df_bunker range
df_filtered = df[(df['date'] >= start_date) & (df['date'] <= end_date)].reset_index(drop=True)

# Now slice by index if needed (e.g., first 100 days of aligned data)

end_time = start_time + total_time

df_window = df_filtered.iloc[start_time:end_time]
df_bunker_window = df_bunker.iloc[start_time:end_time]

print("Oil price range:", df_filtered['date'].min(), "to", df_filtered['date'].max())
print("Bunker data range:", df_bunker['date'].min(), "to", df_bunker['date'].max())

# Extract Marine Gas Oil prices for the selected time window (same indices as T)
marine_gas_oil_costs_metric_tonne = df_bunker_window['Marine Gas Oil'].values

# Convert metric tonne cost to cost per barrel by dividing by 7.6
marine_gas_oil_costs_per_barrel = marine_gas_oil_costs_metric_tonne / conversion_factor

# Starting on making a model
model = gp.Model("Oil Trading Linear Programming")
T = range(start_time, end_time)  

# Parameters
a_0 = 0                                                    # Initial inventory at day t=0
p_t = {t: df_window.iloc[t - start_time]['value'] for t in T}
h_t = {t: marine_gas_oil_costs_per_barrel[t - start_time] for t in T} # Holding cost per barrel per day t
w_t = {t: 1000 for t in T}                                    # Max inventory amount at dat t
max_b_t = {t: 600 for t in T}                                # Max amount what can be bought at day t
max_s_t = {t: 300 for t in T}                                # Max amount what can be sold at day t

# Variables
b_t = model.addVars(T, vtype=GRB.CONTINUOUS, name='b_t')    # Amount oil bought at day t
s_t = model.addVars(T, vtype=GRB.CONTINUOUS, name='s_t')    # Amount oil sold at day t
q_t = model.addVars(T, vtype=GRB.CONTINUOUS, name='q_t')    # Amount oil in storage at day t
x = model.addVars(T, T, vtype=GRB.CONTINUOUS, name='x')     # FIFO sell portion from buy at τ

# Objective Function

model.setObjective(
    gp.quicksum(b_t[t] * p_t[t] + h_t[t] * q_t[t] for t in T) -
    gp.quicksum(x[τ, t] * p_t[t] for τ in T for t in T if τ < t),
    GRB.MINIMIZE
)

# Constraints

# Constraints
for t in T:
    model.addConstr(q_t[t] <= w_t[t], name=f"storage_limit_{t}")
    model.addConstr(b_t[t] <= max_b_t[t], name=f"buy_limit_{t}")
    model.addConstr(s_t[t] <= max_s_t[t], name=f"sell_limit_{t}")

model.addConstr(q_t[start_time] == a_0, name="start_inventory")

for t in range(start_time + 1, end_time):
    model.addConstr(q_t[t] == q_t[t - 1] + b_t[t] - s_t[t], name=f"inventory_balance_{t}")
    model.addConstr(s_t[t] <= q_t[t - 1], name=f"no_same_day_sell_{t}")

# FIFO Tracking Constraints
for t in T:
    if t == start_time:
        continue
    model.addConstr(gp.quicksum(x[τ, t] for τ in T if τ < t) == s_t[t], name=f"fifo_sell_total_{t}")

for τ in T:
    model.addConstr(gp.quicksum(x[τ, t] for t in T if t > τ) <= b_t[τ], name=f"fifo_no_oversell_{τ}")


# Optimize
model.optimize()

if model.status == GRB.OPTIMAL:
    print("\nOptimal solution found:")

    day_profit = []
    for t in T:
        profit_t = 0
        for τ in T:
            if τ < t:
                holding_cost = sum(h_t[r] for r in range(τ, t))
                profit_margin = (p_t[t] - p_t[τ]) - holding_cost
                profit_t += x[τ, t].X * profit_margin
        day_profit.append(profit_t)

    results = pd.DataFrame({
        'Day': list(T),
        'Date': df_window['date'].values,
        'Price': [p_t[t] for t in T],
        'Buy': [b_t[t].X for t in T],
        'Sell': [s_t[t].X for t in T],
        'Inventory': [q_t[t].X for t in T],
        'Holding cost': list(h_t.values()),
        'Max Inventory': list(w_t.values()),
        'Day Profit': day_profit
    })

    for idx, t in enumerate(T):
        print(f"Day {t}: Buy = {b_t[t].X:.2f}, Sell = {s_t[t].X:.2f}, Inventory = {q_t[t].X:.2f}, Profit = {day_profit[idx]:.2f}")
else:
    print("No optimal solution found.")


# Making plots

# Plot only the selected time window
fig, ax1 = plt.subplots(figsize=(15, 7))

# First plot: Oil Price (left y-axis)
ax1.plot(df_window['date'], df_window['value'], label='Oil Price', color='blue')
ax1.set_xlabel('Date')
ax1.set_ylabel('Oil Price', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')
ax1.grid(True)

# Second plot: Day Profit (right y-axis)
ax2 = ax1.twinx()
ax2.plot(df_window['date'], day_profit, label='Day Profit', color='orange')
ax2.set_ylabel('Day Profit', color='orange')
ax2.tick_params(axis='y', labelcolor='orange')

# Title and layout
plt.title(f'Oil Price and Day Profit Over Time (Days {start_time} to {end_time})')
fig.tight_layout()
plt.show()


# Second figure: Oil Price + Buy/Sell bars
fig, ax1 = plt.subplots(figsize=(15, 7))

# Plot oil price on left y-axis
ax1.plot(df_window['date'], df_window['value'], label='Oil Price', color='blue', linewidth=2)
ax1.set_xlabel('Date')
ax1.set_ylabel('Oil Price', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')
ax1.grid(True)

# Create second y-axis
ax2 = ax1.twinx()

# Plot Buy and Sell bars on right y-axis
bar_width = 0.4
dates = df_window['date']

ax2.bar(dates - pd.Timedelta(days=0.2), results['Buy'], width=bar_width, label='Buy', color='green', alpha=0.6)
ax2.bar(dates + pd.Timedelta(days=0.2), results['Sell'], width=bar_width, label='Sell', color='red', alpha=0.6)
ax2.set_ylabel('Buy/Sell Volume', color='black')
ax2.tick_params(axis='y', labelcolor='black')

# Title and legend
plt.title(f'Oil Price with Buy / Sell Activity (Days {start_time} to {end_time})')
fig.tight_layout()
fig.legend(loc='upper left', bbox_to_anchor=(0.1, 0.9))
plt.show()

# Third figure: Oil Price + Marine Gas Oil Bunker Price
fig, ax1 = plt.subplots(figsize=(15, 7))

# Plot Oil Price (left y-axis)
ax1.plot(df_window['date'], df_window['value'], label='Oil Price', color='blue', linewidth=2)
ax1.set_xlabel('Date')
ax1.set_ylabel('Oil Price', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')
ax1.grid(True)

# Create second y-axis for bunker price
ax2 = ax1.twinx()

# Plot Marine Gas Oil bunker price (per barrel) on right y-axis
ax2.plot(df_bunker_window['date'], marine_gas_oil_costs_per_barrel, label='Marine Gas Oil Price (per barrel)', color='green', linestyle='--', linewidth=2)
ax2.set_ylabel('Marine Gas Oil Price (per barrel)', color='green')

# Title and legend
plt.title(f'Oil Price and Marine Gas Oil Bunker Price (Days {start_time} to {end_time})')
fig.tight_layout()

# Combine legends from both axes
lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
plt.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left')

plt.show()















