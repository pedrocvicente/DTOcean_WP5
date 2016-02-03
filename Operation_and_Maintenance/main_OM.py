"""
@author: WavEC Offshore Renewables
email: boris.teillant@wavec.org; paulo@wavec.org, pedro.vicente@wavec.org

main.py is the main file of the WP5 module within the suite of design tools
developped under the EU FP7 DTOcean project. main.py provides an estimation of
the predicted performance of feasible maritime infrastructure solutions
that can carry out marine operations pertaining to the installation of
wave and tidal energy arrays.

main.py can be described in five core sub-modules:
0- Loading input data
1- Initialising the logistic classes
2- Defining the installation plan
3- Selecting the installation port
4- Performing the assessment of all logistic phases sequencially, following
   six steps:
    (i) characterizartion of logistic requirements
    (ii) selection of the maritime infrastructure
    (iii) schedule assessment of the logistic phase
    (iv) cost assessment of the logistic phase
    (v) risk assessment of the logistic phase
    (vi) environmental impact assessment of the logistic phase

Parameters
----------
vessels(DataFrame): Panda table containing the vessel database

equipments (DataFrame): Panda table containing the equipment database

ports (DataFrame): Panda table containing the ports database

user_inputs (dict): dictionnary containing all required inputs to WP5 coming from WP1/end-user:
     'device' (Dataframe): inputs required from the device
     'metocean' (Dataframe): metocean data

hydrodynamic_outputs (dict): dictionnary containing all required inputs to WP5 coming from WP2
     'units' (DataFrame): number of devices
     'position' (DataFrame): UTM position of the devices

electrical_outputs (dict): dictionnary containing all required inputs to WP5 coming from WP3
     'layout' (DataFrame): to be specified

M&F_outputs (DataFrame): containing foundation data required for each device

O&M_outputs (dict):  dictionnary containing all required inputs to WP5 coming from WP6
     'LogPhase1' (DataFrame): All inputs required for LpM1 logistic phase as defined by WP6

Returns
-------

install (dict): dictionnary compiling all key results obtained from the assessment of the logistic phases for installation
    'plan' (dict): installation sequence of the required logistic phases
    'port' (DataFrame): port data related to the selected installation port
    'requirement' (tuple): minimum requirements returned from the feasibility functions
    'eq_select' (dict): list of equipments satisfying the minimum requirements
    've_select' (dict): list of vessels satisfying the minimum requirements
    'combi_select' (dict): list of solutions passing the compatibility check
    'schedule' (dict): list of parameters with data about time
    'cost'  (dict): vessel equiment and port cost
    'risk': to be defined
    'envir': to be defined
    'status': to be defined


Examples
--------
>>> LOGISTICS()


See also: ...

                       DTOcean project
                    http://www.dtocean.eu

                   WavEC Offshore Renewables
                    http://www.wavec.org/en

"""

from os import path
import os
import sys
sys.path.append('..')

from Logistics.load import load_phase_order_data, load_time_olc_data
from Logistics.load import load_eq_rates
from Logistics.load import load_sf
from Logistics.load import load_vessel_data, load_equipment_data
from Logistics.load import load_port_data
from Logistics.load.wp_bom import load_user_inputs, load_hydrodynamic_outputs
from Logistics.load.wp_bom import load_electrical_outputs, load_MF_outputs
from Logistics.load.wp_bom import load_OM_outputs

from Logistics.phases.operations import logOp_init
from Logistics.phases.om import logPhase_om_init
from Logistics.installation import select_port_OM
from Logistics.installation import logPhase_select
from Logistics.feasibility.glob import glob_feas
from Logistics.selection.select_ve import select_e, select_v
from Logistics.selection.match import compatibility_ve
from Logistics.performance.schedule.schedule import sched
from Logistics.performance.economic.eco import cost

# # Set directory paths for loading inputs
mod_path = path.dirname(path.realpath(__file__))

def database_file(file):
    """shortcut function to load files from the database folder
    """
    fpath = path.join('databases', '{0}'.format(file))
    db_path = path.join(mod_path, fpath)
    return db_path

#def run():
"""
Load required inputs and database into panda dataframes
"""

import pickle

