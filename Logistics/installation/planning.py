# -*- coding: utf-8 -*-
"""
@author: WavEC Offshore Renewables
email: boris.teillant@wavec.org; paulo@wavec.org

This module is responsible for the interphase relation between the different
logistic phases during installation. The inputs from the user and other DTOcean
packages build up unique projects which require specific installation sequences.
The functions in this module return the installation sequence required based on
some pre-defined cases (type of foundations, type of moorings, type of device,
type of electrical infranstrucutres).

BETA VERSION NOTES: the methodology was defined and implemented, should not
suffer major changes on the next version of the code. However the content (the
installation sequences) will be updated.
"""

import warnings
import pandas as pd


def install_plan(file_path, user_inputs, electrical_outputs, MF_outputs):
    """install_plan receives upstream data providing information to build the
    project case, based on this info the function returns a dictionary containing
    a specific installation sequence, using the following methodology:
        - the first key of the dict contains a list of the logistic phases which
        can start independently of others being finished.
        - the second key contains a information of the logistic interphase
         dependency from the logistic phases contained in the first key.
        - the third key contains a information of the logistic interphase
         dependency from the logistic phases contained in the second key.
        - etc...

    Parameters
    ----------
    user_inputs : dict
     dictionnary containing all required inputs to WP5 coming from WP1/end-user.
    wp3_outputs : dict
     dictionnary containing all required inputs to WP5 coming from WP3.
    wp4_outputs : DataFrame
     panda table containing all required inputs to WP5 coming from WP4.

    Returns
    -------
    install_seq : dict
     dictionnary containing a list of the logistic phases required to conduct
     the installation of the project plus information about the interphase
     relation and sequence.
    """

    # Transform order database .xls into panda type
    excel = pd.ExcelFile(file_path)

    # Collect data from a particular tab
    instal_order_db = excel.parse('InstallationOrder', header=0, index_col=0)

    operation = {0: ['Electrical', 1],
                 1: ['Moorings', 2],  # ?!?!
                 2: ['Devices', 3]}  # replace by int(instal_order_db['id'].ix[]) ?????????

    instal_order = {}
    for ind_instal in range(len(instal_order_db['Default Order'])):
        instal_order_i = int(instal_order_db['Default Order'].ix[ind_instal])
        if instal_order_i != 0:
            instal_order[instal_order_i] = operation[ind_instal]


    install_seq = {}

    if user_inputs['device']['type [-]'].ix[0] == "seabed fixed":
        if electrical_outputs['layout']['Electrical Layout [-]'].ix[0] == "type 1":
            if MF_outputs['foundation']['type [-]'].ix[0] == "shallow foundation":
                # Explanation of the distionnary install_seq
                # install_seq = {0: [100, 101, 112],
                #                1: [{120: 112}],
                #                2: [{102: (120, 100)}]}
                install_seq = {0: ['E_export', 'E_array', 'E_cp', 'Driven', 'Devices']}

            elif MF_outputs['foundation']['type [-]'].ix[0] == "pile":
                install_seq = {0: ['E_export', 'E_array', 'E_cp', 'Driven', 'Devices']}

            elif MF_outputs['foundation']['type [-]'].ix[0] == "suction caisson":
                install_seq = {0: ['E_export', 'E_array', 'E_cp', 'M_Suction', 'Devices']}

            elif MF_outputs['foundation']['type [-]'].ix[0] == "gravity based":
                install_seq = {0: ['E_export', 'E_array', 'E_cp', 'Gravity', 'Devices']}

            elif MF_outputs['foundation']['type [-]'].ix[0] == "drag-embedment":
                install_seq = {0: ['E_export', 'E_array', 'E_cp', 'M_drag', 'Devices']}

            elif MF_outputs['foundation']['type [-]'].ix[0] == "direct embedment":
                install_seq = {0: ['E_export', 'E_array', 'E_cp', 'M_direct', 'Devices']}

            else:
                warnings.warn("unknown electrical layout type")

        elif electrical_outputs['layout']['Electrical Layout [-]'] == "type 2":
            if MF_outputs['foundation']['type [-]'].ix[0] == "shallow foundation":
                install_seq = {0: ['E_export', 'E_array', 'E_cp', 'Driven', 'Devices']}

            elif MF_outputs['foundation']['type [-]'].ix[0] == "pile":
                install_seq = {0: ['E_export', 'E_array', 'E_cp', 'Driven', 'Devices']}

            elif MF_outputs['foundation']['type [-]'].ix[0] == "suction caisson":
                install_seq = {0: ['E_export', 'E_array', 'E_cp', 'M_Suction', 'Devices']}

            elif MF_outputs['foundation']['type [-]'].ix[0] == "gravity based":
                install_seq = {0: ['E_export', 'E_array', 'E_cp', 'Gravity', 'Devices']}

            elif MF_outputs['foundation']['type [-]'].ix[0] == "drag-embedment":
                install_seq = {0: ['E_export', 'E_array', 'E_cp', 'M_drag', 'Devices']}

            elif MF_outputs['foundation']['type [-]'].ix[0] == "direct embedment":
                install_seq = {0: ['E_export', 'E_array', 'E_cp', 'M_direct', 'Devices']}

        elif electrical_outputs['layout']['Electrical Layout [-]'] == "type 3":
            if MF_outputs['foundation']['type [-]'].ix[0] == "shallow foundation":
                install_seq = {0: ['E_export', 'E_array', 'E_cp', 'Driven', 'Devices']}

            elif MF_outputs['foundation']['type [-]'].ix[0] == "pile":
                install_seq = {0: ['E_export', 'E_array', 'E_cp', 'Driven', 'Devices']}

            elif MF_outputs['foundation']['type [-]'].ix[0] == "suction caisson":
                install_seq = {0: ['E_export', 'E_array', 'E_cp', 'M_Suction', 'Devices']}

            elif MF_outputs['foundation']['type [-]'].ix[0] == "gravity based":
                install_seq = {0: ['E_export', 'E_array', 'E_cp', 'Gravity', 'Devices']}

            elif MF_outputs['foundation']['type [-]'].ix[0] == "drag-embedment":
                install_seq = {0: ['E_export', 'E_array', 'E_cp', 'M_drag', 'Devices']}

            elif MF_outputs['foundation']['type [-]'].ix[0] == "direct embedment":
                install_seq = {0: ['E_export', 'E_array', 'E_cp', 'M_direct', 'Devices']}


    elif user_inputs['device']['type [-]'].ix[0] == "floating":
        if electrical_outputs['layout']['Electrical Layout [-]'].ix[0] == "type 1":
            if MF_outputs['foundation']['type [-]'].ix[0] == "shallow foundation":
                install_seq = {0: ['E_export', 'E_array', 'E_cp', 'Driven', 'Devices']}

            elif MF_outputs['foundation']['type [-]'].ix[0] == "pile":
                install_seq = {0: ['E_export', 'E_array', 'E_cp', 'Driven', 'Devices']}

            elif MF_outputs['foundation']['type [-]'].ix[0] == "suction caisson":
                install_seq = {0: ['E_export', 'E_array', 'E_cp', 'M_Suction', 'Devices']}

            elif MF_outputs['foundation']['type [-]'].ix[0] == "gravity based":
                install_seq = {0: ['E_export', 'E_array', 'E_cp', 'Gravity', 'Devices']}

            elif MF_outputs['foundation']['type [-]'].ix[0] == "drag-embedment":
                install_seq = {0: ['E_export', 'E_array', 'E_cp', 'M_drag', 'Devices']}

            elif MF_outputs['foundation']['type [-]'].ix[0] == "direct embedment":
                install_seq = {0: ['E_export', 'E_array', 'E_cp', 'M_direct', 'Devices']}

            else:
                warnings.warn("unknown electrical layout type")

        elif electrical_outputs['layout']['Electrical Layout [-]'] == "type 2":
            if MF_outputs['foundation']['type [-]'].ix[0] == "shallow foundation":
                install_seq = {0: ['E_export', 'E_array', 'E_cp', 'Driven', 'Devices']}

            elif MF_outputs['foundation']['type [-]'].ix[0] == "pile":
                install_seq = {0: ['E_export', 'E_array', 'E_cp', 'Driven', 'Devices']}

            elif MF_outputs['foundation']['type [-]'].ix[0] == "suction caisson":
                install_seq = {0: ['E_export', 'E_array', 'E_cp', 'M_Suction', 'Devices']}

            elif MF_outputs['foundation']['type [-]'].ix[0] == "gravity based":
                install_seq = {0: ['E_export', 'E_array', 'E_cp', 'Gravity', 'Devices']}

            elif MF_outputs['foundation']['type [-]'].ix[0] == "drag-embedment":
                install_seq = {0: ['E_export', 'E_array', 'E_cp', 'M_drag', 'Devices']}

            elif MF_outputs['foundation']['type [-]'].ix[0] == "direct embedment":
                install_seq = {0: ['E_export', 'E_array', 'E_cp', 'M_direct', 'Devices']}

        elif electrical_outputs['layout']['Electrical Layout [-]'] == "type 3":
            if MF_outputs['foundation']['type [-]'].ix[0] == "shallow foundation":
                install_seq = {0: ['E_export', 'E_array', 'E_cp', 'Driven', 'Devices']}

            elif MF_outputs['foundation']['type [-]'].ix[0] == "pile":
                install_seq = {0: ['E_export', 'E_array', 'E_cp', 'Driven', 'Devices']}

            elif MF_outputs['foundation']['type [-]'].ix[0] == "suction caisson":
                install_seq = {0: ['E_export', 'E_array', 'E_cp', 'M_Suction', 'Devices']}

            elif MF_outputs['foundation']['type [-]'].ix[0] == "gravity based":
                install_seq = {0: ['E_export', 'E_array', 'E_cp', 'Gravity', 'Devices']}

            elif MF_outputs['foundation']['type [-]'].ix[0] == "drag-embedment":
                install_seq = {0: ['E_export', 'E_array', 'E_cp', 'M_drag', 'Devices']}

            elif MF_outputs['foundation']['type [-]'].ix[0] == "direct embedment":
                install_seq = {0: ['E_export', 'E_array', 'E_cp', 'M_direct', 'Devices']}

    else:
        warnings.warn("unknown device type")

    return install_seq, instal_order

# see = selectSeq(end_user_inputs, WP3_outputs, WP4_outputs)
