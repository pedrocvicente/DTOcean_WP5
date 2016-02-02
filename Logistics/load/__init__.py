# -*- coding: utf-8 -*-
"""
@author: WavEC Offshore Renewables
email: boris.teillant@wavec.org; paulo@wavec.org

This module imports the WP5 databases required to run WP5 package.  All data
imported is translated to panda dataframes.

BETA VERSION NOTES: the module also aims to provide a buffer between the database
source and WP5 package, so it becomes simple to shift from the temporary .xlsx
and .csv files to the final SQL solution.
"""

import pandas as pd

from ..phases import VesselType
from ..phases import EquipmentType


def load_time_olc_data(file_path):
    """Imports olc database into a panda table

    Parameters
    ----------
    file_path : string
     the folder path of the time and olc data set

    Returns
    -------
    time_olc : dict
     dictionnary containing a panda dataframe with time duration and olc
    """
    # Transform time and olc database .xls into panda type
    excel = pd.ExcelFile(file_path)
    # Collect data from a particular tab
    time_olc = excel.parse('operations', header=0, index_col=0)

    return time_olc



def load_phase_order_data(file_path):
    """Imports phase order database into a panda table

    Parameters
    ----------
    file_path : string
     the folder path of the phase order table

    Returns
    -------
    phase_order : dict
     dictionnary containing a panda dataframe with time duration and olc
    """
    # Transform phase table .xls into panda type
    excel = pd.ExcelFile(file_path)
    # Collect data from a particular tab
    phase_order = excel.parse('InstallationOrder', header=0, index_col=0)

    return phase_order

def load_eq_rates(file_path):
    """Imports pile driving penetration rates and cable laying/trenching/burial
    rates into two panda tables

    Parameters
    ----------
    file_path : string
     the folder path of the phase order table

    Returns
    -------
    penet_rates : panda dataFrame table
     panda table containing the pile driving vertical penetration rates and the
     cable laying/trenching/burial horizontal progress rates
    """
    # Transform equipment performance rates table .xls into panda type
    excel = pd.ExcelFile(file_path)
    # Collect data from a particular tab
    penet_rates = excel.parse('penet', header=0, index_col=0)
    laying_rates = excel.parse('laying', header=0, index_col=0)

    return penet_rates, laying_rates

def load_sf(file_path):
    """Imports safety factors into a panda table

    Parameters
    ----------
    file_path : string
     the folder path of the phase order table

    Returns
    -------
    safety_factors : panda dataFrame table
     panda table containing the safety factors to apply on the feasiblity
     functions
    """
    # Transform equipment performance rates table .xls into panda type
    excel = pd.ExcelFile(file_path)
    # Collect data from a particular tab
    port_sf = excel.parse('port_sf', header=0, index_col=0)
    vessel_sf = excel.parse('vessel_sf', header=0, index_col=0)
    eq_sf = excel.parse('eq_sf', header=0, index_col=0)

    return port_sf, vessel_sf, eq_sf

