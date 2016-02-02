# -*- coding: utf-8 -*-
"""
@author: WavEC Offshore Renewables
email: boris.teillant@wavec.org; paulo@wavec.org

This module is responsible for the interphase relation between the different
logistic phases during installation. The inputs from the user and other DTOcean
packages build up unique projects which require specific installation sequences.
The functions in this module return the installation sequence required based on
some pre-defined cases (type of foundations, type of moorings, type of device,
type of electrical infranstrucutres).

BETA VERSION NOTES: the methodology was defined and implemented, should not
suffer major changes on the next version of the code. However the content (the
installation sequences) will be updated.
"""

import numpy as np
import pandas as pd
#from transit_algorithm import transit_algorithm
from Logistics.installation.select_port import distance
#from Logistics.ancillaries.dist import distance
from Logistics.ancillaries.find import indices
import math

def sched_dev(seq, ind_sol, install, log_phase, user_inputs,
              hydrodynamic_outputs, sched_sol):
    """sched_dev determines the duration of each individual logistic operations
    for the installtion of ocean energy devices following a common methodology:
        - the time value duration can be extracted from a direct average
        default value
        - the time value duration can result from a specialized function
        - the time value duration can be derived from other sources, mostly by
        making use of values available in the database or provided from the
        end-user
    Parameters
    ----------
    seq: integer
     index of the operation sequencing strategy under consideration
    ind_sol: integer
     index representing the feasible logistic solution under consideration
    log_phase: class
     class containing all data relevant to the characterization of the feasible
     logistic solutions
    user_inputs : dict
     dictionnary containing all required inputs to WP5 coming from WP1/end-user.
    ...

    Returns
    -------
    sched_sol : dict
     ...
    """
    
    """
    Initialise variables
    """
    # initialise list containing the time value durations and OLC
    op_id_prep = []
    op_dur_prep = []
    op_id_sea = []
    op_dur_sea = []
    op_olc_sea = []
    op_id_demob = []
    op_dur_demob = []
    op_id_jour = {0:[]}
    op_dur_jour = {0:[]}
    op_olc_jour = {0:[]}
    # number of devices to install    
    nb_dev = len(hydrodynamic_outputs['device [-]'])
    # number of vessel type in this feasible solution
    nb_ves_type = range(len(log_phase.op_ve[seq].sol[ind_sol]['VEs']))
    # list of the vessel(s) and equipment combination used for this feasible solution
    ve_combi = log_phase.op_ve[seq].sol[ind_sol]['VEs']
    # use the proper names of the pandas as sent to WP1
    site = user_inputs['site']
    device = user_inputs['device']
    layout = hydrodynamic_outputs
    
    
    """
    Time assessment for the installation of ocean energy devices
    """
    # check the transportation method
    # (1st branch in the decision making tree)
    if log_phase.op_ve[seq].description == 'On-deck transportation':
        # check the device assembly strategy
        # (2nd and FINAL branch in the decision making tree)
        assemb_method = device['assembly strategy [-]'].ix[0]
        if assemb_method == '([A,B,C,D])':
            # initialise the area and dry mass list
            elem_area = [0]*nb_dev
            elem_mass = [0]*nb_dev
            for dev in range(nb_dev): # loop over the number of devices
                # calculate the area and dry mass of all elements
                elem_area[dev] = device['length [m]'].ix[0]*user_inputs['device']['width [m]'].ix[0] # [m^2]
                elem_mass[dev] = device['dry mass [kg]'].ix[0]/1000 # [ton]
                
            nb_elem_port = nb_dev # initialise the number of elements to be transported that are initially at port
            nb_journey = 0 # initialise the number of vessel journeys
            nb_el_journey = [] # initialise the list of number of elements per journey
            while nb_elem_port > 0:
                # extract the panda series of the tranporting vessel
                # assumption: the first vessel is always the transporting vessel 
                sol_pd_series = log_phase.op_ve[seq].sol[ind_sol]['VEs'][0][2]
                # extract the deck area and cargo
                deck_area = sol_pd_series.ix['Deck space [m^2]']
                deck_cargo = sol_pd_series.ix['Max. cargo [t]']
                # determine the cumulative vector of element areas and dry masses
                elem_area_accum = list(np.cumsum(elem_area))
                elem_mass_accum = list(np.cumsum(elem_mass))
                # determine the maximum number of elements that can fit on-deck due to max deck area or max deck cargo limitations
                nb_dev_area = indices(elem_area_accum, lambda x: x>deck_area)
                if not nb_dev_area:
                    nb_dev_area = len(elem_area_accum)
                else:
                    nb_dev_area = min(nb_dev_area)
                nb_dev_mass = indices(elem_mass_accum, lambda x: x>deck_cargo)
                if not nb_dev_mass:
                    nb_dev_mass = len(elem_mass_accum)
                else:
                    nb_dev_mass = min(nb_dev_mass)
                nb_el_journey.append(min([nb_dev_area,nb_dev_mass]))
                # update the number of elements remaining at port and their areas/masses lists
                if nb_el_journey[nb_journey] == nb_elem_port:
                    nb_elem_port = 0
                elif nb_el_journey[nb_journey] == 0:
                    # error that means not a single element can fit!
                    print 'not a single device can fit in the deck!' 
                else:
                    nb_elem_port = nb_elem_port - nb_el_journey[nb_journey]
                    elem_area = elem_area[nb_el_journey[-1]:]
                    elem_mass = elem_mass[nb_el_journey[-1]:]
                # update the number of vessel journeys
                nb_journey = nb_journey + 1
                
                ind_el = 0
            for jour in range(nb_journey):
                if jour>0:
                    op_id_jour[jour] = []
                    op_dur_jour[jour] = []
                    op_olc_jour[jour] = []
                # number of operation sequence in the preparation phase
                nb_op_prep = len(log_phase.op_ve[seq].op_seq_prep)                       
                # determine the duration of the logistic phase preparation before departure of the vessel(s)
                for op_prep in range(nb_op_prep): # loop over the nb of onshore logistic operations
                    log_op_prep = log_phase.op_ve[seq].op_seq_prep[op_prep]
                    # create a panda series suitable for the discrimination 
                    # between type of methods for time assessment
                    time_method = pd.Series([log_op_prep.time_value,
                                             log_op_prep.time_function,
                                             log_op_prep.time_other])
                    # discriminate between the time assessment methods
                    if not pd.isnull(time_method[0]): # direct value
                        if log_op_prep.description == "LoadOut_Lift":
                            op_dur_prep.append(nb_el_journey[jour]*log_op_prep.time_value)
                            op_id_prep.append(log_op_prep.description)
                            op_id_jour[jour].append(log_op_prep.description)
                            op_dur_jour[jour].append(nb_el_journey[jour]*log_op_prep.time_value)
                        elif log_op_prep.description == "LoadOut_Skidded":
                            op_dur_prep.append(nb_el_journey[jour]*log_op_prep.time_value)
                            op_id_prep.append(log_op_prep.description)
                            op_id_jour[jour].append(log_op_prep.description)
                            op_dur_jour[jour].append(nb_el_journey[jour]*log_op_prep.time_value)
                        elif log_op_prep.description == "LoadOut_Float":
                            op_dur_prep.append(nb_el_journey[jour]*log_op_prep.time_value)
                            op_id_prep.append(log_op_prep.description)
                            op_id_jour[jour].append(log_op_prep.description)
                            op_dur_jour[jour].append(nb_el_journey[jour]*log_op_prep.time_value)
                        else:
                            print 'unknown default value time value duration for this logistic operation associated with the installation of devices'
                    elif not pd.isnull(time_method[1]): # function
                        # type of function
                         print 'no functions are currently handled for onshore operations' 
                            
                    elif not pd.isnull(time_method[2]):
                        if log_op_prep.time_other == "vesselsDB['Mob time [h]']" and jour == 0:
                            ves_mob_time = []
                            for vt in nb_ves_type:
                                ves_mob_time.append(ve_combi[vt][2].ix['Mob time [h]'])
                            ves_mob_time_long = max(ves_mob_time)
                            op_dur_prep.append(ves_mob_time_long)
                            op_id_prep.append(log_op_prep.description)
                            op_id_jour[jour].append(log_op_prep.description)
                            op_dur_jour[jour].append(ves_mob_time_long)
                        elif log_op_prep.time_other == "device['assembly duration [h]']":
                            assemb_time = device['assembly duration [h]'].ix[0]
                            op_dur_prep.append(nb_el_journey[jour]*assemb_time)
                            op_id_prep.append(log_op_prep.description)
                            op_id_jour[jour].append(log_op_prep.description)
                            op_dur_jour[jour].append(nb_el_journey[jour]*assemb_time)
                        else:
                            print 'unknown "other" method for time value duration assessment of this onshore operation'
