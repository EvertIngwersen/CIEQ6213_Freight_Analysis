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

