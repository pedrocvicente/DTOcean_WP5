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
import random

def cost(install, log_phase):

    sol = {}
    sched = {}
    sched ['sea time'] =  random.choice([10, 25, 32, 48, 56])
    sched ['waiting time'] = random.choice([2, 6, 9, 15, 22])

    # loop over the number of operation sequencing options
    for seq in range(len(log_phase.op_ve)):

        # loop over the number of solutions, i.e feasible combinations of port/vessel(s)/equipment(s)
        for ind_sol in range(len(log_phase.op_ve[seq].sol)):

            # sched = log_phase.op_ve[seq].sol[sol].schedule  # CHANGE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

            dur_sea_wait = sched['sea time'] + sched['waiting time']
            nb_ves_type = len(log_phase.op_ve[seq].sol[ind_sol]['VEs'])

            # loop over the nb of vessel types
            vessel_cost = []
            equip_cost_ves = []
            for vt in range(nb_ves_type):

                qty_vt = log_phase.op_ve[0].sol[ind_sol]['VEs'][vt][1]
                ves_data = log_phase.op_ve[seq].sol[ind_sol]['VEs'][vt][2]

                op_cost_max = ves_data['Op max Day Rate']
                op_cost_min = ves_data['Op min Day Rate']
                vessel_cost_h = numpy.mean([op_cost_max, op_cost_min]) / 24  # [€/hour]
                vessel_cost.append ( qty_vt * (vessel_cost_h * dur_sea_wait) )

                # check if vessel carries any equipment
                nr_equip = len(log_phase.op_ve[0].sol[ind_sol]['VEs'][vt]) - 3  #  first 3 elements are type, quant and series

                equip_cost_eq_i = []
                for eqp in range(nr_equip):
                    eq_type = log_phase.op_ve[0].sol[ind_sol]['VEs'][vt][3+eqp][0]
                    qty_eqp = log_phase.op_ve[0].sol[ind_sol]['VEs'][vt][3+eqp][1]
                    eq_data = log_phase.op_ve[0].sol[ind_sol]['VEs'][vt][3+eqp][2]

                    if eq_type == 'rov':
                        eq_cost = eq_data['ROV day rate [EURO/day]'] + \
                                  eq_data['AE supervisor [-]']*eq_data['Supervisor rate [EURO/12h]']*2 + \
                                  eq_data['AE technician [-]']*eq_data['Technician rate [EURO/12h]']*2  # [€/day]
                    elif eq_type == 'divers':
                        eq_cost = eq_data['Total day rate [EURO/day]'] # [€/day]
                    elif eq_type == 'cable_burial':
                        eq_cost = eq_data['Burial tool day rate [EURO/day]'] + eq_data['Personnel day rate [EURO/12h]']*2 # [€/day]
                    elif eq_type == 'excavating':
                        eq_cost = eq_data['Excavator day rate [EURO/day]'] + eq_data['Personnel day rate [EURO/12h]']*2 # [€/day]
                    elif eq_type == 'mattress':
                        eq_cost = eq_data['Cost per unit [EURO]']
                    elif eq_type == 'rock_filter_bags':
                        eq_cost = eq_data['Cost per unit [EURO]']
                    elif eq_type == 'split_pipe':
                        eq_cost = eq_data['Cost per unit [EURO]']
                    elif eq_type == 'hammer':
                        eq_cost = eq_data['Hammer day rate [EURO/day]'] + eq_data['Personnel day rate [EURO/12h]']*2 # [€/day]
                    elif eq_type == 'drilling_rigs':
                        eq_cost = eq_data['Drill rig day rate [EURO/day]'] + eq_data['Personnel day rate [EURO/day]'] # [€/day]
                    elif eq_type == 'vibro_driver': # ?!?!
                        eq_cost = eq_data['Vibro diver day rate [EURO/day]'] + eq_data['Personnel day rate [EURO/day]'] # [€/day]

                    if eq_type == 'mattress' or eq_type == 'rock_filter_bags' or eq_type == 'split_pipe':
                        eq_cost_h = eq_cost / 24  # [€/hour]
                    else:
                        eq_cost_h = eq_cost  # [€] ?????????
                    equip_cost_eq_i.append ( qty_eqp * (eq_cost_h * dur_sea_wait) )
                equip_cost_ves.append ( sum(equip_cost_eq_i) )

            equip_total_cost = sum(equip_cost_ves)
            vessel_total_cost = sum(vessel_cost)
            port_total_cost = 0  # to be improved !!!!!!!! port_total_cost = install_port['Selected base port for installation']['Tonnage charges [euro/GT]']

            log_phase.op_ve[seq].sol_cost[ind_sol] = {'vessel cost': vessel_total_cost, 'equipment cost': equip_total_cost, 'port cost': port_total_cost}
            sol[seq] = log_phase.op_ve[seq].sol_cost

    return sol, log_phase
