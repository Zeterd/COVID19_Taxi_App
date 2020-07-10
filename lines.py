import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
import numpy as np
import math
import psycopg2
from postgis import Polygon,MultiPolygon,LineString
from postgis.psycopg import register
import csv
import random
import datetime


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

#Porto
center_lon = -41601.3030699869
center_lat = 165663.59287178

#Lisboa
#center_lon = -87973.4688070632
#center_lat = -103263.891293955

scale=1/30000
zoom = 10000

plt.style.use('dark_background')
xs_min, xs_max, ys_min, ys_max = center_lon - zoom, center_lon + zoom, center_lat - zoom, center_lat + zoom
width_in_inches = (xs_max-xs_min)/0.0254*1.1
height_in_inches = (ys_max-ys_min)/0.0254*1.1
fig, ax = plt.subplots(figsize=(width_in_inches*scale, height_in_inches*scale))
ax.axis('off')
ax.set(xlim=(xs_min, xs_max), ylim=(ys_min, ys_max))

conn = psycopg2.connect("dbname=postgres user=postgres")
register(conn)

cursor_psql = conn.cursor()

sql = "select proj_track from tracks limit 5000"

cursor_psql.execute(sql)

results = cursor_psql.fetchall()

cont = 0

for track in results:
    if type(track[0]) is LineString:
        xy = track[0].coords
        xxx = []
        yyy = []
        first = 1
        for (x,y) in xy:
            if first == 1:
                xxx.append(x)
                yyy.append(y)
                previousx=x
                previousy=y
                first = 0
            elif math.sqrt(abs(x-previousx)**2+abs(y-previousy)**2)<50:
                xxx.append(x)
                yyy.append(y)
                previousx=x
                previousy=y
        ax.plot(xxx,yyy,linewidth=0.2,color='white')

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

def animate(i):
    ax.set_title(datetime.datetime.utcfromtimestamp(ts_i+i*10))
    scat.set_offsets(offsets[i])
    scat.set_color(anim_offsets[i])

# Mostrar todos os serviços com origem no Porto em taxis ocupados
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

scat=ax.scatter(x,y,s=5,color=[])

anim = FuncAnimation(
    fig, animate, interval=10, frames=len(offsets)-1, repeat = False)


plt.draw()
plt.show()
