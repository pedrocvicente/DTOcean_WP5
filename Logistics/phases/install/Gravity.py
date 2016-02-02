from .classes import DefPhase, LogPhase


def initialize_gravity_phase(log_op, vessels, equipments, MF_outputs):

    # save outputs required inside short named variables
    found_db = MF_outputs['foundation']
    gravity_db = found_db[found_db['type [-]'] == 'gravity foundation']
    gravity_db = gravity_db.append(found_db[found_db['type [-]'] == 'gravity anchor'])
    gravity_db = gravity_db.append(found_db[found_db['type [-]'] == 'shallow foundation'])
    gravity_db = gravity_db.append(found_db[found_db['type [-]'] == 'shallow anchor'])

    # initialize logistic phase
    phase = LogPhase(112, "Installation of gravity based foundations")

    '''On-deck Transportation Strategy'''

    # initialize strategy (all strategies will be individually assessed by the
    # performance functions, with the lowest costs on being choosen)
    phase.op_ve[0] = DefPhase(1, 'Gravity based anchor installation with on deck transportation')

    # define vessel and equipment combinations suited for this strategy
    phase.op_ve[0].ve_combination[0] = {'vessel': [ (1, vessels['Crane Vessel']), (1, vessels['Multicat']) ],
                                        'equipment': [ (1, equipments['rov'], 0) ]}

    phase.op_ve[0].ve_combination[1] = {'vessel': [ (1, vessels['CSV']), (1, vessels['Multicat']) ],
                                        'equipment': [ (1, equipments['rov'], 0) ]}

    phase.op_ve[0].ve_combination[2] = {'vessel': [ (1, vessels['Fit for Purpose']), (1, vessels['Multicat']) ],
                                        'equipment': [ (1, equipments['rov'], 0) ]}

    phase.op_ve[0].ve_combination[3] = {'vessel': [ (1, vessels['Barge']), (1, vessels['Tugboat']), (1, vessels['Multicat']) ],
                                        'equipment': [ (1, equipments['divers'], 0), (1, equipments['rov'], 0) ]}

    phase.op_ve[0].ve_combination[4] = {'vessel': [ (1, vessels['Crane Barge']), (1, vessels['Tugboat']), (1, vessels['Multicat'])],
                                        'equipment': [ (1, equipments['rov'], 0) ]}

    phase.op_ve[0].ve_combination[5] = {'vessel': [ (1, vessels['PSV']), (1, vessels['Multicat']) ],
                                        'equipment': [ (1, equipments['rov'], 0) ]}

    # define initial mobilization and onshore preparation tasks
    phase.op_ve[0].op_seq_prep = [log_op["Mob"],
                                  log_op["AssPort"],
                                  log_op["VessPrep"]]

    # iterate over the list of elements to be installed.
    # each element is associated with a customized operation sequence depending on it's characteristics,
    for index, row in gravity_db.iterrows():

        # initialize an empty operation sequence list for the 'index' element
        phase.op_ve[0].op_seq_sea[index] = []

        phase.op_ve[0].op_seq_sea[index].extend([ log_op["VesPos"],
                                                  log_op["GBSpos"] ])

        if gravity_db['type [-]'].ix[index] == 'gravity anchor' or gravity_db['type [-]'].ix[index] == 'shallow anchor':
            phase.op_ve[0].op_seq_sea[index].extend([ log_op["PreLay"] ])

    # define final demobilization tasks
    phase.op_ve[0].op_seq_demob = [log_op["Demob"]]

    return phase
