# -*- coding: utf-8 -*-
"""
Created on Sat Jun 14 13:43:07 2025

@author: evert
"""

import pandas as pd

# Define flows between zones (in tons)
# Let's assume 3 zones: A, B, C
# OD flow matrix (tons of goods)
m = {
    ('A', 'B'): 1200,
    ('B', 'A'): 300,
    ('A', 'C'): 800,
    ('C', 'A'): 100,
    ('B', 'C'): 500,
    ('C', 'B'): 600
}

# Average load per trip (tons/truck)
a = {
    ('A', 'B'): 20,
    ('B', 'A'): 20,
    ('A', 'C'): 25,
    ('C', 'A'): 25,
    ('B', 'C'): 15,
    ('C', 'B'): 15
}

# Parameters
M = 0.85   # Inefficiency constant for Naive model
p = 1.0    # Empty return factor for Noortman & Van Es

# Calculate trips using both methods
results = []

for (i, j), mij in m.items():
    aij = a[(i, j)]
    mji = m.get((j, i), 0)
    
    # Naive model
    z_naive = mij / (M * aij)
    
    # Noortman & Van Es model
    z_nve = (mij + p * mji) / aij
    
    results.append({
        'From': i,
        'To': j,
        'Flow (tons)': mij,
        'Reverse flow (tons)': mji,
        'Avg load (tons/trip)': aij,
        'Trips (Naive)': round(z_naive, 2),
        'Trips (N&VE)': round(z_nve, 2)
    })

# Convert to DataFrame
df_results = pd.DataFrame(results)
df_results.sort_values(by=['From', 'To'], inplace=True)
df_results.reset_index(drop=True, inplace=True)
df_results