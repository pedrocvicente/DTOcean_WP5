# -*- coding: utf-8 -*-
"""
@author: WavEC Offshore Renewables
email: boris.teillant@wavec.org; paulo@wavec.org

This module is responsible for the selection of ports for both the installation
and O&M logistic activities. 

BETA VERSION NOTES: This current version is limited to the feasibility functions 
of two logistic phases (one for the installation module and one for the O&M), 
this will be upgraded for the beta version due to october.
"""

from transit_algorithm import transit_algorithm
from geopy.distance import great_circle
import utm
import math


def distance(UTM_ini, UTM_fin):
    """
    distance returns the calculated distance (in kms) between two points
    defined in the UTM coordinate system
    """

    UTM_ini_x = UTM_ini[0]
    UTM_ini_y = UTM_ini[1]
    UTM_ini_zone = UTM_ini[2]

    UTM_fin_x = UTM_fin[0]
    UTM_fin_y = UTM_fin[1]
    UTM_fin_zone = UTM_fin[2]

    [LAT_INI, LONG_INI] = utm.to_latlon(UTM_ini_x, UTM_ini_y, int(UTM_ini_zone[0:2]), str(UTM_ini_zone[3]))  # to get dd.dd from utm
    [LAT_FIN, LONG_FIN] = utm.to_latlon(UTM_fin_x, UTM_fin_y, int(UTM_fin_zone[0:2]), str(UTM_fin_zone[3]))  # to get dd.dd from utm

    point_i = (LAT_INI, LONG_INI)
    point_f = (LAT_FIN, LONG_FIN)

    distance = great_circle(point_i, point_f).kilometers # gives you a distance (in kms) between two coordinate in dd.dd

    return distance




