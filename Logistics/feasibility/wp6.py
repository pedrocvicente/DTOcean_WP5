# -*- coding: utf-8 -*-
"""
@author: WavEC Offshore Renewables
email: boris.teillant@wavec.org; paulo@wavec.org

This module is part of the characterization step in the WP5 methodology. It 
contains feasibility functions to compute the minimum logistic requirements to 
carry out the different logistic phases. This particular modules includes the
function related to the O&M repair actions.

BETA VERSION NOTES: The current version is limited to one logistic phase, the
repair action related to offshore inspection and maintenance activities.
"""

def wp6_feas(log_phase, log_phase_id, wp6_outputs):
    """ wp6_feas is a function which determines the logistic requirement 
    associated with the one logistic phase dealing O&M offshore inspection action
    
    Parameters
    ----------
    log_phase : Class
     Class of the logistic phase under consideration for assessment
    log_phase_id : str
     string describing the ID of the logistic phase under consideration
    wp6_outputs : dict
     dictionnary containing all required inputs to WP5 coming from WP6
    
    Returns
    -------
    feas_e : dict
     dictionnary containing all logistic requirements associated with every
     equipment type of the logistic phase under consideration
    feas_v : dict
     dictionnary containing all logistic requirements associated with every
     vessel type of the logistic phase under consideration
    """
    if log_phase_id == 'insp':

        # Input collection
        lenght_SP = wp6_outputs['LogPhase1']['Length_SP [m]'].ix[0]
        width_SP = wp6_outputs['LogPhase1']['Width_SP [m]'].ix[0]
        height_SP = wp6_outputs['LogPhase1']['Height_SP [m]'].ix[0]
        total_mass_SP = wp6_outputs['LogPhase1']['Total_Mass_SP [t]'].ix[0]
        indiv_mass_SP = wp6_outputs['LogPhase1']['Indiv_Mass_SP [t]'].ix[0]

        # Feasibility functions
        SP_area = float(lenght_SP) * float(width_SP)
        SP_loading = float(total_mass_SP) / float(SP_area)
        lifting_req = float(indiv_mass_SP)

        feas_e = {}
        feas_v = {'CTV': [['Deck loading [ton/m2]', 'sup', SP_loading],
                          ['Deck space [m2]', 'sup', SP_area],
                          ['Crane weight [t]', 'sup', lifting_req]],

                  'Multicat': [['Deck loading [ton/m2]', 'sup', SP_loading],
                               ['Deck space [m2]', 'sup', SP_area],
                               ['Crane weight [t]', 'sup', lifting_req]]}

    return feas_e, feas_v
