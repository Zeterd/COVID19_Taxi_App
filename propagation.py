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
import queue 
import time


start_time = time.time()


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



conn = psycopg2.connect("dbname=postgres user=postgres")
register(conn)
cursor_psql = conn.cursor()


#Select the first 10 services with origin at Porto
sql = """
        select taxi, ts
        from tracks as tr, cont_aad_caop2018 as caop
        where caop.concelho='PORTO' and
              st_within(st_pointn(tr.proj_track,1), caop.proj_boundary) and
              tr.state='BUSY' order by ts limit 10;
      """

cursor_psql.execute(sql)
results = cursor_psql.fetchall()

i = random.randint(0,len(results))
taxi_porto = results[i-1][0]
print(taxi_porto)

#Select the first 10 services with origin at Lisboa
sql = """
        select taxi, ts
        from tracks as tr, cont_aad_caop2018 as caop
        where caop.concelho='LISBOA' and
              st_within(st_pointn(tr.proj_track,1), caop.proj_boundary) and
              tr.state='BUSY' order by ts limit 10;
      """

cursor_psql.execute(sql)
results = cursor_psql.fetchall()

i = random.randint(0,len(results))
taxi_lisboa = results[i-1][0]
print(taxi_lisboa)




#Para saber a que coluna corresponde cada taxi no ficheiro offsets
sql = " select distinct taxi from tracks order by 1"

cursor_psql.execute(sql)
results = cursor_psql.fetchall()

infetados = queue.Queue(maxsize=1660) 
taxi_id = {}
visitados = [0] * 1660
a = 0


for i in results:
    i = int(i[0])
    taxi_id[i] = a
    a = a+1

print(taxi_id[int(taxi_porto)])

#Obter a coluna do taxi escolhido aleatóriamente do Porto e de Lisboa
id_taxi_porto = taxi_id[int(taxi_porto)]
id_taxi_lisboa = taxi_id[int(taxi_lisboa)]


# Plot all services with origin at Porto
#Depois alterar para ser um carro aleatório 
#sql = "select st_astext(st_pointn(tr.proj_track,1))from tracks as tr, cont_aad_caop2018 as caop where taxi = '20000333'   limit 10 " 

#cursor_psql.execute(sql)
#results_p1 = cursor_psql.fetchall()
#print(results_p1)
#xs_p1, ys_p1 = points_list_to_points(results_p1)
#print(xs_p1)

#sql = "select st_astext(st_pointn(proj_track,1))from tracks as tr where taxi = '20000001'  order by ts limit 10 " 

#print(" ")
#cursor_psql.execute(sql)
#results_p2 = cursor_psql.fetchall()
#print(results_p2)

#xs_p2, ys_p2 = points_list_to_points(results_p2)





#Criar queue para saber quais taxis já foram infetados

infetados = queue.Queue(maxsize=1660) 
infetados.put(id_taxi_porto)   
infetados.put(id_taxi_lisboa)


offsets = []

with open('offsets3.csv', 'r') as csvFile:    
    reader = csv.reader(csvFile)
    i = 0
    for row in reader:
        l = []
        for j in row:            
            x,y = j.split()            
            x = float(x)            
            y = float(y)            
            l.append([x,y])        
        offsets.append(l)




#começa no zero 
conta = 0
while infetados.empty() != True:
    flag_3 = 0
    if infetados.qsize() >=2:
        taxi_1 = infetados.get()
        taxi_2 = infetados.get()
        conta = conta + 2
    else:
        taxi_1 = infetados.get()
        flag_3 = 1
    
    print("SIZE")
    print(infetados.qsize()) 
    for i in range(0,len(offsets),6):
        p1 = []
        p1 = offsets[i][taxi_1]
        x_p1 = p1[0]
        y_p1 = p1[1]
            
        p3 = []

        p3 = offsets[i][taxi_2]
        x_p3 = p3[0]
        y_p3 = p3[1]

        #print(taxi_1)
        for j in range(1660):
            flag_1 = 0
            flag_2 = 0
            #print(offsets[i][6]) # Imprime os ts da coluna 6 
            #print(offsets[1][j]) #Imprime o ts de cada taxi po ts
            
            p2 = []

            p2 = offsets[i][j]
            x_p2 = p2[0]
            y_p2 = p2[1]

          
            if ((x_p1 == 0) and (y_p1 == 0)) or ((x_p2 == 0) and (y_p2 == 0)) or (math.dist(p1,p2)>50) or (visitados[j]==1) or (taxi_1==j):
                flag_1 = 1;
            
            
            if ((x_p3 == 0) and (y_p3 == 0)) or ((x_p2 == 0) and (y_p2 == 0)) or (math.dist(p3,p2)>50) or (visitados[j]==1) or (taxi_2==j):
                flag_2 = 1
     
                
            else:
                if (flag_1 == 0 and flag_2 == 1) or (flag_1 == 0 and flag_2==0):
                    #distance = math.dist(p1,p2) 
                    #print(distance)
                    prob = random.randint(1,10)
                    if prob == 1:
                        print("entrei")
                        infetados.put(j)
                        visitados[j] = 1
                elif  flag_1 == 1 and flag_2 == 0:
                    #distance = math.dist(p3,p2) 
                    #print(distance)
                    prob = random.randint(1,10)
                    if prob == 1:
                        print("entrei")
                        infetados.put(j)
                        visitados[j] = 1
                


print("Conta " + str(conta))      



print("--- %s seconds ---" % (time.time() - start_time))
#i=random.randint(0,len(xs))
#j=random.randint(0,len(xs))



