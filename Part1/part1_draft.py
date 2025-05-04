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