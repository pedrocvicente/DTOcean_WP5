# -*- coding: utf-8 -*-
"""
@author: WavEC Offshore Renewables
email: boris.teillant@wavec.org; paulo@wavec.org

This module is responsible for the schedule step in the WP5 methodology. It
contains functions to calculate the time required to perform certain operations
such as transit to site, always taking into account the weather windows through
the operation limit conditions defined for each operation.

BETA VERSION NOTES: The module will suffer major changes in the next version of
the code.
"""

import numpy
#import utm
#from geopy.distance import great_circle
from transit_algorithm import transit_algorithm
#import itertools
from Logistics.installation.select_port import distance
from schedule_dev import sched_dev
import math

def indices(a, func):
    """
    indices returns the indices of a list "a" that satisfy the
    conditional function "func"
    """
    return [i for (i, val) in enumerate(a) if func(val)]


def differences(a):
    """
    differences returns a vector containing the difference
    """
    return [j - i for i, j in zip(a[:-1], a[1:])]


def weatherWindow(user_inputs, olc):
    """
    this functions returns the starting times and the durations of all weather
    windows found in the met-ocean data for the given operational limit
    conditions (olc)
    """
    # Initialisation
    met_ocean = user_inputs['metocean']
    ww = {'start': 0,
          'duration': 0}
    # Operational limit conditions (consdiered static over the entire duration of the marine operation fro the moment)
    timeStep = met_ocean['hour [-]'].ix[2] - met_ocean['hour [-]'].ix[1]
    # resourceDataPointNb = len(met_ocean.waveHs)
    # Build the binary weather windows: 1=authorized access, 0=denied access
    Hs_bin = map(float, met_ocean['Hs [m]'] > olc['maxHs'])
    Ws_bin = map(float, met_ocean['Ws [m/s]'] > olc['maxWs'])

    WW_bin = Hs_bin or Ws_bin

    # Determine the durations and the starting times of the weather windows
    # Look for all indexes permitting access
    WW_authorized = indices(WW_bin, lambda x: x == 1)
    if not WW_authorized:
        print'Not a single permitting weather window was found with the criteria specified for one vessel with these met-ocean data!'
    else:
        # Return the number of consecutive time steps where marine operations are not permitted ("Gap") or 0 otherwise
        WW_authorized = numpy.array(WW_authorized)
        index = numpy.array(range(len(WW_authorized)))
        WW_authorized_0 = WW_authorized - index
        WW_Gap1 = differences(WW_authorized_0)
        # Find position of consecutive permitting weather window among Gap
        WW_posConsecutiveGap1 = indices([1] + WW_Gap1, lambda x: x == 1)
        # Give the number of consecutive permitting weather conditions without
        # interuption, i.e the durations of all weather windows
        # except the last one!
        WW_findConsecutive1 = differences(WW_posConsecutiveGap1)
        WW_findConsecutive1_2 = [1] + WW_findConsecutive1
        WW_findConsecutive1_2 = numpy.cumsum(WW_findConsecutive1_2)
        # Locate the starting times of each weather windows
        WW_posConsecutive1 = WW_authorized[WW_findConsecutive1_2]
        # assign starting times and durations of all weather windows to output
        # tt = numpy.multiply(timeStep,range(WW_posConsecutive1))
        # WW_posConsecutive1 * timeStep
        ww['start'] = WW_posConsecutive1 * timeStep
        # [x*timeStep for x in WW_posConsecutive1]
        duration = numpy.array(WW_findConsecutive1)
        ww['duration'] = duration * timeStep
    return ww