#                only required if there are different element type which is not possible for devices
#                for dev_id, row in layout.iterrows(): # loop over the number of element type
#                    # number of operation sequence in the sea-work phase
#                    nb_op_sea = len(log_phase.op_ve[seq].op_seq_sea[dev_id])
                nb_op_sea = len(log_phase.op_ve[seq].op_seq_sea[0])
                # determine the duration of the logistic phase sea-work
                for op_sea in range(nb_op_sea): # loop over the nb of offshore logistic operations
                    log_op_sea = log_phase.op_ve[seq].op_seq_sea[0][op_sea]
                    # create a panda series suitable for the discrimination
                    # between type of methods for time assessment
                    time_method = pd.Series([log_op_sea.time_value,
                                             log_op_sea.time_function,
                                             log_op_sea.time_other])  
                    # discriminate between the time assessment methods
                    if not pd.isnull(time_method[0]): # default value
                        # type of logistic operation
                        if log_op_sea.description == "VesPos": # vessel positioning
                            # vessel type
                            if ve_combi[0][2].ix['Vessel type [-]'] == "JUP Barge" or ve_combi[0][2].ix['Vessel type [-]'] == "JUP Vessel":
#                                    for dev in nb_el_journey[jour]:# water depth at each device location...
#                                        water_depth
                                # UTM coordinates of the first device
                                UTM_dev_x = layout['x coord [m]'].ix[0] 
                                UTM_dev_y = layout['x coord [m]'].ix[0] 
