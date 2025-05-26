# -*- coding: utf-8 -*-
"""
Created on Mon May 26 12:04:47 2025

@author: evert
"""

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

# -*- coding: utf-8 -*-
"""
Created on Mon May 26 12:04:47 2025

@author: evert
"""

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

# Paths to shapefiles (adjusted for your folder)
shapefile_path = r'C:\Users\evert\Documents\TU-Delft\TIL Master\CIEQ6213 Freight Transport Networks and Systems\CIEQ6213_Freight_Analysis\old_works\ne_10m_admin_0_countries\ne_10m_admin_0_countries.shp'
roads_shapefile_path = r'C:\Users\evert\Documents\TU-Delft\TIL Master\CIEQ6213 Freight Transport Networks and Systems\CIEQ6213_Freight_Analysis\old_works\tl_2024_us_primaryroads\tl_2024_us_primaryroads.shp'

# Load shapefiles
world = gpd.read_file(shapefile_path)
roads = gpd.read_file(roads_shapefile_path)

# Filter for the United States only
usa = world[world['ADMIN'] == 'United States of America']

# (Optional) Filter roads to only interstate or major highways if available
# For example, if there is a column 'MTFCC' or 'RTTYP' to filter by
# print(roads.columns)  # uncomment this line to inspect columns
# roads = roads[roads['MTFCC'] == 'S1100']  # S1100 = Primary roads in TIGER dataset

# Define major US cities with coordinates
cities = pd.DataFrame({
    'City': [
        'New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Miami',
        'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose',
        'Austin', 'Jacksonville', 'Fort Worth', 'Columbus', 'Charlotte',
        'San Francisco', 'Indianapolis', 'Seattle', 'Denver', 'Washington D.C.'
    ],
    'Latitude': [
        40.7128, 34.0522, 41.8781, 29.7604, 33.4484, 25.7617,
        39.9526, 29.4241, 32.7157, 32.7767, 37.3382,
        30.2672, 30.3322, 32.7555, 39.9612, 35.2271,
        37.7749, 39.7684, 47.6062, 39.7392, 38.9072
    ],
    'Longitude': [
        -74.0060, -118.2437, -87.6298, -95.3698, -112.0740, -80.1918,
        -75.1652, -98.4936, -117.1611, -96.7970, -121.8863,
        -97.7431, -81.6557, -97.3308, -82.9988, -80.8431,
        -122.4194, -86.1581, -122.3321, -104.9903, -77.0369
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
roads.plot(ax=ax, color='red', linewidth=1, label='Primary Roads')
cities_gdf.plot(ax=ax, color='blue', markersize=50)

# Annotate city names
for x, y, label in zip(cities_gdf.geometry.x, cities_gdf.geometry.y, cities_gdf.City):
    ax.text(x + 1, y + 1, label, fontsize=9)

# Set limits to focus on the continental US
ax.set_xlim(-130, -65)
ax.set_ylim(24, 50)

plt.title("Major US Cities and Primary Roads")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.legend()
plt.show()



















