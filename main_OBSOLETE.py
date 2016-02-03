"""
@author: WavEC Offshore Renewables
email: boris.teillant@wavec.org; paulo@wavec.org

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

from Logistics.load import load_phase_order_data, load_time_olc_data
from Logistics.load import load_eq_rates
from Logistics.load import load_sf
from Logistics.load import load_vessel_data, load_equipment_data
from Logistics.load import load_port_data
from Logistics.load.wp_bom import load_user_inputs, load_hydrodynamic_outputs
from Logistics.load.wp_bom import load_electrical_outputs, load_MF_outputs
from Logistics.load.wp_bom import load_OM_outputs

from Logistics.phases.operations import logOp_init
from Logistics.phases.install import logPhase_install_init
from Logistics.phases.om import logPhase_om_init         # FOR OM ONLY!!!!!!!!
from Logistics.installation import planning
from Logistics.installation import select_port
from Logistics.feasibility.glob import glob_feas
from Logistics.selection.select_ve import select_e, select_v
from Logistics.selection.match import compatibility_ve
from Logistics.performance.schedule.schedule import sched
# from Logistics.performance.economic.eco import cost

# # Set directory paths for loading inputs (@Tecnalia)
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

# inputs_SV_LD = 'save'
inputs_SV_LD = 'load'

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

    with open('objs.pickle', 'w') as f:
        pickle.dump([phase_order, schedule_OLC, vessels, equipments, ports, user_inputs, hydrodynamic_outputs, electrical_outputs, MF_outputs], f)

elif inputs_SV_LD == "load":
    # Getting back the objects:
    with open('objs.pickle') as f:
        phase_order, schedule_OLC, vessels, equipments, ports, user_inputs, hydrodynamic_outputs, electrical_outputs, MF_outputs = pickle.load(f)

else:
    print 'Invalid SaveLoad option'

"""
 Initialise logistic operations and logistic phases
"""

# logOp = logOp_init()

logOp = logOp_init(database_file("operations_time_OLC.xlsx"))


"""
Determine the adequate installation logistic phase plan
"""
#install_plan, instal_order = planning.install_plan(database_file("Installation_Order.xlsx"), user_inputs, electrical_outputs, MF_outputs)

# DUMMY-TO BE ERASED, install plan is constrained to F_driven because
# we just have the F_driven characterized for now
# install_plan = {0: ['F_driven']}
install_plan = {0: ['Devices'] }


"""
Select the most appropriate base installation port
"""

install_port = select_port.install_port(user_inputs, hydrodynamic_outputs,
                                        electrical_outputs, MF_outputs, ports,
                                        install_plan)

# Incremental assessment of all logistic phase forming the the installation process
install = {'plan': install_plan,
          'port': install_port,
          'requirement': {},
          'eq_select': {},
          've_select': {},
          'combi_select': {},
          'schedule': {},
          'cost': {},
          'risk': {},
          'envir': {},
          'status': "pending"}


logPhase_install = logPhase_install_init(logOp, vessels, equipments, user_inputs,
                                         electrical_outputs, MF_outputs, hydrodynamic_outputs)

#logPhase_om = logPhase_om_init(logOp, vessels, equipments, user_inputs, OM_outputs)

if install['status'] == "pending":
   # loop over the number of layers of the installation plan
   for x in range(len(install['plan'])):
       for y in range(len(install['plan'][x])):
           # extract the LogPhase ID to be evaluated from the installation plan
           log_phase_id = install['plan'][x][y]
           log_phase = logPhase_install[log_phase_id]
           # print log_phase

           # characterize the logistic requirements
           install['requirement'] = glob_feas(log_phase, log_phase_id,
                                              user_inputs,
                                              hydrodynamic_outputs,
                                              electrical_outputs, MF_outputs)

           # selection of the maritime infrastructure
           install['eq_select'], log_phase = select_e(install, log_phase)
           install['ve_select'], log_phase = select_v(install, log_phase)

           # matching requirements for combinations of port/vessel(s)/equipment
           install['combi_select'], log_phase = compatibility_ve(install,
                                                                 log_phase,
                                                                 install_port['Selected base port for installation'])
#           print install['combi_select']

#          schedule assessment of the different operation sequence
           install['schedule'], log_phase = sched(x, install, log_phase,
                                                  log_phase_id, user_inputs,
                                                  hydrodynamic_outputs,
                                                  electrical_outputs,
                                                  MF_outputs)

#           # cost assessment of the different operation sequenc
#            install['cost'], log_phase = cost(install, log_phase)

           # TO DO
               # -> finish Matching
               # -> Ship Routing Algorithm
               # -> Port Choice
               # -> Planning
               # -> Weather Window
               # -> Performance Evaluation
               # -> Risk Analysis
