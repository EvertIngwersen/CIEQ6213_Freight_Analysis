# -*- coding: utf-8 -*-
"""
Created on Mon May 26 12:04:47 2025

@author: evert
"""

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

# Correct path to the shapefile (use raw string to avoid issues with backslashes)
shapefile_path = r'C:\Users\evert\Documents\TU-Delft\TIL Master\CIEQ6213 Freight Transport Networks and Systems\CIEQ6213_Freight_Analysis\old_works\ne_10m_admin_0_countries\ne_10m_admin_0_countries.shp'

# Load world geometries from local shapefile
world = gpd.read_file(shapefile_path)

# Check column names to confirm the continent column
print(world.columns)  # Run this once to inspect, likely it's 'CONTINENT'

# Filter Europe
europe = world[world['CONTINENT'] == 'Europe']

# Define city data
cities = pd.DataFrame({
    'City': ['Amsterdam', 'Berlin', 'Paris', 'Rome', 'Madrid', 'Warsaw'],
    'Latitude': [52.3676, 52.5200, 48.8566, 41.9028, 40.4168, 52.2297],
    'Longitude': [4.9041, 13.4050, 2.3522, 12.4964, -3.7038, 21.0122]
})
cities_gdf = gpd.GeoDataFrame(
    cities,
    geometry=gpd.points_from_xy(cities.Longitude, cities.Latitude),
    crs="EPSG:4326"
)

# Plot
fig, ax = plt.subplots(figsize=(10, 10))
europe.plot(ax=ax, color='lightgray', edgecolor='black')
cities_gdf.plot(ax=ax, color='red', markersize=50)

# Annotate city names
for x, y, label in zip(cities_gdf.geometry.x, cities_gdf.geometry.y, cities_gdf.City):
    ax.text(x + 0.5, y + 0.5, label, fontsize=9)

plt.title("Major European Cities")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.show()
















