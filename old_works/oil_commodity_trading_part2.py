# -*- coding: utf-8 -*-
"""
Created on Wed May  7 13:04:08 2025

@author: evert
"""

import random
import numpy as np
import gurobipy as gp
from gurobipy import GRB

random.seed(77)


# Define time periods
t_end = 100  # 100 days
T = np.arange(0, t_end, 1)

#---------SET AND INDICES--------------
#oil suppliers (I)
I = ['Shell', 'Vitol BV', 'BP', 'ExxonMobil', 'Chevron', 'TotalEnergies', 'Saudi Aramco', 'Royal Dutch Shell']

#oil storage locations (J)
J = ['Rotterdam', 'Qatar', 'Dallas', 'Amsterdam', 'Sydney', 'Antwerpen', 'Singapore', 'Houston', 'Dubai']

#customers (K)
K = ['RedBull Racing', 'DeutscheBahn', 'Maersk', 'MSC', 'KLM', 'Delta', 'Air France', 'Porsche', 'Tesla']

# Define set P (Transportation routes) with expanded routes
P = {
    0: ('Shipping', 'Vitol BV', 'Rotterdam'),        # p0: Shipping Route from Vitol BV to Rotterdam (Storage)
    1: ('Pipeline', 'Shell', 'Rotterdam'),           # p1: Pipeline Route from Shell to Rotterdam (Storage)
    2: ('Truck', 'Rotterdam', 'RedBull Racing'),     # p2: Truck Route from Rotterdam (Storage) to RedBull Racing (Customer)
    3: ('Pipeline', 'Vitol BV', 'Qatar'),            # p3: Pipeline Route from Vitol BV to Qatar (Storage)
    4: ('Shipping', 'BP', 'Sydney'),                 # p4: Shipping Route from BP to Sydney (Storage)
    5: ('Truck', 'Antwerpen', 'DeutscheBahn'),       # p5: Truck Route from Antwerpen to DeutscheBahn (Customer)
    6: ('Pipeline', 'ExxonMobil', 'Singapore'),      # p6: Pipeline Route from ExxonMobil to Singapore (Storage)
    7: ('Shipping', 'Chevron', 'Houston'),           # p7: Shipping Route from Chevron to Houston (Storage)
    8: ('Truck', 'Qatar', 'MSC'),                    # p8: Truck Route from Qatar (Storage) to MSC (Customer)
    9: ('Pipeline', 'TotalEnergies', 'Dubai'),       # p9: Pipeline Route from TotalEnergies to Dubai (Storage)
    10: ('Shipping', 'Saudi Aramco', 'Rotterdam'),   # p10: Shipping Route from Saudi Aramco to Rotterdam (Storage)
    11: ('Truck', 'Amsterdam', 'Porsche'),           # p11: Truck Route from Amsterdam to Porsche (Customer)
    12: ('Shipping', 'Royal Dutch Shell', 'Maersk'), # p12: Shipping Route from Royal Dutch Shell to Maersk (Customer)
    13: ('Pipeline', 'ExxonMobil', 'Dallas'),        # p13: Pipeline Route from ExxonMobil to Dallas (Storage)
    14: ('Truck', 'Houston', 'Tesla'),               # p14: Truck Route from Houston to Tesla (Customer)
    15: ('Shipping', 'Chevron', 'Dubai'),            # p15: Shipping Route from Chevron to Dubai (Storage)
    16: ('Truck', 'Rotterdam', 'KLM'),               # p16: Truck Route from Rotterdam (Storage) to KLM (Customer)
    17: ('Shipping', 'TotalEnergies', 'Sydney'),     # p17: Shipping Route from TotalEnergies to Sydney (Storage)
    18: ('Truck', 'Singapore', 'Air France'),        # p18: Truck Route from Singapore (Storage) to Air France (Customer)
    19: ('Pipeline', 'Saudi Aramco', 'Houston'),     # p19: Pipeline Route from Saudi Aramco to Houston (Storage)
}

# Display the expanded sets and transportation routes
print("Suppliers (I):", I)
print("Storage Locations (J):", J)
print("Customers (K):", K)

print("\nTransportation Routes (P):")
for route_id, details in P.items():
    mode, source, destination = details
    print(f"Route {route_id}: Mode = {mode}, Source = {source}, Destination = {destination}")

#--------------PARAMETERS--------------------
p_oil = {i: 50 for i in range(0, t_end)} # fixed price at 50% per barrel
c_p = {i: random.randint(1, 100) for i in range(0, 20)} #cost per route
r_p = {i: random.randint(1, 100) for i in range(0, 20)} #risk penalty for route p
h_j = {
 'Rotterdam': 4,
 'Qatar': 2,
 'Dallas': 6,
 'Amsterdam': 1,
 'Sydney': 3,
 'Antwerpen': 6,
 'Singapore': 8,
 'Houston': 2,
 'Dubai': 1
} #holding cost oil

