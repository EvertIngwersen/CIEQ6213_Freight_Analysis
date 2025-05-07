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

#----------------DECISION VARIABLES-----------









