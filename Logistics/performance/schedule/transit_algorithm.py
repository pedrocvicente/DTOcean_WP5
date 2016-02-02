# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 10:04:16 2015

@author: pcvicente adapted from acollin
"""

from geopy.distance import great_circle
import csv
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import math
import pickle
import utm


def transit_algorithm(point_INI, point_FIN):


    ini_x_utm = point_INI[0], ini_y_utm = point_INI[1], ini_zone_utm = point_INI[2,:]
    fin_x_utm = point_FIN[0], fin_y_utm = point_FIN[1], fin_zone_utm = point_FIN[2,:]


    num_points = 1
    lat_i = []
    long_i = []
    with open('Point_DTOcean_0.csv', 'rb') as csvfile:
        datareader = csv.reader(csvfile, delimiter='\t')
        for row in datareader:
            # print num_points
            # print ', '.join(row)

            if num_points<=1000:
                lat_i.append(float(row[2])/1e15)
                long_i.append(float(row[3])/1e15)

            elif num_points==1001:
                lat_i.append(float(row[3])/1e15)
                long_i.append(float(row[4])/1e15)

            elif num_points>=1001:
                if num_points%1000==0 or (num_points-1)%1000==0:
                    lat_i.append(float(row[3])/1e15)
                    long_i.append(float(row[4])/1e15)
                else:
                    lat_i.append(float(row[4])/1e15)
                    long_i.append(float(row[5])/1e15)

            if (long_i[num_points-1]<1 and long_i[num_points-1]>0) or (long_i[num_points-1]>-1 and long_i[num_points-1]<0):
                long_i[num_points-1] = long_i[num_points-1]*1e15

            num_points = num_points+1

    delt_lat = abs(lat_i[1168] - lat_i[0])
    delt_long = abs(long_i[1] - long_i[0])




    ### inputs_SV_LD_FullGraph = 'save'
    inputs_SV_LD_FullGraph = 'load'
    # inputs_SV_LD_FullGraph = 'nothing'

    if inputs_SV_LD_FullGraph == "save":
        # Saving the graph:

        PRINT_PERC=10 #%
        GRID = {}
        for ind_point in range(len(lat_i)):
        # for ind_point in range(2000):

            # if (ind_point/len(lat_i))%PRINT_PERC == 0:
            #     print (ind_point/len(lat_i))*100


            # -1 +1 -X +X
            CONNECTIONS = [0, 0, 0, 0]
            if ind_point==0: # PRIMEIRO PONTO

                if abs(long_i[ind_point+1] - long_i[ind_point]) < 1.2*delt_long:
                    # GRID = {ind_point: {ind_point+1: {'weight':delt_long}}}
                    CONNECTIONS[1]=1

                for ind_point_aux in range(ind_point+1,len(lat_i)):   # VER FRENTE
                    if (lat_i[ind_point_aux] < lat_i[ind_point] + 1.2*delt_lat) and (abs(lat_i[ind_point_aux] - lat_i[ind_point]) > 0.02):
                        if abs(long_i[ind_point_aux] - long_i[ind_point]) < 0.02:
                            # GRID.update( {ind_point: {ind_point_aux:{'weight':delt_lat}}} )
                            # GRID.update( {ind_point_aux: {ind_point: {'weight':delt_lat}}} )
                            CONNECTIONS[3]=1
                            break

            elif ind_point==len(lat_i)-1:  # ULTIMO PONTO
                if abs(long_i[ind_point-1] - long_i[ind_point]) < 1.2*delt_long:
                    # GRID.update( {ind_point: {ind_point-1: {'weight':delt_long}}} )
                    CONNECTIONS[0]=1

                for ind_point_aux_1 in range(ind_point-1, 0, -1):   # VER TRAS
                    if (lat_i[ind_point_aux] > lat_i[ind_point] - 1.2*delt_lat) and (abs(lat_i[ind_point_aux] - lat_i[ind_point]) > 0.02):
                        if abs(long_i[ind_point_aux_1] - long_i[ind_point]) < 0.02:
                            # GRID.update( {ind_point: {ind_point_aux:{'weight':delt_lat}}} )
                            # GRID.update( {ind_point_aux: {ind_point: {'weight':delt_lat}}} )
                            CONNECTIONS[2]=1
                            break

            else:

                if abs(long_i[ind_point-1] - long_i[ind_point]) < 1.2*delt_long:
                    # GRID.update( {ind_point: {ind_point-1: {'weight':delt_long}}} )
                    CONNECTIONS[0]=1


                if abs(long_i[ind_point+1] - long_i[ind_point]) < 1.2*delt_long:
                    # GRID.update( {ind_point: {ind_point+1: {'weight':delt_long}}} )
                    CONNECTIONS[1]=1

                for ind_point_aux in range(ind_point+1,len(lat_i)):    # VER FRENTE
                    if (lat_i[ind_point_aux] < lat_i[ind_point] + 1.2*delt_lat) and (abs(lat_i[ind_point_aux] - lat_i[ind_point]) > 0.02):
                        if abs(long_i[ind_point_aux] - long_i[ind_point]) < 0.02:
                            # GRID.update( {ind_point: {ind_point_aux:{'weight':delt_lat}}} )
                            # GRID.update( {ind_point_aux: {ind_point: {'weight':delt_lat}}} )
                            CONNECTIONS[3]=1
                            break

                for ind_point_aux_1 in range(ind_point-1, 0, -1):    # VER TRAS
                    if (lat_i[ind_point_aux] > lat_i[ind_point] - 1.2*delt_lat) and (abs(lat_i[ind_point_aux] - lat_i[ind_point]) > 0.02):
                        if abs(long_i[ind_point_aux_1] - long_i[ind_point]) < 0.02:
                            # GRID.update( {ind_point: {ind_point_aux:{'weight':delt_lat}}} )
                            # GRID.update( {ind_point_aux: {ind_point: {'weight':delt_lat}}} )
                            CONNECTIONS[2]=1
                            break



            BIN_CON = 0
            for ind_connect in range(len(CONNECTIONS)):
                if CONNECTIONS[ind_connect]==1:
                    BIN_CON = BIN_CON + pow(2,ind_connect)

            if BIN_CON==1:
                GRID.update( {ind_point: {ind_point-1: {'weight':delt_long}}} ) # -1
            elif BIN_CON==2:
                GRID.update( {ind_point: {ind_point+1: {'weight':delt_long}}} ) # +1
            elif BIN_CON==3:
                GRID.update( {ind_point: {ind_point-1: {'weight':delt_long}, ind_point+1: {'weight':delt_long}}} ) # -1 +1
            elif BIN_CON==4:
                GRID.update( {ind_point: {ind_point_aux_1: {'weight':delt_lat}}} ) # -x
            elif BIN_CON==5:
                GRID.update( {ind_point: {ind_point-1: {'weight':delt_long}, ind_point_aux_1: {'weight':delt_lat}}} ) # -1 -x
            elif BIN_CON==6:
                GRID.update( {ind_point: {ind_point+1: {'weight':delt_long}, ind_point_aux_1: {'weight':delt_lat}}} ) # +1 -x
            elif BIN_CON==7:
                GRID.update( {ind_point: {ind_point-1: {'weight':delt_long}, ind_point+1: {'weight':delt_long}, ind_point_aux_1: {'weight':delt_lat}}} ) # -1 +1 -x
            elif BIN_CON==8:
                GRID.update( {ind_point: {ind_point_aux: {'weight':delt_lat}}} ) # +x
            elif BIN_CON==9:
                GRID.update( {ind_point: {ind_point-1: {'weight':delt_long}, ind_point_aux: {'weight':delt_lat}}} ) # -1 +x
            elif BIN_CON==10:
                GRID.update( {ind_point: {ind_point+1: {'weight':delt_long}, ind_point_aux: {'weight':delt_lat}}} ) # +1 +x
            elif BIN_CON==11:
                GRID.update( {ind_point: {ind_point-1: {'weight':delt_long}, ind_point+1: {'weight':delt_long}, ind_point_aux: {'weight':delt_lat}}} ) # -1 +1 +x
            elif BIN_CON==12:
                GRID.update( {ind_point: {ind_point_aux_1: {'weight':delt_lat}, ind_point_aux: {'weight':delt_lat}}} ) # -x +x
            elif BIN_CON==13:
                GRID.update( {ind_point: {ind_point-1: {'weight':delt_long}, ind_point_aux_1: {'weight':delt_lat}, ind_point_aux: {'weight':delt_lat}}} ) # -1 -x +x
            elif BIN_CON==14:
                GRID.update( {ind_point: {ind_point+1: {'weight':delt_long}, ind_point_aux_1: {'weight':delt_lat}, ind_point_aux: {'weight':delt_lat}}} ) # +1 -x +x
            elif BIN_CON==15:
                GRID.update( {ind_point: {ind_point-1: {'weight':delt_long}, ind_point+1: {'weight':delt_long}, ind_point_aux_1: {'weight':delt_lat}, ind_point_aux: {'weight':delt_lat}}} ) # -1 +1 -x +x


        print 'build of graph'
        graph=nx.Graph(GRID)

        # print GRID

        # plt.figure()
        # nx.draw(graph)
        # plt.show()

        print 'save of graph'
        pickle.dump( graph, open( "graph_european_sea.p", "wb" ) )


    elif inputs_SV_LD_FullGraph == "load":
        # Getting back the graph:
        graph = pickle.load( open( "graph_european_sea.p", "rb" ) )
        print 'graph loaded'

        plt.figure()
        nx.draw(graph)
        plt.show()

    else:
        print 'Invalid SaveLoad option'





    ### coordinates of the locations to graph points!
    ERROR_POINTS = delt_long/2

    [LAT_INI, LONG_INI] = utm.to_latlon(ini_x_utm, ini_y_utm, ini_zone_utm[1], ini_zone_utm[2])
    for point_vec in range(len(lat_i)):

        LAT_ini = lat_i[point_vec]
        LONG_ini = long_i[point_vec]
        # print [LAT, LONG]

        if LAT_ini>LAT_INI-ERROR_POINTS and LAT_ini<LAT_INI+ERROR_POINTS:
            if LONG_ini>LONG_INI-ERROR_POINTS and LONG_ini<LONG_INI+ERROR_POINTS:
                if graph.has_node(point_vec):
                    point_INI = point_vec
                    # print point_INI
                    break


    [LAT_FIN, LONG_FIN] = utm.to_latlon(fin_x_utm, fin_y_utm, fin_zone_utm[1], fin_zone_utm[2])
    for point_vec in range(len(lat_i)):

        LAT_fin = lat_i[point_vec]
        LONG_fin = long_i[point_vec]
        # print [LAT, LONG]

        if LAT_fin>LAT_FIN-ERROR_POINTS and LAT_fin<LAT_FIN+ERROR_POINTS:
            if LONG_fin>LONG_FIN-ERROR_POINTS and LONG_fin<LONG_FIN+ERROR_POINTS:
                if graph.has_node(point_vec):
                    point_FIN = point_vec
                    # print point_FIN
                    break



    # # define start and end point
    start = point_INI # port
    end = point_FIN # array location


    import timeit
    start_time = timeit.default_timer()
    # print start_time

    # if path exists, run this
    if nx.has_path(graph,start,end):
        route = nx.dijkstra_path(graph,start,end)
        # route_length = nx.dijkstra_path_length(graph,start,end)


    stop_time = timeit.default_timer()
    # print stop_time


    duration =  stop_time - start_time


    total_length = 0
    point_i = (lat_i[route[0]], long_i[route[0]])
    for points_path in range(1,len(route)):
        point_f = (lat_i[route[points_path]], long_i[route[points_path]])
        total_length = total_length + great_circle(point_i, point_f).kilometers
        point_i = point_f

    print route
    print total_length
    # print route_length




    LONG_ROUTE = []
    LAT_ROUTE = []
    for ind_rout in range(len(route)):
        LONG_ROUTE.append(long_i[route[ind_rout]])
        LAT_ROUTE.append(lat_i[route[ind_rout]])




    plt.figure()

    plt.plot(long_i,lat_i, 'ro')

    plt.plot(LONG_ini,LAT_ini, 'yo')
    plt.plot(LONG_fin,LAT_fin, 'yo')

    plt.plot(LONG_ROUTE,LAT_ROUTE,'y-')

    plt.show()




    return total_length