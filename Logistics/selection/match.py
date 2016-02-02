# -*- coding: utf-8 -*-
"""
@author: WavEC Offshore Renewables
email: boris.teillant@wavec.org; paulo@wavec.org

This module is the second and last part of the selection step in the WP5 methodology.
It contains functions to make the compatibility check between the characteristics
of port/vessel, port/equipment and vessel/equipment, returning only the feasible
and compatible solutions of vessels and equipments to perform the operations
sequence of the logistic phase.

BETA VERSION DETAILS: up to date, the functionalities explained previously have
not been implemented, this module should suffer major changes for the beta version
"""

from ..phases.install.classes import VE_solutions
import itertools
import numpy

def compatibility_ve(install, log_phase, port_chosen_data):
    """This function is currently limited to the selection of the first two
    feasible solutions for the installation logistic phase in analysis.

    Parameters
    ----------
    install : dict
     not used
    log_phase : class
     class of the logistic phase under consideration for assessment, contains
     data refered to the feasible vessel and equipment combinations specific of
     each operation sequence of the logistic phase

    Returns
    -------
    sol : dict
     A dict of panda dataframes with unique feasible solutions
    log_phase : class
     An updated version of the log_phase argument containing only the feasible
     equipments within each vessel and equipment combinations dataframes
    """

    sols_ve_indxs_combs_inseq = []

    # Go through different sequence options
    for seq in log_phase.op_ve:


        nr_sol = 0
        sols_ve_indxs_combs_incomb = []


        # Go through different possible combination
        for combi in range(len(log_phase.op_ve[seq].ve_combination)):


            # initialise solution variables
            ves_sol = {}
            ves_indexs = {}
            eq_sol = {}
            eq_indexs = {}


            #  Go through vessels
            nr_diff_ves = len(log_phase.op_ve[seq].ve_combination[combi]['vessel']) # nr_diff_ves in combination
            for ves_type in range(nr_diff_ves):

                ves = {}
                ves_index_vec = {}

                ves_quant = log_phase.op_ve[seq].ve_combination[combi]['vessel'][ves_type][0]  # Quantity of vessels in the solution
                ves_class = log_phase.op_ve[seq].ve_combination[combi]['vessel'][ves_type][1]  # Vessel class
                type_of_ves = log_phase.op_ve[seq].ve_combination[combi]['vessel'][ves_type][1].id

                ves_index_vec = ves_class.panda.index  # Get indexs that correspond to vessel class
                nr_feas_vess_i = len(ves_index_vec)  # Number of feasible vessels within vessel type

                for indx_vec in range(nr_feas_vess_i):
                  # ves[indx_vec] = ves_class.panda.ix[indx_vec]  # Get info of the feasible vessels
                  ves[indx_vec] = ves_class.panda.ix[ves_index_vec[indx_vec]]
                ves_sol[ves_type] = {'type': type_of_ves, 'quantity': ves_quant,
                                     'Series': ves, 'indexs': ves_index_vec}  # Store info of the vessels
                ves_indexs[ves_type] = list(ves_index_vec)  # Vector of indexs of feasible vessels per type



            #  Go through equips
            nr_diff_equi = len(log_phase.op_ve[seq].ve_combination[combi]['equipment'])
            for eq_type in range(nr_diff_equi):

                eq = {}
                eq_index_vec = {}

                eq_quant = log_phase.op_ve[seq].ve_combination[combi]['equipment'][eq_type][0]  # Quantity of vessels in the solution
                eq_class = log_phase.op_ve[seq].ve_combination[combi]['equipment'][eq_type][1]  # Equipment class
                type_of_eq = log_phase.op_ve[seq].ve_combination[combi]['equipment'][eq_type][1].id
                eq_reltd_ves = log_phase.op_ve[seq].ve_combination[combi]['equipment'][eq_type][2]

                eq_index_vec = eq_class.panda.index
                nr_feas_eq_i = len(eq_index_vec)

                for indx_vec in range(nr_feas_eq_i):
