import random
import numpy as np
import matplotlib.pyplot as plt
import psycopg2
import math
from matplotlib.animation import FuncAnimation
import datetime
import csv
from postgis import Polygon,MultiPolygon
from postgis.psycopg import register

def polygon_to_points(polygon_string):
    xs, ys = [],[]
    points = polygon_string[9:-2].split(',')
    for point in points:
        (x,y) = point.split()
        xs.append(float(x))
        ys.append(float(y))
    return xs,ys

def points_list_to_points(points_list):
    xs = []
    ys = []

    for point in points_list:
        point_string = point[0]
        point_string = point_string[6:-1]
        (x,y) = point_string.split()
        xs.append(float(x))
        ys.append(float(y))
    return xs, ys


scale=1/30000

con = psycopg2.connect("dbname=postgres user=postgres")
register(con)

sql ="""
        select st_astext(st_envelope(st_collect(proj_boundary)))
        from cont_aad_caop2018
        where concelho='PORTO'
     """
cursor_psql = con.cursor()
cursor_psql.execute(sql)
results = cursor_psql.fetchall()

row = results[0]
polygon_string = row[0]
xs,ys = polygon_to_points(polygon_string)
width_in_inches = ((max(xs)-min(xs))/0.0254)*1.1
height_in_inches = ((max(ys)-min(ys))/0.0254)*1.1
fig = plt.figure(figsize=(width_in_inches*scale,height_in_inches*scale))

# Plot freguesias of Porto
sql ="""
        select st_astext(proj_boundary)
        from cont_aad_caop2018
        where concelho='PORTO';
     """

cursor_psql.execute(sql)
results = cursor_psql.fetchall()

for row in results:
    polygon_string = row[0]
    xs, ys = polygon_to_points(polygon_string)
    plt.plot(xs,ys,color='black')

# Plot all services with origin at Porto
sql = """
        select st_astext(st_pointn(tr.proj_track,1))
        from tracks as tr, cont_aad_caop2018 as caop
        where caop.concelho='PORTO' and
              st_within(st_pointn(tr.proj_track,1), caop.proj_boundary) and
              tr.state='BUSY';
      """

cursor_psql.execute(sql)
results = cursor_psql.fetchall()

xs, ys = points_list_to_points(results)

i=random.randint(0,len(xs))
plt.scatter(xs[i],ys[i],s=5,color='red')
plt.show()
