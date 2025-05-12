# -*- coding: utf-8 -*-
"""
Created on Mon May 12 13:46:24 2025

@author: evert
"""

import gurobipy as gp
from gurobipy import GRB

# --------------------------
# Problem Data
# --------------------------

N = 3  # Products
S = 3  # Scenarios
R = 3  # Materials

products = range(N)
scenarios = range(S)
materials = range(R)

Prob = [0.3, 0.4, 0.3]

Dem = [
    [50, 20, 200],   # Scenario 0
    [150, 110, 225], # Scenario 1
    [250, 250, 500]  # Scenario 2
]

Profits = [60, 40, 10]
Cost = [2, 4, 5.2]

usage = [
    [8, 6, 1],    # Material 0
    [4, 2, 1.5],  # Material 1
    [2, 1.5, 0.5] # Material 2
]

# --------------------------
# Gurobi Model
# --------------------------

model = gp.Model("TwoStageProduction")

# First-stage decision variables: material quantities
x = model.addVars(materials, name="x", vtype=GRB.CONTINUOUS, lb=0)

# Second-stage decision variables: products per scenario
y = model.addVars(products, scenarios, name="y", vtype=GRB.CONTINUOUS, lb=0)

# --------------------------
# Objective Function
# --------------------------

material_cost = gp.quicksum(x[i] * Cost[i] for i in materials)

expected_profit = gp.quicksum(
    y[j, s] * Profits[j] * Prob[s]
    for s in scenarios
    for j in products
)

model.setObjective(expected_profit - material_cost, GRB.MAXIMIZE)

# --------------------------
# Constraints
# --------------------------

# Material usage constraint for every scenario
for i in materials:
    for s in scenarios:
        model.addConstr(
            gp.quicksum(usage[i][j] * y[j, s] for j in products) <= x[i],
            name=f"Usage_mat{i}_scen{s}"
        )

# Demand constraints
for j in products:
    for s in scenarios:
        model.addConstr(
            y[j, s] <= Dem[s][j],
            name=f"Demand_prod{j}_scen{s}"
        )

# --------------------------
# Solve the Model
# --------------------------

model.optimize()

# --------------------------
# Print Results
# --------------------------

if model.status == GRB.OPTIMAL:
    print("\nOptimal Solution Found:")
    for i in materials:
        print(f"Material {i+1} purchased: {x[i].X:.2f}")
    for s in scenarios:
        print(f"\nScenario {s+1} production:")
        for j in products:
            print(f"  Product {j+1}: {y[j, s].X:.2f}")
    print(f"\nExpected Profit: {model.ObjVal:.2f}")
else:
    print("No optimal solution found.")
