# -*- coding: utf-8 -*-
"""
Created on Wed Jun 18 14:44:22 2025

@author: evert
"""

import numpy as np
import matplotlib.pyplot as plt

# Problem data
cost_per_unit = 10
penalty_per_unit_unmet = 20

# Scenario probabilities and demands
scenarios = [
    {"prob": 0.3, "demand": 100},
    {"prob": 0.1, "demand": 200},
    {"prob": 0.2, "demand": 800},
    {"prob": 0.25, "demand": 700},
    {"prob": 0.15, "demand": 30}
]

# === Step 1: Expected Value Problem (EEV) ===
expected_demand = sum(s["prob"] * s["demand"] for s in scenarios)
x_EEV = expected_demand
cost_EEV = cost_per_unit * x_EEV

# Apply x_EEV to each scenario to calculate expected cost
EEV = 0
for s in scenarios:
    unmet = max(s["demand"] - x_EEV, 0)
    scenario_cost = cost_per_unit * x_EEV + penalty_per_unit_unmet * unmet
    EEV += s["prob"] * scenario_cost

# === Step 2: Stochastic Problem (RP) ===
def total_cost(x):
    """Compute total expected cost for a given production quantity x"""
    expected_cost = cost_per_unit * x
    for s in scenarios:
        unmet = max(s["demand"] - x, 0)
        expected_cost += s["prob"] * penalty_per_unit_unmet * unmet
    return expected_cost

# Try a range of x values to find the minimum RP cost
x_vals = np.arange(90, 210, 1)
costs = [total_cost(x) for x in x_vals]
min_index = np.argmin(costs)
x_RP = x_vals[min_index]
RP = costs[min_index]

# === Step 3: Wait-and-See (WS) ===
WS = 0
for s in scenarios:
    x_ws = s["demand"]
    scenario_cost = cost_per_unit * x_ws
    WS += s["prob"] * scenario_cost

# === KPIs (corrected definitions) ===
VSS = EEV - RP  # Value of using stochastic instead of deterministic
EVPI = RP - WS  # Value of perfect information


# === Print results ===
print("=== Stochastic LP KPI Example ===")
print(f"Expected demand (EEV production quantity): {x_EEV}")
print(f"Cost when using deterministic solution across scenarios (EEV): {EEV:.2f}")
print(f"Best stochastic solution x = {x_RP}, cost (RP): {RP:.2f}")
print(f"Wait-and-see cost (WS): {WS:.2f}")
print(f"Value of Stochastic Solution (VSS): {VSS:.2f}")
print(f"Expected Value of Perfect Information (EVPI): {EVPI:.2f}")


# === Plotting ===
plt.figure(figsize=(10, 6))
plt.plot(x_vals, costs, label="Stochastic Cost Curve (Total Expected Cost)", color='blue')

# Highlight RP solution
plt.axvline(x=x_RP, color='green', linestyle='--', label=f"RP (x={x_RP})")
plt.axhline(y=RP, color='green', linestyle='--')

# Highlight EEV solution
plt.axvline(x=x_EEV, color='orange', linestyle='--', label=f"EEV (x={x_EEV:.1f})")
plt.axhline(y=EEV, color='orange', linestyle='--')

# Highlight WS cost
plt.axhline(y=WS, color='red', linestyle='--', label=f"WS Cost = {WS:.2f}")

# Labels and legend
plt.xlabel("Production Quantity (x)")
plt.ylabel("Total Expected Cost")
plt.title("Stochastic Linear Programming Cost Curve")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


