def sched(x, install, log_phase, log_phase_id,
          user_inputs, hydrodynamic_outputs, electrical_outputs, MF_outputs):

    for seq in range(len(log_phase.op_ve)): # loop over the number of operation
    # sequencing options

        for ind_sol in range(len(log_phase.op_ve[seq].sol)): # loop over the
        # number of solutions, i.e feasible combinations of
        # port/vessel(s)/equipment(s)
        
            sched_sol = {'olc': [],
                         'log_op_dur_all': [],
                         'preparation': [],
                         'sea time': [],
                         'weather windows': [],
                         'waiting time': [],
                         'detail': {}
                         }

            # check the nature of the logistic phase
            if log_phase_id == 'Devices':
                sched_sol = sched_dev(seq, ind_sol, install, log_phase,
                                      user_inputs, hydrodynamic_outputs,
                                      sched_sol)
            elif log_phase_id == 'E_eport':
                sched_sol = sched_e_export(seq, ind_sol, install, log_phase,
                                      user_inputs, hydrodynamic_outputs,
                                      sched_sol)
            elif log_phase_id == 'E_array':
                sched_sol = sched_e_array(seq, ind_sol, install, log_phase,
                                      user_inputs, hydrodynamic_outputs,
                                      sched_sol)
            elif log_phase_id == 'E_dynamic':
                sched_sol = sched_e_dynamic(seq, ind_sol, install, log_phase,
                                      user_inputs, hydrodynamic_outputs,
                                      sched_sol)
            elif log_phase_id == 'E_cp_seabed':
                sched_sol = sched_e_cp_seabed(seq, ind_sol, install, log_phase,
                                      user_inputs, hydrodynamic_outputs,
                                      sched_sol)
            elif log_phase_id == 'Driven':
                sched_sol = sched_driven(seq, ind_sol, install, log_phase,
                                      user_inputs, hydrodynamic_outputs,
                                      sched_sol)
            elif log_phase_id == 'Gravity':
                sched_sol = sched_gravity(seq, ind_sol, install, log_phase,
                                      user_inputs, hydrodynamic_outputs,
                                      sched_sol)
            elif log_phase_id == 'M_drag':
                sched_sol = sched_m_drag(seq, ind_sol, install, log_phase,
                                      user_inputs, hydrodynamic_outputs,
                                      sched_sol)
            elif log_phase_id == 'M_direct':
                sched_sol = sched_m_direct(seq, ind_sol, install, log_phase,
                                      user_inputs, hydrodynamic_outputs,
                                      sched_sol)
            elif log_phase_id == 'M_suction':
                sched_sol = sched_m_suction(seq, ind_sol, install, log_phase,
                                      user_inputs, hydrodynamic_outputs,
                                      sched_sol)
            elif log_phase_id == 'M_pile':
                sched_sol = sched_m_pile(seq, ind_sol, install, log_phase,
                                      user_inputs, hydrodynamic_outputs,
                                      sched_sol)
            else:
                print 'unknown logistic phase ID'
            
            olc = {'maxHs':[],
                   'maxTp':[],
                   'maxWs':[],
                   'maxCs':[]}
            # change panda series into float values
            sched_sol['olc'][0] = float(sched_sol['olc'][0])
            sched_sol['olc'][1] = float(sched_sol['olc'][1])
            sched_sol['olc'][2] = float(sched_sol['olc'][2])
            sched_sol['olc'][3] = float(sched_sol['olc'][3])
            sched_sol['sea time'] = float(sched_sol['sea time'])
            if sched_sol['olc'][0]>0 and not math.isnan(sched_sol['olc'][0]):
                olc['maxHs'] = sched_sol['olc'][0]
            if sched_sol['olc'][1]>0 and not math.isnan(sched_sol['olc'][1]):
                olc['maxTp'] = sched_sol['olc'][1]
            if sched_sol['olc'][2]>0 and not math.isnan(sched_sol['olc'][2]):
                olc['maxWs'] = sched_sol['olc'][2]
            if sched_sol['olc'][3]>0 and not math.isnan(sched_sol['olc'][3]):
                olc['maxCs'] = sched_sol['olc'][3]


            weather_wind = weatherWindow(user_inputs, olc)
            
            if x == 0:  # find layer of installation plan
                start_proj = user_inputs['device']['Project start date [-]'].ix[0]
                starting_time = start_proj + sched_sol['preparation']
            elif x > 0:  # to be implemented (dummy not functional at the moment)
                last_end_time = max(install['schedule'][end_time])
                starting_time = last_end_time + sched_sol['preparation']

            index_ww_start = indices(weather_wind['start'], lambda x: x > starting_time)
            # and weatherWind['duration'] >= duration_total)/
            index_ww_dur = indices(weather_wind['duration'], lambda x: x >= sched_sol['sea time'])
            index_ww = index_ww_start or index_ww_dur
            waiting_time = weather_wind['start'][index_ww[0]] - starting_time
            sched_sol['waiting time'] = waiting_time
            sched_sol['weather windows'] = weather_wind
            log_phase.op_ve[seq].sol[ind_sol]['schedule'] = sched_sol

    sol = {}
#    sol[0] = log_phase.op_ve[1].sol[0].schedule
#    sol[1] = log_phase.op_ve[1].sol[1].schedule

    return sol, log_phase
