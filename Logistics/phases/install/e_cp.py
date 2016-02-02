from .classes import DefPhase, LogPhase

def initialize_e_cp_seabed_phase(log_op, vessels, equipments, electrical_outputs):

    # save outputs required inside short named variables
    cp_db = electrical_outputs['collection point']
    cp_db = cp_db[cp_db['type [-]'] != 'surface piercing']
    cp_db = cp_db[cp_db['downstream ei type [-]'] != 'hard-wired cable']

    # initialize logistic phase
    phase = LogPhase(102, "Installation of offshore electrical collection point")

    # initialize strategy (all strategies will be individually assessed by the
    # performance functions, with the lowest costs on being choosen)
    phase.op_ve[0] = DefPhase(1, 'all seabed collection points')

    # define vessel and equipment combinations suited for this strategy
    phase.op_ve[0].ve_combination[0] = {'vessel': [(1, vessels['Crane Vessel']), (1, vessels['Multicat'])],
                                        'equipment': [(1, equipments['rov'], 0)]}

    phase.op_ve[0].ve_combination[1] = {'vessel': [(1, vessels['Crane Barge']), (2, vessels['Tugboat']), (1, vessels['Multicat'])],
                                        'equipment': [(1, equipments['rov'], 0)]}

    phase.op_ve[0].ve_combination[2] = {'vessel': [(1, vessels['JUP Vessel']), (1, vessels['Multicat'])],
                                        'equipment': [(1, equipments['rov'], 0)]}

    phase.op_ve[0].ve_combination[3] = {'vessel': [(1, vessels['JUP Barge']), (2, vessels['Tugboat']), (1, vessels['Multicat'])],
                                        'equipment': [(1, equipments['rov'], 0)]}

    phase.op_ve[0].ve_combination[4] = {'vessel': [(1, vessels['CSV']), (1, vessels['Multicat'])],
                                        'equipment': [(1, equipments['rov'], 0)]}

    # define initial mobilization and onshore preparation tasks
    phase.op_ve[0].op_seq_prep = [log_op["Mob"],
                                  log_op["AssPort"],
                                  log_op["VessPrep"]]

    # check the collection point type
    for index, row in cp_db.iterrows():

        # initialize an empty operation sequence list for the 'index' element
        phase.op_ve[0].op_seq_sea[index] = []

        if cp_db['type [-]'].ix[index] == 'seabed':

            if 'dry-mate' in cp_db['upstream ei type [-]'].ix[index]: #checks whether 'dry-mate' is inside the list

                for x in range(cp_db['upstream ei type [-]'].ix[index].count('dry-mate')): #counts how may 'dry-mate' types exist and loops over the number
                    phase.op_ve[0].op_seq_sea[index].extend([ log_op["LiftCable"] ])

            if 'dry-mate' in cp_db['downstream ei type [-]'].ix[index]:

                for x in range(cp_db['downstream ei type [-]'].ix[index].count('dry-mate')):
                    phase.op_ve[0].op_seq_sea[index].extend([ log_op["LiftCable"] ])

            if 'dry-mate' in cp_db['upstream ei type [-]'].ix[index] or 'dry-mate' in cp_db['downstream ei type [-]'].ix[index]:
                phase.op_ve[0].op_seq_sea[index].extend([ log_op["DryConnect"],
                                                          log_op["LowerCP"] ])

            elif all(x in 'wet-mate' for x in cp_db['upstream ei type [-]'].ix[index]) and all(x in 'wet-mate' for x in cp_db['downstream ei type [-]'].ix[index]):
                 phase.op_ve[0].op_seq_sea[index].extend([ log_op["LowerCP"] ])

            else:
                print 'CP: Wrong Inputs'

        if cp_db['type [-]'].ix[index] == 'seabed with pigtails':

            if 'dry-mate' in cp_db['downstream ei type [-]'].ix[index]:

                for x in range(cp_db['downstream ei type [-]'].ix[index].count('dry-mate')):
                    phase.op_ve[0].op_seq_sea[index].extend([ log_op["LiftCable"] ])

                phase.op_ve[0].op_seq_sea[index].extend([ log_op["DryConnect"],
                                                           log_op["LowerCP"] ])

            elif all(x in 'wet-mate' for x in cp_db['downstream ei type [-]'].ix[index]):
                  phase.op_ve[0].op_seq_sea[index].extend([ log_op["LowerCP"]] )

            else:
                print 'CP: Wrong Inputs'

        else:
            print 'CP: Wrong Inputs'

    # define final demobilization tasks
    phase.op_ve[0].op_seq_demob = [log_op["Demob"]]

    return phase


def initialize_e_cp_surface_phase(log_op, vessels, equipments, electrical_outputs):

    return