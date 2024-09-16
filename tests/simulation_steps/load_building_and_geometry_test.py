"""
Unit tests BIPV_simulation
"""

import os
import pytest

from src.bua.simulation_steps import *
from src.bua.config.config_default_values_user_parameters import *

from src.bua.urban_canopy import UrbanCanopy
from src.bua.building import BuildingModeled

# Inputs to be used
test_file_dir = os.getcwd()
print()
test_folder_dir = os.path.dirname(test_file_dir)
test_data_dir = os.path.join(test_folder_dir, "test_data")
path_test_building_hbjson_0 = os.path.join(test_data_dir, "test_hbjsons", "Building_sample_0.hbjson")
print("")
print(f"path_test_building_hbjson_0: {path_test_building_hbjson_0}")


def test_bua_simulation_flow_until_bipv():
    """
    Check that
    """
    print("")
    print(f"test_file_dir: {test_file_dir}")
    print(f"path_test_building_hbjson_0: {path_test_building_hbjson_0}")
    # Clear simulation temp folder
    SimulationCommonMethods.clear_simulation_temp_folder()
    assert os.listdir(default_path_simulation_folder) == []
    # Create simulation folder
    SimulationCommonMethods.make_simulation_folder(path_simulation_folder=default_path_simulation_folder)

    # Create an UrabanCanopy object
    urban_canopy_object = SimulationCommonMethods.create_or_load_urban_canopy_object(
        path_simulation_folder=default_path_simulation_folder)
    # Save the UrbanCanopy object to a pickle and json files
    SimulationCommonMethods.save_urban_canopy_object_to_pickle(urban_canopy_object=urban_canopy_object,
                                                               path_simulation_folder=default_path_simulation_folder)

    ###############################
    # Load HBJSONs
    ###############################

    # Add HBJSON building to the UrbanCanopy object
    SimulationLoadBuildingOrGeometry.add_buildings_from_hbjson_to_urban_canopy(
        urban_canopy_object=urban_canopy_object,
        path_folder_hbjson=None,
        path_file_hbjson=path_test_building_hbjson_0,
        are_buildings_targets=True,
        keep_context_from_hbjson=False)

    print("")
    print(f"UrbanCanopy object after adding the building: {urban_canopy_object.building_dict}")

