from .classes import DefPhase, LogPhase


def initialize_e_array_phase(log_op, vessels, equipments, electrical_outputs):
    phase = LogPhase(101, "Installation of static subsea inter-array power cables")

#    phase.op_ve[0] = DefPhase(1, 'Drilling')
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
