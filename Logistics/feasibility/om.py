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

def om_feas(log_phase, log_phase_id, OM_outputs, user_inputss):
    """ om_feas is a function which determines the logistic requirement
    associated with the logistic phases related to the O&M

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

    ''' LogPhase LpM1: Inspection or on-site maintenance of topside elements'''

    if log_phase_id == 'LpM1':

        # Input collection
        lenght_SP = OM_outputs['sp_length [m]']
        width_SP = OM_outputs['sp_width [m]']
        dry_mass_SP = OM_outputs['sp_dry_mass [kg]']/1000
        nr_technician = OM_outputs['technician [-]']

        # Feasibility functions
        deck_area = max(lenght_SP*width_SP)
        deck_cargo = max(dry_mass_SP)
        deck_loading = max(dry_mass_SP/(lenght_SP*width_SP))
        ext_personnel = max(nr_technician)

        feas_e = {}
        feas_v = {'CTV':        [['Deck loading [t/m^2]', 'sup', deck_loading],
                                 ['Deck space [m^2]', 'sup', deck_area],
                                 ['Max. cargo [t]', 'sup', deck_cargo],
                                 ['External  personnel [-]', 'sup', ext_personnel]],

                  'Multicat':   [['Deck loading [t/m^2]', 'sup', deck_loading],
                                 ['Deck space [m^2]', 'sup', deck_area],
                                 ['Max. cargo [t]', 'sup', deck_cargo],
                                 ['External  personnel [-]', 'sup', ext_personnel]],

                  'Helicopter': [['Deck loading [t/m^2]', 'sup', deck_loading],
                                 ['Deck space [m^2]', 'sup', deck_area],
                                 ['Max. cargo [t]', 'sup', deck_cargo],
                                 ['External  personnel [-]', 'sup', ext_personnel]]

                                 }

        # Matching
        feas_m_pv = {'CTV': [ ['Beam [m]', 'sup', 'Entrance width [m]'],
                              ['Length [m]', 'sup', 'Terminal length [m]'],
                              ['Max. draft [m]', 'sup', 'Terminal draught [m]'] ],

                     'Multicat': [ ['Beam [m]', 'sup', 'Entrance width [m]'],
                                   ['Length [m]', 'sup', 'Terminal length [m]'],
                                   ['Max. draft [m]', 'sup', 'Terminal draught [m]'] ]
                        }

        feas_m_pe = {}

        feas_m_ve = {}

    if log_phase_id == 'LpM2':

        # Input collection
        lenght_SP = OM_outputs['sp_length [m]']
        width_SP = OM_outputs['sp_width [m]']
        dry_mass_SP = OM_outputs['sp_dry_mass [kg]']/1000
        nr_technician = OM_outputs['technician [-]']
        depth = OM_outputs['depth [m]']

        # Feasibility functions
        deck_area = max(lenght_SP*width_SP)
        deck_cargo = max(dry_mass_SP)
        deck_loading = max(dry_mass_SP/(lenght_SP*width_SP))
        ext_personnel = max(nr_technician)
        bathymetry = max(depth)

        feas_e = {'divers': [ ['Max operating depth [m]', 'sup', bathymetry] ]

                           }

        feas_v = {'CTV':        [ ['Deck loading [t/m^2]', 'sup', deck_loading],
                                  ['Deck space [m^2]', 'sup', deck_area],
                                  ['Max. cargo [t]', 'sup', deck_cargo],
                                  ['External  personnel [-]', 'sup', ext_personnel] ],

                  'Multicat':   [ ['Deck loading [t/m^2]', 'sup', deck_loading],
                                  ['Deck space [m^2]', 'sup', deck_area],
                                  ['Max. cargo [t]', 'sup', deck_cargo],
                                  ['External  personnel [-]', 'sup', ext_personnel] ]

                                 }

        # Matching
        feas_m_pv = {'CTV': [ ['Beam [m]', 'sup', 'Entrance width [m]'],
                              ['Length [m]', 'sup', 'Terminal length [m]'],
                              ['Max. draft [m]', 'sup', 'Terminal draught [m]'] ],

                     'Multicat': [ ['Beam [m]', 'sup', 'Entrance width [m]'],
                                   ['Length [m]', 'sup', 'Terminal length [m]'],
                                   ['Max. draft [m]', 'sup', 'Terminal draught [m]'] ]
                        }

        feas_m_pe = {}

        feas_m_ve = {}

    if log_phase_id == 'LpM3':

        # Input collection
        lenght_SP = OM_outputs['sp_length [m]']
        width_SP = OM_outputs['sp_width [m]']
        dry_mass_SP = OM_outputs['sp_dry_mass [kg]']/1000
        nr_technician = OM_outputs['technician [-]']
        depth = OM_outputs['depth [m]']
        om_id = OM_outputs['id [-]'].ix[0]

        # Feasibility functions
        deck_area = max(lenght_SP*width_SP)
        deck_cargo = max(dry_mass_SP)
        deck_loading = max(dry_mass_SP/(lenght_SP*width_SP))
        ext_personnel = max(nr_technician)
        bathymetry = max(depth)
        if om_id == 'Insp5':
            rov_class = 'Workclass'
        elif om_id == 'Insp4' or om_id == 'MoS4':
            rov_class = ' Inspection class'


        feas_e = {'rov': [ ['Depth rating [m]', 'sup', bathymetry],
                          ['ROV class [-]', 'equal', rov_class] ]
                         }

        feas_v = {'CTV':        [ ['Deck loading [t/m^2]', 'sup', deck_loading],
                                  ['Deck space [m^2]', 'sup', deck_area],
                                  ['Max. cargo [t]', 'sup', deck_cargo],
                                  ['External  personnel [-]', 'sup', ext_personnel] ],

                  'Multicat':   [ ['Deck loading [t/m^2]', 'sup', deck_loading],
                                  ['Deck space [m^2]', 'sup', deck_area],
                                  ['Max. cargo [t]', 'sup', deck_cargo],
                                  ['External  personnel [-]', 'sup', ext_personnel] ]

                                 }

        # Matching
        feas_m_pv = {'CTV': [ ['Beam [m]', 'sup', 'Entrance width [m]'],
                              ['Length [m]', 'sup', 'Terminal length [m]'],
                              ['Max. draft [m]', 'sup', 'Terminal draught [m]'] ],

                     'Multicat': [ ['Beam [m]', 'sup', 'Entrance width [m]'],
                                   ['Length [m]', 'sup', 'Terminal length [m]'],
                                   ['Max. draft [m]', 'sup', 'Terminal draught [m]'] ]
                        }

        feas_m_pe = {}

        feas_m_ve = {}

    if log_phase_id == 'LpM4':

        # Input collection
        lenght_SP = OM_outputs['sp_length [m]']
        width_SP = OM_outputs['sp_width [m]']
        dry_mass_SP = OM_outputs['sp_dry_mass [kg]']/1000
        nr_technician = OM_outputs['technician [-]']
        depth = OM_outputs['depth [m]']
        om_id = OM_outputs['id [-]'].ix[0]

        # Feasibility functions
        deck_area = max(lenght_SP*width_SP)
        deck_cargo = max(dry_mass_SP)
        deck_loading = max(dry_mass_SP/(lenght_SP*width_SP))
        ext_personnel = max(nr_technician)
        bathymetry = max(depth)
        winch_pull = max(dry_mass_SP)

        feas_e = {'rov': [ ['Depth rating [m]', 'sup', bathymetry],
                           ['ROV class [-]', 'equal', 'Workclass'] ]
                         }

        feas_v = {'AHTS':        [ ['Deck loading [t/m^2]', 'sup', deck_loading],
                                   ['Deck space [m^2]', 'sup', deck_area],
                                   ['Max. cargo [t]', 'sup', deck_cargo],
                                   ['External  personnel [-]', 'sup', ext_personnel],
                                   ['AH winch rated pull [t]', 'sup', winch_pull] ],

                  'Multicat':   [ ['Deck loading [t/m^2]', 'sup', deck_loading],
                                  ['Deck space [m^2]', 'sup', deck_area],
                                  ['Max. cargo [t]', 'sup', deck_cargo],
                                  ['External  personnel [-]', 'sup', ext_personnel],
                                  ['AH winch rated pull [t]', 'sup', winch_pull] ]

                                 }

        # Matching
        feas_m_pv = {'AHTS': [ ['Beam [m]', 'sup', 'Entrance width [m]'],
                               ['Length [m]', 'sup', 'Terminal length [m]'],
                               ['Max. draft [m]', 'sup', 'Terminal draught [m]'] ],

                     'Multicat': [ ['Beam [m]', 'sup', 'Entrance width [m]'],
                                   ['Length [m]', 'sup', 'Terminal length [m]'],
                                   ['Max. draft [m]', 'sup', 'Terminal draught [m]'] ]
                        }

        feas_m_pe = {}

        feas_m_ve = {}

    if log_phase_id == 'LpM5':

        # Input collection
        lenght_SP = OM_outputs['sp_length [m]']
        width_SP = OM_outputs['sp_width [m]']
        dry_mass_SP = OM_outputs['sp_dry_mass [kg]']/1000
        nr_technician = OM_outputs['technician [-]']
        depth = OM_outputs['depth [m]']

        # Feasibility functions
        cable_weight = max(dry_mass_SP)
        ext_personnel = max(nr_technician)
        bathymetry = max(depth)

        feas_e = {'rov': [ ['Depth rating [m]', 'sup', bathymetry],
                           ['ROV class [-]', 'equal', 'Workclass'] ]
                         }

        feas_v = {'CLV':        [ ['Turntable loading [t]', 'sup', cable_weight],
                                  ['Cable Splice [yes/no]', 'equal', 'yes'] ]
                                 }

        # Matching
        feas_m_pv = {'CLV': [ ['Beam [m]', 'sup', 'Entrance width [m]'],
                              ['Length [m]', 'sup', 'Terminal length [m]'],
                              ['Max. draft [m]', 'sup', 'Terminal draught [m]'] ]

                        }

        feas_m_pe = {}

        feas_m_ve = {}


    return feas_e, feas_v, feas_m_pv, feas_m_pe, feas_m_ve

