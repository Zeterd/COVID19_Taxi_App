import numpy as np
import matplotlib.pyplot as plt
import psycopg2
import math
from matplotlib.animation import FuncAnimation
import datetime
import csv
from postgis import Polygon,MultiPolygon
from postgis.psycopg import register

conn = psycopg2.connect("dbname=postgres user=postgres")
register(conn)
cursor_psql = conn.cursor()

sql = "select distinct concelho  from cont_aad_caop2018 where distrito='PORTO'"
cursor_psql.execute(sql)
results = cursor_psql.fetchall()


concelhos_p = []
for i in results:
    concelhos_p.append(i[0])


sql = "select distinct concelho  from cont_aad_caop2018 where distrito='LISBOA'"
cursor_psql.execute(sql)
results = cursor_psql.fetchall()


concelhos_l = []
for i in results:
    concelhos_l.append(i[0])

taxi = []
dic = {}

for i in range(len(concelhos_p)):
    sql = "select distinct taxi from tracks as tr, cont_aad_caop2018 as caop where caop.concelho= '" + str(concelhos_p[i]) + "' and st_within(st_pointn(tr.proj_track,1), caop.proj_boundary) ;"
    cursor_psql.execute(sql)
    results = cursor_psql.fetchall()
    a = []
    for j in range(len(results)):
       a.append(results[j][0])
    taxi.append(a)
    dic[i] = concelhos_p[i]





for i in range(len(concelhos_l)):
    sql = "select distinct taxi from tracks as tr, cont_aad_caop2018 as caop where caop.concelho= '" + str(concelhos_l[i]) + "' and st_within(st_pointn(tr.proj_track,1), caop.proj_boundary) ;"
    cursor_psql.execute(sql)
    results = cursor_psql.fetchall()
    a = []
    for j in range(len(results)):
       a.append(results[j][0])
    taxi.append(a)
    dic[i+18] = concelhos_l[i]




#Para saber a que coluna corresponde cada taxi no ficheiro anim
sql = " select distinct taxi from tracks order by 1"
cursor_psql.execute(sql)
results = cursor_psql.fetchall()

taxi_id = {}
a = 0

for i in results:
    i = int(i[0])
    taxi_id[a] = i
    a = a+1

anim_offsets = []
with open('anim.csv', 'r') as anim:
    reader = csv.reader(anim)
    for row in reader:
        l = []
        for j in row:
            l.append(j)
        anim_offsets.append(l)

visitados = [0]*1660
infetados = []

for i in range(len(anim_offsets)):
    for j in range(1660):
        if int(anim_offsets[i][j]) == 1 and visitados[j] == 0:
            x = taxi_id[j]
            visitados[j] = 1
            infetados.append(x)

final = {}
for i in range(len(dic)):
    final[dic[i]] = 0


for i in range(len(infetados)):
    x = infetados[i]
    for j in range(len(taxi)):
        for k in range(len(taxi[j])):
            if int(x) == int(taxi[j][k]):
                    c = dic[j]
                    final[c] = final[c] + 1


######## Bar plot ########
bars = []
height = []
for i in range(len(dic)):
    bars.append(dic[i])
    height.append(final[dic[i]])

y_pos = np.arange(len(bars))
plt.bar(y_pos, height)
plt.xticks(y_pos, bars, rotation=90)
plt.subplots_adjust(bottom=0.3)

r1 = range(0,len(bars))
for i in range(len(bars)):
    plt.text(x = r1[i] , y = height[i]+3.0, s = height[i], size = 8, horizontalalignment='center')

plt.show()