def install_port(user_inputs, hydrodynamic_outputs, electrical_outputs, MF_outputs, ports, instal_order):
    """install_port function selects the home port used by all logistic phases
    during installation. This selection is based on a 2 step process: 
        1 - the port feasibility functions from all logistic phases are taken
        into account, and the unfeasible ports are erased from the panda dataframes.  
        2 - the closest port to the project site is choosen from the feasbile
        list of ports.

    Parameters
    ----------
    user_inputs : dict
     dictionnary containing all required inputs to WP5 coming from WP1/end-user
    electrical_outputs : dict
     dictionnary containing all required inputs to WP5 coming from WP3
    MF_outputs : DataFrame
     panda table containing all required inputs to WP5 coming from WP4
    port_data : DataFrame
     panda table containing the ports database     

    Returns
    -------
    port : dict
     dictionnary containing the results port_listof the port selection
    """    
    # initialisation
    port_data = ports
    port = {'Terminal load bearing [t/m^2]': 0,
            'Terminal area [m^2]': 0,
            'Port list satisfying the minimum requirements': 0,
            'Distance port-site [km]': 0,
            'Selected base port for installation': 0}

    max_total_load = 0
    max_total_area = 0

    instal_order_list = list(instal_order)
    for ind_order in range(len(instal_order_list)):

        # if instal_order_list[ind_order] == 1: # electrical
        #     # calculate loading and projected area of electrical elements
        #     max_electr_loading = 0
        #     max_electr_area = 0
        #
        #     # ?????!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #     for ind_electr in range(len(electrical_outputs['collection point'])):
        #         load_u = electrical_outputs['collection point']['dry mass [kg]'][ind_electr] / (electrical_outputs['collection point']['length [m]'][ind_electr] * electrical_outputs['collection point']['width [m]'][ind_electr])
        #         area_u = electrical_outputs['collection point']['length [m]'][ind_electr] * electrical_outputs['collection point']['width [m]'][ind_electr]
        #
        #         max_electr_loading = max(max_electr_loading,load_u)
        #         max_electr_area = max(max_electr_area,area_u)
        #
        #     for ind_electr in range(len(electrical_outputs['connectors'])):
        #         load_u = electrical_outputs['connectors']['dry mass [kg]'][ind_electr] / (electrical_outputs['connectors']['length [m]'][ind_electr] * electrical_outputs['connectors']['width [m]'][ind_electr])
        #         area_u = electrical_outputs['connectors']['length [m]'][ind_electr] * electrical_outputs['connectors']['width [m]'][ind_electr]
        #
        #         max_electr_loading = max(max_electr_loading,load_u)
        #         max_electr_area = max(max_electr_area,area_u)
        #
        #
        #
        #     max_total_load = max(max_total_load,max_electr_loading)
        #     max_total_area = max(max_total_area,max_electr_area)



        if instal_order_list[ind_order] == 2: # moorings
            # calculate loading and projected area of foundations/anchors
            max_moo_loading = 0
            max_moo_area = 0
            for ind_found in range(len(MF_outputs['foundation'])):
                load_u = MF_outputs['foundation']['dry mass [kg]'][ind_found] / (MF_outputs['foundation']['length [m]'][ind_found] * MF_outputs['foundation']['width [m]'][ind_found])
                area_u = MF_outputs['foundation']['length [m]'][ind_found] * MF_outputs['foundation']['width [m]'][ind_found]

                max_moo_loading = max(max_moo_loading,load_u)
                max_moo_area = max(max_moo_area,area_u)

            max_total_load = max(max_total_load,max_moo_loading)
            max_total_area = max(max_total_area,max_moo_area)



        if instal_order_list[ind_order] == 3: # devices
            # calculate loading and projected area of device or sub-device
            max_dev_loading = 0
            max_dev_area = 0
            for ind_dev in range(len(user_inputs['sub_device'])):
                load_u = user_inputs['sub_device']['dry mass [kg]'][ind_dev] / (user_inputs['sub_device']['length [m]'][ind_dev] * user_inputs['sub_device']['width [m]'][ind_dev])
                area_u = user_inputs['sub_device']['length [m]'][ind_dev] * user_inputs['sub_device']['width [m]'][ind_dev]

                max_dev_loading = max(max_dev_loading,load_u)
                max_dev_area = max(max_dev_area,area_u)

            max_total_load = max(max_total_load,max_dev_loading)
            max_total_area = max(max_total_area,max_dev_area)

            # check load out strategy
            loadout_methd = user_inputs['device']['load out [-]'].ix[0]
            if loadout_methd == 'float away':
                port_data_all = port_data
                port_data = port_data_all[ port_data_all['Type of terminal [Quay/Dry-dock]'] == 'Dry-dock']
                port_data = port_data.append( port_data_all[ port_data_all['Type of terminal [Quay/Dry-dock]'] == 'Quay, dry-dock'] )
                port_data = port_data.append( port_data_all[ port_data_all['Type of terminal [Quay/Dry-dock]'] == 'Yard, dry-dock'] )
                port_data = port_data.append( port_data_all[ port_data_all['Type of terminal [Quay/Dry-dock]'].isnull()] )


    # terminal load bearing minimum requirement
    port['Terminal load bearing [t/m^2]'] = max_total_load/1000  # t/m^2
    port_data = port_data[ port_data['Terminal load bearing [t/m^2]'] >= port['Terminal load bearing [t/m^2]'] ]

    port['Terminal area [m^2]'] = max_total_area
    port_data = port_data[ port_data['Terminal area [m^2]'] >= port['Terminal area [m^2]'] ]

    port['Port list satisfying the minimum requirements'] = port_data



    # Distance ports-site calculation to be implemented once the transit distance algorithm is available
    # by making use of the grid coordinate position of the site and the ports

    index_dev = 0  # USING POSITION OF FIRST DEVICE!!!
    site_coords_x = hydrodynamic_outputs['x coord [m]'][index_dev]
    site_coords_y = hydrodynamic_outputs['y coord [m]'][index_dev]
    site_coords_zone = hydrodynamic_outputs['zone [-]'][index_dev]
    site_coords = [site_coords_x, site_coords_y, site_coords_zone]
    dist_to_port_vec = []
    for ind_port, row in port_data.iterrows():
        port_coords_x = port_data['UTM x [m]'][ind_port]
        port_coords_y = port_data['UTM y [m]'][ind_port]
        port_coords_zone = port_data['UTM zone [-]'][ind_port]
        port_coords = [port_coords_x, port_coords_y, port_coords_zone]

        if math.isnan(port_coords_x):
            continue
        dist_to_port_i = distance(site_coords, port_coords)   # closest ports by geo distance!
        dist_to_port_vec.append( [dist_to_port_i, ind_port, port_data['Name [-]'][ind_port]] )
    closest_ports_all=sorted(dist_to_port_vec)
    # furthest_ports_all = closest_ports_all.reverse()

    # check if repeted port (by terminal)
    LEN_clst = len(closest_ports_all)-1
    ind_clst=0
    while ind_clst < LEN_clst:
        if closest_ports_all[ind_clst+1][2] == closest_ports_all[ind_clst][2]:   # if same name
            del closest_ports_all[ind_clst+1]
            LEN_clst = LEN_clst-1
        else:
            ind_clst = ind_clst+1


    # Identify the n=num_ports_consider closest ports:
    # num_ports_consider = len(dist_to_port_vec)  # consider all
    num_ports_consider = 5
    closest_ports_n = closest_ports_all[:min(num_ports_consider,len(closest_ports_all))]


    # Find the closest port using the transit_algorithm:
    dist_to_clost_port_vec=[]
    for ind_closest_port in range(len(closest_ports_n)):
        ind_port= closest_ports_n[ind_closest_port][1]
        port_coords_x = port_data['UTM x [m]'][ind_port]
        port_coords_y = port_data['UTM y [m]'][ind_port]
        port_coords_zone = port_data['UTM zone [-]'][ind_port]
        port_coords = [port_coords_x, port_coords_y, port_coords_zone]

        if math.isnan(port_coords_x):
            continue
        # dist_to_port_i = transit_algorithm(site_coords, port_coords)
        dist_to_port_i = distance(site_coords, port_coords)  # simplification just for testing
        dist_to_clost_port_vec.append(dist_to_port_i)
        min_dist_to_clst_port = min(dist_to_clost_port_vec)
        if min_dist_to_clst_port == dist_to_port_i:
            port_choice_index = ind_port

    # Nearest port selection to be modified by making use of port['Distance port-site'] will be implemented
    port['Selected base port for installation'] = port_data.ix[port_choice_index]
    port['Distance port-site [km]'] = min_dist_to_clst_port

    return port




