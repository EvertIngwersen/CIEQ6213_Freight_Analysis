# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


import numpy as np
import math
from scipy import optimize
from openpyxl import * 


wb = load_workbook(filename = 'Part1_data.xlsx')

# Import the worksheets
wsRoadVol   = wb["RoadVol"]
wsRailVol   = wb["RailVol"]
wsTotalVol  = wb["TotalVol"]
wsRoadDist  = wb["RoadDist"]
wsRailDist  = wb["RailDist"]

# Load in the arrays
Countries   = np.array([[i.value for i in j] for j in wsRoadVol['A2':'A10']])
RoadVol     = np.array([[i.value for i in j] for j in wsRoadVol['B2':'J10']])
RailVol     = np.array([[i.value for i in j] for j in wsRailVol['B2':'J10']])
TotalVol    = np.array([[i.value for i in j] for j in wsTotalVol['B2':'J10']])
RoadDist    = np.array([[i.value for i in j] for j in wsRoadDist['B2':'J10']])
RailDist    = np.array([[i.value for i in j] for j in wsRailDist['B2':'J10']])

# ---- Sets ----
n = len(RoadVol)    # Number of countries
N = range(n)        # Set of countries (from 0 to 8)

# ---- Parameters ----
# Performance parameters for transport modes
RoadTariff  = 1     # Euro/km
RailTariff  = 0.4   # Euro/km
RoadSpeed   = 60    # km/h
RailSpeed   = 30    # km/h

# ---- Build cost and time matrices, based on performance parameters ----
RoadCosts   = RoadTariff*RoadDist    # Euro
RailCosts   = RailTariff*RailDist    # Euro
RoadTime    = RoadDist/RoadSpeed    # hour
RailTime    = RailDist/RailSpeed    # hour

# ---- Build observed shares matrices, with 0.5 for intra-country ----
# Create empty matrices
Obs_Shares_Road = np.zeros((n,n))
Obs_Shares_Rail = np.zeros((n,n))
# Fill observed shares matrices
for i in N:
    for j in N:
        # Intrazonal/intra-country gets modal split 50/50 %
        if i == j:
            Obs_Shares_Road[i,j] = 0.5
            Obs_Shares_Rail[i,j] = 0.5
        # Observed modal split from one country to another for all OD-pairs
        if i != j:
            Obs_Shares_Road[i,j] = RoadVol[i,j]/TotalVol[i,j]
            Obs_Shares_Rail[i,j] = RailVol[i,j]/TotalVol[i,j]

# ---- Create empty systemic utility matrices we will fill later on ----
# For road
SystUtilRoad = np.zeros((n,n))
# For rail
SystUtilRail = np.zeros((n,n))

































