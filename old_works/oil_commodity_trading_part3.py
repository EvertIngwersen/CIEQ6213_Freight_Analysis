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
total_time = 2000 #3320 max
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
a_0 = 20                                                    # Initial inventory at day t=0
p_t = {t: df_window.iloc[t - start_time]['value'] for t in T}
h_t = {t: 100 for t in T}                                   # Holding cost per barrel per day t
w_t = {t: 300 for t in T}                                   # Max inventory amount at dat t
max_b_t = {t: 80 for t in T}                                # Max amount what can be bought at day t
max_s_t = {t: 90 for t in T}                                # Max amount what can be sold at day t

# Variables
b_t = model.addVars(T, vtype=GRB.CONTINUOUS, name='b_t')    # Amount oil bought at day t
s_t = model.addVars(T, vtype=GRB.CONTINUOUS, name='s_t')    # Amount oil sold at day t
q_t = model.addVars(T, vtype=GRB.CONTINUOUS, name='q_t')    # Amount oil in storage at day t

# Objective Function

r"""

\text{min} \quad ( \sum_{t \in T}^{}(b_t \cdot p_t + h_t \cdot q_t) - \sum_{t \in T }^{}s_t \cdot p_t) 
 
"""

model.setObjective(
    gp.quicksum(b_t[t] * p_t[t] + h_t[t] * q_t[t] - s_t[t] * p_t[t] for t in T),
    GRB.MINIMIZE
)

# Constraints

#1: inventory must not exceed max storage capacity
for t in T:
    model.addConstr(q_t[t] <= w_t[t], name=f"storage_limit_{t}") 
    






