#                    eq[indx_vec] = eq_class.panda.ix[indx_vec]  # Get info of the feasible equipments
                    eq[indx_vec] = eq_class.panda.ix[eq_index_vec[indx_vec]]
                # eq_sol[eq_type] = {'type': type_of_eq, 'quantity': eq_quant,
                #                  'Series': eq, 'indexs': eq_index_vec, 'req_vessel': ves_sol[eq_reltd_ves]['type']}  # Store info of the equipments
                eq_sol[eq_type] = {'type': type_of_eq, 'quantity': eq_quant,
                                 'Series': eq, 'indexs': eq_index_vec, 'req_vessel': eq_reltd_ves}  # Store info of the equipments
                eq_indexs[eq_type] = list(eq_index_vec)  # Vector of indexs of feasible equipments per type




            # Build solutions
            # sols_ve_indxs = []

            sols_ves = []
            for ves_type in range(nr_diff_ves):  # Agregatte vessel type solutions

                VES = []
                for ves_intype in range(len(ves_sol[ves_type]['Series'])):

                    ves_type_name = ves_sol[ves_type]['type']
                    ves_type_quant = ves_sol[ves_type]['quantity']
                    ves_type_panda = ves_sol[ves_type]['Series'][ves_intype]

                    VES.append( [ves_type_name, ves_type_quant, ves_type_panda] )

                sols_ves.append(VES)

            sols_v_indxs_combs = list(itertools.product(*sols_ves))  # Combine vessel solutions

            sols_eq = []
            for eq_type in range(nr_diff_equi):  # Agregatte equipment type solutions

                EQS = []
                for eqs_intype in range(len(eq_sol[eq_type]['Series'])):

                    eq_type_name = eq_sol[eq_type]['type']
                    eq_type_quant = eq_sol[eq_type]['quantity']
                    eq_type_panda = eq_sol[eq_type]['Series'][eqs_intype]
                    eq_type_relation = eq_sol[eq_type]['req_vessel']


                    EQS.append( [eq_type_name, eq_type_quant, eq_type_panda, eq_type_relation] )

                sols_eq.append(EQS)

            sols_e_indxs_combs = list(itertools.product(*sols_eq))  # Combine vessel solutions

            sols_ve_indxs_sprt = (sols_v_indxs_combs, sols_e_indxs_combs)  # Agregatte vessel and equipment solutions
            sols_ve_indxs_comb = list(itertools.product(*sols_ve_indxs_sprt))  # Combine solutions

            sols_ve_indxs_combs_incomb.append(sols_ve_indxs_comb)  # Store solution per combination


        sols_ve_indxs_combs_inseq.append(sols_ve_indxs_combs_incomb)  # Store solution per sequence



    # Apply MATCHING

    port_pd = port_chosen_data

    # Port/Vessel
    req_m_pv = install['requirement'][2]
    match_rq_pv = dict.fromkeys(req_m_pv.keys())

    for typ_req in range(len(req_m_pv)):
        m_pv_key_req = req_m_pv.keys()[typ_req]

        for seq in range(len(log_phase.op_ve)):

            for combin in range(len(sols_ve_indxs_combs_inseq[0])):

                ve_combinations = sols_ve_indxs_combs_inseq[seq][combin]

                LEN_combi = len(ve_combinations)
                ind_ve_combi = -1
                while ind_ve_combi < LEN_combi-1:

                    ind_ve_combi = ind_ve_combi+1

                    ve_comb = ve_combinations[ind_ve_combi]
                    ve_comb_ves = ve_combinations[ind_ve_combi][0]
                    ve_comb_eqs = ve_combinations[ind_ve_combi][1]

                    for ind_ves_in_combi in range(len(ve_comb_ves)):
                        m_v_key_type = ve_comb_ves[ind_ves_in_combi][0]
                        ves_pd = ve_comb_ves[ind_ves_in_combi][2] # panda series data
                        if m_v_key_type == m_pv_key_req:

                            for req in range(len(req_m_pv[m_pv_key_req])):
                               m_ev_read = req_m_pv[m_pv_key_req][req]

                               aux_op = ves_pd[m_ev_read[0]]
                               for ind_rd in range(1,len(m_ev_read)-1,2):

                                   if m_ev_read[ind_rd] == 'plus':
                                       aux_op = aux_op + ves_pd[m_ev_read[ind_rd+1]]
                                   elif m_ev_read[ind_rd] == 'mul':
                                       aux_op = aux_op * ves_pd[m_ev_read[ind_rd+1]]
                                   elif m_ev_read[ind_rd] == 'div':
                                       aux_op = aux_op / ves_pd[m_ev_read[ind_rd+1]]
                                   elif m_ev_read[ind_rd] == 'sup':
                                       if port_pd[m_ev_read[ind_rd+1]] >= aux_op :
                                           continue
                                       else:
                                            del sols_ve_indxs_combs_inseq[seq][combin][ind_ve_combi]
                                            LEN_combi = LEN_combi-1
                                   elif m_ev_read[ind_rd] == 'equal':
                                       if port_pd[m_ev_read[ind_rd+1]] == aux_op :
                                          continue
                                       else:
                                            del sols_ve_indxs_combs_inseq[seq][combin][ind_ve_combi]
                                            LEN_combi = LEN_combi-1


    # # Port/Equipment
    # req_m_pe = install['requirement'][3]
    # match_rq_pe = dict.fromkeys(req_m_pe.keys())


    # Vessel/Equipment
    req_m_ev = install['requirement'][4]
    match_rq = dict.fromkeys(req_m_ev.keys())

    for typ_req in range(len(req_m_ev)):
        m_ev_key_req = req_m_ev.keys()[typ_req]

        for seq in range(len(log_phase.op_ve)):

            for combin in range(len(sols_ve_indxs_combs_inseq[0])):

                ve_combinations = sols_ve_indxs_combs_inseq[seq][combin]

                LEN_combi = len(ve_combinations)
                ind_ve_combi = -1
                while ind_ve_combi < LEN_combi-1:

                    ind_ve_combi = ind_ve_combi+1

                    ve_comb = ve_combinations[ind_ve_combi]
                    ve_comb_ves = ve_combinations[ind_ve_combi][0]
                    ve_comb_eqs = ve_combinations[ind_ve_combi][1]

                    for ind_eq_in_combi in range(len(ve_comb_eqs)):

                        m_e_key_type = ve_comb_eqs[ind_eq_in_combi][0]
                        eq_pd = ve_comb_eqs[ind_eq_in_combi][2] # panda series data
                        req_ves = ve_comb_eqs[ind_eq_in_combi][3]  # vessel (index) required to use equipment

                        m_v_key_type = ve_comb_ves[req_ves][0]
                        ves_pd = ve_comb_ves[req_ves][2] # panda series data

                        if m_e_key_type == m_ev_key_req:

                           for req in range(len(req_m_ev[m_ev_key_req])):
                               m_ev_read = req_m_ev[m_ev_key_req][req]

                               aux_op = eq_pd[m_ev_read[0]]
                               for ind_rd in range(1,len(m_ev_read)-1,2):

                                   if m_ev_read[ind_rd] == 'plus':
                                       aux_op = aux_op + eq_pd[m_ev_read[ind_rd+1]]
                                   elif m_ev_read[ind_rd] == 'mul':
                                       aux_op = aux_op * eq_pd[m_ev_read[ind_rd+1]]
                                   elif m_ev_read[ind_rd] == 'div':
                                       aux_op = aux_op / eq_pd[m_ev_read[ind_rd+1]]
                                   elif m_ev_read[ind_rd] == 'sup':
                                       if ves_pd[m_ev_read[ind_rd+1]] >= aux_op :
                                           continue
                                       else:
                                            del sols_ve_indxs_combs_inseq[seq][combin][ind_ve_combi]
                                            LEN_combi = LEN_combi-1
                                   elif m_ev_read[ind_rd] == 'equal':
                                       if ves_pd[m_ev_read[ind_rd+1]] == aux_op :
                                            continue
                                       else:
                                            del sols_ve_indxs_combs_inseq[seq][combin][ind_ve_combi]
                                            LEN_combi = LEN_combi-1

        # log_phase.op_ve[seq].sol = sols_ve_indxs_combs_inseq[seq]
        # sol = sols_ve_indxs_combs_inseq[seq]


    # Shape solution for performance:
    for seq in range(len(sols_ve_indxs_combs_inseq)):
        sol = {}
        sols_iter = 0
        for combi in range(len(sols_ve_indxs_combs_inseq[seq])):
            for sols in range(len(sols_ve_indxs_combs_inseq[seq][combi])):

                sol_i = sols_ve_indxs_combs_inseq[seq][combi][sols]
                vels = sol_i[0]
                equips = sol_i[1]

                # sol[sols_iter] = { 'port': port_chosen_data, str(sols): [list(vels), list(equips)] }
                # OR
                ve_sols=[]
                for ind_ves_sol in range(len(vels)):
                    sol[sols_iter] = { 'port': port_chosen_data}
                    ve_sol = list(vels[ind_ves_sol])
                    for ind_eq_sol in range(len(equips)):
                        ves_dpend = equips[ind_eq_sol][3]
                        if ves_dpend==ind_ves_sol:
                            ve_sol.append( list(equips[ind_eq_sol]) )
                    ve_sols.append(ve_sol)
                sol[sols_iter].update (  {'VEs': ve_sols} )

                sols_iter = sols_iter + 1

                # continue

        log_phase.op_ve[seq].sol = sol


    final_sol = log_phase.op_ve[seq].sol

    return final_sol, log_phase




