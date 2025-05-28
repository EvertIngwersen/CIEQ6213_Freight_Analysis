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
total_time = 200 #3320 max
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
T = range(start_time, end_time)  
p = {t: df_window.iloc[t - start_time]['value'] for t in T}
h = {t: 100 for t in T}             # holding cost per barrel per day
c_q = 2                            # transaction cost per barrel bought
c_s = 3                            # transaction cost per barrel sold
A_max = 1000                      # max storage capacity
Q_max = 200                       # max buy per day
S_max = 150                       # max sell per day
a0 = 0                           # initial inventory
















