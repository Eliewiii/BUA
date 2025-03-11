"""
Unit tests for the BUA workflow.
"""
import os
import time

from src.bua.urban_canopy import UrbanCanopy
from src.bua.simulation_steps import *
from src.bua.config.config_default_values_user_parameters import *

# Inputs to be used
test_file_dir = os.path.dirname(os.path.abspath(__file__))
test_folder_dir = os.path.dirname(os.path.dirname(test_file_dir))
test_data_dir = os.path.join(test_folder_dir, "test_data")


def init_urban_canopy_with_x_buildingmodels(num_buildings) -> UrbanCanopy:
    """
    Generate an UrbanCanopy object with 2 BuildingModeled and BuildingBasic objects
    """
    path_hbjson_folder = os.path.join(test_data_dir, "test_hbjsons")
    list_hbjson_files = os.listdir(path_hbjson_folder)
    if num_buildings > len(list_hbjson_files):
        raise ValueError("num_buildings should be less than the number of HBJSON files in the folder")
    # Clear simulation temp folder
    SimulationCommonMethods.clear_simulation_temp_folder()
    # Create simulation folder
    SimulationCommonMethods.make_simulation_folder(path_simulation_folder=default_path_simulation_folder)
    # Create an UrabanCanopy object
    urban_canopy_object = SimulationCommonMethods.create_or_load_urban_canopy_object(
        path_simulation_folder=default_path_simulation_folder)

    for i in range(num_buildings):
        path_hbjson = os.path.join(path_hbjson_folder, list_hbjson_files[i])
        SimulationLoadBuildingOrGeometry.add_buildings_from_hbjson_to_urban_canopy(
            urban_canopy_object=urban_canopy_object,
            path_folder_hbjson=None,
            path_file_hbjson=path_hbjson,
            are_buildings_targets=True,
            keep_context_from_hbjson=False)

    return urban_canopy_object


def test_run_bes():
    """
    Check that
    """
    urban_canopy_object = init_urban_canopy_with_x_buildingmodels(num_buildings=2)

    # Clear simulation temp folder
    building_ids = list(urban_canopy_object.building_dict.keys())

    # Load epw and simulation parameters
    UrbanBuildingEnergySimulationFunctions.load_epw_and_hb_simulation_parameters_for_ubes_in_urban_canopy(
        urban_canopy_obj=urban_canopy_object,
        # path_simulation_folder=default_path_simulation_folder,
        # path_hbjson_simulation_parameter_file=default_path_hbjson_simulation_parameter_file,
        # path_file_epw=default_path_weather_file,
        # ddy_file=None,
        hourly_report_frequency=True,
        overwrite=True)

    # Write IDF
    UrbanBuildingEnergySimulationFunctions.generate_idf_files_for_ubes_with_openstudio_in_urban_canopy(
        urban_canopy_obj=urban_canopy_object,
        path_simulation_folder=default_path_simulation_folder,
        building_id_list=building_ids,
        overwrite=True,
        silent=True)

    # Run IDF through EnergyPlus
    UrbanBuildingEnergySimulationFunctions.run_idf_files_with_energyplus_for_ubes_in_urban_canopy(
        urban_canopy_obj=urban_canopy_object,
        path_simulation_folder=default_path_simulation_folder,
        building_id_list=building_ids,
        overwrite=True,
        silent=True)

    # Extract results
    UrbanBuildingEnergySimulationFunctions.extract_results_from_ep_simulation(
        urban_canopy_obj=urban_canopy_object,
        path_simulation_folder=default_path_simulation_folder,
        cop_heating=3., cop_cooling=3.)


    # Extract results
    UrbanBuildingEnergySimulationFunctions.extract_results_from_ep_simulation(
        urban_canopy_obj=urban_canopy_object,
        path_simulation_folder=default_path_simulation_folder,
        cop_heating=3., cop_cooling=3.)

    # Save the UrbanCanopy object to a pickle and json files
    SimulationCommonMethods.save_urban_canopy_object_to_pickle(urban_canopy_object=urban_canopy_object,
                                                               path_simulation_folder=path_simulation_temp_folder)
    SimulationCommonMethods.save_urban_canopy_to_json(urban_canopy_object=urban_canopy_object,
                                                      path_simulation_folder=path_simulation_temp_folder)
