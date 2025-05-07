# -*- coding: utf-8 -*-
"""
Created on Wed May  7 11:35:27 2025

@author: evert
"""

import numpy as np
import gurobipy as gp
from gurobipy import GRB

#-------------------SETS AND INDICES-----------------
# Demand nodes (origins and destinations)
V_d = ['A', 'B', 'C']  # example demand nodes

# Potential hub nodes
V_h = ['H1', 'H2']     # example hubs

# All nodes
V = V_d + V_h          # Union of demand and hub nodes

# Service types (e.g., rail, high-speed rail)
T = ['rail', 'ship']

# Commodity pairs (i, j) ∈ V_d × V_d, i ≠ j
commodity_pairs = [(i, j) for i in V_d for j in V_d if i != j]

# Hub pairs (k, m) ∈ V_h × V_h
hub_pairs = [(k, m) for k in V_h for m in V_h]

# Triple index for service type links between hubs
hub_service_triples = [(k, m, t) for k, m in hub_pairs for t in T]

#-------------------PARAMTERS------------------
W = {
    ('A', 'B'): 15,
    ('A', 'C'): 20,
    ('B', 'A'): 10,
    ('B', 'C'): 25,
    ('C', 'A'): 30,
    ('C', 'B'): 5,
}

C_road = {
    ('A', 'B'): 30,
    ('A', 'C'): 25,
    ('B', 'A'): 28,
    ('B', 'C'): 20,
    ('C', 'A'): 35,
    ('C', 'B'): 22,
}

C_access = {
    ('A', 'H1'): 10,
    ('A', 'H2'): 12,
    ('B', 'H1'): 8,
    ('B', 'H2'): 9,
    ('C', 'H1'): 11,
    ('C', 'H2'): 7,
}

C_hub = {
    ('H1', 'H2', 'rail'): 20,
    ('H1', 'H2', 'ship'): 15,
    ('H2', 'H1', 'rail'): 20,
    ('H2', 'H1', 'ship'): 15,
}

C_delivery = {
    ('H1', 'A'): 6,
    ('H1', 'B'): 5,
    ('H1', 'C'): 4,
    ('H2', 'A'): 7,
    ('H2', 'B'): 6,
    ('H2', 'C'): 5,
}

F_k = {
       'H1': 200,
       'H2': 400}

F_kmt = {
    ('H1', 'H2', 'rail'): 100,
    ('H1', 'H2', 'ship'): 80,
    ('H2', 'H1', 'rail'): 100,
    ('H2', 'H1', 'ship'): 80,
}

#-------------------DECISION VARIABLES-------------------
model = gp.Model("Oil Network")

# z_k: 1 if hub k is selected
z = model.addVars(V_h, vtype=GRB.BINARY, name="z")

# y_{kmt}: 1 if service t is activated between hubs k and m
y = model.addVars(V_h, V_h, T, vtype=GRB.BINARY, name="y")

# e_{ij}: Commodity (i,j) goes directly by road
e = model.addVars(commodity_pairs, vtype=GRB.BINARY, name="e")

# a_{ijk}: Commodity (i,j) accesses hub k from origin i
a = model.addVars(commodity_pairs, V_h, vtype=GRB.BINARY, name="a")

# x_{ijkmt}: Commodity (i,j) goes from hub k to hub m using service t
x = model.addVars(commodity_pairs, V_h, V_h, T, vtype=GRB.BINARY, name="x")

# b_{ijk}: Commodity (i,j) is delivered from hub k to destination j
b = model.addVars(commodity_pairs, V_h, vtype=GRB.BINARY, name="b")



#-------------------OBJECTIVE FUNCTION-------------------
# Initialize the objective
objective = gp.QuadExpr()  # Gurobi's quadratic expression, useful for terms with binary variables

# Add the commodity transport costs (first part of the objective)
for (i, j) in commodity_pairs:
    # Direct road transport cost (W_{ij} * C^{road}_{ij} * e_{ij})
    objective += W.get((i, j), 0) * C_road.get((i, j), 0) * e[(i, j)]

    # Add access and hub transport costs
    for k in V_h:
        objective += C_access.get((i, k), 0) * a[(i, j, k)]
        for (k, m, t) in hub_service_triples:
            objective += C_hub.get((k, m, t), 0) * x[(i, j, k, m, t)]

    # Delivery costs
    for k in V_h:
        objective += C_delivery.get((k, j), 0) * b[(i, j, k)]

# Add fixed costs for hubs (sum of F_k * z_k)
for k in V_h:
    objective += F_k.get(k, 0) * z[k]

# Add fixed costs for services (sum of F_{kmt} * y_{kmt})
for (k, m, t) in hub_service_triples:
    objective += F_kmt.get((k, m, t), 0) * y[(k, m, t)]

# Set the objective to minimize
model.setObjective(objective, GRB.MINIMIZE)

#------------------CONSTRAINTS----------------------------

# First constraint: Each commodity (i,j) is either connected to a hub or goes directly by road
for (i, j) in commodity_pairs:
    model.addConstr(gp.quicksum(a[i, j, k] for k in V_h) + e[i, j] == 1, name=f"hub_connection_{i}_{j}")

# Second constraint: Each commodity (i,j) is either delivered from a hub to destination j or goes directly by road
for (i, j) in commodity_pairs:
    model.addConstr(gp.quicksum(b[i, j, k] for k in V_h) + e[i, j] == 1, name=f"delivery_connection_{i}_{j}")