Q_p = {i: random.randint(1, 100) for i in range(0, 20)} #capacity of route P

# Maximum supply capacity: s_i(t)
s_it = {(i, t): np.random.randint(500, 1000) for i in I for t in T}

# Demand: d_k(t)
d_kt = {(k, t): np.random.randint(2, 6) for k in K for t in T}

#----------DECISION VARIABLES--------------

model = gp.Model("Oil_Logistics")


x = model.addVars(I, J, P.keys(), T, name="x", lb=0)  # oil transported from supplier i to storage j via route p at time t
y = model.addVars(J, K, P.keys(), T, name="y", lb=0)  # oil transported from storage j to customer k via route p at time t
z = model.addVars(J, T, name="z", lb=0)  # storage level at location j at time t

model.setObjective(
    gp.quicksum(c_p[p] * x[i, j, p, t] for i in I for j in J for p in P.keys() for t in T) +  # Transportation cost
    gp.quicksum(h_j[j] * z[j, t] for j in J for t in T) +  # Storage cost
    gp.quicksum(r_p[p] * x[i, j, p, t] for i in I for j in J for p in P.keys() for t in T),  # Risk penalty
    GRB.MINIMIZE
)

#---------------CONSTRAINTS----------------
# Supply Constraints: ensure that the total oil supplied does not exceed the supply capacity
for i in I:
    for t in T:
        model.addConstr(gp.quicksum(x[i, j, p, t] for j in J for p in P.keys()) <= s_it[(i, t)],
                        name=f"Supply_{i}_{t}")

# Demand Constraints: ensure that the total oil delivered to each customer meets their demand
for k in K:
    for t in T:
        model.addConstr(gp.quicksum(y[j, k, p, t] for j in J for p in P.keys()) == d_kt[(k, t)],
                        name=f"Demand_{k}_{t}")

# Storage Balance Constraints: ensure that the storage balance is correct
for j in J:
    for t in T:
        if t == 0:
            # Initial storage constraint (at t=0)
            model.addConstr(z[j, t] == 0, name=f"InitialStorage_{j}_{t}")  # assuming initial storage is zero
        else:
            # Storage balance constraint
            model.addConstr(z[j, t] == z[j, t-1] + gp.quicksum(x[i, j, p, t] for i in I for p in P.keys()) - 
                             gp.quicksum(y[j, k, p, t] for k in K for p in P.keys()), 
                             name=f"StorageBalance_{j}_{t}")

# Route Capacity Constraints: ensure that no route exceeds its capacity
for p in P.keys():
    for t in T:
        model.addConstr(
            gp.quicksum(x[i, j, p, t] for i in I for j in J) + gp.quicksum(y[j, k, p, t] for j in J for k in K) 
            <= Q_p[p],
            name=f"RouteCapacity_{p}_{t}"
        )

# Non-Negativity Constraints: ensure all variables are non-negative
for i in I:
    for j in J:
        for p in P.keys():
            for t in T:
                model.addConstr(x[i, j, p, t] >= 0, name=f"NonNeg_x_{i}_{j}_{p}_{t}")
                model.addConstr(y[j, k, p, t] >= 0, name=f"NonNeg_y_{j}_{k}_{p}_{t}")
                model.addConstr(z[j, t] >= 0, name=f"NonNeg_z_{j}_{t}")

#---------PROGRESS CALLBACK FUNCTION------------------

def my_callback(model, where):
    if where == GRB.Callback.MIP:
        # Get the current best objective value
        obj_val = model.cbGet(GRB.Callback.MIP_OBJBST)
        # Get the current iteration
        iteration = model.cbGet(GRB.Callback.MIP_NODCNT)
        # Print progress at regular intervals (every 100 iterations)
        if iteration % 100 == 0:
            print(f"Iteration {iteration}: Best Obj = {obj_val:.2f}")


#-----------SOLVE THE MODEL------------------
# Set up to log the progress with the callback function
model.optimize(my_callback)

#-----------PRINT SUMMARY AFTER OPTIMAL SOLUTION------------------

# Check if the optimization was successful
if model.status == GRB.OPTIMAL:
    print("\nOptimization is complete and an optimal solution has been found.")
    print(f"Optimal Objective Value: {model.objVal:.2f}")

    # Print out the values of the decision variables in the optimal solution
    print("\nOptimal decision variables (some examples):")
    for i in I:
        for j in J:
            for p in P.keys():
                for t in T:
                    if x[i, j, p, t].x > 0:  # If there is positive transportation
                        print(f"x[{i}, {j}, {p}, {t}] = {x[i, j, p, t].x}")

    # Print storage levels
    for j in J:
        for t in T:
            if z[j, t].x > 0:  # If there is positive storage
                print(f"z[{j}, {t}] = {z[j, t].x}")
else:
    print("Optimization failed to find an optimal solution.")











