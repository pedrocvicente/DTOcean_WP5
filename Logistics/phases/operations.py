# -*- coding: utf-8 -*-
"""
@author: WavEC Offshore Renewables
email: boris.teillant@wavec.org; paulo@wavec.org

This module governs the definition of all individual logistic operations
considered within the DTOcean tool, in terms of id, description, pre-defined
time for completition and operational limit conditions. These will be used to
further characterize the operation sequence of each logistic phase.

BETA VERSION NOTES: In this version, a limited number of operations were defined
and their characterization was mostly limited to the id and description. This
will be further expanded in the following version.
"""

import pandas as pd

class LogOp(object):

    def __init__(self, id, description, time_value, time_function, time_other, olc):
        self.id = id
        self.description = description
        self.time_value = time_value
        self.time_function = time_function
        self.time_other = time_other
        self.olc = olc


def logOp_init(file_path):
    """logOp_init function defines all individual logistic operations considered
    within the DTOcean tool. Each individual operation is defined by invoking
    the class LogOp. Explanation of the key ID numbering system implemented:
    1st digit:  1 = General individual operation shared with all/most logistic phases;
                2 = Specialized individual operation for the installation of electrical infrastructure;
                3 = Specialized individual operation for the installation of foundations;
                4 = Specialized individual operation for the installation of moorings;
                5 = Specialized individual operation for the installation of tidal or wave energyd devices;
                6 = Specialized individual operation for inspection activities;
                7 = Specialized individual operation for on-site maintenance interventions;
                8 = Specialized individual operation for port-based maintenance interventions;
    2nd/3rd digit: simple counter to discriminate between different individual
                   operations within the same category defined by the 1st digit

    Parameters
    ----------

    Returns
    -------
    logOp : dict
     dictionnary containing all classes defining the logistic operations
    """

    # Transform vessel database .xls into panda type
    excel = pd.ExcelFile(file_path)

    # Collect data from a particular tab
    op_db = excel.parse('operations', header=0, index_col=0)

    logOp = {}

    # Create a dictionary containing all listed operations
    for op_nr in range(len(op_db)):

        logOp[op_db.index[op_nr]] = LogOp(op_db.ix[op_nr]['id [-]'],
                                          op_db.ix[op_nr]['Logitic operation [-]'],
                                          op_db.ix[op_nr]['Time: value [h]'],
                                          op_db.ix[op_nr]['Time: function [-]'],
                                          op_db.ix[op_nr]['Time: other [-]'],
                                          [op_db.ix[op_nr]['OLC: Hs [m]'],
                                           op_db.ix[op_nr]['OLC: Tp [s]'],
                                           op_db.ix[op_nr]['OLC: Ws [m/s]'],
                                           op_db.ix[op_nr]['OLC: Cs [m/s]']
                                           ]
                                           )

    return logOp