def load_vessel_data(file_path):
    """Imports vessel database into panda dataframe and creates a class for each
    vessel type

    Parameters
    ----------
    file_path : string
     the folder path of the vessel database

    Returns
    -------
    vessels : dict
     dictionnary containing all classes defining the different vessel types
    """
    # Transform vessel database .xls into panda type
    excel = pd.ExcelFile(file_path)
    # Collect data from a particular tab
    pd_vessel = excel.parse('Python_Format', header=0, index_col=0)

    # Splits the pd_vessel object with the full dataset, into smaller panda
    # objects with specific vessel types. Each vessel object is initiated with
    # the vessel class: VesselType
    vessels = {'Barge': VesselType("Barge", pd_vessel[pd_vessel['Vessel type [-]'] == 'Barge']),
               'Tugboat': VesselType("Tugboat", pd_vessel[pd_vessel['Vessel type [-]'] == 'Tugboat']),
               'Crane Barge': VesselType("Crane Barge", pd_vessel[pd_vessel['Vessel type [-]'] == 'Crane Barge']),
               'Crane Vessel': VesselType("Crane Vessel", pd_vessel[pd_vessel['Vessel type [-]'] == 'Crane Vessel']),
               'JUP Barge': VesselType("JUP Barge", pd_vessel[pd_vessel['Vessel type [-]'] == 'JUP Barge']),
               'JUP Vessel': VesselType("JUP Vessel", pd_vessel[pd_vessel['Vessel type [-]'] == 'JUP Vessel']),
               'AHTS': VesselType("AHTS", pd_vessel[pd_vessel['Vessel type [-]'] == 'AHTS']),
               'Multicat': VesselType("Multicat", pd_vessel[pd_vessel['Vessel type [-]'] == 'Multicat']),
               'AHTS': VesselType("AHTS", pd_vessel[pd_vessel['Vessel type [-]'] == 'AHTS']),
               'CLV': VesselType("CLV", pd_vessel[pd_vessel['Vessel type [-]'] == 'CLV']),
               'CLB': VesselType("CLB", pd_vessel[pd_vessel['Vessel type [-]'] == 'CLB']),
               'CTV': VesselType("CTV", pd_vessel[pd_vessel['Vessel type [-]'] == 'CTV']),
               'CSV': VesselType("Construction Support Vessel", pd_vessel[pd_vessel['Vessel type [-]'] == 'Construction Support Vessel']),
               'Fit for Purpose': VesselType("Fit for Purpose", pd_vessel[pd_vessel['Vessel type [-]'] == 'Fit for Purpose']),
               'PSV': VesselType("Platform Supply Vessel", pd_vessel[pd_vessel['Vessel type [-]'] == 'Platform Support Vessel']),
               'Helicopter': VesselType("Helicopter", pd_vessel[pd_vessel['Vessel type [-]'] == 'Helicopter'])
               }

    return vessels


def load_equipment_data(file_path):
    """Imports equipment database into panda dataframe    hammer = excel.parse('hammer', header=0, index_col=0)
s and creates a class for
    each equipment type

    Parameters
    ----------
    file_path : string
     the folder path of the equipment database

    Returns
    -------
    vessels : dict
     dictionnary containing all classes defining the different equipment types
    """

    # Transform Equipment database .xls into panda type
    excel = pd.ExcelFile(file_path)

    # Collect data from a particular tab
    rov = excel.parse('rov', header=0, index_col=0)
    divers = excel.parse('divers', header=0, index_col=0)
    cable_burial = excel.parse('cable_burial', header=0, index_col=0)
    excavating = excel.parse('excavating', header=0, index_col=0)
    mattress = excel.parse('mattress', header=0, index_col=0)
    rock_filter_bags = excel.parse('rock_filter_bags', header=0, index_col=0)
    split_pipe = excel.parse('split_pipe', header=0, index_col=0)
    hammer = excel.parse('hammer', header=0, index_col=0)
    drilling_rigs = excel.parse('drilling_rigs', header=0, index_col=0)
    vibro_driver = excel.parse('vibro_driver', header=0, index_col=0)

    # Define equipment types by invoking EquipmentType class
    equipments = {'rov': EquipmentType("rov", rov),
                  'divers': EquipmentType("divers", divers),
                  'cable burial': EquipmentType("cable_burial", cable_burial),
                  'excavating': EquipmentType("excavating", excavating),
                  'mattress': EquipmentType("mattress", mattress),
                  'rock filter bags': EquipmentType("rock_filter_bags", rock_filter_bags),
                  'split pipe': EquipmentType("split_pipe", split_pipe),
                  'hammer': EquipmentType("hammer", hammer),
                  'drilling rigs': EquipmentType("drilling_rigs", drilling_rigs),
                  'vibro driver': EquipmentType("vibro_driver", vibro_driver)
                 }

    return equipments


def load_port_data(file_path):
    """Imports port database into a panda table

    Parameters
    ----------
    file_path : string
     the folder path of the port database

    Returns
    -------
    vessels : dict
     dictionnary containing a panda dataframe with all ports
    """
    # Transform vessel database .xls into panda type
    excel = pd.ExcelFile(file_path)
    # Collect data from a particular tab
    ports = excel.parse('python', header=0, index_col=0)

    return ports