def compatibility_ve_om(install, log_phase):
    """This function is currently limited to the selection of the first two
    feasible solutions for the O&M logistic phase in analisys.

    Parameters
    ----------
    install : dict
     not used
    log_phase : class
     class of the logistic phase under consideration for assessment, contains
     data refered to the feasible vessel and equipment combinations specific of
     each operation sequence of the logistic phase

    Returns
    -------
    sol : dict
     A dict of panda dataframes with unique feasible solutions
    log_phase : class
     An updated version of the log_phase argument containing only the feasible
     equipments within each vessel and equipment combinations dataframes
    """

    log_phase.op_ve[0].sol[0] = VE_solutions(0)
    log_phase.op_ve[0].sol[1] = VE_solutions(1)

    pd_ves0 = log_phase.op_ve[0].ve_combination[0]['vessel'][0][1].panda
    pd_ves0_index = pd_ves0.index

    pd_ves1 = log_phase.op_ve[0].ve_combination[1]['vessel'][0][1].panda
    pd_ves1_index = pd_ves1.index

    log_phase.op_ve[0].sol[0].sol_ves[0] = pd_ves0.ix[pd_ves0_index[0]]

    log_phase.op_ve[0].sol[1].sol_ves[0] = pd_ves1.ix[pd_ves1_index[1]]

    sol = {}
    sol[0] = log_phase.op_ve[0].sol[0]
    sol[1] = log_phase.op_ve[0].sol[1]

    return sol, log_phase
