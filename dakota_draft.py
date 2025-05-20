# -*- coding: utf-8 -*-
"""
Created on Tue May 20 14:09:03 2025

@author: evert
"""

import numpy as np
import gurobipy as gp
from gurobipy import GRB

# Sets
N = ["Container1", "Container2", "Container3", "Container4",
     "Container5", "Container6", "Container7", "Container8",
     "Container9", "Container10", "Container11", "Container12"]
M = ["Truck1", "Truck2", "Plane1", "Ship1", "Ship2"] 

# Parameters

# Cost of bin j
C_j = {"Truck1": 100,
       "Truck2": 150,
       "Plane1": 550,
       "Ship1": 30,
       "Ship2": 25}

# Capacity of bin j
Q_j = {"Truck1": 38,
       "Truck2": 35,
       "Plane1": 75,
       "Ship1": 105,
       "Ship2": 150}

# Transport time of bin j (days)
T_j = {"Truck1": 5,
       "Truck2": 4,
       "Plane1": 2,
       "Ship1": 10,
       "Ship2": 14}

# Weight of container i
w_i = {"Container1": 25, "Container2": 12, "Container3": 44, "Container4": 3,
     "Container5": 22, "Container6": 10, "Container7": 55, "Container8": 76,
     "Container9": 42, "Container10": 19, "Container11": 36, "Container12": 7}

# Due time of container i
D_i = {"Container1": 12, "Container2": 8, "Container3": 4, "Container4": 22,
     "Container5": 21, "Container6": 21, "Container7": 18, "Container8": 17,
     "Container9": 30, "Container10": 12, "Container11": 5, "Container12": 17}

# Release time of container i
A_i = {"Container1": 3, "Container2": 0, "Container3": 0, "Container4": 2,
     "Container5": 5, "Container6": 6, "Container7": 9, "Container8": 10,
     "Container9": 26, "Container10": 1, "Container11": 1, "Container12": 1}

# A very large number for bigM >> 0 
bigM = 1000000

# Making Model

model = gp.Model("Bin Packing with Time Constraint")

x_ij = model.addVars(N, M, vtype=GRB.BINARY, name="x_ij")
u_j = model.addVars(M, vtype=GRB.BINARY, name="u_j")
t_j = model.addVars(M, vtype=GRB.CONTINUOUS, name="t_j")
d_i = model.addVars(N, vtype=GRB.CONTINUOUS, name="d_i")



























