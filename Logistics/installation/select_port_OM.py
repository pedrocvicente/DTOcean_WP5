# -*- coding: utf-8 -*-
"""
@author: WavEC Offshore Renewables

This module is responsible for the selection of ports for the O&M logistic activities.

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




def OM_port(hydrodynamic_outputs, OM_outputs, port_data):
    """OM_port function selects the port used by OM logistic phases
    required by the O&M module, depending if is inspection or actual maintenance.
    For the case of inspection the closest port is chosen and the ID in the input should be INS_PORT.
    For the case of the other logistic phases the selection is based on a 2 step process:
        1 - the port feasibility functions from all logistic phases are taken
        into account, and the unfeasible ports are erased from the panda dataframes.  
        2 - the closest port to the project site is choosen from the feasbile
        list of ports.
    In this case, the ID in the input should be OM_PORT.
    In both cases, the dimensions of the spare parts should correspond to the biggest dimensions possibly expected.
=======
    Parameters
    ----------
    OM_outputs : dict
     dictionnary containing all required inputs to WP5 coming from WP6/end-user stating the biggest of all the sp dimensions and weight for either
     inspection or actual maintenance
    port_data : DataFrame
     panda table containing the ports database     

    Returns
    -------
    port : dict
     dictionnary containing the results of the port selection
    """       
    # initialisation
    port = {'Terminal load bearing [t/m^2]': 0,
            'Terminal area [m^2]': 0,
            'Port list satisfying the minimum requirements': 0,
            'Distance port-site [km]': 0,
            'Selected base port for installation': 0}


    if OM_outputs['ID [-]'].ix[0] == 'INS_PORT':

        print 'Inspection only, will use the closest port'

    elif OM_outputs['ID [-]'].ix[0] == 'OM_PORT':

        print 'Will use the closest feasible port'

        # Calculate loading and projeted area of Spare Parts:
        # Input collection
        lenght_SP = OM_outputs['sp_length [m]'].ix[0]
        width_SP = OM_outputs['sp_width [m]'].ix[0]
        height_SP = OM_outputs['sp_height [m]'].ix[0]
        total_mass_SP = OM_outputs['sp_dry_mass [kg]'].ix[0]

        # Feasibility functions
        SP_area = float(lenght_SP) * float(width_SP)
        SP_loading = float(total_mass_SP) / float(SP_area)

        # terminal load bearing minimum requirement
        port_data = port_data[port_data['Terminal area [m^2]'] >= SP_area]
        port_data = port_data[port_data['Terminal load bearing [t/m^2]'] >= SP_loading/1000] # t/m^2

        port['Port list satisfying the minimum requirements'] = port_data

    else:
        print 'ERROR: unkwon ID for port calculation'


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
        if closest_ports_all[ind_clst+1][2] == closest_ports_all[ind_clst][2]:  # if same name
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


    port['Selected base port for installation'] = port_data.ix[port_choice_index]
    port['Distance port-site [km]'] = min_dist_to_clst_port


    return port