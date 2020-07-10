import numpy as np
import matplotlib.pyplot as plt
import psycopg2
import math 
from matplotlib.animation import FuncAnimation
import datetime
import csv
from postgis import Polygon,MultiPolygon
from postgis.psycopg import register
import random
import pandas as pd
from heapq import heappush, heappop
import geopandas as gpd

# set the filepath and load in a shapefile
fp = "Rodovia_nacional.shp"
#fp = "Portugal_shapefile/pt_1km.shp"
map_df = gpd.read_file(fp)
print(map_df)
#map_df.head()

map_df.plot()
plt.show()