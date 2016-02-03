import warnings

def select_logPhase(OM_outputs):

    for index, row in OM_outputs.iterrows():

        om_id = OM_outputs['ID [-]'].ix[index]

        # Select the suitable Log phase id
        if om_id == 'Insp1' or om_id == 'MoS1' or om_id == 'Insp2' or om_id == 'MoS2':
            log_phase_id = 'LpM1'

        elif om_id == 'Insp3' or om_id == 'MoS3':
              log_phase_id = 'LpM2'

        elif om_id == 'Insp4' or om_id == 'Insp4' or om_id == 'MoS3':
              log_phase_id = 'LpM3'

        elif om_id == 'MoS5' or om_id == 'MoS6':
              log_phase_id = 'LpM4'

        else:
            warnings.warn('maintenance id - not supported')

    return log_phase_id



