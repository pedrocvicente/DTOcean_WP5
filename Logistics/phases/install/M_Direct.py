from .classes import DefPhase, LogPhase

def initialize_m_direct_phase(log_op, vessels, equipments, MF_outputs):

    # save outputs required inside short named variables
    found_db = MF_outputs['foundation']
    direct_db = found_db[found_db['type [-]'] == 'direct-embedment anchor']

    # initialize logistic phase
    phase = LogPhase(114, "Installation of mooring systems with direct-embedment anchors")

    ''' Direct-embedment anchor penetration through suction-embedment installation strategy '''

    # initialize strategy
    phase.op_ve[0] = DefPhase(1, 'Deploy direct-embedment anchor by suction-embedment')

    # define vessel and equipment combinations suited for this strategy
    phase.op_ve[0].ve_combination[0] = {'vessel': [(1, vessels['AHTS'])],
                                        'equipment': [(1, equipments['rov'], 0)]}

    phase.op_ve[0].ve_combination[1] = {'vessel': [(1, vessels['Multicat'])],
                                        'equipment': [(1, equipments['rov'], 0)]}

    # define initial mobilization and onshore preparation tasks
    phase.op_ve[0].op_seq_prep = [log_op["Mob"],
                                  log_op["AssPort"],
                                  log_op["VessPrep"]]

    # iterate over the list of elements to be installed.
    # each element is associated with a customized operation sequence depending on it's characteristics
    for index, row in direct_db.iterrows():

        # initialize an empty operation sequence list for the 'index' element
        phase.op_ve[0].op_seq_sea[index] = []

        phase.op_ve[0].op_seq_sea[index].extend([ log_op["SeafloorEquipPrep"],
                                                  log_op["DirecSuct"],
                                                  log_op["PreLay"] ])

    # define final demobilization tasks
    phase.op_ve[0].op_seq_demob = [log_op["Demob"]]

    ''' Direct-embedment anchor penetration through hydro-jetting installation strategy '''

    # initialize strategy
    phase.op_ve[1] = DefPhase(1, 'Deploy direct-embedment anchor by hydro-jetting')

    # define vessel and equipment combinations suited for this strategy
    phase.op_ve[1].ve_combination[0] = {'vessel': [(1, vessels['AHTS'])],
                                        'equipment': [(1, equipments['rov'], 0)]}

    phase.op_ve[1].ve_combination[1] = {'vessel': [(1, vessels['Multicat'])],
                                        'equipment': [(1, equipments['rov'], 0)]}

    # define initial mobilization and onshore preparation tasks
    phase.op_ve[1].op_seq_prep = [log_op["Mob"],
                                  log_op["AssPort"],
                                  log_op["VessPrep"]]

    # iterate over the list of elements to be installed.
    # each element is associated with a customized operation sequence depending on it's characteristics
    for index, row in direct_db.iterrows():

        # initialize an empty operation sequence list for the 'index' element
        phase.op_ve[1].op_seq_sea[index] = []

        phase.op_ve[1].op_seq_sea[index].extend([ log_op["SeafloorEquipPrep"],
                                                  log_op["DirecJet"],
                                                  log_op["PreLay"] ])

    # define final demobilization tasks
    phase.op_ve[1].op_seq_demob = [log_op["Demob"]]

    ''' Direct-embedment anchor penetration through mechanical-embedment installation strategy '''

    # initialize strategy
    phase.op_ve[2] = DefPhase(1, 'Deploy direct-embedment anchor by mechanical-embedment')

    # define vessel and equipment combinations suited for this strategy
    phase.op_ve[2].ve_combination[0] = {'vessel': [(1, vessels['AHTS'])],
                                        'equipment': [(1, equipments['rov'], 0)]}

    phase.op_ve[2].ve_combination[1] = {'vessel': [(1, vessels['Multicat'])],
                                        'equipment': [(1, equipments['rov'], 0)]}

    # define initial mobilization and onshore preparation tasks
    phase.op_ve[2].op_seq_prep = [log_op["Mob"],
                                  log_op["AssPort"],
                                  log_op["VessPrep"]]

    # iterate over the list of elements to be installed.
    # each element is associated with a customized operation sequence depending on it's characteristics
    for index, row in direct_db.iterrows():

        # initialize an empty operation sequence list for the 'index' element
        phase.op_ve[2].op_seq_sea[index] = []

        phase.op_ve[2].op_seq_sea[index].extend([ log_op["SeafloorEquipPrep"],
                                                  log_op["DirecMech"],
                                                  log_op["PreLay"] ])

    # define final demobilization tasks
    phase.op_ve[2].op_seq_demob = [log_op["Demob"]]

    return phase
