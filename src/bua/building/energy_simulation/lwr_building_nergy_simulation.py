"""
Performs the energy simulation of a building using the EnergyPlus software and saves the results in a dictionary.
"""

import os
import json
import logging
import shutil
from packaging import version

from time import time
from copy import deepcopy

from honeybee.model import Model
from honeybee_energy.simulation.parameter import SimulationParameter
from honeybee_energy.run import to_openstudio_osw, run_osw, run_idf, to_openstudio_sim_folder
from honeybee_energy.config import folders as hb_folders
from honeybee_energy.result.eui import eui_from_sql

from ladybug.sql import SQLiteResult

required_outputs = ["Zone Electric Equipment Electricity Energy",
                    "Zone Ideal Loads Supply Air Total Cooling Energy",
                    "Zone Ideal Loads Supply Air Total Heating Energy", "Zone Lights Electricity Energy"]

user_logger = logging.getLogger("user")
dev_logger = logging.getLogger("dev")

empty_bes_results_dict = {
    "heating": {"monthly": [], "monthly_cumulative": [], "yearly": None},
    "cooling": {"monthly": [], "monthly_cumulative": [], "yearly": None},
    "equipment": {"monthly": [], "monthly_cumulative": [], "yearly": None},
    "lighting": {"monthly": [], "monthly_cumulative": [], "yearly": None},
    # "ventilation": {"monthly": [], "monthly_cumulative": [], "yearly": None},  # Unused for now
    "total": {"hourly": [], "monthly": [], "monthly_cumulative": [], "yearly": None}
}


class LWRBuildingEnergySimulation:
    """
    Class to perform the energy simulation of a building using the EnergyPlus software and saves the results in a
    dictionary.
    """

    def __init__(self, building_id: str):
        """
        Initialize the BuildingEnergySimulation class.
        :param building_id: str, id of the building the object belongs to
        """

        self.building_id = building_id
        # Parameters
        self.cop_heating = None
        self.cop_cooling = None
        # Flags
        self.hourly_report_frequency = False
        # Results
        self.bes_results_dict = None
        # Simulation tracking
        self.sim_duration = None

    def extract_total_energy_use(self, path_ubes_sim_result_folder: str):
        """
        Extract the energy use intensity at the building scale from the result files.
        :param path_ubes_sim_result_folder: str, path to the result folder
        """
        # Paths to the result BES folder
        path_bes_result_folder = os.path.join(path_ubes_sim_result_folder, self.building_id)
        # Paths to the results files
        path_eplusout_sql = os.path.join(path_bes_result_folder, "eplusout.sql")
        # Check if the BES result folder and the result files exist
        if not os.path.isdir(path_bes_result_folder):
            logging.warning(f"The result folder for the building {self.building_id} does not exist.")
        elif not os.path.isfile(path_eplusout_sql):
            return
        # Initialize the results dictionary
        self.bes_results_dict = deepcopy(empty_bes_results_dict)

        # Get hourly results if the reporting frequency is hourly
        sql_obj = SQLiteResult(path_eplusout_sql)
        if sql_obj.reporting_frequency == "Hourly":
            self.hourly_report_frequency = True
            self.bes_results_dict["total"]["hourly"] = get_hourly_results_from_sql(sql_obj,
                                                                                   self.cop_cooling,
                                                                                   self.cop_heating)
        # Get End Use intensity
        eui_dict = eui_from_sql(path_eplusout_sql)
        total_floor_area = eui_dict["total_floor_area"]

        self.bes_results_dict["heating"]["yearly"] = eui_dict["end_uses"][
                                                         "Heating"] * total_floor_area / self.cop_heating
        self.bes_results_dict["cooling"]["yearly"] = eui_dict["end_uses"][
                                                         "Cooling"] * total_floor_area / self.cop_cooling
        self.bes_results_dict["equipment"]["yearly"] = eui_dict["end_uses"][
                                                           "Electric Equipment"] * total_floor_area
        self.bes_results_dict["lighting"]["yearly"] = eui_dict["end_uses"][
                                                          "Interior Lighting"] * total_floor_area
        # self.bes_results_dict["ventilation"]["yearly"] = eui_dict["end_uses"]["ventilation"] * total_floor_area
        self.bes_results_dict["total"]["yearly"] = sum([self.bes_results_dict["heating"]["yearly"],
                                                        self.bes_results_dict["cooling"]["yearly"],
                                                        self.bes_results_dict["equipment"]["yearly"],
                                                        # self.bes_results_dict["ventilation"]["yearly"],
                                                        self.bes_results_dict["lighting"]["yearly"]])




