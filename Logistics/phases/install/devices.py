import warnings

from .classes import DefPhase, LogPhase


def initialize_devices_phase(log_op, vessels, equipments, user_inputs, hydrodynamic_outputs):

    # save outputs required inside short named variables
    dev_type = user_inputs['device']['type [-]'].ix[0]
    assembly_strategy = user_inputs['device']['assembly strategy [-]'].ix[0]
    trans_methd = user_inputs['device']['transportation method [-]'].ix[0]
    loadout_methd = user_inputs['device']['load out [-]'].ix[0]
    hydro_db = hydrodynamic_outputs

    # initialize logistic phase
    phase = LogPhase(121, "Installation of devices")

    ''' On-deck Transportation Strategy '''

    # initialize strategy
    phase.op_ve[0] = DefPhase(1, 'On-deck transportation')

    # define vessel and equipment combinations suited for this strategy
    phase.op_ve[0].ve_combination[0] = {'vessel': [ (1, vessels['Crane Vessel']), (1, vessels['Multicat']) ],
                                        'equipment': [ (1, equipments['rov'], 0) ]}

    phase.op_ve[0].ve_combination[1] = {'vessel': [ (1, vessels['JUP Vessel']), (1, vessels['Multicat']) ],
                                        'equipment': [ (1, equipments['rov'], 0) ]}

    phase.op_ve[0].ve_combination[2] = {'vessel': [ (1, vessels['CSV']), (2, vessels['Multicat']) ],
                                        'equipment': [ (1, equipments['rov'], 0) ]}

    phase.op_ve[0].ve_combination[3] = {'vessel': [ (1, vessels['Fit for Purpose']), (2, vessels['Multicat']) ],
                                        'equipment': [ (1, equipments['rov'], 0) ]}

    phase.op_ve[0].ve_combination[4] = {'vessel': [ (1, vessels['Crane Barge']), (1, vessels['Tugboat']), (1, vessels['Multicat']) ],
                                        'equipment': [ (1, equipments['rov'], 0) ]}

    phase.op_ve[0].ve_combination[5] = {'vessel': [ (1, vessels['JUP Barge']), (1, vessels['Tugboat']), (1, vessels['Multicat']) ],
                                        'equipment': [ (1, equipments['rov'], 0) ]}

    # define initial mobilization and onshore preparation tasks
    phase.op_ve[0].op_seq_prep = [log_op["Mob"],
                                  log_op["DevAssPort"]]
    # check the transportation method
    # (1st branch in the decision making tree)
    if trans_methd == 'deck':
        # check the device loadout strategy
        # (2nd branch in the decision making tree)
        if loadout_methd == 'lift away':
            phase.op_ve[0].op_seq_prep.extend([log_op["LoadOut_Lift"]])

        elif loadout_methd == 'skidded':
            phase.op_ve[0].op_seq_prep.extend([log_op["LoadOut_Skidded"]])

        else:
            warnings.warn('Device Loadout Method: Wrong Inputs')

    elif trans_methd == 'tow':
        # check the device loadout strategy
        # (2nd branch in the decision making tree)
        if loadout_methd == 'lift away':
            phase.op_ve[0].op_seq_prep.extend([log_op["LoadOut_Lift"]])

        elif loadout_methd == 'skidded' or dev_type == 'trailer':
            phase.op_ve[0].op_seq_prep.extend([log_op["LoadOut_Skidded"]])

        elif loadout_methd == 'float away':
            phase.op_ve[0].op_seq_prep.extend([log_op["LoadOut_Float"]])

        else:
            warnings.warn('Device Loadout Method: Wrong Inputs')

    else:
       warnings.warn('Device Transportation Method: Wrong Inputs')

    # iterate over the list of elements to be installed.
    # each element is associated with a customized operation sequence depending on it's characteristics,.
    for index, row in hydro_db.iterrows():

        # initialize an empty operation sequence list for the 'index' element
        phase.op_ve[0].op_seq_sea[index] = []

        if dev_type == 'float WEC' or dev_type == 'float TEC':

            phase.op_ve[0].op_seq_sea[index].extend([log_op["PosFLTdev"]])

        elif dev_type == 'fixed WEC' or dev_type == 'fixed TEC':

             phase.op_ve[0].op_seq_sea[index].extend([log_op["PosBFdev"]])

        else:
           warnings.warn('device type: Wrong Inputs')

    # define final demobilization tasks
    phase.op_ve[0].op_seq_demob = [log_op["Demob"]]

    ''' Tow Transportation Strategy '''

    # initialize strategy
    phase.op_ve[1] = DefPhase(1, 'Towing transportation')

    # define vessel and equipment combinations suited for this strategy
    phase.op_ve[1].ve_combination[0] = {'vessel': [(1, vessels['AHTS']), (1, vessels['Multicat'])],
                                        'equipment': [(1, equipments['rov'], 0) ]}

    phase.op_ve[1].ve_combination[1] = {'vessel': [(1, vessels['Fit for Purpose']), (1, vessels['Multicat'])],
                                        'equipment': [(1, equipments['rov'], 0) ]}

    phase.op_ve[1].ve_combination[2] = {'vessel': [(1, vessels['Tugboat']), (1, vessels['Multicat'])], # TUGBOAT CANNOT BE CHARACTERIZED AS BOTH INSTALLATION AND SUPPORT VESSEL IN THE FEASIBILITY FUNCTIONS
                                        'equipment': [(1, equipments['rov'], 0) ]}

    # define initial mobilization and onshore tasks
    phase.op_ve[1].op_seq_prep = [log_op["Mob"],
                                  log_op["DevAssPort"]]
    if trans_methd == 'deck':

        if loadout_methd == 'lift away':
            phase.op_ve[1].op_seq_prep.extend([log_op["LoadOut_Lift"]])

        elif loadout_methd == 'skidded':
            phase.op_ve[1].op_seq_prep.extend([log_op["LoadOut_Skidded"]])

        else:
            warnings.warn('Device Loadout Method: Wrong Inputs')

    elif trans_methd == 'tow':

        if loadout_methd == 'lift away':
            phase.op_ve[1].op_seq_prep.extend([log_op["LoadOut_Lift"]])

        elif loadout_methd == 'skidded' or dev_type == 'trailer':
            phase.op_ve[1].op_seq_prep.extend([log_op["LoadOut_Skidded"]])

        elif loadout_methd == 'float away':
            phase.op_ve[1].op_seq_prep.extend([log_op["LoadOut_Float"]])

        else:
            warnings.warn('Device Loadout Method: Wrong Inputs')

    else:
       warnings.warn('Device Transportation Method: Wrong Inputs')

    # iterate over the list of elements to be installed.
    # each element is associated with a customized operation sequence depending on it's characteristics,.
    for index, row in hydro_db.iterrows():

        # initialize an empty operation sequence list for the 'index' element
        phase.op_ve[1].op_seq_sea[index] = []

        if dev_type == 'float WEC' or dev_type == 'float TEC':
            phase.op_ve[1].op_seq_sea[index].extend([log_op["PosFLTdev"]])

        elif dev_type == 'fixed WEC' or dev_type == 'fixed TEC':
             phase.op_ve[1].op_seq_sea[index].extend([log_op["PosBFdev"]])

        else:
           warnings.warn('device type: Wrong Inputs')


    # define final demobilization tasks
    phase.op_ve[1].op_seq_demob = [log_op["Demob"]]

    ''' Selection of suitable strategies '''

    # delete the strategies that are not applicable for the scenario
    # so they're not tested in the performance functions
    if trans_methd == 'tow':
        del phase.op_ve[0]
    elif trans_methd == 'deck':
        del phase.op_ve[1]

    return phase

