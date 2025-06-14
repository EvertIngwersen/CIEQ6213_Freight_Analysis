# -*- coding: utf-8 -*-
"""
Created on Sat Jun 14 13:49:38 2025

@author: evert
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Set number of regions
n_origins = 50
n_destinations = 50

# Random seed for reproducibility
np.random.seed(77)

# Define constants
A = np.random.rand(n_origins) * 100  # Origin factors
B = np.random.rand(n_destinations) * 100  # Destination factors
C = np.random.rand(n_origins, n_destinations) * 10  # Travel cost matrix

# Gravity model equation: T_ij = A_i * B_j * exp(-c_ij)
T = np.zeros((n_origins, n_destinations))
for i in range(n_origins):
    for j in range(n_destinations):
        T[i, j] = A[i] * B[j] * np.exp(-C[i, j])

# Create DataFrame for clarity
df_T = pd.DataFrame(T, 
                    index=[f"Origin_{i+1}" for i in range(n_origins)], 
                    columns=[f"Dest_{j+1}" for j in range(n_destinations)])

# Print the resulting trip matrix
print("Gravity Model Trip Matrix:")
print(df_T.round(2))