#                                    UTM_dev_z = layout['zone [-]'].ix[0] 
                                site_dev = site[site['x coord [m]'] == UTM_dev_x and site['y coord [m]'] == UTM_dev_y]
                                water_depth_dev = site_dev['bathymetry [m]'] 
                                jacking_time = water_depth_dev/ve_combi[0][2].ix['JackUp speed down [m/min]']*60 # [8hour]
                                op_dur_sea.append(nb_el_journey[jour]*jacking_time)
                                olc_Hs = ve_combi[0][2].ix['OLC: Jacking maxHs [m]']
                                olc_Tp = ve_combi[0][2].ix['OLC: Jacking maxTp [s]']
                                olc_Ws = ve_combi[0][2].ix['OLC: Jacking maxWs [m/s]']
                                olc_Cs = ve_combi[0][2].ix['OLC: Jacking maxCs [m/s]']
                                olc_jack = [olc_Hs, olc_Tp, olc_Ws, olc_Cs]
                                op_olc_sea.append(olc_jack)
                                op_id_sea.append(log_op_sea.description)
                                op_id_jour[jour].append(log_op_sea.description)
                                op_dur_jour[jour].append(nb_el_journey[jour]*jacking_time)
                                op_olc_jour[jour].append(olc_jack)
                            else: 
                                op_dur_sea.append(nb_el_journey[jour]*log_op_sea.time_value)
                                olc_Hs = ve_combi[0][2].ix['OLC: Transit maxHs [m]']
                                olc_Tp = ve_combi[0][2].ix['OLC: Transit maxTp [s]']
                                olc_Ws = ve_combi[0][2].ix['OLC: Transit maxWs [m/s]']
                                olc_Cs = ve_combi[0][2].ix['OLC: Transit maxCs [m/s]']
                                olc_trans = [olc_Hs, olc_Tp, olc_Ws, olc_Cs]
                                op_olc_sea.append(olc_trans)
                                op_id_sea.append(log_op_sea.description)
                                op_id_jour[jour].append(log_op_sea.description)
                                op_dur_jour[jour].append(nb_el_journey[jour]*log_op_sea.time_value)
                                op_olc_jour[jour].append(olc_trans)
                    elif not pd.isnull(time_method[1]): # function
                        # type of function
                        if log_op_prep.time_function == "transit_algorithm":
