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

# ---- Define a function that using parameters estimated by the optimization 
# tool, will return a RSME value ----
def Estimate(Parameters):
    # All unknowns as parameters
    Beta        = Parameters[0]
    Mu          = Parameters[1]
    RailASC_O   = Parameters[2:11]
    RailASC_D   = Parameters[11:20]
    
    # With these (estimated) parameters, calculate the systematic utility for
    # both modes, for all OD-pairs
    for i in N:
        for j in N:
            # We take the systematic utility for intrazonal transport as 0, no
            # matter the ASCs, this is done to get the modal split to 50/50 % 
            # for intrazonal transport
            if i == j:
                SystUtilRoad[i,j] = 0
                SystUtilRail[i,j] = 0
            # For non-intrazonal transport, the systematic utility per OD-pair
            # for both road and rail
            if i != j:
                SystUtilRoad[i,j] = Beta*RoadCosts[i,j] + Beta*RoadTime[i,j]
                SystUtilRail[i,j] = Beta*RailCosts[i,j] + Beta*RailTime[i,j]
    
    # If the denominator of the logit function is really small (0), 
    # return RMSE = 27.05 (which is too high to be a global minimum)
    if 0 in (np.exp(-Mu*SystUtilRoad) + np.exp(-Mu*SystUtilRail)):
        return 27.05 
    
    else:
        # If the denominator of the logit function is all right, calculate the
        # estimated share(s) of rail (and road)
        Est_P_Rail = np.exp(-Mu*SystUtilRail) / (np.exp(-Mu*SystUtilRail) + np.exp(-Mu*SystUtilRoad))
        Est_P_Road = np.exp(-Mu*SystUtilRoad) / (np.exp(-Mu*SystUtilRoad) + np.exp(-Mu*SystUtilRail))
        
        # Calculate the RMSE value, by comparing the observed shares for rail,
        # with the estimated shares for rail, excluding the intrazonal values
        # (including these would make for a better model fit then we have, as
        # we set the intrazonal values to make the model work)
        
        SE_Road = np.square(np.subtract(Obs_Shares_Road, Est_P_Road))
        SE_Rail = np.square(np.subtract(Obs_Shares_Rail, Est_P_Rail)) 
        RMSE = np.sqrt((SE_Rail+SE_Road)/2).sum() #Divided by the number of modes

        
        return RMSE

# Initialize the bounds for parameter estimation (first one is for
# Parameters[0], so the Beta (or VoT). The second one is for Parameters[1],
# so the mu. The rest is for the rail ASCs per country (Origin and destination
# respectively)
Bounds      = ((0,40),(0,1),(0,1000),(0,1000),(0,1000),(0,1000),(0,1000),\
                (0,1000),(0,1000),(0,1000),(0,1000),(0,1000),(0,1000),\
                    (0,1000),(0,1000),(0,1000),(0,1000),(0,1000),(0,1000),\
                        (0,1000))

# Define a (callback) function that stops the algorithm from further improving
# after a desired RSME value. Use RMSE < 0.02 to see if your model works, use
# RMSE < 0.0001 for the final results to be used in your report
def Callback(x, RMSE, context):
    if RMSE < 0.0001:
        return True
    else: return False




























