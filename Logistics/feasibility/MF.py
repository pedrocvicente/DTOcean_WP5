# -*- coding: utf-8 -*-
"""
@author: WavEC Offshore Renewables
email: boris.teillant@wavec.org; paulo@wavec.org

This module is part of the characterization step in the WP5 methodology. It 
contains feasibility functions to compute the minimum logistic requirements to 
carry out the different logistic phases. This particular modules includes the
function related to the installation of moorings and foundations.

BETA VERSION NOTES: The current version is limited to an installation strategy
consisting of installation of 1 set of foundations at the time. This will be 
futher developed in the beta version due to October.
"""

def MF_feas(log_phase, log_phase_id, hydrodynamic_outputs, MF_outputs):
    """ wp4_feas is a function which determines the logistic requirement 
    associated with one logistic phase dealing with the installation of 
    moorings and foundation systems
    
    Parameters
    ----------
    log_phase : Class
     Class of the logistic phase under consideration for assessment
    log_phase_id : str
     string describing the ID of the logistic phase under consideration
    hydrodynamic_outputs : dict
     dictionnary containing all required inputs to WP5 coming from WP2
    MF_outputs : DataFrame
     Panda table containing all required inputs to WP5 coming from WP4
    
    Returns
    -------
    feas_e : dict
     dictionnary containing all logistic requirements associated with every
     equipment type of the logistic phase under consideration
    feas_v : dict
     dictionnary containing all logistic requirements associated with every
     vessel type of the logistic phase under consideration
    """

    diam_u = []  # list of max diameter per unit
    load_u = []  # list of loading due to the set of foundation(s) per unit
    cargo_u = []  # list of cargo due to the set of foundation(s) per unit
    area_u = []  # list of loading occupied by the set of foundation(s) per unit
    depth_u = []  # list of water depth by the set of foundation(s) per unit
    moo_line_len_u = []  # list of mooring line length by the set of foundation(s) per unit
    moo_mass_u = []  # list of mooring line mass by the set of foundation(s) per unit

    find_fd_num = 0
    fundt_num = 0
    for dev in range(len(hydrodynamic_outputs['device [-]'])):

        dev_string = str( hydrodynamic_outputs['device [-]'].ix[dev] )
        num_found = len(MF_outputs['foundation'])
        count_fd_num = 0
        while find_fd_num < num_found:

            if MF_outputs['foundation']['devices [-]'][find_fd_num]== dev_string:
                count_fd_num = count_fd_num + 1
                find_fd_num = find_fd_num + 1
            else:
                break
            found_per_dev = count_fd_num

        diam_u_f = []  # list of diameter of each foundation per unit
        load_u_f = []  # list of loading due to each foundation per unit
        cargo_u_f = []  # list of loading due to each foundation per unit
        area_u_f = []  # list of area occupied by each foundation per unit
        depth_u_f = []  # list of area occupied by each foundation per unit
        moo_line_len_u_f = []  # list of area occupied by each foundation per unit
        moo_mass_u_f = []  # list of area occupied by each foundation per unit
        for ind_found in range(fundt_num, fundt_num+found_per_dev):
            load_u_f[len(load_u_f):] = [MF_outputs['foundation']['dry mass [kg]'].ix[ind_found] / (MF_outputs['foundation']['length [m]'].ix[ind_found] * MF_outputs['foundation']['width [m]'].ix[ind_found])]
            cargo_u_f[len(load_u_f):] = [MF_outputs['foundation']['dry mass [kg]'].ix[ind_found]]
            area_u_f[len(area_u_f):] = [MF_outputs['foundation']['length [m]'].ix[ind_found] * MF_outputs['foundation']['width [m]'].ix[ind_found]]
            diam_u_f[len(diam_u_f):] = [MF_outputs['foundation']['length [m]'].ix[ind_found]]
            depth_u_f[len(diam_u_f):] = [MF_outputs['foundation']['installation depth [m]'].ix[ind_found]]
            moo_line_len_u_f[len(diam_u_f):] = [MF_outputs['line']['length [m]'].ix[ind_found]]
            moo_mass_u_f[len(diam_u_f):] = [MF_outputs['line']['dry mass [kg]'].ix[ind_found]] + [MF_outputs['foundation']['dry mass [kg]'].ix[ind_found]]

        fundt_num = found_per_dev

        load_u[len(load_u):] = [max(load_u_f)]
        cargo_u[len(cargo_u):] = [sum(cargo_u_f)]
        area_u[len(area_u):] = [sum(area_u_f)]
        diam_u[len(diam_u):] = [max(diam_u_f)]
        depth_u[len(depth_u):] = [max(depth_u_f)]
        moo_line_len_u[len(moo_line_len_u):] = [max(moo_line_len_u_f)]
        moo_mass_u[len(moo_mass_u):] = [max(moo_mass_u_f)]

    deck_loading = max(load_u)/1000  # t/m^2!
    deck_cargo = max(cargo_u)/1000  # t!
    deck_area = max(area_u)  # m^2
    sleeve_diam = max(diam_u)  # m
    max_depth = max(depth_u)  # m
    max_linelength = max(moo_line_len_u)  # m
    max_moomass = max(moo_mass_u)/1000  # t!


    # ***********************************************************************************************************************
    if log_phase_id == 'M_Drag' or log_phase_id == 'M_Direct' or log_phase_id == 'M_Suction': # ??!?!?!?!?!??!?!?!?!?!?!?!?!?!?!?

        # Equipment and vessel feasiblity

        feas_e = {'rov': [['Depth rating [m]', 'sup', max_depth]]}

        feas_v = {'Crane Barge': [['Deck loading [t/m^2]', 'sup', deck_loading],
                           ['Max. cargo [t]', 'sup', deck_cargo],
                           ['AH winch rated pull [t]', 'sup', max_moomass],
                           ['AH drum capacity [m]', 'sup', max_linelength],
                           ['Crane capacity [t]', 'sup', deck_cargo],
                           ['AH drum capacity [m]', 'sup', max_depth],
                           ['Deck space [m^2]', 'sup', deck_area],
                           # ['ROV inspection [yes/no]', 'equal', 'yes'],
                           # ['ROV workclass [yes/no]', 'equal', 'yes']
                                  ],
                  'Crane Vessel': [['Deck loading [t/m^2]', 'sup', deck_loading],
                           ['Max. cargo [t]', 'sup', deck_cargo],
                           ['AH winch rated pull [t]', 'sup', max_moomass],
                           ['AH drum capacity [m]', 'sup', max_linelength],
                           ['Crane capacity [t]', 'sup', deck_cargo],
                           ['AH drum capacity [m]', 'sup', max_depth],
                           ['Deck space [m^2]', 'sup', deck_area],
                           # ['ROV inspection [yes/no]', 'equal', 'yes'],
                           # ['ROV workclass [yes/no]', 'equal', 'yes']
                                   ],
                  'Multicat': [['Deck loading [t/m^2]', 'sup', deck_loading],
                           ['Max. cargo [t]', 'sup', deck_cargo],
                           ['AH winch rated pull [t]', 'sup', max_moomass],
                           ['AH drum capacity [m]', 'sup', max_linelength],
                           ['Crane capacity [t]', 'sup', deck_cargo],
                           ['AH drum capacity [m]', 'sup', max_depth],
                           ['Deck space [m^2]', 'sup', deck_area],
                           # ['ROV inspection [yes/no]', 'equal', 'yes'],
                           # ['ROV workclass [yes/no]', 'equal', 'yes']
                               ],
                  'JUP Barge': [['Deck loading [t/m^2]', 'sup', deck_loading],
                           ['Max. cargo [t]', 'sup', deck_cargo],
                           ['AH winch rated pull [t]', 'sup', max_moomass],
                           ['AH drum capacity [m]', 'sup', max_linelength],
                           ['Deck space [m^2]', 'sup', deck_area],
                           # ['ROV inspection [yes/no]', 'equal', 'yes'],
                           # ['ROV workclass [yes/no]', 'equal', 'yes']
                                ],
                  'JUP Vessel': [['Deck loading [t/m^2]', 'sup', deck_loading],
                           ['Max. cargo [t]', 'sup', deck_cargo],
                           ['AH winch rated pull [t]', 'sup', max_moomass],
                           ['AH drum capacity [m]', 'sup', max_linelength],
                           ['Deck space [m^2]', 'sup', deck_area],
                           # ['ROV inspection [yes/no]', 'equal', 'yes'],
                           # ['ROV workclass [yes/no]', 'equal', 'yes']
                                 ],
                  'AHTS': [['Deck loading [t/m^2]', 'sup', deck_loading],
                           ['Max. cargo [t]', 'sup', deck_cargo],
                           ['AH winch rated pull [t]', 'sup', max_moomass],
                           ['AH drum capacity [m]', 'sup', max_linelength],
                           ['Deck space [m^2]', 'sup', deck_area],
                           # ['ROV inspection [yes/no]', 'equal', 'yes'],
                           # ['ROV workclass [yes/no]', 'equal', 'yes']
                           ]}

        # Matching

        feas_m_pv = {'Crane Barge': [['Beam [m]', 'sup', 'Entrance width [m]'],
                          ['Length [m]', 'sup', 'Terminal length [m]'],
                          ['Max. draft [m]', 'sup', 'Terminal draught [m]']],
                     'Crane Vessel': [['Beam [m]', 'sup', 'Entrance width [m]'],
                          ['Length [m]', 'sup', 'Terminal length [m]'],
                          ['Max. draft [m]', 'sup', 'Terminal draught [m]']],
                     'Multicat': [['Beam [m]', 'sup', 'Entrance width [m]'],
                          ['Length [m]', 'sup', 'Terminal length [m]'],
                          ['Max. draft [m]', 'sup', 'Terminal draught [m]']],
                     'JUP Barge': [['Beam [m]', 'sup', 'Entrance width [m]'],
                          ['Length [m]', 'sup', 'Terminal length [m]'],
                          ['Max. draft [m]', 'sup', 'Terminal draught [m]']],
                     'JUP Vessel': [['Beam [m]', 'sup', 'Entrance width [m]'],
                          ['Length [m]', 'sup', 'Terminal length [m]'],
                          ['Max. draft [m]', 'sup', 'Terminal draught [m]']],
                     'AHTS': [['Beam [m]', 'sup', 'Entrance width [m]'],
                          ['Length [m]', 'sup', 'Terminal length [m]'],
                          ['Max. draft [m]', 'sup', 'Terminal draught [m]']]}

        feas_m_pe = {'rov': [['Length [m]', 'mul', 'Width [m]', 'plus', 'AE footprint [m^2]', 'sup', 'Terminal area [m^2]'],
                  ['Weight [t]', 'plus', 'AE weight [t]', 'sup', 'Max gantry crane lift capacity [t]'],
                  ['Weight [t]', 'plus', 'AE weight [t]', 'sup', 'Max tower crane lift capacity [t]'],
                  ['Weight [t]', 'plus', 'AE weight [t]', 'div', 'Length [m]', 'mul', 'Width [m]', 'sup', 'Terminal load bearing [t/m^2]']]}

        feas_m_ve = {'rov': [['Length [m]', 'mul', 'Width [m]', 'plus', 'AE footprint [m^2]', 'sup', 'Deck space [m^2]'],
                  ['Weight [t]', 'plus', 'AE weight [t]', 'sup', 'Max. cargo [t]'],
                  ['Weight [t]', 'plus', 'AE weight [t]', 'div', 'Length [m]', 'mul', 'Width [m]', 'sup', 'Deck loading [t/m^2]'],
                      ['Weight [t]', 'sup', 'AH winch rated pull [t]']]}



    # ***********************************************************************************************************************
    elif log_phase_id == 'Gravity':

        # Equipment and vessel feasiblity

        feas_e = {'rov': [['Depth rating [m]', 'sup', max_depth]]}

        feas_v = {'Crane Barge': [['Deck loading [t/m^2]', 'sup', deck_loading],
                           ['Max. cargo [t]', 'sup', deck_cargo],
                           ['Deck space [m^2]', 'sup', deck_area],
                           ['Crane capacity [t]', 'sup', deck_cargo],
                           ['DP [-]', 'sup', 0]
                           # ['ROV inspection [yes/no]', 'equal', 'yes'],
                           # ['ROV workclass [yes/no]', 'equal', 'yes']
                                  ],
                  'Crane Vessel': [['Deck loading [t/m^2]', 'sup', deck_loading],
                           ['Max. cargo [t]', 'sup', deck_cargo],
                           ['Deck space [m^2]', 'sup', deck_area],
                           ['Crane capacity [t]', 'sup', deck_cargo],
                           ['DP [-]', 'sup', 0]
                           # ['ROV inspection [yes/no]', 'equal', 'yes'],
                           # ['ROV workclass [yes/no]', 'equal', 'yes']
                                   ],
                  'CSV': [['Deck loading [t/m^2]', 'sup', deck_loading],
                           ['Max. cargo [t]', 'sup', deck_cargo],
                           ['Deck space [m^2]', 'sup', deck_area],
                           ['Crane capacity [t]', 'sup', deck_cargo],
                           ['DP [-]', 'sup', 0]
                           # ['ROV inspection [yes/no]', 'equal', 'yes'],
                           # ['ROV workclass [yes/no]', 'equal', 'yes']
                          ],
                  'Barge': [['Deck loading [t/m^2]', 'sup', deck_loading],
                           ['Max. cargo [t]', 'sup', deck_cargo],
                           ['Deck space [m^2]', 'sup', deck_area],
                           ['Crane capacity [t]', 'sup', deck_cargo],
                           ['DP [-]', 'sup', 0]],
                  'AHV': [['AH winch rated pull [t]', 'sup', max_linelength],
                           ['AH drum capacity [m]', 'sup', max_moomass]],
                  'Tugboat': [['AH winch rated pull [t]', 'sup', max_linelength],
                           ['AH drum capacity [m]', 'sup', max_moomass]]}

        # Matching

        feas_m_pv = {'Crane Barge': [['Beam [m]', 'sup', 'Entrance width [m]'],
                          ['Length [m]', 'sup', 'Terminal length [m]'],
                          ['Max. draft [m]', 'sup', 'Terminal draught [m]']],
                     'Crane Vessel': [['Beam [m]', 'sup', 'Entrance width [m]'],
                          ['Length [m]', 'sup', 'Terminal length [m]'],
                          ['Max. draft [m]', 'sup', 'Terminal draught [m]']],
                     'CSV': [['Beam [m]', 'sup', 'Entrance width [m]'],
                          ['Length [m]', 'sup', 'Terminal length [m]'],
                          ['Max. draft [m]', 'sup', 'Terminal draught [m]']],
                     'Barge': [['Beam [m]', 'sup', 'Entrance width [m]'],
                          ['Length [m]', 'sup', 'Terminal length [m]'],
                          ['Max. draft [m]', 'sup', 'Terminal draught [m]']],
                     'AHV': [['Beam [m]', 'sup', 'Entrance width [m]'],
                          ['Length [m]', 'sup', 'Terminal length [m]'],
                          ['Max. draft [m]', 'sup', 'Terminal draught [m]']],
                     'Tugboat': [['Beam [m]', 'sup', 'Entrance width [m]'],
                          ['Length [m]', 'sup', 'Terminal length [m]'],
                          ['Max. draft [m]', 'sup', 'Terminal draught [m]']]}

        feas_m_pe = {'rov': [['Length [m]', 'mul', 'Width [m]', 'plus', 'AE footprint [m^2]', 'sup', 'Terminal area [m^2]'],
                  ['Weight [t]', 'plus', 'AE weight [t]', 'div', 'Length [m]', 'mul', 'Width [m]', 'sup', 'Terminal load bearing [t/m^2]']]}

        feas_m_ve = {'rov': [['Length [m]', 'mul', 'Width [m]', 'plus', 'AE footprint [m^2]', 'sup', 'Deck space [m^2]'],
                  ['Weight [t]', 'plus', 'AE weight [t]', 'sup', 'Max. cargo [t]'],
                  ['Weight [t]', 'plus', 'AE weight [t]', 'div', 'Length [m]', 'mul', 'Width [m]', 'sup', 'Deck loading [t/m^2]'],
                      ['Weight [t]', 'sup', 'AH winch rated pull [t]']]}




    # ***********************************************************************************************************************
    elif log_phase_id == 'Driven':

        # Equipment and vessel feasiblity

        feas_e = {'hammer': [['Depth rating [m]', 'sup', max_depth],
                             ['Min pile diameter [mm]', 'sup', sleeve_diam],
                             ['Max pile diameter [mm]', 'inf', sleeve_diam]],
                  'drilling rigs': [['Max water depth [m]', 'sup', max_depth],
                                    ['Min pile diameter [mm]', 'inf', sleeve_diam],
                                    ['Max pile diameter [mm]', 'sup', sleeve_diam],
                                    ['Max drilling depth [m]', 'sup', max_depth]],
                  'vibro driver': [['Max pile weight [t]', 'sup', max_moomass],
                                   ['Min pile diameter [mm]', 'inf', sleeve_diam],
                                   ['Max pile diameter [mm]', 'sup', sleeve_diam],
                                   ['Depth rating [m]', 'sup', max_depth]],
                  'suction pump': [['Depth rating [m]', 'sup', max_depth]], # ?????!
                  'rov': [['Depth rating [m]', 'sup', max_depth]]}

        feas_v = {'JUP Vessel': [['Deck loading [t/m^2]', 'sup', deck_loading],
                           ['Max. cargo [t]', 'sup', deck_cargo],
                           ['Deck space [m^2]', 'sup', deck_area],
                           ['Crane capacity [t]', 'sup', deck_cargo],
                           ['DP [-]', 'sup', 0],
                           # ['ROV inspection [yes/no]', 'equal', 'yes'],
                           # ['ROV workclass [yes/no]', 'equal', 'yes'],
                           ['JackUp max payload [t]', 'sup', deck_cargo],
                           ['JackUp max water depth [m]', 'sup', max_depth]],
                  'CSV': [['Deck loading [t/m^2]', 'sup', deck_loading],
                           ['Max. cargo [t]', 'sup', deck_cargo],
                           ['Deck space [m^2]', 'sup', deck_area],
                           ['Crane capacity [t]', 'sup', deck_cargo],
                           ['DP [-]', 'sup', 0],
                           # ['ROV inspection [yes/no]', 'equal', 'yes'],
                           # ['ROV workclass [yes/no]', 'equal', 'yes']
                          ],
                  'JUP Barge': [['Deck loading [t/m^2]', 'sup', deck_loading],
                           ['Max. cargo [t]', 'sup', deck_cargo],
                           ['Deck space [m^2]', 'sup', deck_area],
                           ['Crane capacity [t]', 'sup', deck_cargo],
                           ['DP [-]', 'sup', 0],
                           # ['ROV inspection [yes/no]', 'equal', 'yes'],
                           # ['ROV workclass [yes/no]', 'equal', 'yes'],
                           ['JackUp max payload [t]', 'sup', deck_cargo],
                           ['JackUp max water depth [m]', 'sup', max_depth]],
                  'Tugboat': [['Bollard pull [t]', 'sup', max_moomass]]}

        # Matching

        feas_m_pv = {'JUP Vessel': [['Beam [m]', 'sup', 'Entrance width [m]'],
                          ['Length [m]', 'sup', 'Terminal length [m]'],
                          ['Max. draft [m]', 'sup', 'Terminal draught [m]'],
                          ['Jacking capability [yes/no]','equal','yes']],
                     'CSV': [['Beam [m]', 'sup', 'Entrance width [m]'],
                          ['Length [m]', 'sup', 'Terminal length [m]'],
                          ['Max. draft [m]', 'sup', 'Terminal draught [m]']],
                     'JUP Barge': [['Beam [m]', 'sup', 'Entrance width [m]'],
                          ['Length [m]', 'sup', 'Terminal length [m]'],
                          ['Max. draft [m]', 'sup', 'Terminal draught [m]'],
                          ['Jacking capability [yes/no]','equal','yes']],
                     'Tugboat': [['Beam [m]', 'sup', 'Entrance width [m]'],
                          ['Length [m]', 'sup', 'Terminal length [m]'],
                          ['Max. draft [m]', 'sup', 'Terminal draught [m]']]}

        feas_m_pe = {'rov': [['Length [m]', 'mul', 'Width [m]', 'plus', 'AE footprint [m^2]', 'sup', 'Terminal area [m^2]'],
                  ['Weight [t]', 'plus', 'AE weight [t]', 'div', 'Length [m]', 'mul', 'Width [m]', 'sup', 'Terminal load bearing [t/m^2]']]}

        feas_m_ve = {'rov': [['Length [m]', 'mul', 'Width [m]', 'plus', 'AE footprint [m^2]', 'sup', 'Deck space [m^2]'],
                  ['Weight [t]', 'plus', 'AE weight [t]', 'sup', 'Max. cargo [t]'],
                  ['Weight [t]', 'plus', 'AE weight [t]', 'div', 'Length [m]', 'mul', 'Width [m]', 'sup', 'Deck loading [t/m^2]'],
                      ['Weight [t]', 'sup', 'AH winch rated pull [t]']]}





    return feas_e, feas_v, feas_m_pv, feas_m_pe, feas_m_ve