#                            port_pd = log_phase.op_ve[seq].sol[ind_sol]['port']
#                            UTM_port = [port_pd.ix['UTM x [m]'],
#                                        port_pd.ix['UTM y [m]'],
#                                        port_pd.ix['UTM zone [-]']]
#                            site = user_inputs['site']
#                            UTM_site = [site['x coord [m]'].ix[0],
#                                        site['y coord [m]'].ix[0],
#                                        site['zone [-]'].ix[0]]
#                            port_2_site_dist = transit_algorithm(UTM_port, UTM_site)
                            port_2_site_dist = install['port']['Distance port-site [km]']
                            
                            # loop over the nb of vessel types  
                            ves_speed = []                                      
                            for vt in nb_ves_type:
                                ves_speed.append(log_phase.op_ve[seq].sol[ind_sol]['VEs'][vt][2].ix['Transit speed [m/s]'])
                                ves_type = ve_combi[vt][2].ix['Vessel type [-]']
                                if log_op_sea.olc == "vessel":
                                    if ves_type == "JUP Barge" or ves_type == "JUP Vessel":
                                        olc_Hs = ve_combi[0][2].ix['OLC: Jacking maxHs [m]']
                                        olc_Tp = ve_combi[0][2].ix['OLC: Jacking maxTp [s]']
                                        olc_Ws = ve_combi[0][2].ix['OLC: Jacking maxWs [m/s]']
                                        olc_Cs = ve_combi[0][2].ix['OLC: Jacking maxCs [m/s]']
                                        olc_jack = [olc_Hs, olc_Tp, olc_Ws, olc_Cs]
                                        op_olc_sea.append(olc_jack)
                                        op_olc_jour[jour].append(olc_jack)
                                    else:
                                        olc_Hs = ve_combi[0][2].ix['OLC: Transit maxHs [m]']
                                        olc_Tp = ve_combi[0][2].ix['OLC: Transit maxTp [s]']
                                        olc_Ws = ve_combi[0][2].ix['OLC: Transit maxWs [m/s]']
                                        olc_Cs = ve_combi[0][2].ix['OLC: Transit maxCs [m/s]']
                                        olc_trans = [olc_Hs, olc_Tp, olc_Ws, olc_Cs]
                                        op_olc_sea.append(olc_trans)
                                        op_olc_jour[jour].append(olc_trans)
                            ves_slow = 3.6*min(ves_speed) # [km/h]
                            port_2_site_time = port_2_site_dist/ves_slow
                            # append transit time from port to site
                            op_dur_sea.append(port_2_site_time)
                            op_id_sea.append(log_op_sea.description)
                            op_id_jour[jour].append(log_op_sea.description)
                            op_dur_jour[jour].append(port_2_site_time)

                        elif log_op_prep.time_function == "distance":
                            dist_tot = 0
                            dist_el = []
                            for el in range(nb_el_journey[jour]):
                                UTM_el_i = [layout['x coord [m]'].ix[ind_el+el],
                                            layout['y coord [m]'].ix[ind_el+el],
                                            layout['zone [-]'].ix[ ind_el+el]]
                                UTM_el_f = [layout['x coord [m]'].ix[ind_el+el+1],
                                            layout['y coord [m]'].ix[ind_el+el+1],
                                            layout['zone [-]'].ix[ind_el+el+1]]
                                dist_el.append(distance(UTM_el_i,UTM_el_f))
                                dist_tot = dist_tot + dist_el[el]
                            ves_speed = []
                            for vt in nb_ves_type:
                                ves_type = ve_combi[vt][2].ix['Vessel type [-]']
                                ves_speed.append(ve_combi[vt][2].ix['Transit speed [m/s]'])
                                if log_op_sea.olc == "vessel":
                                    if ves_type == "JUP Barge" or ves_type == "JUP Vessel":
                                        olc_Hs = ve_combi[0][2].ix['OLC: Jacking maxHs [m]']
                                        olc_Tp = ve_combi[0][2].ix['OLC: Jacking maxTp [s]']
                                        olc_Ws = ve_combi[0][2].ix['OLC: Jacking maxWs [m/s]']
                                        olc_Cs = ve_combi[0][2].ix['OLC: Jacking maxCs [m/s]']
                                        olc_jack = [olc_Hs, olc_Tp, olc_Ws, olc_Cs]
                                        op_olc_sea.append(olc_jack)
                                        op_olc_jour[jour].append(olc_jack)
                                    else:
                                        olc_Hs = ve_combi[0][2].ix['OLC: Transit maxHs [m]']
                                        olc_Tp = ve_combi[0][2].ix['OLC: Transit maxTp [s]']
                                        olc_Ws = ve_combi[0][2].ix['OLC: Transit maxWs [m/s]']
                                        olc_Cs = ve_combi[0][2].ix['OLC: Transit maxCs [m/s]']
                                        olc_trans = [olc_Hs, olc_Tp, olc_Ws, olc_Cs]
                                        op_olc_sea.append(olc_trans)
                                        op_olc_jour[jour].append(olc_trans)
                            ves_slow = 3.6*min(ves_speed) # [km/h]
                            site_2_site_time = dist_tot/ves_slow
                            # append transit time from site to site
                            op_dur_sea.append(site_2_site_time)
                            op_id_sea.append(log_op_sea.description)
                            op_id_jour[jour].append(log_op_sea.description)
                            op_dur_jour[jour].append(site_2_site_time)
                           

                    elif not pd.isnull(time_method[2]):
                        if log_op_sea.time_other == "device['connect duration [h]']":
                            dev_connect_time = user_inputs['device']['connect duration [h]']
                            op_id_sea.append(log_op_sea.description)
                            op_dur_sea.append(dev_connect_time) 
                            olc_Hs = device['max Hs [m]']
                            olc_Tp = device['max Tp [s]']
                            olc_Ws = device['max wind speed [m/s]']
                            olc_Cs = device['max current speed [m/s]']
                            olc_dev_connect = [olc_Hs, olc_Tp, olc_Ws, olc_Cs]
                            op_olc_sea.append(olc_dev_connect)
                            op_id_jour[jour].append(log_op_sea.description)
                            op_dur_jour[jour].append(dev_connect_time)
                            op_olc_jour[jour].append(olc_dev_connect)
                        elif log_op_sea.time_other == "device['disconnect duration [h]']":
                            dev_disconnect_time = user_inputs['device']['connect duration [h]']
                            op_id_sea.append(log_op_sea.description)
                            op_dur_sea.append(dev_disconnect_time)
                            olc_Hs = device['max Hs [m]']
                            olc_Tp = device['max Tp [s]']
                            olc_Ws = device['max wind speed [m/s]']
                            olc_Cs = device['max current speed [m/s]']
                            olc_dev_disconnect = [olc_Hs, olc_Tp, olc_Ws, olc_Cs]
                            op_olc_sea.append(olc_dev_disconnect)
                            op_id_jour[jour].append(log_op_sea.description)
                            op_dur_jour[jour].append(dev_disconnect_time)
                            op_olc_jour[jour].append(olc_dev_disconnect)
                    ind_el = ind_el + nb_el_journey[jour]
                
            # add demobilisation time to finalise the logistic phase 
            log_op_demob = log_phase.op_ve[seq].op_seq_demob[0]
            # create a panda series suitable for the discrimination
            # between type of methods for time assessment
            time_method = pd.Series([log_op_demob.time_value,
                                     log_op_demob.time_function,
                                     log_op_demob.time_other])  
            if not pd.isnull(time_method[2]):
                ves_demob_time = []
                for vt in nb_ves_type:
                    ves_demob_time.append(ve_combi[vt][2].ix['Mob time [h]'])
                ves_demob_time_long = max(ves_demob_time)
                op_dur_demob.append(ves_demob_time_long) 
                op_id_demob.append(log_op_demob.description)
                op_id_jour[nb_journey-1].append(log_op_demob.description)
                op_dur_jour[nb_journey-1].append(ves_demob_time_long)
            else:
                print 'only demob is expected at the end of a logistic phase'            
