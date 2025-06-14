# -*- coding: utf-8 -*-
"""
Created on Sat Jun 14 14:01:42 2025

@author: evert
"""

import numpy as np

# Define the technical coefficient matrix 'A' from the example on slide 2 of your document.
# This matrix shows the amount of input from each sector required to produce one unit of output for each sector.
# For example, A[0, 1] = 0.2 means 0.2 units from sector A are needed to produce 1 unit in sector M.
A = np.array([
    [0.2, 0.2, 0.1],  # Row A: Inputs from A, M, S needed for output of A
    [0.2, 0.4, 0.1],  # Row M: Inputs from A, M, S needed for output of M
    [0.1, 0.2, 0.3]   # Row S: Inputs from A, M, S needed for output of S
])

# Define the final demand vector 'D'.
# This represents the demand for goods and services for final consumption (e.g., households, government, exports).
# For this example, we assume a hypothetical final demand for sectors A, M, and S.
D = np.array([100, 150, 200]) # Example: 100 units for sector A, 150 for M, 200 for S

# Calculate the Leontief inverse matrix.
# The formula is (I - A)^-1, where 'I' is the identity matrix of the same dimension as 'A'.
# The Leontief inverse shows the total output from each sector required to satisfy one unit of final demand.
I = np.identity(A.shape[0])  # Create an identity matrix with dimensions matching A
leontief_inverse = np.linalg.inv(I - A)

# Calculate the total output vector 'X'.
# The formula is X = (I - A)^-1 * D.
# 'X' represents the total production (output) required from each sector to meet both intermediate
# demand (inputs for other sectors' production) and final demand.
X = np.dot(leontief_inverse, D)

print("Technical Coefficient Matrix (A):\n", A)
print("\nFinal Demand Vector (D):\n", D)
print("\nIdentity Matrix (I):\n", I)
print("\n(I - A) Matrix:\n", I - A)
print("\nLeontief Inverse Matrix (I - A)^-1:\n", leontief_inverse)
print("\nTotal Output Vector (X):\n", X)