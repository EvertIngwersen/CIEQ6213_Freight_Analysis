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
    0: ('Shipping', 'Vitol BV', 'Maersk'),        # p0: Shipping Route from Vitol BV to Maersk 
    1: ('Pipeline', 'Shell', 'Rotterdam'),         # p1: Pipeline Route from Shell to Rotterdam
    2: ('Truck', 'Rotterdam', 'RedBull Racing'),  # p2: Truck Route from Rotterdam to RedBull Racing
    3: ('Pipeline', 'Vitol BV', 'Qatar'),         # p3: Pipeline Route from Vitol BV to Qatar
    4: ('Shipping', 'BP', 'Sydney'),              # p4: Shipping Route from BP to Sydney
    5: ('Truck', 'Antwerpen', 'DeutscheBahn'),    # p5: Truck Route from Antwerpen to DeutscheBahn
    6: ('Pipeline', 'ExxonMobil', 'Singapore'),   # p6: Pipeline Route from ExxonMobil to Singapore
    7: ('Shipping', 'Chevron', 'Houston'),        # p7: Shipping Route from Chevron to Houston
    8: ('Truck', 'Qatar', 'MSC'),                 # p8: Truck Route from Qatar to MSC
    9: ('Pipeline', 'TotalEnergies', 'Dubai'),    # p9: Pipeline Route from TotalEnergies to Dubai
    10: ('Shipping', 'Saudi Aramco', 'Rotterdam'), # p10: Shipping Route from Saudi Aramco to Rotterdam
    11: ('Truck', 'Amsterdam', 'Porsche'),        # p11: Truck Route from Amsterdam to Porsche
    12: ('Shipping', 'Royal Dutch Shell', 'Maersk'), # p12: Shipping Route from Royal Dutch Shell to Maersk
    13: ('Pipeline', 'ExxonMobil', 'Dallas'),     # p13: Pipeline Route from ExxonMobil to Dallas
    14: ('Truck', 'Houston', 'Tesla'),            # p14: Truck Route from Houston to Tesla
    15: ('Shipping', 'Chevron', 'Dubai'),         # p15: Shipping Route from Chevron to Dubai
    16: ('Truck', 'Rotterdam', 'KLM'),            # p16: Truck Route from Rotterdam to KLM
    17: ('Shipping', 'TotalEnergies', 'Sydney'),  # p17: Shipping Route from TotalEnergies to Sydney
    18: ('Truck', 'Singapore', 'Air France'),     # p18: Truck Route from Singapore to Air France
    19: ('Pipeline', 'Saudi Aramco', 'Houston'),  # p19: Pipeline Route from Saudi Aramco to Houston
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
 'Rotterdam': 91,
 'Qatar': 14,
 'Dallas': 35,
 'Amsterdam': 31,
 'Sydney': 28,
 'Antwerpen': 17,
 'Singapore': 94,
 'Houston': 13,
 'Dubai': 86
} #holding cost oil

Q_p = {i: random.randint(1, 100) for i in range(0, 20)} #capacity of route P

# Maximum supply capacity: s_i(t)
s_it = {(i, t): np.random.randint(500, 1000) for i in I for t in T}

# Demand: d_k(t)
d_kt = {(k, t): np.random.randint(200, 600) for k in K for t in T}



















