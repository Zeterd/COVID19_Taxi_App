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



ts_i = 1570665600
scale=1/3000000
conn = psycopg2.connect("dbname=postgres user=postgres")
register(conn)

xs_min, xs_max, ys_min, ys_max = -120000, 165000, -310000, 285000
width_in_inches = (xs_max-xs_min)/0.0254*1.1
height_in_inches = (ys_max-ys_min)/0.0254*1.1

fig, ax = plt.subplots(figsize=(width_in_inches*scale, height_in_inches*scale))
ax.axis('off')
ax.set(xlim=(xs_min, xs_max), ylim=(ys_min, ys_max))

cursor_psql = conn.cursor()

sql = "select distrito,st_union(proj_boundary) from cont_aad_caop2018 group by distrito"

cursor_psql.execute(sql)
results = cursor_psql.fetchall()

xs , ys = [],[]
for row in results:
    geom = row[1]
    if type(geom) is MultiPolygon:
        for pol in geom:
            xys = pol[0].coords
            xs, ys = [],[]
            for (x,y) in xys:
                xs.append(x)
                ys.append(y)
            ax.plot(xs,ys,color='black',lw='0.2')
    if type(geom) is Polygon:
        xys = geom[0].coords
        xs, ys = [],[]
        for (x,y) in xys:
            xs.append(x)
            ys.append(y)
        ax.plot(xs,ys,color='black',lw='0.2')

offsets = []

with open('offsets3.csv', 'r') as csvFile:
    reader = csv.reader(csvFile)
    i = 0
    for row in reader:
        l = []
        for j in row:
            x,y = j.split()
            x = float(x)
            y= float(y)
            l.append([x,y])
        offsets.append(l)

anim_offsets = []

with open('anim.csv', 'r') as anim:
    reader = csv.reader(anim)
    i = 0
    for row in reader:
        l = []
        for j in row:
            if int(j) == 1:
                x = "red"
                l.append(x)
            else:
                x = "green"
                l.append(x)
        anim_offsets.append(l)

x,y = [],[]
for i in offsets[0]:
    x.append(i[0])
    y.append(i[1])


##########################

def animate(i):
    ax.set_title(datetime.datetime.utcfromtimestamp(ts_i+i*10))
    scat.set_offsets(offsets[i])
    scat.set_color(anim_offsets[i])

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
j=random.randint(0,len(xs))

#print(x)
#print(y)


##########
scat=ax.scatter(x,y,s=2,color=[])

#print(xs[i])

anim = FuncAnimation(
    fig, animate, interval=10, frames=len(offsets)-1, repeat = False)

plt.draw()
plt.show()
