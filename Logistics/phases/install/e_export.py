from .classes import DefPhase, LogPhase


def initialize_e_export_phase(log_op, vessels, equipments, electrical_outputs, user_inputs):

    # save outputs required inside short named variables
    static_db = electrical_outputs['static cable']
    static_export_db = static_db[static_db['type [-]'] == 'export']
    landfall_db = user_inputs['landfall']
    cable_route_db = electrical_outputs['cable route']

    # initialize logistic phase
    phase = LogPhase(100, "Installation of static subsea export power cables")

    ''' Static Export Cable Surface Laying Installation Strategy '''

    # initialize strategy
    phase.op_ve[0] = DefPhase(1, 'Surface Laying')

    # define vessel and equipment combinations suited for this strategy
    phase.op_ve[0].ve_combination[0] = {'vessel': [(1, vessels['CLV']), (2, vessels['Multicat'])],
                                        'equipment': [(1, equipments['split pipe'], 1), (1, equipments['rov'], 1)]}

    phase.op_ve[0].ve_combination[1] = {'vessel': [(1, vessels['CLB']), (1, vessels['Tugboat']), (2, vessels['Multicat'])],
                                        'equipment': [(1, equipments['split pipe'], 1), (1, equipments['rov'], 2)]}

    # define initial mobilization and onshore preparation tasks
    phase.op_ve[0].op_seq_prep = [log_op["Mob"],
                                  log_op["AssPort"],
                                  log_op["LoadCableFactory"]]

    # iterate over the list of elements to be installed.
    # each element is associated with a customized operation sequence depending on it's characteristics,.
    for index, row in static_export_db.iterrows():

        # initialize operation sequence list for the 'index' element
        phase.op_ve[0].op_seq_sea[index] = []

        # condition check to obtain the select landfall method
        if landfall_db['method [-]'].ix[index] == 'OCT':
            phase.op_ve[0].op_seq_sea[index].extend([ log_op["OCT"] ])

        elif landfall_db['method [-]'].ix[index] == 'HDD':
              phase.op_ve[0].op_seq_sea[index].extend([ log_op["HDD"] ])

        else:
            print 'E_export: Wrong inputs'

        # cable lay through cable route
        cable_route = cable_route_db[cable_route_db['static cable id [-]'] == index] # obtains the cable route for 'index' static cable

        for index, row in cable_route.iterrows():
            if cable_route['split pipe [-]'].ix[index] == 'yes':
                phase.op_ve[0].op_seq_sea[index].extend([ log_op["CableLaySplitPipe"] ])
            elif cable_route['split pipe [-]'].ix[index] == 'no':
                phase.op_ve[0].op_seq_sea[index].extend([ log_op["CableLayRoute"] ])
            else:
                print 'Wrong inputs: export cable'
        # condition check to obtain suitable operation sequence for the upstream termination


    # define final demobilization tasks
    phase.op_ve[0].op_seq_demob = [log_op["Demob"]]

    ''' Static Export Cable Simultaneous Lay and Burial Installation Strategy '''

    phase.op_ve[1] = DefPhase(1, 'Simultaneous Lay and Burial')

    ''' Static Export Cable Pre-lay Trenching Installation Strategy '''

    phase.op_ve[2] = DefPhase(1, 'Pre-lay Trenching')

    ''' Static Export Cable Post-Lay Burial Installation Strategy '''

    phase.op_ve[3] = DefPhase(1, 'Post-Lay Burial')

#    phase.op_ve[0].op_sequence = [log_op["op1"],
#                                  log_op["op2"],
#                                  log_op["op3"],
#                                  log_op["op4"],
#                                  log_op["op5"],
#                                  log_op["op_EI1"],
#                                  log_op["op6"],
#                                  log_op["op7"],
#                                  log_op["op8"]]
#
#    phase.op_ve[0].ve_combination[0] = {'vessel': [(1, vessels['Crane Barge']), (2, vessels['Tugboat'])],
#                                        'equipment': [(1, equipments['Drill Rig'], 0)]}
#
#    phase.op_ve[0].ve_combination[1] = {'vessel': [(1, vessels['Crane Vessel'])],
#                                        'equipment': [(1, equipments['Drill Rig'], 0)]}
#
#    phase.op_ve[0].ve_combination[2] = {'vessel': [(1, vessels['JUP Barge']), (2, vessels['Tugboat'])],
#                                        'equipment': [(1, equipments['Drill Rig'], 0)]}
#
#    phase.op_ve[0].ve_combination[3] = {'vessel': [(1, vessels['JUP Vessel'])],
#                                        'equipment': [(1, equipments['Drill Rig'], 0)]}
#
#    phase.op_ve[1] = DefPhase(2, 'Hammering')
#    phase.op_ve[1].op_sequence = [log_op["op1"],
#                                  log_op["op2"],
#                                  log_op["op3"],
#                                  log_op["op4"],
#                                  log_op["op5"],
#                                  log_op["op_F2"],
#                                  log_op["op_F7"],
#                                  log_op["op6"],
#                                  log_op["op7"],
#                                  log_op["op8"]]
#
#    phase.op_ve[1].ve_combination[0] = {'vessel': [(1, vessels['Crane Barge']), (2, vessels['Tugboat'])],
#                                        'equipment': [(1, equipments['Hammer'], 0)]}
#
#    phase.op_ve[1].ve_combination[1] = {'vessel': [(1, vessels['Crane Vessel'])],
#                                        'equipment': [(1, equipments['Hammer'], 0)]}
#
#    phase.op_ve[1].ve_combination[2] = {'vessel': [(1, vessels['JUP Barge']), (2, vessels['Tugboat'])],
#                                        'equipment': [(1, equipments['Hammer'], 0)]}
#
#    phase.op_ve[1].ve_combination[3] = {'vessel': [(1, vessels['JUP Vessel'])],
#                                        'equipment': [(1, equipments['Hammer'], 0)]}
#
#    phase.op_ve[2] = DefPhase(3, 'Vibro Pilling')
#    phase.op_ve[2].op_sequence = [log_op["op1"],
#                                  log_op["op2"],
#                                  log_op["op3"],
#                                  log_op["op4"],
#                                  log_op["op5"],
#                                  log_op["op_F3"],
#                                  log_op["op_F7"],
#                                  log_op["op6"],
#                                  log_op["op7"],
#                                  log_op["op8"]]

    return phase
