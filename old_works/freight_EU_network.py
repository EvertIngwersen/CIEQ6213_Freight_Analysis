# -*- coding: utf-8 -*-
"""
Created on Mon May 26 12:04:47 2025

@author: evert
"""

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pandas as pd

# Paths to shapefiles (adjust for your folder)
shapefile_path = r'C:\Users\evert\Documents\TU-Delft\TIL Master\CIEQ6213 Freight Transport Networks and Systems\CIEQ6213_Freight_Analysis\old_works\ne_10m_admin_0_countries\ne_10m_admin_0_countries.shp'
roads_shapefile_path = r'C:\Users\evert\Documents\TU-Delft\TIL Master\CIEQ6213 Freight Transport Networks and Systems\CIEQ6213_Freight_Analysis\old_works\tl_2024_us_primaryroads\tl_2024_us_primaryroads.shp'

# Load shapefiles
world = gpd.read_file(shapefile_path)
roads = gpd.read_file(roads_shapefile_path)

# Filter for the United States only
usa = world[world['ADMIN'] == 'United States of America']

# Filter only Interstates (RTTYP == 'I')
interstates = roads[roads['RTTYP'] == 'I']

# Define major US cities with coordinates
cities = pd.DataFrame({
    'City': [
        'New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Miami',
        'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose',
        'Austin', 'Jacksonville', 'Fort Worth', 'Columbus', 'Charlotte',
        'San Francisco', 'Indianapolis', 'Seattle', 'Denver', 'Washington D.C.',
        'Boston', 'El Paso', 'Detroit', 'Nashville', 'Memphis', 'Portland',
        'Oklahoma City', 'Las Vegas', 'Louisville', 'Baltimore', 'Milwaukee',
        'Albuquerque', 'Tucson', 'Fresno', 'Sacramento', 'Kansas City',
        'Mesa', 'Atlanta', 'Omaha', 'Colorado Springs', 'Raleigh', 'Miami',
        'Long Beach', 'Virginia Beach', 'Oakland', 'Minneapolis', 'Tulsa',
        'Boise', 'Cheyenne', 'Billings', 'Spokane', 'Salt Lake City',
        'Helena', 'Pocatello', 'Missoula', 'Casper', 'Idaho Falls',
        'Rapid City', 'Reno'
    ],
    'Latitude': [
        40.7128, 34.0522, 41.8781, 29.7604, 33.4484, 25.7617,
        39.9526, 29.4241, 32.7157, 32.7767, 37.3382,
        30.2672, 30.3322, 32.7555, 39.9612, 35.2271,
        37.7749, 39.7684, 47.6062, 39.7392, 38.9072,
        42.3601, 31.7619, 42.3314, 36.1627, 35.1495, 45.5051,
        35.4676, 36.1699, 38.2527, 39.2904, 43.0389,
        35.0844, 32.2226, 36.7378, 38.5816, 39.0997,
        33.4152, 33.7490, 41.2565, 38.8339, 35.7796, 25.7617,
        33.7701, 36.8529, 37.8044, 44.9778, 36.15398,
        43.6150, 41.1398, 45.7833, 47.6588, 40.7608,
        46.5958, 42.8713, 46.8721, 42.8501, 43.4917,
        44.0805, 39.5296
    ],
    'Longitude': [
        -74.0060, -118.2437, -87.6298, -95.3698, -112.0740, -80.1918,
        -75.1652, -98.4936, -117.1611, -96.7970, -121.8863,
        -97.7431, -81.6557, -97.3308, -82.9988, -80.8431,
        -122.4194, -86.1581, -122.3321, -104.9903, -77.0369,
        -71.0589, -106.4850, -83.0458, -86.7816, -90.0490, -122.6750,
        -97.5164, -115.1398, -85.7585, -76.6122, -87.9065,
        -106.6504, -110.9747, -119.7871, -121.4944, -94.5786,
        -111.8315, -84.3880, -95.9345, -104.8214, -78.6382, -80.1918,
        -118.1937, -75.9779, -122.2711, -93.2650, -95.99278,
        -116.2023, -104.8202, -108.5007, -117.4260, -111.8910,
        -112.0391, -112.4455, -114.0140, -106.3237, -112.0341,
        -103.2318, -119.8138
    ]
})

# Convert to GeoDataFrame
cities_gdf = gpd.GeoDataFrame(
    cities,
    geometry=gpd.points_from_xy(cities.Longitude, cities.Latitude),
    crs="EPSG:4326"
)

# Plot
fig, ax = plt.subplots(figsize=(16, 10))
usa.plot(ax=ax, color='lightgray', edgecolor='black')

# Plot only interstates
interstates.plot(ax=ax, color='blue', linewidth=0.7, label='Interstates')

cities_gdf.plot(ax=ax, color='red', markersize=50)

# Annotate city names
for x, y, label in zip(cities_gdf.geometry.x, cities_gdf.geometry.y, cities_gdf.City):
    ax.text(x + 1, y + 1, label, fontsize=9)

# Set limits to focus on the continental US
ax.set_xlim(-130, -65)
ax.set_ylim(24, 50)

plt.title("Major US Cities with Interstates Only")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.legend()
plt.show()


def haversine(lat1, lon1, lat2, lon2):
    # Radius of Earth in kilometers
    R = 6371.0

    # Convert degrees to radians
    lat1_rad, lon1_rad = np.radians(lat1), np.radians(lon1)
    lat2_rad, lon2_rad = np.radians(lat2), np.radians(lon2)

    # Differences
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Haversine formula
    a = np.sin(dlat / 2.0) ** 2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlon / 2.0) ** 2
    c = 2 * np.arcsin(np.sqrt(a))

    distance = R * c
    return distance

# Number of cities
n = len(cities)

# Initialize an empty distance matrix
distance_matrix = np.zeros((n, n))

# Compute the distance matrix
for i in range(n):
    for j in range(n):
        distance_matrix[i, j] = haversine(
            cities.loc[i, 'Latitude'], cities.loc[i, 'Longitude'],
            cities.loc[j, 'Latitude'], cities.loc[j, 'Longitude']
        )

# Convert to DataFrame for easier use and labeling
distance_df = pd.DataFrame(distance_matrix, index=cities['City'], columns=cities['City'])


















