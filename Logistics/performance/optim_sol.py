# -*- coding: utf-8 -*-
"""
@author: WavEC Offshore Renewables
email: boris.teillant@wavec.org; paulo@wavec.org, pedro.vicente@wavec.org


"""
import numpy

def opt_sol(log_phase):

    # loop over the number of operation sequencing options
    sol_index_inseq_vec=[]
    for seq in range(len(log_phase.op_ve)):

        # loop over the number of solutions, i.e feasible combinations of port/vessel(s)/equipment(s)
        total_cost_vec=[]
        for ind_sol in range(len(log_phase.op_ve[seq].sol)):

            total_cost = log_phase.op_ve[seq].sol_cost[ind_sol]['total cost']
            total_cost_vec.append(total_cost)
            min_total_cost = min(total_cost_vec)
            if min_total_cost == total_cost:
                sol_index_inseq = [total_cost, ind_sol, seq]

        sol_index_inseq_vec.append(sol_index_inseq)

    min_sol_cost_sorted = sorted(sol_index_inseq_vec)

    seq_final_sol = min_sol_cost_sorted[0][2]
    sol_nr_final_sol = min_sol_cost_sorted[0][1]
    min_cost_final_sol = min_sol_cost_sorted[0][0]

    solution = log_phase.op_ve[seq_final_sol].sol[sol_nr_final_sol]

    sol = {'total cost': min_cost_final_sol,
           'vessel_equipment': solution}

    return sol