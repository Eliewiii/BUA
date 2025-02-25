"""
Functions to load buildings or geometries from a 2D GIS, hbjson files or json files
"""

import os
import logging
import json

from ..urban_canopy import UrbanCanopy

from ..config.config_default_values_user_parameters import default_path_simulation_folder

user_logger = logging.getLogger("user")
dev_logger = logging.getLogger("dev")


class SimulationLWR:

    @staticmethod
    def generate_radiative_surface_manager_for_lwr_computation(urban_canopy_object: UrbanCanopy,
                                                               overwrite: bool = False,
                                                               include_windows: bool = True):
        """
        Add buildings in a 2D GIS to the urban canopy
        :param urban_canopy:
        :param path_gis:
        :param path_additional_gis_attribute_key_dict:
        :param unit:
        :return:
        """
        # Add the buildings from the GIS to the urban canopy
        urban_canopy_object.generate_radiative_surface_manager_for_lwr_computation(
            overwrite=overwrite,
            include_windows=include_windows
        )
        user_logger.info("Radiative surface manager for LWR computation generated successfully")
        dev_logger.info("Radiative surface manager for LWR computation generated successfully")
    @staticmethod
    def perform_lwr_vf_computation(urban_canopy_object: UrbanCanopy,
                                   path_simulation_folder: str = default_path_simulation_folder,
                                   overwrite: bool = False, **kwargs):
        """

        """
        urban_canopy_object.perform_lwr_vf_computation(
            path_simulation_folder=path_simulation_folder,
            overwrite=overwrite,
            **kwargs
        )
        user_logger.info("LWR view factors computed successfully")
        dev_logger.info("LWR view factors computed successfully")