inputs_SV_LD = 'save'
#inputs_SV_LD = 'load'

if inputs_SV_LD == "save":
    # Saving the objects:

    #default_values inputs
    phase_order = load_phase_order_data(database_file("Installation_Order.xlsx"))
    schedule_OLC = load_time_olc_data(database_file("operations_time_OLC.xlsx"))
    penet_rates, laying_rates = load_eq_rates(database_file("equipment_perf_rates.xlsx"))
    port_sf, vessel_sf, eq_sf = load_sf(database_file("safety_factors.xlsx"))

    #Internal logistic module databases
    vessels = load_vessel_data(database_file("logisticsDB_vessel_python.xlsx"))
    equipments = load_equipment_data(database_file("logisticsDB_equipment_python.xlsx"))
    ports = load_port_data(database_file("logisticsDB_ports_python.xlsx"))

    #upstream module inputs/outputs
    user_inputs = load_user_inputs(database_file("inputs_user.xlsx"))
    hydrodynamic_outputs = load_hydrodynamic_outputs(database_file("ouputs_hydrodynamic.xlsx"))
    electrical_outputs = load_electrical_outputs(database_file("ouputs_electrical.xlsx"))
    MF_outputs = load_MF_outputs(database_file("outputs_MF.xlsx"))
    OM_outputs = load_OM_outputs(database_file("outputs_OM.xlsx"))
    OM_outputs_PORT = load_OM_outputs(database_file("outputs_OM_INS_PORT.xlsx"))

    with open('objs.pickle', 'w') as f:
        pickle.dump([phase_order, schedule_OLC, vessels, equipments, ports, user_inputs, hydrodynamic_outputs, electrical_outputs, MF_outputs, OM_outputs, OM_outputs_PORT], f)

elif inputs_SV_LD == "load":
    # Getting back the objects:
    with open('objs.pickle') as f:
        phase_order, schedule_OLC, vessels, equipments, ports, user_inputs, hydrodynamic_outputs, electrical_outputs, MF_outputs, OM_outputs, OM_outputs_PORT = pickle.load(f)

else:
    print 'Invalid SaveLoad option'

"""
 Initialise logistic operations and logistic phases
"""

logOp = logOp_init( database_file("operations_time_OLC.xlsx") )

"""
Select the most appropriate base port for OM
OM_port function selects the port used by OM logistic phases
    required by the O&M module, depending if is inspection or actual maintenance.
    For the case of inspection the closest port is chosen and the ID in the input should be INS_PORT.
    For the case of the other logistic phases the selection is based on a 2 step process:
        1 - the port feasibility functions from all logistic phases are taken
        into account, and the unfeasible ports are erased from the panda dataframes.
        2 - the closest port to the project site is choosen from the feasbile
        list of ports.
    In this case, the ID in the input should be OM_PORT.
    In both cases, the dimensions of the spare parts should correspond to the biggest dimensions possibly expected.
    This should be called the first time the logistic module is called.
"""

install_port = select_port_OM.OM_port(hydrodynamic_outputs, OM_outputs_PORT, ports)  # JUST FOR TESTING!!!

logPhase_om = logPhase_om_init(logOp, vessels, equipments, user_inputs, OM_outputs)

log_phase_id = logPhase_select

log_phase = logPhase_om[log_phase_id]  # ?!

# characterize the logistic requirements
om['requirement'] = glob_feas(log_phase, log_phase_id, user_inputs,
                              hydrodynamic_outputs, electrical_outputs,
                              MF_outputs, OM_outputs)

# selection of the maritime infrastructure
om['eq_select'], log_phase = select_e(om, log_phase)
om['ve_select'], log_phase = select_v(om, log_phase)

# matching requirements for combinations of port/vessel(s)/equipment
om['combi_select'], log_phase = compatibility_ve(om, log_phase,
                                                 om['Selected base port for installation'])

# schedule assessment of the different operation sequence
om['schedule'], log_phase = sched(x, install, log_phase, log_phase_id, user_inputs,
                                  hydrodynamic_outputs, electrical_outputs, MF_outputs)

# cost assessment of the different operation sequence
om['cost'], log_phase = cost(om, log_phase)
