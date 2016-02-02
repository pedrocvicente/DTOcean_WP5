from .classes import DefPhase, LogPhase


def initialize_LpM5_phase(log_op, vessels, equipments, OM_outputs):

    # save outputs required inside short named variables


    # initialize logistic phase
    phase = LogPhase(920, "Underwater inspection or on-site maintenance using ROV")

    ''' Underwater inspection or on-site maintenance strategy using ROVs '''

    # initialize strategy
    phase.op_ve[0] = DefPhase(1, 'Inspection / On-site maintenance using ROV')

    # define vessel and equipment combinations suited for this strategy
    phase.op_ve[0].ve_combination[0] = {'vessel': [(1, vessels['CLV'])],
                                        'equipment': [ (1, equipments['rov'], 0) ] }


    # define initial mobilization and onshore preparation tasks
    phase.op_ve[0].op_seq_prep = [ log_op["Mob"],
                                   log_op["VessPrep"] ]

    # define sea operations

    i = 0 #initialize the number of sea operations within this logistic phase
    for index, row in OM_outputs.iterrows():

        if index == 'MoS7' or index == 'MoS8':

            phase.op_ve[0].op_seq_sea[i] = [ log_op["Access"],
                                             log_op["Maintenance"] ]

        i = i+1

    # define final demobilization tasks
    phase.op_ve[0].op_seq_demob = [log_op["Demob"]]

    return phase
