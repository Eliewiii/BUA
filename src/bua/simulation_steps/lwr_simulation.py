"""
Functions to load buildings or geometries from a 2D GIS, hbjson files or json files
"""

import os
import logging
import json

from ..urban_canopy import UrbanCanopy

from ..config.config_default_values_user_parameters import default_path_simulation_folder, \
    default_path_hbjson_simulation_parameter_file, default_path_weather_file

user_logger = logging.getLogger("user")
dev_logger = logging.getLogger("dev")


class SimulationLWR:

    @staticmethod
    def perform_building_selection_for_lwr_computation(urban_canopy_object: UrbanCanopy,
                                                       min_vf_criterion=0.01,
                                                       num_rays=9,
                                                       convert_to_hb_model=False,
                                                       overwrite=False):
        """

        """

        urban_canopy_object.perform_building_selection_for_lwr_computation(
            min_vf_criterion=min_vf_criterion,
            num_rays=num_rays,
            convert_to_hb_model=convert_to_hb_model,
            overwrite=overwrite
        )
        user_logger.info("Building selection for LWR computation performed successfully")
        dev_logger.info("Building selection for LWR computation performed successfully")

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
        path_vf_mtx_crs_npz, path_eps_mtx_crs_npz, path_rho_mtx_crs_npz, path_tau_mtx_crs_npz = urban_canopy_object.perform_lwr_vf_computation(
            path_simulation_folder=path_simulation_folder,
            overwrite=overwrite,
            **kwargs
        )

        return path_vf_mtx_crs_npz, path_eps_mtx_crs_npz, path_rho_mtx_crs_npz, path_tau_mtx_crs_npz

        user_logger.info("View factors computed successfully")
        dev_logger.info("View factors computed successfully")

    @staticmethod
    def set_up_and_run_lwr_simulation(urban_canopy_object: UrbanCanopy,
                              path_energyplus_dir,
                              path_simulation_folder=default_path_simulation_folder,
                              path_hbjson_simulation_parameter_file=default_path_hbjson_simulation_parameter_file,
                              path_weather_file=default_path_weather_file,
                              ddy_file=None,
                              hourly_report_frequency: bool = False,
                              num_time_steps_per_hour: int = 20,
                              **kwargs):
        """

        """
        urban_canopy_object.set_up_and_run_lwr_simulation(
            path_simulation_folder=path_simulation_folder,
            path_hbjson_simulation_parameter_file=path_hbjson_simulation_parameter_file,
            path_weather_file=path_weather_file,
            path_energyplus_dir=path_energyplus_dir,
            ddy_file=ddy_file,
            hourly_report_frequency=hourly_report_frequency,
            num_time_steps_per_hour=num_time_steps_per_hour,
            **kwargs
        )
        user_logger.info("LWR simulation set up successfully")
        dev_logger.info("LWR simulation set up successfully")