#                    elif assemb_method == '([A,B,C],D)':
                
                
    # pass outputs to sched_sol
    sched_sol['detail'] = {'journey': nb_el_journey,
                           'prep': [op_id_prep, op_dur_prep],
                           'sea': [op_id_sea, op_dur_sea, op_olc_sea],
                           'demob': [op_id_demob, op_dur_demob]}
    # remove NAN from the time duration values retrieved
    op_dur_prep_clean = [x for x in op_dur_prep if (math.isnan(x) == False)]
    if not op_dur_prep_clean:
        op_dur_prep_clean = 0
    op_dur_sea_clean = [x for x in op_dur_sea if (math.isnan(x) == False)]
    if not op_dur_sea_clean:
        op_dur_sea_clean = 0
    op_dur_demob_clean = [x for x in op_dur_demob if (math.isnan(x) == False)]
    if not op_dur_demob_clean:
        op_dur_demob_clean = 0
    sched_sol['olc'] = min(op_olc_sea)  
    sched_sol['preparation'] = sum(op_dur_prep_clean)
    sched_sol['sea time'] = sum(op_dur_sea_clean)
    sched_sol['log_op_dur_all'] = sum(op_dur_prep_clean) + sum(op_dur_sea_clean) + op_dur_demob_clean

    return sched_sol

# see = selectSeq(end_user_inputs, WP3_outputs, WP4_outputs)
