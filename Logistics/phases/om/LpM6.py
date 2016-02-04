from .classes import DefPhase, LogPhase


def initialize_LpM6_phase(log_op, vessels, equipments, OM_outputs):

    # save outputs required inside short named variables

    # initialize logistic phase
    phase = LogPhase(920, "Onshore maintenance of devices or array sub-component - on deck transport")

    ''' Retrieval from surface including lifting - maintenance strategy '''

    # initialize strategy
    phase.op_ve[0] = DefPhase(1, 'Retrieval from surface including lifting')

    # define vessel and equipment combinations suited for this strategy
    phase.op_ve[0].ve_combination[0] = {'vessel': [ (1, vessels['Crane Vessel']) ],
                                        'equipment': []}

    phase.op_ve[0].ve_combination[1] = {'vessel': [ (1, vessels['JUP Vessel']) ],
                                        'equipment': []}

    phase.op_ve[0].ve_combination[2] = {'vessel': [ (1, vessels['CSV']) ],
                                        'equipment': []}

    phase.op_ve[0].ve_combination[4] = {'vessel': [ (1, vessels['Crane Barge']), (1, vessels['Tugboat']) ],
                                        'equipment': []}

    phase.op_ve[0].ve_combination[5] = {'vessel': [ (1, vessels['JUP Barge']), (1, vessels['Tugboat']) ],
                                        'equipment': []}

    phase.op_ve[0].ve_combination[6] = {'vessel': [ (1, vessels['Multicat']) ],
                                        'equipment': []}

    # define initial mobilization and onshore preparation tasks
    phase.op_ve[0].op_seq_prep = [ log_op["Mob"],
                                   log_op["VessPrep"] ]

    # define sea operations
    for index, row in OM_outputs.iterrows():

        om_id = OM_outputs['ID [-]'].ix[index]

        if om_id == 'RtP1':

            phase.op_ve[0].op_seq_sea[index] = [ log_op["TranPortSite"],
                                                 log_op["VesPos"],

                                                 log_op["Access"],
                                                 log_op["Maintenance"],

                                                 log_op["TranSiteSite"],
                                                 log_op["TranSitePort"] ]


    # define final demobilization tasks
    phase.op_ve[0].op_seq_demob = [log_op["Demob"]]

    ''' Retrieval from bottom including lifting and subsea operations - maintenance strategy '''

    # initialize strategy
    phase.op_ve[0] = DefPhase(1, 'Retrieval from bottom including lifting and subsea operations')

    # define vessel and equipment combinations suited for this strategy
    phase.op_ve[0].ve_combination[0] = {'vessel': [ (1, vessels['Crane Vessel']) ],
                                        'equipment': [ (1, equipments['rov'], 0) ] }

    phase.op_ve[0].ve_combination[1] = {'vessel': [ (1, vessels['JUP Vessel']) ],
                                        'equipment': [ (1, equipments['rov'], 0) ] }

    phase.op_ve[0].ve_combination[2] = {'vessel': [ (1, vessels['CSV']) ],
                                        'equipment': [ (1, equipments['rov'], 0) ] }

    phase.op_ve[0].ve_combination[4] = {'vessel': [ (1, vessels['Crane Barge']), (1, vessels['Tugboat']) ],
                                        'equipment': [ (1, equipments['rov'], 0) ] }

    phase.op_ve[0].ve_combination[5] = {'vessel': [ (1, vessels['JUP Barge']), (1, vessels['Tugboat']) ],
                                        'equipment': [ (1, equipments['rov'], 0) ] }


    # define initial mobilization and onshore preparation tasks
    phase.op_ve[0].op_seq_prep = [ log_op["Mob"],
                                   log_op["VessPrep"] ]

    # define sea operations
    for index, row in OM_outputs.iterrows():

        om_id = OM_outputs['ID [-]'].ix[index]

        if om_id == 'RtP2':

            phase.op_ve[0].op_seq_sea[index] = [ log_op["TranPortSite"],
                                                 log_op["VesPos"],

                                                 log_op["Access"],
                                                 log_op["Maintenance"],

                                                 log_op["TranSiteSite"],
                                                 log_op["TranSitePort"] ]


    # define final demobilization tasks
    phase.op_ve[0].op_seq_demob = [log_op["Demob"]]

    return phase
