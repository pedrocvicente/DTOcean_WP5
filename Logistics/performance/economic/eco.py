# -*- coding: utf-8 -*-
"""
@author: WavEC Offshore Renewables
email: boris.teillant@wavec.org; paulo@wavec.org

This module is responsible for the cost step in the WP5 methodology. It contains
functions to calculate the cost of each solution based on the schedule, day rates
of vessels and equipments and port economic assessment.

BETA VERSION NOTES: The current version of this module only takes into account
the day rates of vessels to calculate the cost. This will be expanded to equipment
and port in the next version of the code.
"""
import numpy


def cost(install, log_phase):
    for seq in range(len(log_phase.op_ve)): # loop over the number of operation
    # sequencing options

        for ind_sol in range(len(log_phase.op_ve[seq].sol)): # loop over the
        # number of solutions, i.e feasible combinations of
        # port/vessel(s)/equipment(s)
#    for seq in range(len(log_phase.op_ve)):
#
#        for sol in range(len(log_phase.op_ve[seq].sol)):
#            sched = log_phase.op_ve[seq].sol[sol].schedule
            dur_sea_wait = sched['sea time'] + sched['waiting time']
            nb_ves_type = range(len(log_phase.op_ve[seq].sol[ind_sol]['VEs']))
            # qty_vt = log_phase.op_ve[0].sol[0]['VEs'][vt][1] 
            # loop over the nb of vessel types  
            ves_speed = []                                      
            for vt in nb_ves_type:
            op_cost_max = log_phase.op_ve[seq].sol[ind_sol].sol_ves[0]['Op max Day Rate']
            op_cost_min = log_phase.op_ve[seq].sol[ind_sol].sol_ves[0]['Op min Day Rate']
            vessel_cost = numpy.mean([op_cost_max, op_cost_min]) / 24  # [€/hour]
            log_phase.op_ve[seq].sol[sol].cost = {'vessel': vessel_cost * dur_sea_wait,
                                                  'equipment': 0,
                                                  'port cost': 0}

    sol = {}
    sol[0] = log_phase.op_ve[1].sol[0].cost
    sol[1] = log_phase.op_ve[1].sol[1].cost

    return sol, log_phase
