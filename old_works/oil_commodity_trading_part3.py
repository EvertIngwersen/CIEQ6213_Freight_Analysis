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

# Load CSV
file_path = r"C:\Users\evert\Documents\TU-Delft\TIL Master\CIEQ6213 Freight Transport Networks and Systems\CIEQ6213_Freight_Analysis\old_works\oil_csv.csv"
df = pd.read_csv(file_path)

# Clean column names
df.columns = df.columns.str.strip()

# Convert 'date' column to datetime
df['date'] = pd.to_datetime(df['date'])

# Parameters for dynamic window
start_time = 0
total_time = 3000 #3320 max
end_time = start_time + total_time

# Slice dataframe by index to get the time window
df_window = df.iloc[start_time:end_time]

# Plot only the selected time window
plt.figure(figsize=(10, 5))
plt.plot(df_window['date'], df_window['value'], label='Oil Price', color='blue')
plt.xlabel('Date')
plt.ylabel('Price')
plt.title(f'Oil Price Over Time (Days {start_time} to {end_time})')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()


# Starting on making a model
model = gp.Model("Oil Trading")
T = range(start_time, end_time)  

# Parameters
a_0 = 0                                                    # Initial inventory at day t=0
p_t = {t: df_window.iloc[t - start_time]['value'] for t in T}
h_t = {t: 1 for t in T}                                     # Holding cost per barrel per day t
w_t = {t: 500 for t in T}                                    # Max inventory amount at dat t
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

    for t in T:
        print(f"Day {t}: Buy = {b_t[t].X:.2f}, Sell = {s_t[t].X:.2f}, Inventory = {q_t[t].X:.2f}, Profit = {day_profit[t]:.2f}")
else:
    print("No optimal solution found.")














