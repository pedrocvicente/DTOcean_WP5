from .classes import DefPhase, LogPhase


def initialize_drive_phase(log_op, vessels, equipments, MF_outputs):

    # save outputs required inside short named variables
    found_db = MF_outputs['foundation']
    driven_db = found_db[found_db['type [-]'] == 'pile foundation']
    driven_db = driven_db.append(found_db[found_db['type [-]'] == 'pile anchor'])

    # initialize logistic phase
    phase = LogPhase(110, "Installation of driven piles anchors/foundations")

    ''' Drilling Installation Strategy (Pre-Piling) '''

    # initialize strategy
    phase.op_ve[0] = DefPhase(1, 'Drilling (Pre-Piling)')

    # define vessel and equipment combinations suited for this strategy
    phase.op_ve[0].ve_combination[0] = {'vessel': [(1, vessels['CSV'])],
                                       'equipment': [(1, equipments['drilling rigs'], 0), (1, equipments['rov'], 0)]}

    phase.op_ve[0].ve_combination[1] = {'vessel': [(1, vessels['JUP Barge']), (1, vessels['Tugboat'])],
                                       'equipment': [(1, equipments['drilling rigs'], 0), (1, equipments['rov'], 0)]}

    phase.op_ve[0].ve_combination[2] = {'vessel': [(1, vessels['JUP Vessel'])],
                                       'equipment': [(1, equipments['drilling rigs'], 0), (1, equipments['rov'], 0)]}

    # define initial mobilization and onshore preparation tasks
    phase.op_ve[0].op_seq_prep = [log_op["Mob"],
                                  log_op["AssPort"],
                                  log_op["VessPrep"]]

    # iterate over the list of elements to be installed.
    # each element is associated with a customized operation sequence depending on it's characteristics
    for index, row in driven_db.iterrows():

        # initialize an empty operation sequence list for the 'index' element
        phase.op_ve[0].op_seq_sea[index] = []

        phase.op_ve[0].op_seq_sea[index].extend([ log_op["VesPos"],
                                                  log_op["PileDrill"],
                                                  log_op["Grout"],
                                                  log_op["GroutRemov"]])

    # define final demobilization tasks
    phase.op_ve[0].op_seq_demob = [log_op["Demob"]]

    ''' Hammering Installation Strategy (Pre-Piling) '''

    # initialize strategy
    phase.op_ve[1] = DefPhase(1, 'Hammering (Pre-Piling)')

    # define vessel and equipment combinations suited for this strategy
    phase.op_ve[1].ve_combination[0] = {'vessel': [(1, vessels['CSV'])],
                                       'equipment': [(1, equipments['hammer'], 0), (1, equipments['rov'], 0)]}

    phase.op_ve[1].ve_combination[1] = {'vessel': [(1, vessels['JUP Barge']), (1, vessels['Tugboat'])],
                                       'equipment': [(1, equipments['hammer'], 0), (1, equipments['rov'], 0)]}

    phase.op_ve[1].ve_combination[2] = {'vessel': [(1, vessels['JUP Vessel'])],
                                       'equipment': [(1, equipments['hammer'], 0), (1, equipments['rov'], 0)]}

    # define initial mobilization and onshore preparation tasks
    phase.op_ve[1].op_seq_prep = [log_op["Mob"],
                                  log_op["AssPort"],
                                  log_op["VessPrep"]]

    # iterate over the list of elements to be installed.
    # each element is associated with a customized operation sequence depending on it's characteristics
    for index, row in driven_db.iterrows():

        # initialize an empty operation sequence list for the 'index' element
        phase.op_ve[1].op_seq_sea[index] = []

        phase.op_ve[1].op_seq_sea[index].extend([ log_op["Positioning"],
                                                  log_op["PileHamm"],
                                                  log_op["Grout"],
                                                  log_op["GroutRemov"]])

    # define final demobilization tasks
    phase.op_ve[1].op_seq_demob = [log_op["Demob"]]

    ''' Vibro-Piling Installation Strategy (Pre-Piling) '''

    # initialize strategy
    phase.op_ve[2] = DefPhase(1, 'Vibro-Piling (Pre-Piling)')

    # define vessel and equipment combinations suited for this strategy
    phase.op_ve[2].ve_combination[0] = {'vessel': [(1, vessels['CSV'])],
                                       'equipment': [(1, equipments['vibro driver'], 0), (1, equipments['rov'], 0)]}

    phase.op_ve[2].ve_combination[1] = {'vessel': [(1, vessels['JUP Barge']), (1, vessels['Tugboat'])],
                                       'equipment': [(1, equipments['vibro driver'], 0), (1, equipments['rov'], 0)]}

    phase.op_ve[2].ve_combination[2] = {'vessel': [(1, vessels['JUP Vessel'])],
                                       'equipment': [(1, equipments['vibro driver'], 0), (1, equipments['rov'], 0)]}

    # define initial mobilization and onshore preparation tasks
    phase.op_ve[2].op_seq_prep = [log_op["Mob"],
                                  log_op["AssPort"],
                                  log_op["VessPrep"]]

    # iterate over the list of elements to be installed.
    # each element is associated with a customized operation sequence depending on it's characteristics
    for index, row in driven_db.iterrows():

        # initialize an empty operation sequence list for the 'index' element
        phase.op_ve[2].op_seq_sea[index] = []

        phase.op_ve[2].op_seq_sea[index].extend([ log_op["Positioning"],
                                                  log_op["PileVibro"],
                                                  log_op["Grout"],
                                                  log_op["GroutRemov"]])

    # define final demobilization tasks
    phase.op_ve[2].op_seq_demob = [log_op["Demob"]]

    return phase
